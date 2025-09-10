from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.services.enterprise_service import set_api_key, list_api_keys

router = APIRouter(prefix="/settings", tags=["settings"])

class KeyIn(BaseModel):
    provider: str
    api_key: str

@router.get("")
async def settings_page():
    from fastapi.responses import HTMLResponse
    html = """
    <!doctype html><html><head><meta charset="utf-8"><title>Settings — idsideAI</title>
      <link rel="stylesheet" href="/static/css/idsideai.css">
    </head><body>
    <main class="container" style="max-width:900px">
      <h1>Settings — API Keys</h1>
      <p>Bring your own keys so idsideAI can route requests to your preferred providers.</p>
      <form id="f">
        <label>Provider</label>
        <select id="provider">
          <option value="openai">OpenAI</option>
          <option value="anthropic">Anthropic</option>
          <option value="gemini">Gemini</option>
          <option value="mistral">Mistral</option>
          <option value="groq">Groq</option>
          <option value="cohere">Cohere</option>
        </select>
        <label>API Key</label>
        <input id="api_key" type="password" placeholder="sk-..." style="width:100%">
        <button type="button" onclick="save()">Save</button>
      </form>
      <h3 style="margin-top:16px;">Your Keys</h3>
      <pre id="out" class="code"></pre>
    </main>
    <script>
    async function save(){
      const provider = document.getElementById('provider').value;
      const api_key = document.getElementById('api_key').value;
      const res = await fetch('/settings/keys', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({provider, api_key})});
      await load();
    }
    async function load(){
      const res = await fetch('/settings/keys');
      const data = await res.json();
      document.getElementById('out').textContent = JSON.stringify(data, null, 2);
    }
    load();
    </script>
    </body></html>
    """
    return HTMLResponse(html)

@router.get("/keys")
async def get_keys(request: Request):
    uid = request.session.get("user_id") if hasattr(request, "session") else None
    creds = list_api_keys(uid)
    return [{"provider":c.provider, "created_at": str(c.created_at)} for c in creds]

@router.post("/keys")
async def post_key(body: KeyIn, request: Request):
    uid = request.session.get("user_id") if hasattr(request, "session") else None
    set_api_key(uid, body.provider, body.api_key)
    return {"ok": True}