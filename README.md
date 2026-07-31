# To-Do List CRUD API

A lightweight RESTful API built with **Python**, **FastAPI** and **SQLite** to manage a simple to-do list. Built as part of the FlyRank Internship Backend Track (Week 3 — Assignment A2) to demonstrate HTTP request-response mechanics, CRUD operations, input validation, proper HTTP status codes, and automatic OpenAPI/Swagger documentation and database layer.

---

## Database Architecture & Persistence

This project use **SQLite** which replace the in-memory list, which would get wiped with every server restart.

### Why SQLite?

* **Zero Overhead:** It's serverless and required no background services to be managed locally.
* **Portable & lightweight:** Everthing lives in a single file `tasks.db` in project root.
* **Auto-Initialization:** On Startup, the app check if `tasks.db` exits. If doen't the automatic crates file with table schema and three initial tasks automatically.

> **Note on Version Control:** `tasks.db` is explicitly ignored via `.gitignore`. So when cloning user start with clean database.

---

## 🚀 Getting Started

### Prerequisites

* **Python 3.10+**
* [uv](https://github.com/astral-sh/uv) (Python package installer & project manager)

### Installation & Running

1. **Clone the repository:**

   ```bash
   git clone [https://github.com/GovIndLok/task-crud-api.git](https://github.com/GovIndLok/task-crud-api.git)
   cd task-crud-api
    ```

2. **Sync dependencies and start the server:**

    ```bash
    uv sync
    uv run uvicorn main:app --reload --port 8000
    ```

---

## Data Exploration

To verify that the database layer independently from FastAPI routes, directly execute query from **DB Browser for SQLite** against `tasks.db`

### Example SQL query

Query:

```SQL
SELECT * FROM tasks WHERE done = 1;
```

Output:

```
Execution finished without errors.
Result: 3 rows returned in 4ms
At line 1:
SELECT * FROM taskbase WHERE done = 1;
```

Screenshot:
![DB browser executing sql query](docs/sql_browser_query.png)
