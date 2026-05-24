import { Link } from 'react-router-dom'

export default function Sidebar(){
  return (
    <div className="w-64 bg-gradient-to-b from-blue-600 to-blue-800 text-white min-h-screen p-4">
      <h1 className="text-2xl font-bold mb-6">SmartML</h1>
      <nav className="space-y-2">
        <Link to="/dashboard" className="block px-4 py-2 rounded hover:bg-blue-700 transition">📊 Dashboard</Link>
        <Link to="/datasets" className="block px-4 py-2 rounded hover:bg-blue-700 transition">📁 Datasets</Link>
        <Link to="/train" className="block px-4 py-2 rounded hover:bg-blue-700 transition">⚙️ Train Model</Link>
        <Link to="/models" className="block px-4 py-2 rounded hover:bg-blue-700 transition">🤖 My Models</Link>
        <Link to="/predict" className="block px-4 py-2 rounded hover:bg-blue-700 transition">🎯 Predict</Link>
        <Link to="/history" className="block px-4 py-2 rounded hover:bg-blue-700 transition">📈 History</Link>
      </nav>
    </div>
  )
}
