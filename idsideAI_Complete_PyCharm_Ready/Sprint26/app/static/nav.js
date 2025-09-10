(function(){
  const links=[
    ['Dashboard','/ui/dashboard'],
    ['Viewer','/ui/viewer'],
    ['Editor','/ui/editor'],
    ['Execute','/ui/execute'],
    ['Inspect','/ui/inspect'],
    ['Search','/ui/search'],
    ['Import/Export','/ui/io'],
    ['Admin','/ui/admin'],
    ['Workspaces','/ui/workspaces'],
    ['Onboarding','/ui/onboarding'],
    ['Home','/ui']
  ];
  const bar=document.createElement('div');
  bar.style.cssText='background:#0b47a1;color:#fff;padding:8px 12px;display:flex;flex-wrap:wrap;gap:10px;align-items:center';
  const ws=(localStorage.getItem('idside_ws')||'personal');
  const left=document.createElement('strong'); left.textContent='IDECIDE • '+ws.toUpperCase();
  bar.appendChild(left);
  links.forEach(([t,href])=>{const a=document.createElement('a');a.textContent=t;a.href=href;a.style.cssText='color:#fff;text-decoration:none;background:rgba(255,255,255,.12);padding:6px 8px;border-radius:8px';bar.appendChild(a);});
  document.body.insertBefore(bar, document.body.firstChild);
})();
// S10.15 toast + aria-live region
(function(){
  const t=document.createElement('div'); t.id='toast'; t.setAttribute('aria-live','polite');
  t.style.cssText='position:fixed;right:16px;bottom:16px;background:#111827;color:#fff;padding:10px 12px;border-radius:10px;box-shadow:0 4px 10px rgba(0,0,0,.2);opacity:0;transition:opacity .2s';
  document.body.appendChild(t);
  window.toast=function(msg){ t.textContent=msg; t.style.opacity='1'; setTimeout(()=>{t.style.opacity='0'}, 1600); };
})();
// S11.7: pick workspace from session if present
;(function(){
  try{
    fetch('/auth/session').then(r=>r.json()).then(d=>{
      var ws = (d && d.workspace) ? d.workspace : (localStorage.getItem('idside_ws')||'personal');
      localStorage.setItem('idside_ws', ws);
      var bar = document.body.firstChild; if(bar && bar.firstChild && bar.firstChild.tagName==='STRONG'){ bar.firstChild.textContent='IDECIDE • '+String(ws).toUpperCase(); }
    }).catch(function(){});
  }catch(e){}
})();

// S11.8: show current user & logout link in header
;(function(){
  try{
    fetch('/auth/whoami').then(r=>r.json()).then(d=>{
      var user = (d && d.user && d.user.username) ? d.user.username : null;
      // ensure header bar exists (created by earlier nav.js)
      var bar = document.body.firstChild;
      if(!bar) return;
      // Right container
      var right = document.createElement('span');
      right.style.cssText='margin-left:auto;display:flex;gap:10px;align-items:center';
      var ws = (localStorage.getItem('idside_ws')||'personal');
      var who = document.createElement('span');
      who.textContent = (user ? ('@'+user) : 'guest') + ' • ' + ws;
      var out = document.createElement('a');
      out.href = '#'; out.textContent = 'Logout';
      out.onclick = function(ev){ ev.preventDefault(); fetch('/auth/logout',{method:'POST'}).then(function(){ try{toast('Logged out')}catch(e){}; location.href='/ui/login';}); };
      right.appendChild(who);
      right.appendChild(out);
      bar.appendChild(right);
    }).catch(function(){});
  }catch(e){}
})();
// S11.9: poll session to reflect expiry and flip header to guest
;(function(){
  try{
    function updateHeader(auth, ws){
      var bar = document.body.firstChild; if(!bar) return;
      var strong = bar.firstChild; if(strong && ws){ strong.textContent='IDECIDE • '+String(ws).toUpperCase(); }
      // find right segment (user • ws + Logout)
      var right = bar.lastChild;
      if(!right || right.tagName==='STRONG'){ right = document.createElement('span'); right.style.cssText='margin-left:auto;display:flex;gap:10px;align-items:center'; bar.appendChild(right); }
      right.innerHTML='';
      var who = document.createElement('span'); who.textContent=(auth && auth.user ? ('@'+auth.user) : 'guest') + ' • ' + (ws||'personal');
      right.appendChild(who);
      if(auth && auth.user){
        var out = document.createElement('a'); out.href='#'; out.textContent='Logout';
        out.onclick=function(ev){ev.preventDefault(); fetch('/auth/logout',{method:'POST'}).then(function(){ try{toast('Logged out')}catch(e){}; location.href='/ui/login';});};
        right.appendChild(out);
      } else {
        var login = document.createElement('a'); login.href='/ui/login'; login.textContent='Login'; right.appendChild(login);
      }
    }
    function tick(){
      fetch('/auth/session').then(r=>r.json()).then(d=>{
        var ws = (d && d.workspace) ? d.workspace : (localStorage.getItem('idside_ws')||'personal');
        // Fetch whoami to know username (optional)
        fetch('/auth/whoami').then(r=>r.json()).then(w=>{
          var user = (w && w.user && w.user.username) ? w.user.username : null;
          updateHeader({user:user}, ws);
        }).catch(function(){ updateHeader({user:null}, ws); });
        localStorage.setItem('idside_ws', ws);
      }).catch(function(){ /* ignore */ });
    }
    setInterval(tick, 5000); // lightweight poll
  }catch(e){}
})();

// S11.26: logout polish (confirm, clear localStorage, toast, redirect)
window.__ids_logout = function(ev){
  if(ev) ev.preventDefault();
  if(!confirm('Log out now?')) return false;
  fetch('/auth/logout',{method:'POST'})
    .then(function(){ try{localStorage.removeItem('idside_ws');toast('Logged out')}catch(e){}; window.location.href='/ui/login'; })
    .catch(function(){ window.location.href='/ui/login'; });
  return false;
};
