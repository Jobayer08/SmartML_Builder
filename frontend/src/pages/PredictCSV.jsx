import { useState } from 'react'
import API from '../api/api'

export default function PredictCSV(){
  const [modelName, setModelName] = useState('')
  const [formData, setFormData] = useState({})
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handlePredict = async () => {
    if (!modelName.trim()) {
      setError('Please enter a model name')
      return
    }
    
    if (Object.keys(formData).length === 0) {
      setError('Please enter at least one feature value')
      return
    }
    
    setLoading(true)
    setError('')
    
    try{
      const res = await API.post('/predict-csv/', { model_name: modelName, data: formData })
      setPrediction(res.data)
    }catch(e){
      setError(e.response?.data?.detail || 'Prediction failed')
      setPrediction(null)
    } finally {
      setLoading(false)
    }
  }

  const handleAddFeature = () => {
    const featureName = prompt('Enter feature name:')
    if (featureName) {
      setFormData({ ...formData, [featureName]: '' })
    }
  }

  const handleRemoveFeature = (featureName) => {
    const newFormData = { ...formData }
    delete newFormData[featureName]
    setFormData(newFormData)
  }

  return (
    <div className="ml-64 p-8 pt-24 min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-extrabold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
          📊 CSV Prediction
        </h1>
        <p className="text-blue-500 mt-2">Make predictions using CSV-based models with custom feature values</p>
      </div>

      {/* Prediction Form Card */}
      <div className="max-w-2xl">
        <div className="bg-gradient-to-br from-white to-blue-50/50 rounded-xl shadow-md border border-blue-200 overflow-hidden">
          <div className="bg-gradient-to-r from-blue-500 to-blue-600 px-6 py-4">
            <h2 className="text-white font-bold text-lg flex items-center gap-2">
              🎯 CSV Model Prediction
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
                placeholder="Enter your trained model name" 
                value={modelName}
                onChange={(e) => setModelName(e.target.value)} 
              />
              <p className="text-xs text-blue-500 mt-1">Enter the exact name of the model you trained</p>
            </div>

            {/* Features Section */}
            <div>
              <div className="flex justify-between items-center mb-3">
                <label className="block font-bold text-blue-800 flex items-center gap-2">
                  📋 Features
                </label>
                <button
                  onClick={handleAddFeature}
                  className="text-sm bg-blue-100 text-blue-600 px-3 py-1 rounded-lg hover:bg-blue-200 transition-all duration-200 flex items-center gap-1"
                >
                  ➕ Add Feature
                </button>
              </div>
              
              {Object.keys(formData).length === 0 ? (
                <div className="text-center py-8 bg-blue-50 rounded-lg border border-blue-200">
                  <p className="text-blue-500">No features added yet</p>
                  <p className="text-blue-400 text-sm mt-1">Click "Add Feature" to start</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {Object.entries(formData).map(([feature, value]) => (
                    <div key={feature} className="flex gap-2 items-center">
                      <div className="flex-1">
                        <label className="block text-xs font-semibold text-blue-600 mb-1">
                          {feature}
                        </label>
                        <input
                          name={feature}
                          type="text"
                          value={value}
                          onChange={handleChange}
                          className="w-full px-3 py-2 border border-blue-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                          placeholder={`Enter value for ${feature}`}
                        />
                      </div>
                      <button
                        onClick={() => handleRemoveFeature(feature)}
                        className="mt-5 text-red-500 hover:text-red-700 transition-colors"
                      >
                        🗑️
                      </button>
                    </div>
                  ))}
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
                  Predicting...
                </span>
              ) : (
                '🔮 Predict'
              )}
            </button>
          </div>
        </div>

        {/* Prediction Result */}
        {prediction && (
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
                  <p className="text-xs text-blue-600 font-semibold">Features Provided</p>
                  <p className="text-gray-800 font-medium">{Object.keys(formData).length}</p>
                </div>
              </div>
              <div className="bg-gradient-to-r from-blue-100 to-blue-50 p-4 rounded-lg">
                <p className="font-semibold text-blue-800 mb-2 flex items-center gap-2">
                  📈 Prediction Output
                </p>
                <pre className="bg-white p-4 rounded-lg text-sm overflow-auto max-h-60 border border-blue-200 font-mono">
                  {JSON.stringify(prediction, null, 2)}
                </pre>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}