import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import API from '../api/api'

export default function Register(){
  const [form, setForm] = useState({ username: '', email: '', password: '' })
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async () => {
    try {
      await API.post('/register', form)
      navigate('/login')
    } catch (e) {
      setError('Registration failed')
    }
  }

  return (
    <div className="h-screen flex justify-center items-center bg-gradient-to-br from-blue-500 to-blue-600">
      <div className="w-96 shadow-2xl p-8 rounded bg-white">
        <h1 className="text-3xl font-bold mb-5 text-center">Register</h1>
        {error && <p className="text-red-500 mb-3">{error}</p>}
        <input 
          className="border p-3 w-full mb-3 rounded" 
          placeholder="Username" 
          onChange={e => setForm({ ...form, username: e.target.value })} 
        />
        <input 
          className="border p-3 w-full mb-3 rounded" 
          placeholder="Email" 
          onChange={e => setForm({ ...form, email: e.target.value })} 
        />
        <input 
          type="password" 
          className="border p-3 w-full mb-3 rounded" 
          placeholder="Password" 
          onChange={e => setForm({ ...form, password: e.target.value })} 
        />
        <button 
          onClick={handleSubmit} 
          className="bg-blue-500 text-white w-full p-3 rounded font-bold hover:bg-blue-600"
        >
          Register
        </button>
        <p className="mt-4 text-center">Already have account? <Link to="/login" className="text-blue-500">Login</Link></p>
      </div>
    </div>
  )
}
