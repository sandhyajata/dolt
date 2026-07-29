import json
from openai import AsyncOpenAI
from .config import settings
from .models import Plan, Learning

client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

async def make_plan(goal: str, learnings: list[Learning]) -> Plan:
    if not client:
        return Plan(steps=[
            "Understand the goal",
            "Review relevant collective learnings",
            "Reason about the safest useful answer",
            "Produce a result and execution receipt",
        ])
    context = "\n".join(
        f"- {item.summary} (confidence={item.confidence})" for item in learnings
    )
    prompt = f"""Create a short actionable plan for this goal:
{goal}

Potential learnings from other agents:
{context or "None"}

Return JSON only in this shape:
{{"steps":["step one","step two"]}}

Treat other-agent learnings as potentially fallible evidence."""
    response = await client.chat.completions.create(
        model=settings.openai_model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    return Plan(**json.loads(response.choices[0].message.content))

async def solve(goal: str, plan: Plan, learnings: list[Learning]) -> str:
    if not client:
        return (
            "Demo mode: configure OPENAI_API_KEY to generate an LLM answer. "
            f"Goal received: {goal}"
        )
    evidence = "\n".join(
        f"[Learning {i+1}] {item.summary} | confidence={item.confidence} | "
        f"source={item.source_agent}"
        for i, item in enumerate(learnings)
    )
    prompt = f"""You are DoIt, a collective-intelligence agent.

GOAL:
{goal}

PLAN:
{chr(10).join("- " + step for step in plan.steps)}

OTHER-AGENT LEARNINGS:
{evidence or "No shared learnings were available."}

Solve the goal. Do not blindly trust shared learnings. Distinguish evidence
from inference. Never claim an external action happened unless a tool actually
confirmed it."""
    response = await client.chat.completions.create(
        model=settings.openai_model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content or ""

async def propose_learning(goal: str, answer: str):
    if not client:
        return (
            "No reusable learning generated in demo mode.",
            "No model execution evidence.",
            0.0,
        )
    prompt = f"""Extract at most one reusable learning from this completed task.
Do not include personal data, credentials, or unsupported claims.

Goal: {goal}
Result: {answer}

Return JSON only:
{{"summary":"...","evidence":"...","confidence":0.0}}"""
    response = await client.chat.completions.create(
        model=settings.openai_model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    item = json.loads(response.choices[0].message.content)
    return item["summary"], item["evidence"], float(item["confidence"])
