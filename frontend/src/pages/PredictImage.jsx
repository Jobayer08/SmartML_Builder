import { useState } from 'react'
import API from '../api/api'

export default function PredictImage(){
  const [modelName, setModelName] = useState('')
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [previewUrl, setPreviewUrl] = useState(null)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      setFile(selectedFile)
      setError('')
      setResult(null)
      
      // Create preview URL
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl)
      }
      setPreviewUrl(URL.createObjectURL(selectedFile))
    }
  }

  const handlePredict = async () => {
    if (!modelName.trim()) {
      setError('Please enter a model name')
      return
    }
    
    if (!file) {
      setError('Please select an image file')
      return
    }
    
    setLoading(true)
    setError('')
    setResult(null)
    
    const fd = new FormData()
    fd.append('file', file)
    fd.append('model_name', modelName)

    try{
      const res = await API.post('/predict-image/', fd)
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
          🖼️ Image Prediction
        </h1>
        <p className="text-blue-500 mt-2">Upload an image to classify or analyze using your trained image model</p>
      </div>

      {/* Prediction Form Card */}
      <div className="max-w-2xl">
        <div className="bg-gradient-to-br from-white to-blue-50/50 rounded-xl shadow-md border border-blue-200 overflow-hidden">
          <div className="bg-gradient-to-r from-blue-500 to-blue-600 px-6 py-4">
            <h2 className="text-white font-bold text-lg flex items-center gap-2">
              🎯 Image Classification
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
                placeholder="Enter your trained image model name" 
                value={modelName}
                onChange={(e) => setModelName(e.target.value)} 
              />
              <p className="text-xs text-blue-500 mt-1">Enter the exact name of your image classification model</p>
            </div>

            {/* File Upload Area */}
            <div>
              <label className="block font-bold text-blue-800 mb-2 flex items-center gap-2">
                📸 Upload Image
              </label>
              <div className="border-2 border-dashed border-blue-300 rounded-lg p-6 text-center hover:border-blue-500 transition-colors bg-blue-50/30">
                <input
                  type="file"
                  accept=".jpg,.jpeg,.png"
                  onChange={handleFileChange}
                  className="w-full text-sm text-blue-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-100 file:text-blue-700 hover:file:bg-blue-200 transition-all cursor-pointer"
                />
                <p className="text-xs text-blue-400 mt-2">
                  Supports JPG, JPEG, PNG formats
                </p>
              </div>
              
              {/* Image Preview */}
              {previewUrl && (
                <div className="mt-4">
                  <p className="text-sm font-semibold text-blue-600 mb-2">Image Preview:</p>
                  <div className="relative inline-block">
                    <img 
                      src={previewUrl} 
                      alt="Preview" 
                      className="max-w-full h-48 rounded-lg border border-blue-200 shadow-md object-cover"
                    />
                    <button
                      onClick={() => {
                        setFile(null)
                        setPreviewUrl(null)
                        setResult(null)
                      }}
                      className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center hover:bg-red-600 transition-colors text-xs"
                    >
                      ✕
                    </button>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    File: {file?.name} ({(file?.size / 1024).toFixed(2)} KB)
                  </p>
                </div>
              )}
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
                  Analyzing Image...
                </span>
              ) : (
                '🔍 Predict Image'
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
                  <p className="text-xs text-blue-600 font-semibold">Image Processed</p>
                  <p className="text-gray-800 font-medium">{file?.name}</p>
                </div>
              </div>
              
              {/* Classification Result */}
              {result.type === 'image_classification' && (
                <div className="bg-gradient-to-r from-green-100 to-green-50 p-4 rounded-lg text-center">
                  <p className="font-semibold text-green-800 mb-2">🏷️ Classification Result</p>
                  <p className="text-3xl font-bold text-green-700">{result.prediction}</p>
                </div>
              )}
              
              {/* Clustering Result */}
              {result.type === 'image_cluster' && (
                <div className="bg-gradient-to-r from-purple-100 to-purple-50 p-4 rounded-lg text-center">
                  <p className="font-semibold text-purple-800 mb-2">🔢 Cluster Assignment</p>
                  <p className="text-3xl font-bold text-purple-700">Cluster {result.cluster_id}</p>
                  {result.example_images_in_this_cluster && (
                    <div className="mt-4 text-left">
                      <p className="font-semibold text-purple-800 mb-2 text-sm">🖼️ Example Images in this Cluster</p>
                      <pre className="bg-white p-3 rounded-lg text-xs overflow-auto max-h-40 border border-purple-200">
                        {JSON.stringify(result.example_images_in_this_cluster, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>
              )}
              
              {/* Full Result Details */}
              <div className="mt-4 bg-blue-50 p-3 rounded-lg">
                <p className="font-semibold text-blue-800 mb-2 flex items-center gap-2">
                  📊 Detailed Response
                </p>
                <pre className="bg-white p-3 rounded-lg text-xs overflow-auto max-h-40 border border-blue-200">
                  {JSON.stringify(result, null, 2)}
                </pre>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}