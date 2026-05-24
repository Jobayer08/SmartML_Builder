import { useState } from 'react'
import API from '../api/api'

export default function Register(){
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleRegister = async () => {
    try{
      await API.post('/register', {username, email, password})
      window.location.href = '/login'
    }catch(e){
      alert('Register failed')
    }
  }

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded shadow">
      <h1 className="text-2xl font-bold mb-4">Register</h1>
      <input className="border p-2 mb-3 w-full" placeholder="Username" value={username} onChange={e=>setUsername(e.target.value)} />
      <input className="border p-2 mb-3 w-full" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
      <input type="password" className="border p-2 mb-3 w-full" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
      <button onClick={handleRegister} className="bg-green-500 text-white px-4 py-2 rounded">Register</button>
    </div>
  )
}
