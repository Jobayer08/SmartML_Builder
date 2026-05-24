import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import API from '../api/api'

export default function Dashboard(){
  const [stats, setStats] = useState({ total_models: 0, total_predictions: 0 })
  const [datasets, setDatasets] = useState([])

  useEffect(() => {
    const fetchData = async () => {
      try {
        const d = await API.get('/my-datasets')
        setDatasets(d.data || [])
      } catch (e) {
        console.log('Error fetching datasets')
      }
    }
    fetchData()
  }, [])

  return (
    <div className="p-8">
      <h1 className="text-4xl font-bold mb-8">SmartML Builder</h1>

      <div className="grid grid-cols-3 gap-5 mb-8">
        <div className="shadow p-6 rounded bg-white border-l-4 border-blue-500">
          <h2 className="text-lg font-bold text-gray-600">Models</h2>
          <p className="text-4xl font-bold mt-2">{stats.total_models}</p>
        </div>

        <div className="shadow p-6 rounded bg-white border-l-4 border-green-500">
          <h2 className="text-lg font-bold text-gray-600">Predictions</h2>
          <p className="text-4xl font-bold mt-2">{stats.total_predictions}</p>
        </div>

        <div className="shadow p-6 rounded bg-white border-l-4 border-purple-500">
          <h2 className="text-lg font-bold text-gray-600">Datasets</h2>
          <p className="text-4xl font-bold mt-2">{datasets.length}</p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <Link to="/datasets" className="shadow p-4 rounded bg-gradient-to-br from-blue-400 to-blue-600 text-white text-center font-bold hover:shadow-lg">
          📊 Datasets
        </Link>
        <Link to="/train" className="shadow p-4 rounded bg-gradient-to-br from-green-400 to-green-600 text-white text-center font-bold hover:shadow-lg">
          🚀 Train Model
        </Link>
        <Link to="/predict" className="shadow p-4 rounded bg-gradient-to-br from-purple-400 to-purple-600 text-white text-center font-bold hover:shadow-lg">
          🔮 Predict
        </Link>
      </div>
    </div>
  )
}
