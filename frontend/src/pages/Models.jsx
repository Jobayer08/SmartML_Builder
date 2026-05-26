import { useEffect, useState } from 'react'
import API from '../api/api'
import ModelCard from '../components/ModelCard'

export default function Models(){
  const [models, setModels] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const token = localStorage.getItem('token')
        const res = await API.get(`/my-models?token=${token}`)
        setModels(res.data?.models || res.data || [])
      } catch (e) {
        console.error('Error fetching models:', e)
      }
      setLoading(false)
    }
    fetchModels()
  }, [])

  return (
    <div className="ml-64 p-8 pt-24 min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-extrabold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
          🧠 My Models
        </h1>
        <p className="text-blue-500 mt-2">Manage and monitor your trained machine learning models</p>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <div className="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-blue-600 font-medium">Loading your models...</p>
          </div>
        </div>
      ) : models.length === 0 ? (
        <div className="bg-gradient-to-br from-blue-50/80 to-white rounded-xl shadow-md border border-blue-200 p-12 text-center">
          <div className="text-6xl mb-4">🎯</div>
          <p className="text-blue-600 text-lg font-medium mb-2">No models trained yet</p>
          <p className="text-blue-400 mb-4">Train your first model to see it here</p>
          <a 
            href="/train" 
            className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-500 to-blue-600 text-white px-6 py-2 rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all duration-200 shadow-md hover:shadow-lg"
          >
            🚀 Go to Train
          </a>
        </div>
      ) : (
        <>
          {/* Stats Summary */}
          <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl shadow-lg p-4 mb-6">
            <div className="flex justify-between items-center text-white">
              <div>
                <p className="text-blue-100 text-sm">Total Models</p>
                <p className="text-3xl font-bold">{models.length}</p>
              </div>
              <div className="text-right">
                <p className="text-blue-100 text-sm">Best Accuracy</p>
                <p className="font-medium">
                  {Math.max(...models.map(m => parseFloat(m.accuracy) || 0), 0).toFixed(4)}%
                </p>
              </div>
            </div>
          </div>

          {/* Models Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {models.map(m => (
              <ModelCard key={m.id} model={m} />
            ))}
          </div>
        </>
      )}
    </div>
  )
}