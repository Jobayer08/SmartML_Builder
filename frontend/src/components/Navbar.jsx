import { Link, useNavigate } from 'react-router-dom'

export default function Navbar(){
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  return(
    <nav className="bg-gradient-to-r from-blue-600 to-blue-500 shadow-lg fixed w-full z-20 backdrop-blur-sm">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo/Brand */}
        <Link 
          to="/dashboard" 
          className="text-2xl font-extrabold bg-gradient-to-r from-white to-blue-100 bg-clip-text text-transparent hover:from-blue-100 hover:to-white transition-all duration-300"
        >
          🧠 SmartML
        </Link>
        
        {/* Navigation Links */}
        <div className="flex items-center gap-6 text-white font-medium">
          <Link 
            to="/dashboard" 
            className="relative px-2 py-1 hover:text-white transition-colors duration-200 group"
          >
            Dashboard
            <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-white rounded-full transition-all duration-300 group-hover:w-full"></span>
          </Link>
          
          <Link 
            to="/datasets" 
            className="relative px-2 py-1 hover:text-white transition-colors duration-200 group"
          >
            Datasets
            <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-white rounded-full transition-all duration-300 group-hover:w-full"></span>
          </Link>
          
          <button 
            onClick={handleLogout} 
            className="ml-2 px-4 py-1.5 bg-white/20 backdrop-blur-sm rounded-lg text-white text-sm font-semibold hover:bg-white/30 hover:scale-105 transition-all duration-200 shadow-md"
          >
            🚪 Logout
          </button>
        </div>
      </div>
    </nav>
  )
}