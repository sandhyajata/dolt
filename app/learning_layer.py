import httpx
from .config import settings
from .models import Learning, ProposedLearning

class LearningLayerClient:
    """Adapter for an AiOps Enabler-compatible Learning Layer.

    Confirm the production API contract and adjust only this file if its
    endpoint paths or response fields differ.
    """

    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {settings.aiops_enabler_api_key}",
            "Content-Type": "application/json",
        }

    async def search(self, query: str, limit: int = 8) -> list[Learning]:
        if not settings.aiops_enabler_api_key:
            return []
        url = settings.aiops_enabler_base_url.rstrip("/") + settings.aiops_learning_search_path
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.post(
                    url, headers=self.headers, json={"query": query, "limit": limit}
                )
                response.raise_for_status()
                data = response.json()
            items = data.get("learnings", data.get("items", []))
            return [
                Learning(
                    id=str(item.get("id", "")),
                    summary=str(item.get("summary", item.get("content", ""))),
                    confidence=float(item.get("confidence", 0)),
                    source_agent=str(item.get("source_agent", item.get("agent_id", ""))),
                    metadata=item.get("metadata", {}),
                )
                for item in items
                if item.get("summary") or item.get("content")
            ]
        except Exception:
            return []

    async def contribute(self, learning: ProposedLearning) -> dict:
        if not settings.aiops_enabler_api_key:
            return {"ok": False, "reason": "AIOPS_ENABLER_API_KEY is not configured"}
        url = settings.aiops_enabler_base_url.rstrip("/") + settings.aiops_learning_contribute_path
        payload = {
            "summary": learning.summary,
            "evidence": learning.evidence,
            "confidence": learning.confidence,
        }
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return {"ok": True, "remote": response.json()}
