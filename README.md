# DoIt Agent

**An open-source AI agent that learns from other agents and teaches them back.**

This GitHub-ready MVP demonstrates a collective-intelligence agent:

1. User submits a goal.
2. DoIt queries an AiOps Enabler-compatible Learning Layer.
3. Relevant learnings are supplied to the LLM as fallible evidence.
4. DoIt produces a plan and answer.
5. An execution receipt is generated.
6. DoIt proposes one reusable learning.
7. The user must explicitly approve before it is contributed.

## Quick start

```bash
cp .env.example .env
```

Add your OpenAI key. To connect the real Learning Layer, also configure the
AiOps Enabler URL, API key, and endpoint paths.

```bash
docker compose up --build
```

Then open `http://localhost:8000`.

Or:

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Important integration note

The public Knowledge Base describes the Learning Layer concept, but this starter
does not assume an undocumented production API contract. All Learning Layer
request/response mapping is isolated in `app/learning_layer.py`.

Set these after confirming your actual API:
- `AIOPS_ENABLER_BASE_URL`
- `AIOPS_ENABLER_API_KEY`
- `AIOPS_LEARNING_SEARCH_PATH`
- `AIOPS_LEARNING_CONTRIBUTE_PATH`

## Safety model

Shared learnings are context, not truth. DoIt tells the model to treat them as
fallible evidence. Learning contribution requires explicit human approval.

Before exposing this publicly, add user authentication, authorization, rate
limiting, persistent storage, moderation/PII filtering, audit logging, and
production-grade tool permissions.

## License

MIT
