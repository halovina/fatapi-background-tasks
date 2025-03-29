from fastapi import FastAPI, BackgroundTasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from contextlib import asynccontextmanager

app = FastAPI()
scheduler = AsyncIOScheduler()

# Simulation task
async def heavy_task(task_id: str):
    try:
        print(f"Starting task: {task_id}")
        await asyncio.sleep(5)  # Heavy process simulation
        print(f"Task {task_id} finished!")
    finally:
        del task_id
    

# Scheduled tasks
async def scheduled_task():
    await heavy_task("scheduled_task")

# Lifecycle for scheduler
@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(scheduled_task, "interval", seconds=10)
    scheduler.start()
    yield
    scheduler.shutdown()

app.router.lifespan_context = lifespan

# Manual endpoints
@app.post("/trigger-task/")
async def trigger_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(heavy_task, "manual_task")
    return {"message": "Task triggered!"}