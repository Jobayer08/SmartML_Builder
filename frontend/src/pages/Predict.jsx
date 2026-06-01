import { useState, useEffect } from 'react'
import API from '../api/api'

export default function Predict(){
  const [models, setModels] = useState([])
  const [selectedModel, setSelectedModel] = useState('')
  const [selectedModelType, setSelectedModelType] = useState('')
  const [headers, setHeaders] = useState('')
  const [values, setValues] = useState('')
  const [file, setFile] = useState(null)
  const [prediction, setPrediction] = useState(null)
  const [loadingModels, setLoadingModels] = useState(true)
  const [predicting, setPredicting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const token = localStorage.getItem('token')
        const res = await API.get(`/my-models?token=${token}`)
        const modelsList = res.data?.models || res.data || []
        const allModels = Array.isArray(modelsList) ? modelsList : []
        setModels(allModels)
        if (allModels.length > 0) {
          setSelectedModel(allModels[0].model_name)
          setSelectedModelType(allModels[0].model_type)
        }
      } catch (e) {
        setError('Failed to load models')
        console.error(e)
      }
      setLoadingModels(false)
    }
    fetchModels()
  }, [])

  const handleModelChange = (modelName) => {
    const model = models.find((m) => m.model_name === modelName)
    setSelectedModel(modelName)
    setSelectedModelType(model?.model_type || '')
    setPrediction(null)
    setError('')
    setHeaders('')
    setValues('')
    setFile(null)
  }

  const handlePredict = async () => {
    if (!selectedModel) {
      setError('Please select a model')
      return
    }

    setPredicting(true)
    setError('')
    setPrediction(null)

    try {
      const token = localStorage.getItem('token')
      let res

      if (selectedModelType === 'csv') {
        if (!headers.trim() || !values.trim()) {
          setError('Enter feature names and matching values for CSV prediction.')
          setPredicting(false)
          return
        }

        const headerItems = headers.split(',').map(h => h.trim()).filter(Boolean)
        const valueItems = values.split(',').map(v => v.trim())

        if (headerItems.length !== valueItems.length) {
          setError('Header count must match value count.')
          setPredicting(false)
          return
        }

        const data = {}
        headerItems.forEach((header, index) => {
          const value = valueItems[index]
          data[header] = value === '' ? null : (isNaN(value) ? value : Number(value))
        })

        res = await API.post('/predict-csv/', {
          model_name: selectedModel,
          data,
          token
        })
      } else if (selectedModelType.includes('image')) {
        if (!file) {
          setError('Upload an image file for this model.')
          setPredicting(false)
          return
        }

        const fd = new FormData()
        fd.append('model_name', selectedModel)
        fd.append('file', file)
        fd.append('token', token)

        res = await API.post('/predict-image/', fd)
      } else if (selectedModelType === 'nc4') {
        if (!file) {
          setError('Upload an NC4 file for this model.')
          setPredicting(false)
          return
        }

        const fd = new FormData()
        fd.append('model_name', selectedModel)
        fd.append('file', file)
        fd.append('token', token)

        res = await API.post('/predict-nc4/', fd)
      } else {
        setError('This model type is not supported for prediction yet.')
        setPredicting(false)
        return
      }

      setPrediction(res.data)
    } catch (e) {
      setError(e.response?.data?.detail || 'Prediction failed')
    }

    setPredicting(false)
  }

  const modelHelpText = () => {
    if (selectedModelType === 'csv') {
      return '📊 Enter feature names and values for a single row, separated by commas.'
    }
    if (selectedModelType.includes('image')) {
      return '🖼️ Upload one image file for prediction with the selected image model.'
    }
    if (selectedModelType === 'nc4') {
      return '🌐 Upload one NC4 file for prediction with the selected NC4 model.'
    }
    return '🎯 Select a model to see the correct prediction input.'
  }

  return (
    <div className="ml-64 p-8 pt-24 min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-extrabold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
          🔮 Make Prediction
        </h1>
        <p className="text-blue-500 mt-2">Use your trained models to make predictions on new data</p>
      </div>

      {loadingModels && (
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-blue-600 font-medium">Loading your models...</p>
          </div>
        </div>
      )}

      {!loadingModels && models.length === 0 && (
        <div className="bg-gradient-to-br from-blue-50/80 to-white rounded-xl shadow-md border border-blue-200 p-12 text-center">
          <div className="text-6xl mb-4">🎯</div>
          <p className="text-blue-600 text-lg font-medium mb-2">No models trained yet</p>
          <p className="text-blue-400 mb-4">Train a model first to make predictions</p>
          <a 
            href="/train" 
            className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-500 to-blue-600 text-white px-6 py-2 rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all duration-200 shadow-md hover:shadow-lg"
          >
             Go to Train
          </a>
        </div>
      )}

      {!loadingModels && models.length > 0 && (
        <>
          {/* Prediction Form Card */}
          <div className="bg-gradient-to-br from-white to-blue-50/50 rounded-xl shadow-md border border-blue-200 overflow-hidden">
            <div className="bg-gradient-to-r from-blue-500 to-blue-600 px-6 py-4">
              <h2 className="text-white font-bold text-lg flex items-center gap-2">
                📝 Prediction Configuration
              </h2>
            </div>
            
            <div className="p-6 space-y-6">
              {/* Model Selection */}
              <div>
                <label className="block font-bold text-blue-800 mb-2 flex items-center gap-2">
                  🧠 Select Model
                </label>
                <select
                  value={selectedModel}
                  onChange={e => handleModelChange(e.target.value)}
                  className="w-full px-4 py-2 border border-blue-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
                >
                  <option value="">-- Choose Model --</option>
                  {models.map(m => (
                    <option key={m.id} value={m.model_name}>
                      {m.model_name} ({m.model_type})
                    </option>
                  ))}
                </select>
              </div>

              {/* Help Text */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                <p className="text-blue-700 text-sm flex items-center gap-2">
                  💡 {modelHelpText()}
                </p>
              </div>

              {/* CSV Input Fields */}
              {selectedModelType === 'csv' && (
                <div className="space-y-4">
                  <div>
                    <label className="block font-semibold text-gray-700 mb-2">
                      📋 Feature Names (comma-separated)
                    </label>
                    <textarea
                      className="w-full px-4 py-2 border border-blue-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
                      rows="3"
                      placeholder="e.g., age, study_time, attendance"
                      value={headers}
                      onChange={e => setHeaders(e.target.value)}
                    />
                  </div>

                  <div>
                    <label className="block font-semibold text-gray-700 mb-2">
                      📊 Values (comma-separated)
                    </label>
                    <textarea
                      className="w-full px-4 py-2 border border-blue-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
                      rows="3"
                      placeholder="e.g., 18, 12, 85"
                      value={values}
                      onChange={e => setValues(e.target.value)}
                    />
                  </div>
                </div>
              )}

              {/* File Upload for Image/NC4 */}
              {(selectedModelType.includes('image') || selectedModelType === 'nc4') && (
                <div>
                  <label className="block font-semibold text-gray-700 mb-2">
                    📁 Upload File
                  </label>
                  <div className="border-2 border-dashed border-blue-300 rounded-lg p-6 text-center hover:border-blue-500 transition-colors">
                    <input
                      type="file"
                      accept={selectedModelType === 'nc4' ? '.nc4,.nc' : '.jpg,.jpeg,.png'}
                      onChange={e => setFile(e.target.files[0])}
                      className="w-full text-sm text-blue-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                    />
                    {file && (
                      <p className="text-sm text-blue-600 mt-2">
                        ✅ Selected: {file.name}
                      </p>
                    )}
                  </div>
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

              {/* Predict Button */}
              <button
                onClick={handlePredict}
                disabled={predicting}
                className="w-full bg-gradient-to-r from-blue-500 to-blue-600 text-white py-3 rounded-lg font-bold hover:from-blue-600 hover:to-blue-700 transition-all duration-200 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-[1.02]"
              >
                {predicting ? (
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
              <div className="p-6 space-y-3">
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-blue-50 p-3 rounded-lg">
                    <p className="text-xs text-blue-600 font-semibold">Model</p>
                    <p className="text-gray-800 font-medium">{selectedModel}</p>
                  </div>
                </div>
                
                {prediction.type === 'csv_prediction' && (
                  <div className="bg-gradient-to-r from-blue-100 to-blue-50 p-4 rounded-lg">
                    <p className="font-semibold text-blue-800 mb-2">📈 Prediction Output</p>
                    <p className="text-gray-800 font-mono text-sm">{JSON.stringify(prediction.prediction)}</p>
                  </div>
                )}
                
                {prediction.type === 'image_classification' && (
                  <div className="space-y-3">
                    <div className="bg-gradient-to-r from-green-100 to-green-50 p-4 rounded-lg">
                      <p className="font-semibold text-green-800 mb-2">🏷️ Classification Result</p>
                      <p className="text-2xl font-bold text-green-700">{prediction.prediction}</p>
                    </div>
                    <div className="bg-blue-50 p-3 rounded-lg">
                      <p className="font-semibold text-blue-800">📚 Available Classes</p>
                      <div className="flex flex-wrap gap-2 mt-2">
                        {prediction.classes?.map((cls, idx) => (
                          <span key={idx} className="bg-white px-2 py-1 rounded text-xs text-blue-600 border border-blue-200">{cls}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
                
                {prediction.type === 'image_cluster' && (
                  <div className="space-y-3">
                    <div className="bg-gradient-to-r from-purple-100 to-purple-50 p-4 rounded-lg text-center">
                      <p className="font-semibold text-purple-800 mb-2">🔢 Cluster Assignment</p>
                      <p className="text-3xl font-bold text-purple-700">Cluster {prediction.cluster_id}</p>
                    </div>
                    {prediction.example_images_in_this_cluster && (
                      <div className="bg-blue-50 p-3 rounded-lg">
                        <p className="font-semibold text-blue-800 mb-2">🖼️ Example Images in this Cluster</p>
                        <pre className="bg-white p-3 rounded-lg text-xs overflow-auto max-h-40 border border-blue-200">
                          {JSON.stringify(prediction.example_images_in_this_cluster, null, 2)}
                        </pre>
                      </div>
                    )}
                  </div>
                )}
                
                {prediction.type === 'nc4_prediction' && (
                  <div className="space-y-3">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-blue-50 p-3 rounded-lg">
                        <p className="text-xs text-blue-600 font-semibold">Target Variable</p>
                        <p className="text-gray-800 font-medium">{prediction.target || 'N/A'}</p>
                      </div>
                      <div className="bg-blue-50 p-3 rounded-lg">
                        <p className="text-xs text-blue-600 font-semibold">Samples Predicted</p>
                        <p className="text-gray-800 font-medium">{prediction.samples_predicted}</p>
                      </div>
                    </div>
                    <div className="bg-blue-50 p-3 rounded-lg">
                      <p className="font-semibold text-blue-800 mb-2">📊 Prediction Sample</p>
                      <pre className="bg-white p-3 rounded-lg text-xs overflow-auto max-h-40 border border-blue-200">
                        {JSON.stringify(prediction.prediction_sample || prediction.prediction || [], null, 2)}
                      </pre>
                    </div>
                  </div>
                )}
                
                {prediction.error && (
                  <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                    <p className="text-red-600 text-sm">❌ Error: {prediction.error}</p>
                  </div>
                )}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}