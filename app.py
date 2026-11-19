"""Workforce Intelligence Agent: a rule-based leave-management prototype."""
from datetime import date
from pathlib import Path
import json

DATA_FILE = Path(__file__).parent / "data" / "leave_requests.json"
EMPLOYEES = {
    "E001": {"name": "John Smith", "department": "Human Resources"},
    "E002": {"name": "Sarah Jones", "department": "Finance"},
    "E003": {"name": "David Brown", "department": "IT"},
}

def load_requests():
    """Load saved requests from JSON, or return an empty list."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError("Saved data must be a list.")
        return data
    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(f"Could not read saved requests: {error}")
        return []

def save_requests(requests):
    """Save requests to a JSON file."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(requests, file, indent=4)

def display_employees():
    print("\nEMPLOYEE DIRECTORY")
    for employee_id, details in EMPLOYEES.items():
        print(f"{employee_id} | {details['name']} | {details['department']}")

def submit_leave_request(requests):
    """Validate and save a new leave request."""
    display_employees()
    employee_id = input("\nEnter employee ID: ").strip().upper()
    if employee_id not in EMPLOYEES:
        print("Employee ID not found.")
        return
    try:
        days = int(input("Number of leave days: "))
    except ValueError:
        print("Please enter a whole number for leave days.")
        return
    if days <= 0:
        print("Leave days must be greater than zero.")
        return
    reason = input("Reason for leave: ").strip()
    if not reason:
        print("Please provide a reason.")
        return

    employee = EMPLOYEES[employee_id]
    next_id = max((item["request_id"] for item in requests), default=0) + 1
    request = {
        "request_id": next_id,
        "employee_id": employee_id,
        "employee": employee["name"],
        "department": employee["department"],
        "leave_days": days,
        "reason": reason,
        "submitted_on": date.today().isoformat(),
        "status": "Pending",
        "decision_note": ""
    }
    requests.append(request)
    save_requests(requests)
    print(f"\nRequest #{next_id} submitted. Status: Pending")

def view_leave_requests(requests):
    print("\nLEAVE REQUESTS")
    if not requests:
        print("There are no leave requests yet.")
        return
    for request in requests:
        print(f"\nRequest #{request['request_id']} - {request['employee']}")
        print(f"Department: {request['department']}")
        print(f"Leave days: {request['leave_days']}")
        print(f"Reason: {request['reason']}")
        print(f"Submitted: {request['submitted_on']}")
        print(f"Status: {request['status']}")
        if request["decision_note"]:
            print(f"Manager note: {request['decision_note']}")

def update_request_status(requests):
    """Approve or reject a request that is still pending."""
    view_leave_requests(requests)
    if not requests:
        return
    try:
        request_id = int(input("\nEnter request ID to review: "))
    except ValueError:
        print("Please enter a valid request ID.")
        return
    selected = next((item for item in requests if item["request_id"] == request_id), None)
    if selected is None:
        print("Request ID not found.")
        return
    if selected["status"] != "Pending":
        print("This request has already been reviewed.")
        return
    print("\n1. Approve\n2. Reject")
    decision = input("Choose an option: ").strip()
    if decision == "1":
        selected["status"] = "Approved"
    elif decision == "2":
        selected["status"] = "Rejected"
    else:
        print("Invalid choice. No changes were made.")
        return
    selected["decision_note"] = input("Manager note (optional): ").strip()
    save_requests(requests)
    print(f"Request #{request_id} updated to {selected['status']}.")

def show_menu():
    print("\n=== WORKFORCE INTELLIGENCE AGENT ===")
    print("1. View employee directory")
    print("2. Submit leave request")
    print("3. View leave requests")
    print("4. Approve or reject a request")
    print("5. Exit")

def main():
    requests = load_requests()
    while True:
        show_menu()
        choice = input("\nSelect an option: ").strip()
        if choice == "1":
            display_employees()
        elif choice == "2":
            submit_leave_request(requests)
        elif choice == "3":
            view_leave_requests(requests)
        elif choice == "4":
            update_request_status(requests)
        elif choice == "5":
            print("Thank you for using the application.")
            break
        else:
            print("Invalid option. Please choose 1 to 5.")

if __name__ == "__main__":
    main()
