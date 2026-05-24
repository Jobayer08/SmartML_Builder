import { useEffect, useState } from 'react'
import API from '../api/api'
import DatasetCard from '../components/DatasetCard'

export default function Datasets(){
  const [datasets, setDatasets] = useState([])
  const [file, setFile] = useState(null)

  useEffect(() => {
    fetchDatasets()
  }, [])

  const fetchDatasets = async () => {
    try {
      const res = await API.get('/my-datasets')
      setDatasets(res.data || [])
    } catch (e) {
      console.log('Error fetching datasets')
    }
  }

  const handleUpload = async () => {
    if (!file) return
    const fd = new FormData()
    fd.append('file', file)
    try {
      await API.post('/upload-dataset/', fd)
      setFile(null)
      fetchDatasets()
    } catch (e) {
      alert('Upload failed')
    }
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Datasets</h1>

      <div className="bg-white p-6 rounded shadow mb-6">
        <h2 className="font-bold mb-3">Upload New Dataset</h2>
        <input type="file" onChange={e => setFile(e.target.files[0])} className="mb-3" />
        <button onClick={handleUpload} className="bg-blue-500 text-white px-4 py-2 rounded">Upload</button>
      </div>

      <div className="grid grid-cols-3 gap-4">
        {datasets.map(ds => (
          <DatasetCard key={ds.id} dataset={ds} />
        ))}
      </div>
    </div>
  )
}
