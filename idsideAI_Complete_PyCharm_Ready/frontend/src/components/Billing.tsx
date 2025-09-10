import React, { useEffect, useState } from 'react'
import { apiGet, apiPost } from '../utils/api'

export default function Billing(){
  const [plans, setPlans] = useState<any[]>([])
  const [pk, setPk] = useState<string>('')
  useEffect(()=>{
    apiGet('/billing/plans').then(d=>{ setPlans(d.plans||[]); setPk(d.publishable_key||'') })
  },[])

  return (
    <div style={{padding:16}}>
      <h2>Billing</h2>
      <p>Pick a plan. You’ll be redirected to Stripe Checkout.</p>
      <div style={{display:'flex', gap:12, flexWrap:'wrap'}}>
        {plans.map(p=>(
          <div key={p.id} className="card" style={{minWidth:220}}>
            <b>{p.name}</b>
            <div className="small">{p.id}</div>
            <button className="btn primary" style={{marginTop:8}} onClick={async()=>{
              const {url} = await apiPost('/billing/checkout', {
                price_id: p.price_id,
                success_url: window.location.origin + '?checkout=success',
                cancel_url: window.location.origin + '?checkout=cancel'
              })
              window.location.href = url
            }}>Choose {p.name}</button>
          </div>
        ))}
      </div>
      <hr style={{margin:'16px 0'}}/>
      <b>Manage existing subscription</b>
      <div className="small">You’ll need your Stripe customer ID</div>
      <div style={{marginTop:6}}>
        <input id="cust" placeholder="cus_..." style={{padding:8, border:'1px solid var(--border)', borderRadius:6}}/> 
        <button className="btn" style={{marginLeft:8}} onClick={async()=>{
          const customer_id = (document.getElementById('cust') as HTMLInputElement).value
          const {url} = await apiPost('/billing/portal', {customer_id, return_url: window.location.origin})
          window.location.href = url
        }}>Open Billing Portal</button>
      </div>
    </div>
  )
}
