import { createContext, useState, useEffect } from 'react'

export const AuthContext = createContext()

export default function AuthProvider({ children }){
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  // Optional: Check for existing token on app load
  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      setUser({ token })
    }
    setLoading(false)
  }, [])

  const login = (token) => {
    localStorage.setItem('token', token)
    setUser({ token })
  }

  const logout = () => {
    localStorage.removeItem('token')
    setUser(null)
  }

  // Show loading spinner while checking auth (matching your theme)
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-blue-100/30 to-white flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-blue-600 font-medium text-lg">Loading SmartML...</p>
          <p className="text-blue-400 text-sm mt-2">Preparing your workspace</p>
        </div>
      </div>
    )
  }

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-blue-100/30 to-white">
        {children}
      </div>
    </AuthContext.Provider>
  )
}