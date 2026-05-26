import { Navigate } from 'react-router-dom'

export default function ProtectedRoute({ children }) {
  const token = localStorage.getItem('token')
  
  if (!token) {
    // Optional: Show a nice toast/message before redirect (if you want)
    return <Navigate to="/login" />
  }
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-blue-100/30 to-white">
      {children}
    </div>
  )
}