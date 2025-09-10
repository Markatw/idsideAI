
import React, { useEffect, useState } from 'react'
import { API_URL } from '../config'

export default function Billing(){
  const [plans, setPlans] = useState<any[]>([])
  const success = window.location.origin
  const cancel = window.location.origin

  useEffect(()=>{
    fetch(`${API_URL}/billing/plans`).then(r=>r.json()).then(d=> setPlans(d.plans||[]))
  },[])

  async function checkout(plan:string){
    const res = await fetch(`${API_URL}/billing/checkout`, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({plan, success_url: success, cancel_url: cancel, customer_email: ''})
    })
    const data = await res.json()
    if(data.url) window.location.href = data.url
  }

  return (
    <div style={{padding:24}}>
      <h1>Billing</h1>
      <p>Select a plan to continue.</p>
      <div style={{display:'flex', gap:16}}>
        {plans.map(p=>(
          <div key={p.id} className="card" style={{width:220}}>
            <b style={{display:'block'}}>{p.id.toUpperCase()}</b>
            <div className="small" style={{margin:'6px 0 12px'}}>{p.price}</div>
            <button className="btn primary" onClick={()=>checkout(p.id)}>Choose {p.id}</button>
          </div>
        ))}
      </div>
    </div>
  )
}
