from pydantic import BaseModel, Field
from typing import Any

class GoalRequest(BaseModel):
    goal: str = Field(min_length=3, max_length=5000)

class Learning(BaseModel):
    id: str = ""
    summary: str
    confidence: float = 0.0
    source_agent: str = ""
    metadata: dict[str, Any] = {}

class Plan(BaseModel):
    steps: list[str]

class ProposedLearning(BaseModel):
    id: str
    summary: str
    evidence: str
    confidence: float = 0.5
    approved: bool = False

class GoalResult(BaseModel):
    goal: str
    plan: list[str]
    learnings_considered: list[Learning]
    answer: str
    receipt: dict[str, Any]
    proposed_learning: ProposedLearning | None = None
