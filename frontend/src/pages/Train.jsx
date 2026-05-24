import { useState } from 'react'
import API from '../api/api'

export default function Train(){
  const [file, setFile] = useState(null)
  const [target, setTarget] = useState('')
  const [modelName, setModelName] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleTrain = async () => {
    if (!file || !target) { 
      setError('Please choose file and target column')
      return 
    }
    setLoading(true)
    setError('')
    const fd = new FormData()
    fd.append('file', file)
    fd.append('target_column', target)
    fd.append('model_name', modelName || 'my_model')
    fd.append('token', localStorage.getItem('token'))

    try {
      const res = await API.post('/train-model/', fd)
      setResult(res.data)
      setFile(null)
      setTarget('')
      setModelName('')
    } catch (e) {
      setError(e.response?.data?.detail || 'Training failed')
    }
    setLoading(false)
  }

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Train Model</h1>

      <div className="bg-white p-6 rounded shadow">
        <div className="mb-4">
          <label className="block font-bold mb-2">Upload CSV File</label>
          <input 
            type="file" 
            accept=".csv" 
            onChange={e => setFile(e.target.files[0])} 
            className="border p-2 w-full rounded"
          />
          {file && <p className="text-sm text-gray-600 mt-1">Selected: {file.name}</p>}
        </div>

        <div className="mb-4">
          <label className="block font-bold mb-2">Target Column</label>
          <input 
            className="border p-2 w-full rounded" 
            placeholder="e.g., target" 
            value={target} 
            onChange={e => setTarget(e.target.value)} 
          />
        </div>

        <div className="mb-4">
          <label className="block font-bold mb-2">Model Name</label>
          <input 
            className="border p-2 w-full rounded" 
            placeholder="e.g., my_model" 
            value={modelName} 
            onChange={e => setModelName(e.target.value)} 
          />
        </div>

        {error && <p className="text-red-600 mb-4">{error}</p>}

        <button 
          onClick={handleTrain} 
          disabled={loading} 
          className="bg-blue-500 text-white px-6 py-2 rounded font-bold hover:bg-blue-600 disabled:opacity-50 w-full"
        >
          {loading ? 'Training...' : 'Train Model'}
        </button>
      </div>

      {result && (
        <div className="mt-6 bg-green-50 p-4 rounded border border-green-200">
          <h2 className="font-bold text-green-700 mb-2">✓ Training Complete</h2>
          <div className="text-sm space-y-1">
            <p><strong>Model:</strong> {result.model_name}</p>
            <p><strong>Type:</strong> {result.problem_type}</p>
            {result.best_model && <p><strong>Best Score:</strong> {parseFloat(result.best_model.score).toFixed(4)}</p>}
          </div>
        </div>
      )}
    </div>
  )
}
