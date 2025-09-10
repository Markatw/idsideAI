import React from 'react'

export default function HotkeysHelp({open,onClose}:{open:boolean;onClose:()=>void}){
  if(!open) return null
  return (
    <div style={{position:'fixed', inset:0, background:'rgba(0,0,0,.35)', zIndex:9998}} onClick={onClose}>
      <div className="card" style={{position:'absolute', top:'10%', left:'50%', transform:'translateX(-50%)', width:520, background:'#fff'}} onClick={e=>e.stopPropagation()}>
        <b>Keyboard Shortcuts</b>
        <ul>
          <li><b>⌘/Ctrl + S</b> — Snapshot</li>
          <li><b>⌘/Ctrl + ⇧ + C</b> — Compare latest two</li>
          <li><b>⌘/Ctrl + E</b> — Export Why</li>
          <li><b>G</b> — Toggle Renderer (SVG/WebGL)</li>
          <li><b>M</b> — Toggle Minimap</li>
          <li><b>❓</b> — Toggle this help</li>
          <li><b>↑ ↓ ← →</b> — Move selection</li>
          <li><b>Enter</b> — Select focused node</li>
        </ul>
        <button className="btn" onClick={onClose}>Close</button>
      </div>
    </div>
  )
}
