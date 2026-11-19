

from datetime import date
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

import app as workforce
from ai_agent import ask_agent
app = FastAPI(
    title="Workforce Intelligence API",
    description="API for managing employee leave requests.",
    version="2.0.0"
)


class LeaveRequest(BaseModel):
    employee_id: str
    leave_days: int = Field(gt=0)
    reason: str = Field(min_length=1)


class Decision(BaseModel):
    decision: Literal["approve", "reject"]
    note: str = ""
class ChatRequest(BaseModel):
    message: str = Field(min_length=1)

@app.get("/")
def home():
    return {
        "message": "Welcome to the Workforce Intelligence API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/employees")
def get_employees():
    return [
        {"employee_id": employee_id, **details}
        for employee_id, details in workforce.EMPLOYEES.items()
    ]


@app.get("/leave-requests")
def get_leave_requests():
    return workforce.load_requests()


@app.post("/leave-requests", status_code=201)
def create_leave_request(request: LeaveRequest):
    employee_id = request.employee_id.strip().upper()

    if employee_id not in workforce.EMPLOYEES:
        raise HTTPException(status_code=404, detail="Employee not found")

    if not request.reason.strip():
        raise HTTPException(status_code=422, detail="Reason cannot be empty")

    requests = workforce.load_requests()
    employee = workforce.EMPLOYEES[employee_id]

    next_id = max(
        (item["request_id"] for item in requests),
        default=0
    ) + 1

    new_request = {
        "request_id": next_id,
        "employee_id": employee_id,
        "employee": employee["name"],
        "department": employee["department"],
        "leave_days": request.leave_days,
        "reason": request.reason.strip(),
        "submitted_on": date.today().isoformat(),
        "status": "Pending",
        "decision_note": ""
    }

    requests.append(new_request)
    workforce.save_requests(requests)

    return new_request


@app.patch("/leave-requests/{request_id}")
def update_leave_request(request_id: int, decision: Decision):
    requests = workforce.load_requests()

    selected = next(
        (item for item in requests if item["request_id"] == request_id),
        None
    )

    if selected is None:
        raise HTTPException(status_code=404, detail="Request not found")

    if selected["status"] != "Pending":
        raise HTTPException(
            status_code=400,
            detail="Request has already been reviewed"
        )

    selected["status"] = (
        "Approved" if decision.decision == "approve" else "Rejected"
    )
    selected["decision_note"] = decision.note

    workforce.save_requests(requests)

    return selected

@app.post("/agent/chat")
def chat_with_agent(request: ChatRequest):
    question = request.message.strip()

    if not question:
        raise HTTPException(
            status_code=422,
            detail="Message cannot be empty"
        )

    try:
        answer = ask_agent(question)
        return {
            "question": question,
            "answer": answer
        }

    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=f"AI agent unavailable: {str(error)}"
        )
