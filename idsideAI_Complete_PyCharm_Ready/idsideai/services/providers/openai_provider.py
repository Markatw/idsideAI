import httpx, time
from ..telemetry import Telemetry
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
async def run_openai(prompt: str, model: str, api_key: str) -> dict:
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": model or "gpt-4o-mini", "messages":[{"role":"user","content":prompt}]}
    t0=time.perf_counter()
    async with httpx.AsyncClient(timeout=60) as client:
        r=await client.post(OPENAI_URL, json=payload, headers=headers)
        r.raise_for_status()
        data=r.json()
    dt=time.perf_counter()-t0
    Telemetry.log("openai", {"latency_ms": int(dt*1000)})
    return {"provider":"openai","model":payload["model"],"response":data}
