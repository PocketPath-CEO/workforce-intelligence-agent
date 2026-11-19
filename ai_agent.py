from ollama import chat
import app as workforce


MODEL = "qwen2.5:3b"


# TOOL 1: Retrieve all employees
def get_employees():
    return [
        {
            "employee_id": employee_id,
            **details
        }
        for employee_id, details in workforce.EMPLOYEES.items()
    ]


# TOOL 2: Retrieve pending leave requests
def get_pending_requests():
    requests = workforce.load_requests()

    return [
        request for request in requests
        if request["status"].lower() == "pending"
    ]


# TOOL 3: Retrieve an employee's leave history
def get_employee_leave_history(employee_identifier):
    employees = workforce.EMPLOYEES

    identifier = employee_identifier.strip().lower()

    matching_id = None

    for employee_id, details in employees.items():
        if (
            employee_id.lower() == identifier
            or details["name"].lower() == identifier
        ):
            matching_id = employee_id
            break

    if matching_id is None:
        return {"error": "Employee not found."}

    requests = workforce.load_requests()

    history = [
        request for request in requests
        if request["employee_id"] == matching_id
    ]

    return {
        "employee": employees[matching_id]["name"],
        "employee_id": matching_id,
        "leave_requests": history
    }


# TOOL 4: Calculate leave statistics
def get_leave_statistics():
    requests = workforce.load_requests()

    statistics = {
        "approved": 0,
        "rejected": 0,
        "pending": 0
    }

    for request in requests:
        status = request["status"].lower()

        if status in statistics:
            statistics[status] += 1

    return statistics


# REGISTER AVAILABLE TOOLS
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_employees",
            "description": "Retrieve all registered employees.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_pending_requests",
            "description": "Retrieve all pending leave requests.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_employee_leave_history",
            "description": "Retrieve leave history for an employee using their name or employee ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_identifier": {
                        "type": "string",
                        "description": "The employee's full name or employee ID."
                    }
                },
                "required": ["employee_identifier"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_leave_statistics",
            "description": "Calculate approved, rejected and pending leave request totals.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


# CONNECT TOOL NAMES TO PYTHON FUNCTIONS
AVAILABLE_FUNCTIONS = {
    "get_employees": get_employees,
    "get_pending_requests": get_pending_requests,
    "get_employee_leave_history": get_employee_leave_history,
    "get_leave_statistics": get_leave_statistics
}


# AI AGENT
def ask_agent(question):
    messages = [
        {
            "role": "system",
            "content": (
                "You are Workforce Intelligence Agent. "
                "Use the available Python tools to retrieve "
                "accurate workforce information. "
                "Use get_employees for employee lists. "
                "Use get_pending_requests for pending applications. "
                "Use get_employee_leave_history for individual history. "
                "Use get_leave_statistics for leave totals. "
                "Never invent records or statistics. "
                "You are read-only and cannot approve or reject leave."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

    response = chat(
        model=MODEL,
        messages=messages,
        tools=TOOLS
    )

    if not response.message.tool_calls:
        return response.message.content

    messages.append(response.message)

    for tool_call in response.message.tool_calls:
        function_name = tool_call.function.name
        function_to_call = AVAILABLE_FUNCTIONS.get(function_name)

        if function_to_call is None:
            result = {"error": "Unknown tool."}

        else:
            arguments = tool_call.function.arguments or {}

            print(f"\n[Calling Python tool: {function_name}]")

            result = function_to_call(**arguments)

            print("[Python result]:", result)

        messages.append({
            "role": "tool",
            "tool_name": function_name,
            "content": str(result)
        })

    final_response = chat(
        model=MODEL,
        messages=messages
    )

    return final_response.message.content


# MAIN PROGRAM
def main():
    print("Workforce Intelligence Agent")
    print("Available tools: employees, pending requests, leave history, statistics.")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nYou: ")

        if question.lower().strip() == "exit":
            print("Agent: Goodbye!")
            break

        try:
            answer = ask_agent(question)
            print("\nAgent:", answer)

        except Exception as error:
            print("\nAn error occurred:", error)


if __name__ == "__main__":
    main()