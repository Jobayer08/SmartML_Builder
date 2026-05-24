import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import API from '../api/api'

export default function Login(){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleLogin = async () => {
    try {
      const res = await API.post('/login', { email, password })
      const token = res.data.access_token || res.data.token
      localStorage.setItem('token', token)
      navigate('/dashboard')
    } catch (e) {
      setError('Login failed')
    }
  }

  return (
    <div className="h-screen flex justify-center items-center bg-gradient-to-br from-blue-500 to-blue-600">
      <div className="w-96 shadow-2xl p-8 rounded bg-white">
        <h1 className="text-3xl font-bold mb-5 text-center">Login</h1>
        {error && <p className="text-red-500 mb-3">{error}</p>}
        <input 
          className="border p-3 w-full mb-3 rounded" 
          placeholder="Email" 
          value={email} 
          onChange={e => setEmail(e.target.value)} 
        />
        <input 
          type="password" 
          className="border p-3 w-full mb-3 rounded" 
          placeholder="Password" 
          value={password} 
          onChange={e => setPassword(e.target.value)} 
        />
        <button 
          onClick={handleLogin} 
          className="bg-green-500 text-white w-full p-3 rounded font-bold hover:bg-green-600"
        >
          Login
        </button>
        <p className="mt-4 text-center">Don't have account? <Link to="/register" className="text-blue-500">Register</Link></p>
      </div>
    </div>
  )
}
