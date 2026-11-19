

\# Workforce Intelligence Agent



A Python-based workforce management prototype that combines a REST API, a locally hosted Large Language Model (LLM), and Python tool calling to retrieve and analyse employee leave information.



\## Project Overview



The Workforce Intelligence Agent allows users to interact with demonstration workforce records using natural language.



It combines:

\- Python for workforce data processing and business logic.

\- FastAPI for REST API endpoints.

\- Ollama for local LLM integration.

\- Qwen 2.5 (3B) for natural-language understanding and responses.

\- JSON files for simple data persistence.

\- Pytest for automated testing.



\## Features



\### Workforce Management

\- View registered employees and departments.

\- Submit leave requests.

\- Validate employee IDs and leave details.

\- Approve or reject leave requests.

\- Store manager decision notes.

\- Save leave records in JSON.



\### AI Agent Capabilities



The AI agent uses Python function calling to retrieve workforce information.



Four available tools:



1\. `get\_employees` – retrieves registered employees.

2\. `get\_pending\_requests` – retrieves pending leave applications.

3\. `get\_employee\_leave\_history` – retrieves an employee's leave history using their name or employee ID.

4\. `get\_leave\_statistics` – calculates approved, rejected and pending request totals.



The agent is currently read-only. It cannot approve or reject leave through AI tool calling.



\### REST API



The FastAPI application exposes the following endpoints:



| Method | Endpoint | Purpose |

|---|---|---|

| GET | `/` | API welcome message |

| GET | `/health` | Health check |

| GET | `/employees` | Retrieve employees |

| GET | `/leave-requests` | Retrieve leave requests |

| POST | `/leave-requests` | Submit a leave request |

| PATCH | `/leave-requests/{request\_id}` | Approve or reject a request |

| POST | `/agent/chat` | Ask the AI agent a question |



Interactive API documentation is available at `/docs`.



\## Technology Stack



\- Python

\- FastAPI

\- Pydantic

\- Ollama

\- Qwen 2.5 (3B)

\- JSON

\- Pytest

\- HTTPX



\## Installation and Setup



\### 1. Clone the repository



```powershell

git clone https://github.com/PocketPath-CEO/workforce-intelligence-agent.git

cd workforce-intelligence-agent

```



\### 2. Install dependencies



```powershell

python -m pip install fastapi uvicorn pydantic ollama pytest httpx

```



\### 3. Install Ollama



Download Ollama:



https://ollama.com/download



\### 4. Download the AI model



```powershell

ollama pull qwen2.5:3b

```



\### 5. Run the application



Start the REST API:



```powershell

python -m uvicorn api:app --reload

```



Open the interactive documentation:



http://127.0.0.1:8000/docs



\## Running the Console Application



```powershell

python app.py

```



\## Running the AI Agent in the Terminal



```powershell

python ai\_agent.py

```



\## Running Automated Tests



```powershell

python -m pytest -v

```



The current test suite contains eight passing tests covering core workforce functionality and API operations.



\## Project Structure



```text

Workforce\_Intelligence\_Agent/

│

├── app.py

├── api.py

├── ai\_agent.py

├── requirements.txt

├── README.md

├── .gitignore

│

├── data/

│   └── leave\_requests.json

│

└── tests/

&#x20;   ├── test\_app.py

&#x20;   └── test\_api.py

```



\## Current Limitations



This is a learning and demonstration project, not a production HR system.



\- Uses demonstration employee records.

\- Uses local JSON storage rather than a production database.

\- Does not implement authentication or role-based access control.

\- The AI agent has read-only workforce tools.

\- The AI model runs locally through Ollama.

\- No integration with external HR platforms.



Real employee or confidential information should not be entered into the demonstration application.



\## Skills Demonstrated



\- Python programming and functions.

\- Dictionaries, lists and loops.

\- JSON serialization and file handling.

\- REST API development.

\- FastAPI and Pydantic.

\- Local LLM integration.

\- AI function calling and tool execution.

\- Automated testing with Pytest.

\- API validation and error handling.



\## Development Background



This project was developed as a practical learning exercise to explore how Python applications, REST APIs and locally hosted language models can work together.



The focus is on building an AI agent that retrieves real application data through controlled Python functions rather than relying solely on generated responses.



