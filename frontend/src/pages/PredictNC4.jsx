import { useState } from 'react'
import API from '../api/api'

export default function PredictNC4(){
  const [modelName, setModelName] = useState('')
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      setFile(selectedFile)
      setError('')
      setResult(null)
    }
  }

  const handlePredict = async () => {
    if (!modelName.trim()) {
      setError('Please enter a model name')
      return
    }
    
    if (!file) {
      setError('Please select an NC4 file')
      return
    }
    
    setLoading(true)
    setError('')
    setResult(null)
    
    const fd = new FormData()
    fd.append('file', file)
    fd.append('model_name', modelName)

    try{
      const res = await API.post('/predict-nc4/', fd)
      setResult(res.data)
    } catch(e){
      setError(e.response?.data?.detail || 'Prediction failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="ml-64 p-8 pt-24 min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-extrabold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
          🌐 NetCDF4 (NC4) Prediction
        </h1>
        <p className="text-blue-500 mt-2">Upload NetCDF4 files for geospatial and scientific data analysis</p>
      </div>

      {/* Prediction Form Card */}
      <div className="max-w-2xl">
        <div className="bg-gradient-to-br from-white to-blue-50/50 rounded-xl shadow-md border border-blue-200 overflow-hidden">
          <div className="bg-gradient-to-r from-blue-500 to-blue-600 px-6 py-4">
            <h2 className="text-white font-bold text-lg flex items-center gap-2">
              🎯 NC4 Model Prediction
            </h2>
          </div>
          
          <div className="p-6 space-y-6">
            {/* Model Name Input */}
            <div>
              <label className="block font-bold text-blue-800 mb-2 flex items-center gap-2">
                🧠 Model Name
              </label>
              <input 
                className="w-full px-4 py-2 border border-blue-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                placeholder="Enter your trained NC4 model name" 
                value={modelName}
                onChange={(e) => setModelName(e.target.value)} 
              />
              <p className="text-xs text-blue-500 mt-1">Enter the exact name of your NetCDF4 model</p>
            </div>

            {/* File Upload Area */}
            <div>
              <label className="block font-bold text-blue-800 mb-2 flex items-center gap-2">
                📁 Upload NC4 File
              </label>
              <div className="border-2 border-dashed border-blue-300 rounded-lg p-6 text-center hover:border-blue-500 transition-colors bg-blue-50/30">
                <input
                  type="file"
                  accept=".nc4,.nc"
                  onChange={handleFileChange}
                  className="w-full text-sm text-blue-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-100 file:text-blue-700 hover:file:bg-blue-200 transition-all cursor-pointer"
                />
                <p className="text-xs text-blue-400 mt-2">
                  Supports NetCDF4 (.nc4, .nc) formats
                </p>
              </div>
              
              {/* File Info Display */}
              {file && (
                <div className="mt-4 bg-blue-50 rounded-lg p-3 border border-blue-200">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-2xl">📄</span>
                      <div>
                        <p className="text-sm font-semibold text-blue-800">{file.name}</p>
                        <p className="text-xs text-blue-500">{(file.size / 1024).toFixed(2)} KB</p>
                      </div>
                    </div>
                    <button
                      onClick={() => {
                        setFile(null)
                        setResult(null)
                        setError('')
                      }}
                      className="text-red-500 hover:text-red-700 transition-colors text-sm px-2 py-1 rounded hover:bg-red-50"
                    >
                      ✕ Remove
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Info Box */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
              <p className="text-blue-700 text-sm flex items-start gap-2">
                <span>💡</span>
                <span>NetCDF4 (Network Common Data Form) files are used for multidimensional scientific data. Make sure your model is trained for NC4 data.</span>
              </p>
            </div>

            {/* Error Message */}
            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-600 text-sm flex items-center gap-2">
                  ❌ {error}
                </p>
              </div>
            )}

            {/* Predict Button */}
            <button
              onClick={handlePredict}
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-500 to-blue-600 text-white py-3 rounded-lg font-bold hover:from-blue-600 hover:to-blue-700 transition-all duration-200 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-[1.02]"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Processing NC4 Data...
                </span>
              ) : (
                '🌊 Predict NC4'
              )}
            </button>
          </div>
        </div>

        {/* Prediction Result */}
        {result && (
          <div className="mt-8 bg-gradient-to-br from-blue-50 to-white rounded-xl shadow-md border border-blue-200 overflow-hidden">
            <div className="bg-gradient-to-r from-green-500 to-teal-500 px-6 py-4">
              <h2 className="text-white font-bold text-lg flex items-center gap-2">
                🎯 Prediction Result
              </h2>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div className="bg-blue-50 p-3 rounded-lg">
                  <p className="text-xs text-blue-600 font-semibold">Model Used</p>
                  <p className="text-gray-800 font-medium">{modelName}</p>
                </div>
                <div className="bg-blue-50 p-3 rounded-lg">
                  <p className="text-xs text-blue-600 font-semibold">File Processed</p>
                  <p className="text-gray-800 font-medium">{file?.name}</p>
                </div>
              </div>
              
              {/* NC4 Specific Result Display */}
              {result.type === 'nc4_prediction' && (
                <>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div className="bg-gradient-to-r from-blue-100 to-blue-50 p-3 rounded-lg">
                      <p className="text-xs text-blue-600 font-semibold">Target Variable</p>
                      <p className="text-gray-800 font-mono text-sm">{result.target || 'N/A'}</p>
                    </div>
                    <div className="bg-gradient-to-r from-blue-100 to-blue-50 p-3 rounded-lg">
                      <p className="text-xs text-blue-600 font-semibold">Samples Predicted</p>
                      <p className="text-gray-800 font-bold text-lg">{result.samples_predicted}</p>
                    </div>
                  </div>
                  
                  {result.prediction_sample && (
                    <div className="bg-blue-50 p-3 rounded-lg mb-4">
                      <p className="font-semibold text-blue-800 mb-2 flex items-center gap-2">
                        📊 Prediction Sample
                      </p>
                      <pre className="bg-white p-3 rounded-lg text-xs overflow-auto max-h-40 border border-blue-200">
                        {JSON.stringify(result.prediction_sample, null, 2)}
                      </pre>
                    </div>
                  )}
                </>
              )}
              
              {/* Full Result Details */}
              <div className="bg-blue-50 p-3 rounded-lg">
                <p className="font-semibold text-blue-800 mb-2 flex items-center gap-2">
                  📋 Complete Response
                </p>
                <pre className="bg-white p-3 rounded-lg text-xs overflow-auto max-h-60 border border-blue-200">
                  {JSON.stringify(result, null, 2)}
                </pre>
              </div>
              
              {/* Download Result Option */}
              <div className="mt-4 flex justify-end">
                <button
                  onClick={() => {
                    const dataStr = JSON.stringify(result, null, 2)
                    const dataBlob = new Blob([dataStr], { type: 'application/json' })
                    const url = URL.createObjectURL(dataBlob)
                    const a = document.createElement('a')
                    a.href = url
                    a.download = `prediction_${modelName}_${new Date().toISOString().slice(0,19)}.json`
                    a.click()
                    URL.revokeObjectURL(url)
                  }}
                  className="text-sm bg-blue-100 text-blue-600 px-3 py-1 rounded-lg hover:bg-blue-200 transition-all duration-200 flex items-center gap-1"
                >
                  📥 Download Result (JSON)
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}