import { useEffect, useState } from 'react'
import API from '../api/api'
import ModelCard from '../components/ModelCard'

export default function Models(){
  const [models, setModels] = useState([])

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const res = await API.get('/my-models')
        setModels(res.data || [])
      } catch (e) {
        console.log('Error fetching models')
      }
    }
    fetchModels()
  }, [])

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">My Models</h1>
      <div className="grid grid-cols-3 gap-4">
        {models.map(m => (
          <ModelCard key={m.id} model={m} />
        ))}
      </div>
    </div>
  )
}
