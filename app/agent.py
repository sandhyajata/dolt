import time
import uuid
from .learning_layer import LearningLayerClient
from .llm import make_plan, solve, propose_learning
from .models import GoalResult, ProposedLearning

learning_layer = LearningLayerClient()
pending: dict[str, ProposedLearning] = {}

async def run_goal(goal: str) -> GoalResult:
    started = time.perf_counter()
    learnings = await learning_layer.search(goal)
    plan = await make_plan(goal, learnings)
    answer = await solve(goal, plan, learnings)

    summary, evidence, confidence = await propose_learning(goal, answer)
    proposal = ProposedLearning(
        id=str(uuid.uuid4()),
        summary=summary,
        evidence=evidence,
        confidence=max(0.0, min(1.0, confidence)),
    )
    pending[proposal.id] = proposal

    receipt = {
        "execution_id": str(uuid.uuid4()),
        "status": "completed",
        "duration_seconds": round(time.perf_counter() - started, 3),
        "steps_planned": len(plan.steps),
        "learnings_considered": len(learnings),
        "learning_contribution_status": "awaiting_human_approval",
    }
    return GoalResult(
        goal=goal,
        plan=plan.steps,
        learnings_considered=learnings,
        answer=answer,
        receipt=receipt,
        proposed_learning=proposal,
    )

async def approve_learning(learning_id: str):
    item = pending.get(learning_id)
    if not item:
        return {"ok": False, "reason": "Unknown learning"}
    item.approved = True
    result = await learning_layer.contribute(item)
    if result.get("ok"):
        pending.pop(learning_id, None)
    return result
