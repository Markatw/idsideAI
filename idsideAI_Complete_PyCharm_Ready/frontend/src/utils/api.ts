export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001'

export async function apiPost(path: string, body: any){
  const res = await fetch(`${API_URL}${path}`, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify(body || {})
  })
  if(!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function apiGet(path: string){
  const res = await fetch(`${API_URL}${path}`)
  if(!res.ok) throw new Error(await res.text())
  return res.json()
}
