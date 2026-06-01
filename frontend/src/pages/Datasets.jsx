import { useEffect, useState } from 'react'
import API from '../api/api'
import DatasetCard from '../components/DatasetCard'

export default function Datasets(){
  const [datasets, setDatasets] = useState([])
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState('')
  const [selectedDataset, setSelectedDataset] = useState(null)
  const [datasetDetails, setDatasetDetails] = useState(null)

  useEffect(() => {
    fetchDatasets()
  }, [])

  const fetchDatasets = async () => {
    try {
      const token = localStorage.getItem('token')
      const res = await API.get(`/my-datasets?token=${token}`)
      const rows = res.data || []
      setDatasets(rows)
      return rows
    } catch (e) {
      console.log('Error fetching datasets')
      return []
    }
  }

  const fetchDatasetDetails = async (dataset_id) => {
    try {
      const token = localStorage.getItem('token')
      const res = await API.get(`/dataset-info/${dataset_id}?token=${token}`)
      setDatasetDetails(res.data)
      setSelectedDataset(dataset_id)
    } catch (e) {
      console.error('Error fetching dataset details:', e)
    }
  }

  const handleUpload = async () => {
    if (!file) return
    setUploading(true)
    setError('')
    const fd = new FormData()
    fd.append('file', file)
    const token = localStorage.getItem('token')
    try {
      await API.post(`/upload-dataset/?token=${token}`, fd)
      const rows = await fetchDatasets()
      const uploaded = rows.find(ds => ds.dataset_name === file.name)
      if (uploaded) {
        await fetchDatasetDetails(uploaded.id)
      }
      setFile(null)
    } catch (e) {
      setError(e.response?.data?.detail || 'Upload failed')
    }
    setUploading(false)
  }

  return (
    <div className="ml-64 p-8 pt-24 min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-extrabold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
          📁 Datasets
        </h1>
        <p className="text-blue-500 mt-2">Manage and upload your ML datasets</p>
      </div>

      {/* Upload Section */}
      <div className="bg-gradient-to-br from-blue-50/80 to-white rounded-xl shadow-md border border-blue-200 p-6 mb-8 transition-all hover:shadow-lg">
        <h2 className="font-bold text-xl text-blue-800 mb-4 flex items-center gap-2">
          📤 Upload New Dataset
        </h2>
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center">
            <label className="flex-1">
              <input 
                type="file" 
                onChange={e => setFile(e.target.files[0])} 
                className="block w-full text-sm text-blue-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 transition-all cursor-pointer"
                accept=".csv,.zip,.nc4"
              />
            </label>
            <button 
              onClick={handleUpload} 
              disabled={uploading || !file}
              className="bg-gradient-to-r from-blue-500 to-blue-600 text-white px-6 py-2 rounded-lg hover:from-blue-600 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-md hover:shadow-lg font-medium"
            >
              {uploading ? '⏳ Uploading...' : ' Upload Dataset'}
            </button>
          </div>
          {file && (
            <p className="text-sm text-blue-600 bg-blue-50 p-2 rounded-lg inline-block">
              📎 Selected: {file.name}
            </p>
          )}
          {error && (
            <p className="text-red-600 bg-red-50 p-3 rounded-lg text-sm border border-red-200">
              ❌ {error}
            </p>
          )}
        </div>
      </div>

      {/* Datasets Grid */}
      {datasets.length === 0 && !uploading ? (
        <div className="text-center py-12 bg-white/50 rounded-xl border border-blue-200">
          <p className="text-blue-500 text-lg">No datasets yet. Upload your first dataset above! 📊</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {datasets.map(ds => (
            <div key={ds.id} onClick={() => fetchDatasetDetails(ds.id)} className="cursor-pointer">
              <DatasetCard dataset={ds} />
            </div>
          ))}
        </div>
      )}

      {/* Dataset Details Modal/Section */}
      {selectedDataset && datasetDetails && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" onClick={() => setSelectedDataset(null)}>
          <div className="bg-gradient-to-br from-white to-blue-50 rounded-2xl shadow-2xl max-w-2xl w-full max-h-[80vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
            <div className="sticky top-0 bg-gradient-to-r from-blue-500 to-blue-600 text-white p-4 rounded-t-2xl flex justify-between items-center">
              <h2 className="text-xl font-bold">📊 Dataset Details</h2>
              <button onClick={() => setSelectedDataset(null)} className="text-white hover:bg-white/20 rounded-lg p-1 transition">✕</button>
            </div>
            <div className="p-6 space-y-4 text-sm">
              {datasetDetails.type === 'csv' && (
                <>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-blue-50 p-3 rounded-lg">
                      <p className="font-semibold text-blue-600">📄 Type:</p>
                      <p className="text-gray-700">CSV</p>
                    </div>
                    <div className="bg-blue-50 p-3 rounded-lg">
                      <p className="font-semibold text-blue-600">📊 Rows:</p>
                      <p className="text-gray-700">{datasetDetails.shape?.[0]}</p>
                    </div>
                    <div className="bg-blue-50 p-3 rounded-lg">
                      <p className="font-semibold text-blue-600">🔧 Features:</p>
                      <p className="text-gray-700">{datasetDetails.shape?.[1]}</p>
                    </div>
                  </div>
                  <div className="bg-blue-50 p-3 rounded-lg">
                    <p className="font-semibold text-blue-600 mb-2">📋 Columns:</p>
                    <div className="flex flex-wrap gap-2">
                      {datasetDetails.columns?.map((col, idx) => (
                        <span key={idx} className="bg-white px-2 py-1 rounded text-xs text-blue-600 border border-blue-200">{col}</span>
                      ))}
                    </div>
                  </div>
                  {datasetDetails.sample_rows && (
                    <div className="bg-blue-50 p-3 rounded-lg">
                      <p className="font-semibold text-blue-600 mb-2">🔍 Sample Data:</p>
                      <pre className="bg-white p-3 rounded-lg text-xs overflow-auto max-h-48 border border-blue-200">
                        {JSON.stringify(datasetDetails.sample_rows, null, 2)}
                      </pre>
                    </div>
                  )}
                </>
              )}
              {datasetDetails.type === 'nc4' && (
                <>
                  <div className="bg-blue-50 p-3 rounded-lg">
                    <p className="font-semibold text-blue-600">🌐 Type:</p>
                    <p className="text-gray-700">NetCDF4</p>
                  </div>
                  <div className="bg-blue-50 p-3 rounded-lg">
                    <p className="font-semibold text-blue-600 mb-2">📊 Variables:</p>
                    <pre className="bg-white p-3 rounded-lg text-xs overflow-auto max-h-48 border border-blue-200">
                      {JSON.stringify(datasetDetails.variables, null, 2)}
                    </pre>
                  </div>
                </>
              )}
              {datasetDetails.type === 'image' && (
                <div className="bg-blue-50 p-3 rounded-lg">
                  <p className="font-semibold text-blue-600">🖼️ Type:</p>
                  <p className="text-gray-700">Image Dataset</p>
                  <p className="mt-2 text-gray-600">{datasetDetails.message}</p>
                </div>
              )}
              {datasetDetails.type === 'zip' && (
                <>
                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div className="bg-blue-50 p-3 rounded-lg">
                      <p className="font-semibold text-blue-600">📦 Type:</p>
                      <p className="text-gray-700">ZIP Archive</p>
                    </div>
                    <div className="bg-blue-50 p-3 rounded-lg">
                      <p className="font-semibold text-blue-600">📊 Dataset Type:</p>
                      <p className="text-gray-700 capitalize">{datasetDetails.dataset_type}</p>
                    </div>
                    <div className="bg-blue-50 p-3 rounded-lg">
                      <p className="font-semibold text-blue-600">📄 CSV Files:</p>
                      <p className="text-gray-700">{datasetDetails.csv_files || 0}</p>
                    </div>
                    <div className="bg-blue-50 p-3 rounded-lg">
                      <p className="font-semibold text-blue-600">🖼️ Images:</p>
                      <p className="text-gray-700">{datasetDetails.images || 0}</p>
                    </div>
                    <div className="bg-blue-50 p-3 rounded-lg">
                      <p className="font-semibold text-blue-600">🌐 NC4 Files:</p>
                      <p className="text-gray-700">{datasetDetails.nc4_files || 0}</p>
                    </div>
                    <div className="bg-blue-50 p-3 rounded-lg">
                      <p className="font-semibold text-blue-600">📦 Size:</p>
                      <p className="text-gray-700">{datasetDetails.size_mb?.toFixed(2) || 'N/A'} MB</p>
                    </div>
                  </div>
                  {datasetDetails.nc4_variables && (
                    <div className="bg-blue-50 p-3 rounded-lg">
                      <p className="font-semibold text-blue-600 mb-2">🌐 NC4 Variables:</p>
                      <div className="flex flex-wrap gap-2">
                        {datasetDetails.nc4_variables.map((var_name, idx) => (
                          <span key={idx} className="bg-white px-2 py-1 rounded text-xs text-blue-600 border border-blue-200">{var_name}</span>
                        ))}
                      </div>
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}