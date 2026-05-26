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
    if (!file) { 
      setError('Please choose a file')
      return 
    }
    if (file.name.endsWith('.csv') && !target) {
      setError('Please specify target column for CSV')
      return
    }

    setLoading(true)
    setError('')
    const fd = new FormData()
    fd.append('file', file)
    if (target) fd.append('target_column', target)
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
    <div className="ml-64 p-8 pt-24 min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-extrabold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
          🚀 Train Model
        </h1>
        <p className="text-blue-500 mt-2">Train machine learning models on your datasets</p>
      </div>

      {/* Training Form Card */}
      <div className="max-w-2xl">
        <div className="bg-gradient-to-br from-white to-blue-50/50 rounded-xl shadow-md border border-blue-200 overflow-hidden">
          <div className="bg-gradient-to-r from-blue-500 to-blue-600 px-6 py-4">
            <h2 className="text-white font-bold text-lg flex items-center gap-2">
              ⚙️ Training Configuration
            </h2>
          </div>
          
          <div className="p-6 space-y-6">
            {/* File Upload */}
            <div>
              <label className="block font-bold text-blue-800 mb-2 flex items-center gap-2">
                📁 Upload Dataset
              </label>
              <div className="border-2 border-dashed border-blue-300 rounded-lg p-6 text-center hover:border-blue-500 transition-colors bg-blue-50/30">
                <input 
                  type="file" 
                  onChange={e => setFile(e.target.files[0])} 
                  className="w-full text-sm text-blue-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-100 file:text-blue-700 hover:file:bg-blue-200 transition-all cursor-pointer"
                  accept=".csv,.zip,.nc4"
                />
                <p className="text-xs text-blue-400 mt-2">
                  Supports CSV, ZIP (images), or NC4 formats
                </p>
              </div>
              {file && (
                <div className="mt-3 bg-blue-50 rounded-lg p-2 border border-blue-200">
                  <p className="text-sm text-blue-700 flex items-center gap-2">
                    📎 Selected: {file.name}
                    <button 
                      onClick={() => setFile(null)}
                      className="ml-auto text-red-500 hover:text-red-700 text-xs"
                    >
                      ✕ Remove
                    </button>
                  </p>
                </div>
              )}
            </div>

            {/* Target Column (CSV only) */}
            <div>
              <label className="block font-bold text-blue-800 mb-2 flex items-center gap-2">
                🎯 Target Column
                <span className="text-xs font-normal text-blue-500">(Required for CSV)</span>
              </label>
              <input 
                className="w-full px-4 py-2 border border-blue-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                placeholder="e.g., price, label, class" 
                value={target} 
                onChange={e => setTarget(e.target.value)} 
              />
              <p className="text-xs text-blue-500 mt-1">
                💡 Leave empty for image/NC4 datasets
              </p>
            </div>

            {/* Model Name */}
            <div>
              <label className="block font-bold text-blue-800 mb-2 flex items-center gap-2">
                🧠 Model Name
              </label>
              <input 
                className="w-full px-4 py-2 border border-blue-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                placeholder="e.g., house_price_model, image_classifier" 
                value={modelName} 
                onChange={e => setModelName(e.target.value)} 
              />
              <p className="text-xs text-blue-500 mt-1">
                💡 Default: "my_model" if left empty
              </p>
            </div>

            {/* Dataset Type Indicator */}
            {file && (
              <div className="bg-blue-50 rounded-lg p-3 border border-blue-200">
                <p className="text-sm text-blue-700">
                  <span className="font-semibold">📊 Dataset Type:</span>{' '}
                  {file.name.endsWith('.csv') ? 'CSV (Tabular Data)' : 
                   file.name.endsWith('.zip') ? 'ZIP (Image Dataset)' : 
                   file.name.endsWith('.nc4') ? 'NetCDF4 (Scientific Data)' : 
                   'Unknown'}
                </p>
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-600 text-sm flex items-center gap-2">
                  ❌ {error}
                </p>
              </div>
            )}

            {/* Train Button */}
            <button 
              onClick={handleTrain} 
              disabled={loading} 
              className="w-full bg-gradient-to-r from-blue-500 to-blue-600 text-white py-3 rounded-lg font-bold hover:from-blue-600 hover:to-blue-700 transition-all duration-200 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-[1.02]"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Training Model...
                </span>
              ) : (
                '🎯 Train Model'
              )}
            </button>
          </div>
        </div>

        {/* Training Result */}
        {result && (
          <div className="mt-8 bg-gradient-to-br from-green-50 to-white rounded-xl shadow-md border border-green-200 overflow-hidden">
            <div className="bg-gradient-to-r from-green-500 to-teal-500 px-6 py-4">
              <h2 className="text-white font-bold text-lg flex items-center gap-2">
                ✅ Training Complete!
              </h2>
            </div>
            <div className="p-6 space-y-3">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-green-50 p-3 rounded-lg">
                  <p className="text-xs text-green-600 font-semibold">Model Name</p>
                  <p className="text-gray-800 font-medium">{result.model_name}</p>
                </div>
                <div className="bg-green-50 p-3 rounded-lg">
                  <p className="text-xs text-green-600 font-semibold">Dataset Type</p>
                  <p className="text-gray-800 font-medium">{result.dataset_type}</p>
                </div>
              </div>
              
              {result.training_result?.problem_type && (
                <div className="bg-green-50 p-3 rounded-lg">
                  <p className="text-xs text-green-600 font-semibold">Problem Type</p>
                  <p className="text-gray-800 font-medium">{result.training_result.problem_type}</p>
                </div>
              )}
              
              {result.training_result?.model_results && (
                <div className="bg-green-50 p-3 rounded-lg">
                  <p className="font-semibold text-green-800 mb-2 flex items-center gap-2">
                    📊 Training Results
                  </p>
                  <pre className="bg-white p-3 rounded-lg text-xs overflow-auto max-h-48 border border-green-200">
                    {JSON.stringify(result.training_result.model_results, null, 2)}
                  </pre>
                </div>
              )}
              
              {/* Quick Action Buttons */}
              <div className="flex gap-3 pt-2">
                <button
                  onClick={() => {
                    setResult(null)
                    setFile(null)
                    setTarget('')
                    setModelName('')
                  }}
                  className="flex-1 text-sm bg-blue-100 text-blue-600 px-3 py-2 rounded-lg hover:bg-blue-200 transition-all duration-200"
                >
                  🆕 Train Another
                </button>
                <a
                  href="/models"
                  className="flex-1 text-center text-sm bg-gradient-to-r from-blue-500 to-blue-600 text-white px-3 py-2 rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all duration-200"
                >
                  👁️ View My Models
                </a>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}