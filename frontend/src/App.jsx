import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import TrainModel from './pages/TrainModel'
import PredictCSV from './pages/PredictCSV'
import PredictImage from './pages/PredictImage'
import PredictNC4 from './pages/PredictNC4'
import Navbar from './components/Navbar'

export default function App(){
  const token = localStorage.getItem('token')

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <Routes>
        <Route path="/login" element={<Login/>} />
        <Route path="/register" element={<Register/>} />
        <Route path="/dashboard" element={token ? <Dashboard/> : <Navigate to="/login" />} />
        <Route path="/train" element={token ? <TrainModel/> : <Navigate to="/login" />} />
        <Route path="/predict/csv" element={token ? <PredictCSV/> : <Navigate to="/login" />} />
        <Route path="/predict/image" element={token ? <PredictImage/> : <Navigate to="/login" />} />
        <Route path="/predict/nc4" element={token ? <PredictNC4/> : <Navigate to="/login" />} />
        <Route path="/" element={<Navigate to={token ? '/dashboard' : '/login'} />} />
      </Routes>
    </div>
  )
}
