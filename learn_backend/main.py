from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Query

app = FastAPI(
    title="Learn Backend API",
    description="A step-by-step learning API for backend concepts",
    version="0.1.0",
)

# ---------------------------------------------------------------------------
# In-memory storage (replaced with a real database in PR 6-9)
# ---------------------------------------------------------------------------
tasks_db: dict[UUID, dict] = {}


@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "ok", "message": "Service is running"}


# ---------------------------------------------------------------------------
# POST /tasks -- Create a task (JSON request body)
# ---------------------------------------------------------------------------
@app.post("/tasks", status_code=201, tags=["Tasks"])
async def create_task(task: dict):
    task_id = uuid4()
    new_task = {
        "id": str(task_id),
        "title": task.get("title", "Untitled"),
        "description": task.get("description", ""),
        "status": "pending",
    }
    tasks_db[task_id] = new_task
    return {"message": "Task created", "data": new_task}


# ---------------------------------------------------------------------------
# GET /tasks -- List tasks with optional query param filters
# ---------------------------------------------------------------------------
@app.get("/tasks", tags=["Tasks"])
async def list_tasks(
    status: str | None = Query(None, description="Filter by status: pending, done"),
    search: str | None = Query(None, description="Search in task title"),
):
    results = list(tasks_db.values())

    if status:
        results = [t for t in results if t["status"] == status]

    if search:
        results = [t for t in results if search.lower() in t["title"].lower()]

    return {"message": "Tasks retrieved", "data": results, "count": len(results)}


# ---------------------------------------------------------------------------
# GET /tasks/{task_id} -- Get a single task by ID (path parameter)
# ---------------------------------------------------------------------------
@app.get("/tasks/{task_id}", tags=["Tasks"])
async def get_task(task_id: UUID):
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task retrieved", "data": task}


# ---------------------------------------------------------------------------
# PUT /tasks/{task_id} -- Update a task (path param + JSON body)
# ---------------------------------------------------------------------------
@app.put("/tasks/{task_id}", tags=["Tasks"])
async def update_task(task_id: UUID, updates: dict):
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if "title" in updates:
        task["title"] = updates["title"]
    if "description" in updates:
        task["description"] = updates["description"]
    if "status" in updates:
        task["status"] = updates["status"]

    return {"message": "Task updated", "data": task}


# ---------------------------------------------------------------------------
# DELETE /tasks/{task_id} -- Delete a task
# ---------------------------------------------------------------------------
@app.delete("/tasks/{task_id}", tags=["Tasks"])
async def delete_task(task_id: UUID):
    task = tasks_db.pop(task_id, None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted", "data": task}
