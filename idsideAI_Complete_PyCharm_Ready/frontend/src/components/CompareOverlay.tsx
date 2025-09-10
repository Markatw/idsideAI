import React, { useEffect, useState } from 'react'
import { API_URL } from '../config'
import type { GraphNode, GraphEdge } from './GraphCanvas'

interface Diff {
  nodes_added: GraphNode[]
  nodes_removed: string[]
  edges_added: GraphEdge[]
  edges_removed: string[]
  props_changed: { id: string, field?: string, from_value?: string, to_value?: string }[]
}

export default function CompareOverlay(){
  const [diff, setDiff] = useState<Diff|null>(null)

  useEffect(()=>{
    fetch(`${API_URL}/graphs/demo/diff?from=v1&to=v2`).then(r=>r.json()).then(d=>{
      setDiff(d.diff || d)
    })
  },[])

  if(!diff) return null
  return (
    <div className="card" style={{position:'absolute', right:16, top:16, width:300, zIndex:10}}>
      <b>Compare v1 ↔ v2</b>
      <ul>
        {diff.nodes_added.map(n=> <li key={'n+'+n.id} style={{color:'#18A957'}}>+ Node {n.id} {n.title}</li>)}
        {diff.edges_added.map(e=> <li key={'e+'+e.id} style={{color:'#18A957'}}>+ Edge {e.type} {e.source}→{e.target}</li>)}
        {diff.props_changed.map(c=> <li key={'c'+c.id} style={{color:'#0099FF'}}>~ {c.id} {c.field}: {c.from_value} → {c.to_value}</li>)}
        {diff.nodes_removed.map(id=> <li key={'n-'+id} style={{color:'#D7263D'}}>− Node {id}</li>)}
        {diff.edges_removed.map(id=> <li key={'e-'+id} style={{color:'#D7263D'}}>− Edge {id}</li>)}
      </ul>
    </div>
  )
}
