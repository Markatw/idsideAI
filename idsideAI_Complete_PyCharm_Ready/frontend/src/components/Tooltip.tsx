import React from 'react'

export default function Tooltip({x,y,children}:{x:number;y:number;children:any}){
  const style: React.CSSProperties = {position:'absolute', left:x, top:y, background:'#111', color:'#fff', padding:8, borderRadius:8, fontSize:12, maxWidth:260, pointerEvents:'none', zIndex:50, boxShadow:'0 6px 20px rgba(0,0,0,.2)'}
  return <div style={style}>{children}</div>
}
