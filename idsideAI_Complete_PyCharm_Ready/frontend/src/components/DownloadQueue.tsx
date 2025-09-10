import React from 'react'

type Job = { id:string, type:'why'|'audit', status:'pending'|'done'|'error', url?:string, label?:string }

const store:any = (window as any).__downloads = (window as any).__downloads || { jobs: [] as Job[], listeners: [] as any[] }

export function enqueue(job: Job){
  store.jobs = [job, ...store.jobs]
  store.listeners.forEach((fn:any)=>fn(store.jobs))
}
export function update(id:string, patch: Partial<Job>){
  store.jobs = store.jobs.map((j:Job)=> j.id===id? {...j, ...patch} : j)
  store.listeners.forEach((fn:any)=>fn(store.jobs))
}

export default function DownloadQueue(){
  const [jobs, setJobs] = React.useState<Job[]>(store.jobs)
  React.useEffect(()=>{
    const fn = (j:any)=>setJobs([...j]); store.listeners.push(fn); return ()=>{
      store.listeners = store.listeners.filter((x:any)=>x!==fn)
    }
  },[])
  if(!jobs.length) return null
  return (
    <div style={{position:'fixed', right:16, bottom:16, width:320, zIndex:9999}}>
      {jobs.map(j=>(
        <div key={j.id} className="card" style={{marginTop:12}}>
          <b>{j.type==='why'?'Why Export':'Audit Export'} — {j.status.toUpperCase()}</b>
          {j.label && <div className="small" style={{marginTop:4}}>{j.label}</div>}
          {j.url && <div style={{marginTop:6}}><a href={j.url} target="_blank">Download</a></div>}
        </div>
      ))}
    </div>
  )
}
