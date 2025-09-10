from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()

BRAND_CSS = '<link rel="stylesheet" href="/static/style.css">'


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    from app.ui.copy import COPY
    return """
    <!doctype html><html lang='en'><head>
      <meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
      <title>{COPY['home']['title']}</title>{BRAND_CSS}
    </head><body>
    {{_NAV}}
    <main class='container home'>
      <h1>{COPY['home']['hero_h1']}</h1>
      <p class='tag'>{COPY['home']['hero_sub']}</p>
      <button onclick="location.href='/dashboard'">{COPY['home']['cta_open']}</button>
      <button onclick="location.href='/export'">{COPY['home']['cta_export']}</button>
      <details><summary>{COPY['common']['help']}</summary>
        <p>Use the dashboard to navigate your workspace.</p>
        <p>You can open your workspace, chat, docs, presence, and export a snapshot.</p>
      </details>
    </main>
    {{_FOOT}}
    </body></html>
    """.replace("{{_NAV}}", _navbar()).replace("{{_FOOT}}", _footer())

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    from app.ui.copy import COPY
    return """
    <!doctype html><html lang='en'><head>
      <meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
      <title>{COPY['dashboard']['title']}</title>{BRAND_CSS}
    </head><body>
    {{_NAV}}
    <main class='container dashboard'>
      <h1>{COPY['dashboard']['title']}</h1>
      <section><h2>{COPY['dashboard']['presence']}</h2><div id='presence'></div></section>
      <section><h2>{COPY['dashboard']['chat']}</h2><div id='chat'></div></section>
      <section><h2>{COPY['dashboard']['docs']}</h2><div id='docs'></div></section>
      <details><summary>{COPY['common']['help']}</summary>
        <ul>
          <li>Check team availability under Presence.</li>
          <li>Review and send messages under Chat.</li>
          <li>Access and edit shared documents under Docs.</li>
          <li>All changes are logged in Activity.</li>
        </ul>
      </details>
    </main>
    {{_FOOT}}
    </body></html>
    """.replace("{{_NAV}}", _navbar()).replace("{{_FOOT}}", _footer())

@router.get("/chat", response_class=HTMLResponse)
def chat(request: Request):
    from app.ui.copy import COPY
    return """
    <!doctype html><html lang='en'><head>
      <meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
      <title>{COPY['chat']['title']}</title>{BRAND_CSS}
    </head><body>
    {{_NAV}}
    <main class='container chat'>
      <h1>{COPY['chat']['title']}</h1>
      <div id='chat-messages'>{COPY['chat']['empty']}</div>
      <form id='chat-form'>
        <input type='text' NOTE="{COPY['chat']['NOTE']}" />
        <button type='submit'>{COPY['chat']['send']}</button>
      </form>
      <details><summary>{COPY['common']['help']}</summary>
        <ul>
          <li>Type your message in the box and press Send.</li>
          <li>Messages will appear above in order, newest last.</li>
          <li>Chats are stored with your workspace activity.</li>
        </ul>
      </details>
    </main>
    {{_FOOT}}
    </body></html>
    """.replace("{{_NAV}}", _navbar()).replace("{{_FOOT}}", _footer())

@router.get("/docs", response_class=HTMLResponse)
def docs(request: Request):
    from app.ui.copy import COPY
    return """
    <!doctype html><html lang='en'><head>
      <meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
      <title>{COPY['docs']['title']}</title>{BRAND_CSS}</head><body>
    {{_NAV}}
    <main class='container docs'>
      <h1>{COPY['docs']['title']}</h1>
      <div id="list">{COPY['docs']['empty']}</div>
      <section id="editor" class="hidden">
        <h3 id="ed-title">{COPY['docs']['edit']}</h3>
        <textarea id="ed-text" rows="8"></textarea><br>
        <button onclick="save()">{COPY['docs']['save']}</button>
      </section>
      <h3>{COPY['docs']['new']}</h3>
      <form id="newf"><input id="newt" NOTE="Title"><br><textarea id="newb" rows="4"></textarea><br><button>{COPY['docs']['save']}</button></form>
      <details><summary>{COPY['common']['help']}</summary>
        <ul>
          <li>Create a new doc below. Give it a clear title.</li>
          <li>Open a doc to edit. Your changes are saved with the Save button.</li>
          <li>Docs are shared with your workspace and appear in Activity.</li>
        </ul>
      </details>
    </main>
    {{_FOOT}}
    </body></html>
    """.replace("{{_NAV}}", _navbar()).replace("{{_FOOT}}", _footer())

@router.get("/presence", response_class=HTMLResponse)
def presence(request: Request):
    from app.ui.copy import COPY
    return """
    <!doctype html><html lang='en'><head>
      <meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
      <title>{COPY['presence']['title']}</title>{BRAND_CSS}</head><body>
    {{_NAV}}
    <main class='container presence'>
      <h1>{COPY['presence']['title']}</h1>
      <div id="presence-list">{COPY['presence']['legend']}</div>
      <details><summary>{COPY['common']['help']}</summary>
        <ul>
          <li>{COPY['presence']['legend']}</li>
          <li>Presence updates automatically every few minutes.</li>
          <li>Only your workspace members can see who is active.</li>
        </ul>
      </details>
    </main>
    {{_FOOT}}
    </body></html>
    """.replace("{{_NAV}}", _navbar()).replace("{{_FOOT}}", _footer())

@router.get("/activity", response_class=HTMLResponse)
def activity(request: Request):
    from app.ui.copy import COPY
    return """
    <!doctype html><html lang='en'><head>
      <meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
      <title>{COPY['activity']['title']}</title>{BRAND_CSS}</head><body>
    {{_NAV}}
    <main class='container activity'>
      <h1>{COPY['activity']['title']}</h1>
      <div id="feed">{COPY['activity']['empty']}</div>
      <details><summary>{COPY['common']['help']}</summary>
        <ul>
          <li>Activity shows a timeline of workspace changes.</li>
          <li>Includes chat, docs edits, presence updates and exports.</li>
          <li>Use this log for auditing and accountability.</li>
        </ul>
      </details>
    </main>
    {{_FOOT}}
    </body></html>
    """.replace("{{_NAV}}", _navbar()).replace("{{_FOOT}}", _footer())

@router.get("/export", response_class=HTMLResponse)
def export_ui(request: Request):
    from app.ui.copy import COPY
    return """
    <!doctype html><html lang='en'><head>
      <meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
      <title>{COPY['export']['title']}</title>{BRAND_CSS}
    </head><body>
    {{_NAV}}
    <main class='container export'>
      <h1>{COPY['export']['title']}</h1>
      <button onclick="doExport()">{COPY['export']['button']}</button>
      <p id="st">{COPY['export']['note']}</p>
      <details><summary>{COPY['common']['help']}</summary>
        <ul>
          <li>Exports include workspace, settings, roles, members, chat, docs, presence and activity.</li>
          <li>Downloads as a JSON file for backup, migration or audit.</li>
          <li>Share exports carefully. They may contain sensitive data.</li>
        </ul>
      </details>
    </main>
    {{_FOOT}}
    <script>
    async function ctx(){try{return await fetch('/workspaces/context').then(r=>r.json())}catch(e){return null}}
    async function doExport(){st.textContent='Exporting…';const c=await ctx();const ws=(c&&(c.ws&&c.ws.id||c.id))||null;if(!ws){st.textContent='No workspace';return}
      const blob=await fetch(`/workspaces/${ws}/export`).then(r=>r.blob());const url=URL.createObjectURL(blob);
      const a=document.createElement('a');a.href=url;a.download=`workspace_${ws}.json`;a.click();URL.revokeObjectURL(url);st.textContent='Download ready';}
    </script>
    </body></html>
    """.replace("{{_NAV}}", _navbar()).replace("{{_FOOT}}", _footer())


@router.get("/help", response_class=HTMLResponse)
def help_index(request: Request):
    from app.ui.copy import COPY
    return """
    <!doctype html><html lang='en'><head>
      <meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
      <title>Help — ID‑SIDE AI</title>{BRAND_CSS}
    </head><body>
    {{_NAV}}
    <main class='container help'>
      <h1>Help & Guides</h1>
      <ul class='list'>
        <li><a href='/'>{COPY['home']['title']}</a> — {COPY['home']['hero_sub']}</li>
        <li><a href='/dashboard'>{COPY['dashboard']['title']}</a> — Presence, Chat, Docs overview</li>
        <li><a href='/chat'>{COPY['chat']['title']}</a> — Send and review messages</li>
        <li><a href='/docs'>{COPY['docs']['title']}</a> — Create and edit shared documents</li>
        <li><a href='/presence'>{COPY['presence']['title']}</a> — {COPY['presence']['legend']}</li>
        <li><a href='/activity'>{COPY['activity']['title']}</a> — Workspace audit trail</li>
        <li><a href='/export'>{COPY['export']['title']}</a> — {COPY['export']['note']}</li>
      </ul>
    </main>
    {{_FOOT}}
    </body></html>
    """.replace("{{_NAV}}", _navbar()).replace("{{_FOOT}}", _footer())
