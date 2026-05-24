import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Datasets from './pages/Datasets'
import Models from './pages/Models'
import Train from './pages/Train'
import Predict from './pages/Predict'
import History from './pages/History'
import ProtectedRoute from './components/ProtectedRoute'
import Navbar from './components/Navbar'
import Sidebar from './components/Sidebar'

export default function App(){
  const token = localStorage.getItem('token')

  return (
    <div className="min-h-screen bg-gray-50">
      {token && <Navbar />}
      <div className="flex">
        {token && <Sidebar />}
        <div className="flex-1">
          <Routes>
            <Route path="/login" element={<Login/>} />
            <Route path="/register" element={<Register/>} />
            <Route path="/dashboard" element={<ProtectedRoute><Dashboard/></ProtectedRoute>} />
            <Route path="/datasets" element={<ProtectedRoute><Datasets/></ProtectedRoute>} />
            <Route path="/models" element={<ProtectedRoute><Models/></ProtectedRoute>} />
            <Route path="/train" element={<ProtectedRoute><Train/></ProtectedRoute>} />
            <Route path="/predict" element={<ProtectedRoute><Predict/></ProtectedRoute>} />
            <Route path="/history" element={<ProtectedRoute><History/></ProtectedRoute>} />
            <Route path="/" element={<Navigate to={token ? '/dashboard' : '/login'} />} />
          </Routes>
        </div>
      </div>
    </div>
  )
}
