import React, { useEffect, useRef, useState } from 'react'
import * as PIXI from 'pixi.js'
import { API_URL } from '../config'
import type { GraphNode, GraphEdge } from './GraphCanvas'

type Data = { nodes: GraphNode[], edges: GraphEdge[] }

function gridKey(x:number, y:number, size:number){ return `${Math.floor(x/size)}:${Math.floor(y/size)}` }

export default function WebGLGraphCanvas(){
  const ref = useRef<HTMLDivElement>(null)
  const appRef = useRef<PIXI.Application|null>(null)
  const [data, setData] = useState<Data>({nodes:[], edges:[]})
  const [scale, setScale] = useState(1)
  const [offset, setOffset] = useState({x:0,y:0})

  useEffect(()=>{
    fetch(`${API_URL}/graphs/demo/subgraph`).then(r=>r.json()).then(setData)
  },[])

  useEffect(()=>{
    if(!ref.current) return
    const app = new PIXI.Application({ background: 0xFFFFFF, resizeTo: ref.current })
    ref.current.appendChild(app.view as any)
    appRef.current = app

    const container = new PIXI.Container()
    app.stage.addChild(container)

    // simple pan
    let dragging=false; let last={x:0,y:0}
    app.view.addEventListener('mousedown', (e:any)=>{ dragging=true; last={x:e.clientX,y:e.clientY} })
    window.addEventListener('mouseup', ()=> dragging=false)
    window.addEventListener('mousemove', (e:any)=>{
      if(!dragging) return
      const dx=e.clientX-last.x, dy=e.clientY-last.y
      container.x += dx; container.y += dy
      last={x:e.clientX,y:e.clientY}
    })
    // wheel zoom
    app.view.addEventListener('wheel', (e:any)=>{
      e.preventDefault()
      const s = e.deltaY<0 ? 1.1 : 0.9
      container.scale.x *= s; container.scale.y *= s
    }, {passive:false})

    return ()=>{ app.destroy(true, { children:true, texture:true, baseTexture:true }); appRef.current=null }
  },[])

  useEffect(()=>{
    const app = appRef.current; if(!app) return
    const container = app.stage.children[0] as PIXI.Container
    container.removeChildren()

    // Determine clustering grid based on zoom
    const zoom = container.scale.x || 1
    const grid = zoom < 0.8 ? 120 : zoom < 1.2 ? 80 : 0 // 0 means render individuals

    // Edges (skip when clustered)
    if(grid===0){
      data.edges.forEach(e=>{
        const a = data.nodes.find(n=>n.id===e.source); const b = data.nodes.find(n=>n.id===e.target)
        if(!a || !b) return
        const g = new PIXI.Graphics()
        const color = e.type==='supported_by' ? 0x18A957 : e.type==='incurs' ? 0xF5A300 : 0x0052CC
        g.lineStyle((e as any).chosen? 3 : 1.6, color).moveTo(a.x||0,a.y||0).lineTo(b.x||0,b.y||0)
        container.addChild(g)
      })
    }

    if(grid>0){
      // cluster nodes into grid cells
      const buckets: Record<string, GraphNode[]> = {}
      data.nodes.forEach(n=>{
        const k = gridKey((n.x||0),(n.y||0),grid)
        if(!buckets[k]) buckets[k]=[]; buckets[k].push(n)
      })
      Object.entries(buckets).forEach(([k, arr])=>{
        const g = new PIXI.Graphics()
        const cx = (arr.reduce((s,n)=>s+(n.x||0),0)/arr.length)
        const cy = (arr.reduce((s,n)=>s+(n.y||0),0)/arr.length)
        const r = Math.max(10, Math.sqrt(arr.length)*6)
        g.beginFill(0x0099FF, 0.15).lineStyle(2, 0x0099FF).drawCircle(cx, cy, r).endFill()
        container.addChild(g)
        const label = new PIXI.Text(String(arr.length), {fontSize:12, fill:0x0F172A})
        label.x = cx-4; label.y = cy-6; container.addChild(label)
      })
    }else{
      // render individual nodes with culling
      const viewW = app.view.width, viewH = app.view.height
      const bounds = container.getBounds()
      data.nodes.forEach(n=>{
        const x = n.x||0, y=n.y||0
        // cull if far outside (simple heuristic)
        if(x < -5000 || x > viewW+5000 || y < -5000 || y > viewH+5000) return
        const g = new PIXI.Graphics()
        if(n.type==='Decision'){
          g.lineStyle(3, 0x0052CC).beginFill(0xFFFFFF).drawRoundedRect(x, y, 220, 56, 10).endFill()
        }else if(n.type==='Option'){
          g.lineStyle(2, 0x0099FF).beginFill(0xFFFFFF).drawRoundedRect(x, y, 220, 48, 10).endFill()
          g.beginFill(0x0099FF).drawRect(x, y, 10, 48).endFill()
        }else if(n.type==='Evidence'){
          g.lineStyle(6, 0x18A957).drawCircle(x, y, 26)
        }else if(n.type==='Risk'){
          g.lineStyle(3, 0xF5A300).beginFill(0xFFFFFF).drawRoundedRect(x, y, 220, 44, 16).endFill()
        }
        container.addChild(g)
      })
    }
  }, [data])

  return <div style={{width:'100%', height:'100%'}} ref={ref}/>
}

// Semantic labeling for clusters (very simple keyword-based)
function dominantLabel(titles:string[]){
  const s = titles.join(' ').toLowerCase()
  if(/risk|lock|incident|issue/.test(s)) return 'Risk'
  if(/cost|price|budget|tco/.test(s)) return 'Cost'
  if(/perf|latency|throughput|scale|kpi/.test(s)) return 'Performance'
  if(/security|iso|soc2|gdpr|compliance/.test(s)) return 'Compliance'
  return 'Mixed'
}
