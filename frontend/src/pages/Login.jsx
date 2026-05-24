import { useState } from 'react'
import API from '../api/api'

export default function Login(){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleLogin = async () => {
    try{
      const res = await API.post('/login', {email, password})
      const token = res.data.access_token || res.data.token || res.data
      localStorage.setItem('token', token)
      window.location.href = '/dashboard'
    }catch(e){
      alert('Login failed')
    }
  }

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded shadow">
      <h1 className="text-2xl font-bold mb-4">Login</h1>
      <input className="border p-2 mb-3 w-full" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
      <input type="password" className="border p-2 mb-3 w-full" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
      <button onClick={handleLogin} className="bg-blue-500 text-white px-4 py-2 rounded">Login</button>
    </div>
  )
}
