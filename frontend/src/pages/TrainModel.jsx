import { useState } from 'react'
import API from '../api/api'

export default function TrainModel(){
  const [file, setFile] = useState(null)
  const [target, setTarget] = useState('')
  const [modelName, setModelName] = useState('')
  const [result, setResult] = useState(null)

  const handleTrain = async ()=>{
    if(!file){ alert('Choose file'); return }
    const fd = new FormData()
    fd.append('file', file)
    fd.append('target_column', target)
    fd.append('model_name', modelName || 'my_model')

    try{
      const res = await API.post('/train-model/', fd)
      setResult(res.data)
    }catch(e){
      alert('Train failed')
    }
  }

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Train Model</h1>
      <input type="file" onChange={e=>setFile(e.target.files[0])} className="mb-3" />
      <input className="border p-2 mb-3 w-full" placeholder="Target column" value={target} onChange={e=>setTarget(e.target.value)} />
      <input className="border p-2 mb-3 w-full" placeholder="Model name" value={modelName} onChange={e=>setModelName(e.target.value)} />
      <button onClick={handleTrain} className="bg-blue-500 text-white px-4 py-2 rounded">Train</button>

      {result && <pre className="mt-4 p-3 bg-white rounded">{JSON.stringify(result, null, 2)}</pre>}
    </div>
  )
}
