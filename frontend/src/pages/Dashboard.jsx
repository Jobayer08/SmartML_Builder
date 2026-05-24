import { useEffect, useState } from 'react'
import API from '../api/api'

export default function Dashboard(){
  const [stats, setStats] = useState({})
  const [datasets, setDatasets] = useState([])

  useEffect(()=>{
    const fetchData = async ()=>{
      try{
        const a = await API.get('/dashboard-stats')
        const d = await API.get('/my-datasets')
        setStats(a.data)
        setDatasets(d.data)
      }catch(e){
        // ignore
      }
    }
    fetchData()
  },[])

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>

      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="p-5 shadow rounded bg-white">
          <h3>Total Models</h3>
          <p className="text-2xl">{stats.total_models ?? '-'}</p>
        </div>
        <div className="p-5 shadow rounded bg-white">
          <h3>Total Predictions</h3>
          <p className="text-2xl">{stats.total_predictions ?? '-'}</p>
        </div>
        <div className="p-5 shadow rounded bg-white">
          <h3>Datasets</h3>
          <p className="text-2xl">{datasets.length}</p>
        </div>
      </div>

      <div className="bg-white p-4 rounded shadow">
        <h2 className="font-bold mb-3">Uploaded Datasets</h2>
        <ul>
          {datasets.map(ds=> (
            <li key={ds.id} className="border-b py-2">{ds.dataset_name} — {ds.dataset_type}</li>
          ))}
        </ul>
      </div>
    </div>
  )
}
