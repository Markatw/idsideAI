import React, { useState } from 'react'
import GraphCanvas, { GraphNode, GraphEdge } from './components/GraphCanvas'
import WebGLGraphCanvas from './components/WebGLGraphCanvas'
import Inspector from './components/Inspector'
import Timeline from './components/Timeline'
import Billing from './components/Billing'
import CompareOverlay from './components/CompareOverlay'
import DownloadQueue, { Job } from './components/DownloadQueue'
import './styles/layout.css'
import Billing from './pages/Billing'
import { API_URL } from './config'
import { apiFetch } from './utils/api'

type Diff = {
  nodes_added: GraphNode[]
  nodes_removed: string[]
  edges_added: GraphEdge[]
  edges_removed: string[]
  props_changed: { id:string, field?:string, from_value?:string, to_value?:string }[]
}
export default function App(){
  type Density = 'cozy'|'compact'|'dense'
  type Renderer = 'svg'|'canvas'|'webgl'
  const [density, setDensity] = useState<Density>('cozy')
  const [renderer, setRenderer] = useState<Renderer>('svg')
  const [selected, setSelected] = useState<GraphNode|null>(null)
  const [view, setView] = useState<'graph'|'billing'>('graph')
  const [showHelp, setShowHelp] = useState(false)
  const [history, setHistory] = useState<any[]>([])
  const [future, setFuture] = useState<any[]>([])
  const [diff, setDiff] = useState<Diff|null>(null)
  const [jobs, setJobs] = useState<Job[]>([])
  const [renderer, setRenderer] = useState<'svg'|'webgl'>('svg')
  const [downloadUrl, setDownloadUrl] = useState<string>('')

  async function doSnapshot(){
    await fetch(`${API_URL}/graphs/demo/snapshot?root=DEC-1&depth=3`, {method:'POST'})
    const resSnaps = await fetch(`${API_URL}/graphs/demo/snapshots`).then(r=>r.json())
    const snaps = resSnaps.snapshots || []
    if(snaps.length>=2){
      const a = snaps[snaps.length-2].id, b = snaps[snaps.length-1].id
      const d = await fetch(`${API_URL}/graphs/demo/diff?frm=${a}&to=${b}`).then(r=>r.json())
      const dd = d.diff || d; setHistory(h=>[...(h||[]), dd]); setFuture([]); setDiff(dd); (window as any).__diff = dd
    }
  }
  async function doCompare(){
    const resSnaps = await fetch(`${API_URL}/graphs/demo/snapshots`).then(r=>r.json())
    const snaps = resSnaps.snapshots || []
    if(snaps.length>=2){
      const a = snaps[snaps.length-2].id, b = snaps[snaps.length-1].id
      const d = await fetch(`${API_URL}/graphs/demo/diff?frm=${a}&to=${b}`).then(r=>r.json())
      const dd = d.diff || d; setHistory(h=>[...(h||[]), dd]); setFuture([]); setDiff(dd); (window as any).__diff = dd
    }
  }
  async function exportWhy(){
    const resSnaps = await fetch(`${API_URL}/graphs/demo/snapshots`).then(r=>r.json())
    const snaps = resSnaps.snapshots || []
    if(snaps.length>=1){
      const latest = snaps[snaps.length-1].id
      const resp = await fetch(`${API_URL}/graphs/demo/export/why?decision=DEC-1&to=${latest}`, {method:'POST'}).then(r=>r.json())
      alert(`Exported: ${resp.file}`)
    }
  }
  return (
    <div className="app">
      <header className="header">
        <h1>IDECIDE — Decision Graphs</h1>
        <div className="kpis"><button className="btn ghost" onClick={()=>setView(view==="graph"?"billing":"graph")}>{view==="graph"?"Manage Billing":"Back to Graph"}</button>
          <span className="chip">Latency P95 &lt; 150ms</span>
          <span className="chip">2k nodes / 5k edges @60fps</span>
          <span className="chip ok">✓ WCAG 2.2 AA</span>
        </div>
      </header>
      
      <div className="toolbar">
        <button className="btn primary" onClick={()=>location.hash='#/graph'}>Graph</button>
        <button className="btn" onClick={()=>location.hash='#/billing'}>Billing</button>
      </div>
      <div className="toolbar">
        <button className="btn" onClick={()=>{const last=history.pop(); if(last){ setFuture(f=>[...(f||[]), diff]); setDiff(last); (window as any).__diff=last; }}}>Undo</button>
        <button className="btn" onClick={()=>{const nxt=future.pop(); if(nxt){ setHistory(h=>[...(h||[]), diff]); setDiff(nxt); (window as any).__diff=nxt; }}}>Redo</button>
        <button className="btn primary">+ Node</button>
        <button className="btn">Connect</button>
        <button className="btn" onClick={doSnapshot}>Snapshot</button>
        <button className="btn" onClick={doCompare}>Compare</button>
        <button className="btn" onClick={exportWhy}>Why</button>
        <button className="btn ghost">Share</button>
        <button className="btn" onClick={async()=>{
          const id = String(Date.now()); setJobs(j=>[...j,{id, type:'why', status:'pending'}])
          try{ const r = await fetch(`${API_URL}/graphs/demo/export/why?decision=DEC-1` ,{method:'POST'}); const data = await r.json();
                setJobs(j=>j.map(x=> x.id===id ? {...x, status:'done', url: data.pdf} : x))
              }catch(e:any){ setJobs(j=>j.map(x=> x.id===id ? {...x, status:'error', error:String(e)} : x)) }
        }}>Export Why</button>
        <button className="btn" onClick={async()=>{
          const id = String(Date.now()+1); setJobs(j=>[...j,{id, type:'audit', status:'pending'}])
          try{ const r = await fetch(`${API_URL}/graphs/demo/export/audit?frm=v1&to=v2`,{method:'POST'}); const data = await r.json();
                setJobs(j=>j.map(x=> x.id===id ? {...x, status:'done', url: data.url} : x))
              }catch(e:any){ setJobs(j=>j.map(x=> x.id===id ? {...x, status:'error', error:String(e)} : x)) }
        }}>Audit Export</button>
        <button className="btn" onClick={async()=>{ const r = await fetch(`${API_URL}/graphs/demo/export/why?decision=DEC-1&to=v2`,{method:'POST'}); const j = await r.json(); setDownloadUrl(j.pdf||j.docx||''); }}>Export Why</button>
        <button className="btn" onClick={async()=>{ const r = await fetch(`${API_URL}/graphs/demo/export/audit?frm=v1&to=v2`,{method:'POST'}); const j = await r.json(); setDownloadUrl(j.url||''); }}>Audit Export</button>
        <span className="small" style={{marginLeft:8}}>Renderer:</span>
        <button className="btn" onClick={()=>setRenderer('svg')}>SVG</button>
        <button className="btn" onClick={()=>setRenderer('webgl')}>WebGL</button>
      </div>
      
  React.useEffect(()=>{
    apiFetch(`/graphs/demo/diff?from=v1&to=v2`).then(r=>r.json()).then(d=>{
      const dd = d.diff || d; setHistory(h=>[...(h||[]), dd]); setFuture([]); setDiff(dd); (window as any).__diff = dd
    }).catch(()=>{})
  },[])

  React.useEffect(()=>{
    function onKey(e: KeyboardEvent){
      const cmd = e.metaKey || e.ctrlKey
      if(cmd && e.key.toLowerCase()==='s'){ e.preventDefault(); document.getElementById('btn-snapshot')?.click(); return }
      if(cmd && e.shiftKey && e.key.toLowerCase()==='c'){ e.preventDefault(); document.getElementById('btn-compare')?.click(); return }
      if(cmd && e.key.toLowerCase()==='e'){ e.preventDefault(); document.getElementById('btn-export-why')?.click(); return }
      if(e.key.toLowerCase()==='g'){ e.preventDefault(); const t = document.getElementById('btn-toggle-renderer'); t && (t as HTMLButtonElement).click(); return }
      if(e.key.toLowerCase()==='m'){ e.preventDefault(); const t = document.getElementById('btn-toggle-minimap'); t && (t as HTMLButtonElement).click(); return }
      if(e.key==='?' || e.key.toLowerCase()==='/' ){ e.preventDefault(); setShowHelp(v=>!v); return }
    }
    window.addEventListener('keydown', onKey)
    return ()=> window.removeEventListener('keydown', onKey)
  },[])
  {location.hash==='#/billing' ? <Billing/> : (
      {view==="graph" ? (<div className="canvas">
        <div className="board">
          <CompareOverlay/>
          <GraphCanvas onSelect={setSelected} diff={diff} density={density} renderer={renderer}/>
        </div>
        <aside className="inspector">
          <Inspector node={selected}/>
        </aside>
      </div>)}
      <Timeline/>
      <DownloadQueue/>
      <HotkeysHelp open={showHelp} onClose={()=>setShowHelp(false)}/>
      <DownloadQueue jobs={jobs}/>
    </div>
  )
}
