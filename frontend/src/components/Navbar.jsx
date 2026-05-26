import { Link, useNavigate } from 'react-router-dom'

export default function Navbar(){
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  return(
    <nav className="bg-white shadow fixed w-full z-20">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <Link to="/dashboard" className="text-xl font-bold text-slate-900">SmartML</Link>
        <div className="flex items-center gap-4 text-slate-600">
          <Link to="/dashboard" className="hover:text-slate-900">Dashboard</Link>
          <Link to="/datasets" className="hover:text-slate-900">Datasets</Link>
          <button onClick={handleLogout} className="text-sm text-red-600 hover:text-red-800">Logout</button>
        </div>
      </div>
    </nav>
  )
}
