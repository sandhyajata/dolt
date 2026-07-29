from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from .models import GoalRequest
from .agent import run_goal, approve_learning

app = FastAPI(title="DoIt Agent", version="0.1.0")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def home():
    path = Path(__file__).parent.parent / "web" / "index.html"
    return path.read_text(encoding="utf-8")

@app.post("/api/goals")
async def goals(req: GoalRequest):
    return await run_goal(req.goal)

@app.post("/api/learnings/{learning_id}/approve")
async def approve(learning_id: str):
    result = await approve_learning(learning_id)
    if not result.get("ok"):
        raise HTTPException(status_code=400, detail=result)
    return result
