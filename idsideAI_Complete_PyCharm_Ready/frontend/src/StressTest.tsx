
import React from 'react'
import WebGLGraphCanvas from './components/WebGLGraphCanvas'

function genNodesEdges(n=10000){
  const nodes = []
  const edges = []
  for(let i=0;i<n;i++){
    const type = i%17===0?'Evidence': i%11===0?'Risk': i%7===0?'Option':'Outcome'
    nodes.push({id:`N${i}`, type, title:`Node ${i}`, x: (i*13)%4000, y: (i*29)%2000})
    if(i>0){
      edges.push({id:`E${i}`, type: 'considers', source:`N${Math.floor(Math.random()*i)}`, target:`N${i}`})
    }
  }
  nodes[0].type = 'Decision'; nodes[0].title = 'Stress Root'
  return {nodes, edges}
}

export default function StressTest(){
  const {nodes, edges} = React.useMemo(()=>genNodesEdges(10000), [])
  return (
    <div style={{height:'100vh'}}>
      <WebGLGraphCanvas initialNodes={nodes} initialEdges={edges}/>
    </div>
  )
}
