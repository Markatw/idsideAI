
import { API_URL } from '../config'
import { apiFetch } from '../utils/api'
import React, { useEffect, useState } from 'react'
import Tooltip from './Tooltip'


export type NodeType = 'Decision'|'Option'|'Evidence'|'Risk'|'Constraint'|'Outcome'
export type EdgeType = 'considers'|'supported_by'|'contradicted_by'|'chosen'|'constrained_by'|'incurs'

export interface GraphNode{
  id: string
  type: NodeType
  title: string
  x: number
  y: number
  w?: number
  h?: number
  confidence?: number // Evidence
  severity?: 'Low'|'Medium'|'High' // Risk
  ghost?: boolean // AI-suggested
}

export interface GraphEdge{
  id: string
  type: EdgeType
  source: string
  target: string
  chosen?: boolean
}

const brand = '#0052CC', accent='#0099FF', success='#18A957', warning='#F5A300', border='#E6EAF0', ink='#0F172A'

const STATIC_NODES: GraphNode[] = [
  { id:'DEC-1', type:'Decision', title:'Decision: Select Supplier', x:140, y:180, w:240, h:56 },
  { id:'OPT-A', type:'Option', title:'Option A — Vendor Alpha', x:520, y:150, w:240, h:48 },
  { id:'OPT-B', type:'Option', title:'Option B — Vendor Beta',  x:520, y:260, w:240, h:48 },
  { id:'EV-42', type:'Evidence', title:'ISO 27001', x:300, y:380, confidence:.75 },
  { id:'RSK-1', type:'Risk', title:'Risk: Vendor Lock‑in', x:840, y:210, w:260, h:44 }
]

const STATIC_EDGES: GraphEdge[] = [
  { id:'E1', type:'considers', source:'DEC-1', target:'OPT-A' },
  { id:'E2', type:'considers', source:'DEC-1', target:'OPT-B' },
  { id:'E3', type:'supported_by', source:'EV-42', target:'OPT-A' },
  { id:'E4', type:'incurs', source:'OPT-B', target:'RSK-1' }
]

function ArrowMarkerDefs(){
  return (
    <defs>
      <marker id="arrowBlue" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
        <polygon points="0 0, 10 5, 0 10" fill={brand} />
      </marker>
      <marker id="arrowGreen" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
        <polygon points="0 0, 10 5, 0 10" fill={success} />
      </marker>
      <marker id="arrowAmber" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
        <polygon points="0 0, 10 5, 0 10" fill={warning} />
      </marker>
    </defs>
  )
}

function edgeColor(t: EdgeType){
  if(t==='supported_by') return success
  if(t==='incurs') return warning
  return brand
}

function EvidenceRing({cx,cy,r,pct}:{cx:number;cy:number;r:number;pct:number}){
  const circumference = 2*Math.PI*r
  const dash = `${circumference*pct} ${circumference*(1-pct)}`
  return (
    <g>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#E6EAF0" strokeWidth={6}/>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={success} strokeWidth={6}
        strokeDasharray={dash} strokeLinecap="round" transform={`rotate(-90 ${cx} ${cy})`} className="pulse"/>
    </g>
  )
}

function DecisionNode({n}:{n:GraphNode}){
  // use rounded rect as visual; label carries "Decision"
  return (
    <g className="glow">
      <rect x={n.x} y={n.y} width={n.w||220} height={n.h||56} rx={10} fill="#fff" stroke={brand} strokeWidth={3}/>
      <text x={(n.x+(n.w||220)/2)} y={n.y+32} textAnchor="middle" fontSize="14" fill={ink}>{n.title}</text>
    </g>
  )
}

function OptionNode({n}:{n:GraphNode}){
  const isChosen = (window as any)?.chosenTargets?.has?.(n.id) || false
  return (
    <g>
      <rect x={n.x} y={n.y} width={n.w||220} height={n.h||48} rx={10} fill="#fff" stroke={accent} strokeWidth={2}/>
      <rect x={n.x} y={n.y} width={10} height={n.h||48} fill={accent}/>
      <text x={n.x+16} y={n.y+30} fontSize="14" fill={ink}>{n.title}</text>
      {chosenTargets.has(n.id) && (
        <g transform={`translate(${(n.x+(n.w||220)-24)},${(n.y-8)})`}>
          <polygon points="0,12 6,0 12,12" fill="#F5A300"/>
          <rect x="-10" y="12" width="32" height="4" fill="#F5A300"/>
        </g>
      )}
    </g>
  )
}

function EvidenceNode({n}:{n:GraphNode}){
  const cx = n.x, cy = n.y, r = 26, pct = n.confidence ?? .6
  return (
    <g>
      <EvidenceRing cx={cx} cy={cy} r={r} pct={pct}/>
      <rect x={cx-32} y={cy+30} width={64} height={24} rx={6} fill="#fff" stroke="#E6EAF0"/>
      <text x={cx-26} y={cy+46} fontSize="12" fill={ink}>{n.title}</text>
    </g>
  )
}

function RiskNode({n}:{n:GraphNode}){
  return (
    <g>
      <rect x={n.x} y={n.y} width={n.w||220} height={n.h||44} rx={16} fill="#fff" stroke={warning} strokeWidth={3}/>
      <text x={n.x+12} y={n.y+28} fontSize="14" fill={ink}>{n.title}</text>
    </g>
  )
}

function NodeView({n}:{n:GraphNode}){
  if(n.type==='Decision') return <DecisionNode n={n}/>
  if(n.type==='Option') return <OptionNode n={n}/>
  if(n.type==='Evidence') return <EvidenceNode n={n}/>
  if(n.type==='Risk') return <RiskNode n={n}/>
  return null
}

export default function GraphCanvas({onSelect, diff, density, renderer}:{onSelect:(n:GraphNode)=>void, diff?: any, density?: 'cozy'|'compact'|'dense', renderer?: 'svg'|'canvas'|'webgl'}){
  const [nodes, setNodes] = useState<GraphNode[]>(STATIC_NODES)
  const [focus, setFocus] = useState<string|null>(null)
  const [hover, setHover] = useState<{x:number,y:number, node:any}|null>(null)
  const [edges, setEdges] = useState<GraphEdge[]>(STATIC_EDGES)
  const chosenTargets = React.useMemo(()=> new Set(edges.filter(e=>(e as any).chosen || e.type==='CHOSEN').map(e=>e.target)), [edges])

  useEffect(()=>{
    apiFetch(`/graphs/demo/subgraph`).then(r=>r.json()).then(data=>{
      setNodes(data.nodes)
      setEdges(data.edges)
    }).catch(()=>{
      // fallback to static
    })
  },[])

  const nodes = NODES
  const edges = EDGES
  function center(n:GraphNode){
    const w = n.w || (n.type==='Evidence'?0:220)
    const h = n.h || (n.type==='Evidence'?0:48)
    return { x: n.type==='Evidence'? n.x : n.x + w/2, y: n.type==='Evidence'? n.y : n.y + h/2 }
  }
  function hitRect(n:GraphNode){
    const w = n.w || (n.type==='Evidence'?60:220)
    const h = n.h || (n.type==='Evidence'?60:48)
    return { x: n.type==='Evidence'? n.x-30 : n.x, y: n.type==='Evidence'? n.y-30 : n.y, w, h }
  }
  return (
    <div style={{position:'relative', width:'100%', height:'100%'}}>
    <svg viewBox="0 0 1200 720" role="img" role="graphics-document" aria-label="Decision graph canvas">
      <ArrowMarkerDefs/>
      {/* edges */}
      {edges.map(e=>{
        const a = nodes.find(n=>n.id===e.source)!
        const b = nodes.find(n=>n.id===e.target)!
        const ca = center(a), cb = center(b)
        const color = edgeColor(e.type)
        const marker = e.type==='supported_by' ? 'url(#arrowGreen)' : e.type==='incurs' ? 'url(#arrowAmber)' : 'url(#arrowBlue)'
        const strokeDasharray = e.type==='contradicted_by' ? '6 4' : 'none'
        const added = diff?.edges_added?.some((x:any)=>x.id===e.id)
        const removed = diff?.edges_removed?.includes?.(e.id)
        const strokeWidth = e.chosen || added ? 3.2 : 1.6
        return (
          <line key={e.id} x1={ca.x} y1={ca.y} x2={cb.x} y2={cb.y}
                stroke={color} strokeWidth={strokeWidth} markerEnd={marker}
                strokeDasharray={strokeDasharray}/>
        )
      })}
      {/* nodes */}
      {nodes.map(n=>{
        const r = hitRect(n)
        return (
          <g key={n.id} onClick={()=>onSelect(n)} onMouseEnter={(e)=>{ if(n.type==='Evidence'){ setHover({x:(e as any).clientX, y:(e as any).clientY, node:n}); } }} onMouseLeave={()=>setHover(null)} onMouseMove={(e)=>{ if(hover) setHover({x:(e as any).clientX+12, y:(e as any).clientY+12, node:n}); }} className={[n.ghost?'ghost':'', (diff?.nodes_added||[]).some((x:any)=>x.id===n.id)?'added':'', (diff?.nodes_removed||[]).includes?.(n.id)?'removed':'', (diff?.props_changed||[]).some((c:any)=>c.id===n.id)?'changed':''].join(' ')} cursor="pointer" >
            <NodeView n={n}/>{focus===n.id && <rect x={(n.type==='Evidence'? n.x-34 : n.x-4)} y={(n.type==='Evidence'? n.y-34 : n.y-4)} width={(n.type==='Evidence'? 68 : (n.w||220)+8)} height={(n.type==='Evidence'? 68 : (n.h||48)+8)} rx={12} fill="none" stroke="#0099FF" strokeWidth={2} />}
            <rect x={r.x} y={r.y} width={r.w} height={r.h} fill="transparent" stroke="transparent"/>
          </g>
        )
      })}
    
    </svg>
    {hover && hover.node?.type==='Evidence' && (
      <Tooltip x={hover.x} y={hover.y}>
        <div><b>{hover.node.title}</b></div>
        {hover.node.source && <div>Source: {hover.node.source}</div>}
        {hover.node.date && <div>Date: {hover.node.date}</div>}
        {hover.node.url && <div>URL: <a href={hover.node.url} target="_blank" rel="noreferrer" style={{color:'#9cf'}}>{hover.node.url}</a></div>}
        {typeof hover.node.confidence==='number' && <div>Confidence: {Math.round(hover.node.confidence*100)}%</div>}
      </Tooltip>
    )}
    {/* Minimap placeholder */}
    <div style={{position:'absolute', right:12, bottom:12, width:160, height:100, border:'1px solid #E6EAF0', borderRadius:8, background:'#fff', opacity:.9}}> 
      <div style={{position:'absolute', left:20, top:30, width:30, height:18, border:'1px solid #0052CC', borderRadius:4}}></div>
      <div style={{position:'absolute', left:80, top:22, width:28, height:14, border:'1px solid #0099FF', borderRadius:4}}></div>
      <div className="small" style={{position:'absolute', bottom:6, left:8, color:'#6B7280'}}>Minimap</div>
    </div>
    </div>
  )
}
