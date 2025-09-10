/* S20.7 — Focus trap + keyboard close (≤50 LOC) */
(function(){
  function q(sel,root){return Array.from((root||document).querySelectorAll(sel));}
  function trap(root){
    const f=()=>q('[tabindex],a[href],button,input,select,textarea,[role="button"]:not([aria-disabled="true"])',root)
      .filter(el=>!el.hasAttribute('disabled')&&!el.getAttribute('aria-hidden'));
    function onKey(e){
      if(e.key==='Escape' && root.dataset.escClose!=='false'){ root.dispatchEvent(new CustomEvent('a11y:close',{bubbles:true})); }
      if(e.key!=='Tab') return;
      const F=f(); if(!F.length) return;
      const first=F[0], last=F[F.length-1];
      const a=document.activeElement;
      if(e.shiftKey && a===first){ last.focus(); e.preventDefault(); }
      else if(!e.shiftKey && a===last){ first.focus(); e.preventDefault(); }
    }
    root.addEventListener('keydown', onKey);
    root.__a11y_untrap = ()=> root.removeEventListener('keydown', onKey);
  }
  document.addEventListener('DOMContentLoaded', ()=>{
    q('[data-focus-trap]').forEach(el=>trap(el));
    // keyboard-only banner toggle support
    let k=false; addEventListener('keydown',e=>{ if(e.key==='Tab'&&!k){ document.body.classList.add('using-kbd'); k=true; }});
  });
})();
/* S20.11 — live region announcer (≤30 LOC) */
(function(){
  function ensureRegion(mode){
    var id='sr-live-'+mode;
    var r=document.getElementById(id);
    if(!r){
      r=document.createElement('div');
      r.id=id;
      r.setAttribute('role', mode==='assertive'?'alert':'status');
      r.setAttribute('aria-live', mode);
      r.className='sr-live';
      document.body.appendChild(r);
    }
    return r;
  }
  window.a11yAnnounce=function(msg, opts){
    opts=opts||{}; var mode=(opts.mode||'polite');
    var r=ensureRegion(mode);
    r.textContent='';
    setTimeout(function(){ r.textContent=msg||''; }, 50);
  };
})();
/* S20.12 — form describe/required helper (≤25 LOC) */
(function(){
  function wire(){
    document.querySelectorAll('input,select,textarea').forEach(function(el){
      var ids=[], attrs=['data-hint','data-error','data-describe'];
      attrs.forEach(function(a){ var v=el.getAttribute(a); if(v) ids.push(v); });
      var exist=el.getAttribute('aria-describedby'); if(exist) ids.push(exist);
      if(ids.length) el.setAttribute('aria-describedby', ids.join(' ').trim());
      if(el.required && !el.hasAttribute('aria-required')) el.setAttribute('aria-required','true');
    });
  }
  if(document.readyState!=='loading') wire();
  else document.addEventListener('DOMContentLoaded', wire);
})();
/* S20.13 — focus-visible polyfill + skip link focus */
(function(){
  var usingKbd=false;
  addEventListener('keydown', function(e){ if(e.key==='Tab'||e.key==='ArrowDown'||e.key==='ArrowUp'||e.key==='ArrowLeft'||e.key==='ArrowRight'){ usingKbd=true; document.body.classList.add('using-kbd'); } });
  addEventListener('mousedown', function(){ usingKbd=false; });
  addEventListener('touchstart', function(){ usingKbd=false; }, {passive:true});
  addEventListener('focusin', function(e){
    if(usingKbd && e.target instanceof HTMLElement){ e.target.classList.add('focus-visible'); }
  });
  addEventListener('focusout', function(e){
    if(e.target instanceof HTMLElement){ e.target.classList.remove('focus-visible'); }
  });
  // Skip link: move focus to target, even if non-focusable
  document.addEventListener('click', function(e){
    var a=e.target.closest && e.target.closest('a.skip-link');
    if(!a) return;
    var href=a.getAttribute('href')||''; if(!href.startsWith('#')) return;
    var id=href.slice(1); var t=document.getElementById(id); if(!t) return;
    e.preventDefault();
    var hadTabindex=t.hasAttribute('tabindex');
    if(!hadTabindex) t.setAttribute('tabindex','-1');
    t.classList.add('skip-target');
    t.focus({preventScroll:false});
    // Clean up tabindex after blur
    function cleanup(){ if(!hadTabindex) t.removeAttribute('tabindex'); t.classList.remove('skip-target'); t.removeEventListener('blur', cleanup); }
    t.addEventListener('blur', cleanup);
  });
})();
/* S20.15 — chart a11y helper (≤30 LOC) */
(function(){
  function enhanceChart(root){
    var g=root.querySelector('canvas,svg'); if(!g) return;
    var titleId=root.getAttribute('data-title-id');
    var label=root.getAttribute('data-label')||'';
    g.setAttribute('tabindex','0');
    g.setAttribute('role','img');
    if(titleId){ g.setAttribute('aria-labelledby', titleId); }
    else if(label){ g.setAttribute('aria-label', label); }
    // If there's a hidden table, link it via aria-describedby
    var tid=root.getAttribute('data-table-id');
    if(tid){ g.setAttribute('aria-describedby', tid); }
  }
  function init(){ document.querySelectorAll('.chart[data-a11y-chart]').forEach(enhanceChart); }
  if(document.readyState!=='loading') init(); else document.addEventListener('DOMContentLoaded', init);
  window.a11yChart = enhanceChart;
})();