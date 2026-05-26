import { useState, useEffect } from 'react'
import API from '../api/api'

export default function Predict(){
  const [models, setModels] = useState([])
  const [selectedModel, setSelectedModel] = useState('')
  const [input, setInput] = useState('')
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const token = localStorage.getItem('token')
        const res = await API.get(`/my-models/?token=${token}`)
        setModels(res.data || [])
      } catch (e) {
        console.error('Failed to fetch models')
      }
    }
    fetchModels()
  }, [])

  const handlePredict = async () => {
    if (!selectedModel || !input) {
      setError('Select model and provide input')
      return
    }
    setLoading(true)
    setError('')

    try {
      const fd = new FormData()
      fd.append('csv_string', input)
      fd.append('model_name', selectedModel)
      fd.append('token', localStorage.getItem('token'))
      
      const res = await API.post('/predict-csv/', fd)
      setPrediction(res.data)
    } catch (e) {
      setError(e.response?.data?.detail || 'Prediction failed')
    }
    setLoading(false)
  }

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Make Prediction</h1>

      <div className="bg-white p-6 rounded shadow">
        <div className="mb-4">
          <label className="block font-bold mb-2">Select Model</label>
          <select 
            value={selectedModel} 
            onChange={e => setSelectedModel(e.target.value)}
            className="border p-2 w-full rounded"
          >
            <option value="">-- Choose Model --</option>
            {models.map(m => (
              <option key={m.id} value={m.model_name}>{m.model_name}</option>
            ))}
          </select>
        </div>

        <div className="mb-4">
          <label className="block font-bold mb-2">CSV Input (comma-separated values)</label>
          <textarea 
            className="border p-2 w-full rounded h-20" 
            placeholder="e.g., 1.5,2.3,4.1"
            value={input}
            onChange={e => setInput(e.target.value)}
          />
          <p className="text-xs text-gray-500 mt-1">Paste a single CSV row (features in same order as training)</p>
        </div>

        {error && <p className="text-red-600 mb-4">{error}</p>}

        <button 
          onClick={handlePredict} 
          disabled={loading}
          className="bg-green-500 text-white px-6 py-2 rounded font-bold hover:bg-green-600 disabled:opacity-50 w-full"
        >
          {loading ? 'Predicting...' : 'Predict'}
        </button>
      </div>

      {prediction && (
        <div className="mt-6 bg-blue-50 p-4 rounded border border-blue-200">
          <h2 className="font-bold text-blue-700 mb-2">🎯 Prediction Result</h2>
          <div className="text-sm space-y-1">
            <p><strong>Model:</strong> {selectedModel}</p>
            <p><strong>Prediction:</strong> {JSON.stringify(prediction.prediction)}</p>
            {prediction.probability && <p><strong>Confidence:</strong> {(prediction.probability * 100).toFixed(2)}%</p>}
          </div>
        </div>
      )}
    </div>
  )
}
