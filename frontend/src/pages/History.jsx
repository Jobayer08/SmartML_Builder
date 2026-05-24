import { useState, useEffect } from 'react'
import API from '../api/api'

export default function History(){
  const [predictions, setPredictions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await API.get('/predictions/')
        setPredictions(res.data || [])
      } catch (e) {
        console.error('Failed to fetch predictions')
      }
      setLoading(false)
    }
    fetchHistory()
  }, [])

  if (loading) return <div className="p-8 text-center">Loading...</div>

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Prediction History</h1>

      {predictions.length === 0 ? (
        <div className="bg-gray-50 p-8 rounded text-center">
          <p className="text-gray-600">No predictions yet</p>
        </div>
      ) : (
        <div className="grid gap-4">
          {predictions.map((pred) => (
            <div key={pred.id} className="bg-white p-4 rounded border border-gray-200">
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-bold text-lg">{pred.model_name}</h3>
                <span className="text-xs text-gray-500">{new Date(pred.created_at).toLocaleString()}</span>
              </div>
              <div className="text-sm space-y-1">
                <p><strong>Prediction:</strong> {JSON.stringify(pred.prediction)}</p>
                {pred.confidence && <p><strong>Confidence:</strong> {(pred.confidence * 100).toFixed(2)}%</p>}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
