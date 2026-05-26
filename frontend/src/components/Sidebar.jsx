import { Link } from 'react-router-dom'

export default function Sidebar(){
  return(
    <div className="w-64 h-screen bg-gray-900 text-white fixed">
      <div className="p-5 text-2xl font-bold border-b border-gray-700">
        SmartML
      </div>
      <div className="flex flex-col p-4 gap-3">
        <Link to="/dashboard" className="hover:text-gray-300">Dashboard</Link>
        <Link to="/datasets" className="hover:text-gray-300">Datasets</Link>
        <Link to="/models" className="hover:text-gray-300">Models</Link>
        <Link to="/train" className="hover:text-gray-300">Train</Link>
        <Link to="/predict" className="hover:text-gray-300">Predict</Link>
        <Link to="/logs" className="hover:text-gray-300">Logs</Link>
      </div>
    </div>
  )
}
