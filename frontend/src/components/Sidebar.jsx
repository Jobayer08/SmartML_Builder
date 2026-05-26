import { Link, useLocation } from 'react-router-dom'

export default function Sidebar() {
  const location = useLocation()
  
  const menuItems = [
    { path: '/dashboard', name: 'Dashboard', icon: '📊' },
    { path: '/datasets', name: 'Datasets', icon: '📁' },
    { path: '/models', name: 'Models', icon: '🧠' },
    { path: '/train', name: 'Train', icon: '⚡' },
    { path: '/predict', name: 'Predict', icon: '🔮' },
    { path: '/logs', name: 'Logs', icon: '📝' },
  ]
  
  return(
    <div className="w-64 h-screen bg-gradient-to-b from-blue-50 via-white to-blue-50 shadow-xl fixed border-r border-blue-200">
      {/* Logo Area */}
      <div className="p-6 text-2xl font-extrabold border-b border-blue-200">
        <span className="bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
          🧠 SmartML
        </span>
      </div>
      
      {/* Navigation Menu */}
      <div className="flex flex-col p-4 gap-2">
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`
                flex items-center gap-3 px-4 py-2.5 rounded-lg transition-all duration-200
                ${isActive 
                  ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-md' 
                  : 'text-blue-700 hover:bg-blue-100 hover:text-blue-800'
                }
              `}
            >
              <span className="text-lg">{item.icon}</span>
              <span className="font-medium">{item.name}</span>
              {isActive && (
                <span className="ml-auto w-1.5 h-1.5 bg-white rounded-full animate-pulse"></span>
              )}
            </Link>
          )
        })}
      </div>
      
      {/* Optional: User Info / Footer */}
      <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-blue-200">
        <div className="text-xs text-blue-500 text-center">
          SmartML v1.0
        </div>
      </div>
    </div>
  )
}