import React from 'react'
import { API_URL } from '../config'
import type { GraphNode } from './GraphCanvas'

export default function Inspector({node}:{node: GraphNode|null}){
  const w:any = window as any; const diff = w.__diff || null;
  if(!node) return <div role="complementary" aria-label="Inspector Panel" tabIndex={0}>Select a node to inspect.</div>
  return (
    <div>
      <div className="h2">Inspector</div>
      <div className="card">
        <b>{node.title}</b>
        {node.type==='Option' && (
          <div style={{marginTop:8}}>
            <button className="btn primary" onClick={async ()=>{
              try{
                await fetch(`${API_URL}/graphs/demo/choose?decision=DEC-1&option=${'{'}node.id{'}'}`, {method:'POST'})
                alert('Chosen edge recorded. Create a new snapshot to capture the state.')
              }catch(e){ alert('Failed to mark chosen') }
            }}>Choose this Option</button>
          </div>
        )}
        <div className="small" style={{marginTop:6}}>Type: {node.type}</div>
        {node.type==='Evidence' && <div style={{marginTop:8}}>Confidence: {(node.confidence??0)*100}%</div>}
        {node.type==='Risk' && <div style={{marginTop:8}}>Severity: {node.severity??'Medium'}</div>}
        <div style={{marginTop:8}}><b>Properties</b><pre>{JSON.stringify(node, null, 2)}</pre></div>
      </div>
      {/* Deltas (if any) */}
      {diff && (diff.props_changed||[]).some((c:any)=>c.id===node.id && (c.field==='confidence' || c.field==='severity')) && (
        <div className="card" style={{marginTop:12}}>
          <b>Change since last snapshot</b>
          {(diff.props_changed||[]).filter((c:any)=>c.id===node.id && (c.field==='confidence'||c.field==='severity')).map((c:any)=>{
            const from = parseFloat(c.from_value)||0, to = parseFloat(c.to_value)||0
            const pct = Math.max(0, Math.min(1, to))
            return (
              <div key={c.field} style={{marginTop:8}}>
                <div className="small">{c.field}: {c.from_value} → {c.to_value}</div>
                <svg width="260" height="10"><rect x="0" y="2" width="260" height="6" fill="#E6EAF0"/><rect x="0" y="2" width={260*pct} height="6" fill="#18A957"/></svg>
              </div>
            )
          })}
        </div>
      )}
      <div className="card" style={{marginTop:12}}">
        <b>Why (Draft)</b>
        <p style={{marginTop:6}}>Option A selected due to stronger compliance evidence (ISO 27001, SOC2), lower integration risk, and favourable TCO over 24 months.</p>
        <button className="btn primary">Export Why</button>
      </div>
    </div>
  )
}
