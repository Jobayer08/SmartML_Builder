import React from 'react'
import { Link } from 'react-router-dom'

export default function Navbar(){
  const token = localStorage.getItem('token')
  const handleLogout = () => {
    localStorage.removeItem('token')
    window.location.href = '/login'
  }

  return (
    <nav className="bg-white shadow">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <Link to="/" className="font-bold text-xl">SmartML</Link>
        <div className="space-x-3">
          {token ? (
            <>
              <Link to="/dashboard" className="text-sm">Dashboard</Link>
              <button onClick={handleLogout} className="text-sm text-red-500">Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-sm">Login</Link>
              <Link to="/register" className="text-sm">Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}
