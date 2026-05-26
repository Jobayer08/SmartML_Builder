import { useState, useEffect } from 'react'
import API from '../api/api'
import PredictionCard from '../components/PredictionCard'

export default function History(){
  const [predictions, setPredictions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const token = localStorage.getItem('token')
        const res = await API.get(`/my-predictions?token=${token}`)
        setPredictions(res.data || [])
      } catch (e) {
        console.error('Failed to fetch predictions')
      }
      setLoading(false)
    }
    fetchHistory()
  }, [])

  if (loading) {
    return (
      <div className="ml-64 p-8 pt-24 min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-blue-600 font-medium">Loading prediction history...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="ml-64 p-8 pt-24 min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-extrabold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
          📜 Prediction History
        </h1>
        <p className="text-blue-500 mt-2">View all your past model predictions</p>
      </div>

      {predictions.length === 0 ? (
        <div className="bg-gradient-to-br from-blue-50/80 to-white rounded-xl shadow-md border border-blue-200 p-12 text-center">
          <div className="text-6xl mb-4">🔮</div>
          <p className="text-blue-600 text-lg font-medium mb-2">No predictions yet</p>
          <p className="text-blue-400">Make your first prediction to see it here</p>
        </div>
      ) : (
        <>
          {/* Stats Summary */}
          <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl shadow-lg p-4 mb-6">
            <div className="flex justify-between items-center text-white">
              <div>
                <p className="text-blue-100 text-sm">Total Predictions</p>
                <p className="text-3xl font-bold">{predictions.length}</p>
              </div>
              <div className="text-right">
                <p className="text-blue-100 text-sm">Last Prediction</p>
                <p className="font-medium">
                  {new Date(predictions[0]?.created_at).toLocaleDateString()}
                </p>
              </div>
            </div>
          </div>

          {/* Predictions Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {predictions.map((pred) => (
              <PredictionCard key={pred.id} prediction={pred} />
            ))}
          </div>
        </>
      )}
    </div>
  )
}