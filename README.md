# To-Do List CRUD API

A lightweight RESTful API built with **Python**, **FastAPI** to manage a simple to-do list. Built as part of the FlyRank Internship Backend Track. This version upgrades the storage layer to a **PostgreSQL** database running inside a **Docker** container, demonstrating containerized development, environment variable secrets, and multi-container orchestration.

---

## 🚀 Getting Started

### Prerequisites

* **Python 3.10+**
* [uv](https://github.com/astral-sh/uv) (Python package installer & project manager)
* [Docker](https://www.docker.com/) and **Docker Compose** (for the PostgreSQL container)

### Installation & Running

1. **Clone the repository:**

   ```bash
   git clone [https://github.com/GovIndLok/task-crud-api.git](https://github.com/GovIndLok/task-crud-api.git)
   cd task-crud-api
    ```

2. **Set up environment variables:**
Copy the example environment file to set up your local database credentials.

```bash
cp .env.example .env
```

3. **Start the complete stack:**

```bash
docker compose up --build
```

---

## Data Exploration

To verify that the database layer independently from FastAPI routes, directly execute query from **postgres container**.

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