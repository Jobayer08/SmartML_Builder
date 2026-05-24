import { useState } from 'react'
import API from '../api/api'

export default function PredictImage(){
  const [modelName, setModelName] = useState('')
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)

  const handlePredict = async () => {
    if(!file){ alert('Choose image'); return }
    const fd = new FormData()
    fd.append('file', file)
    fd.append('model_name', modelName)

    try{
      const res = await API.post('/predict-image/', fd)
      setResult(res.data)
    }catch(e){
      alert('Predict failed')
    }
  }

  return (
    <div className="p-6 max-w-lg mx-auto">
      <h1 className="text-3xl font-bold mb-5">Image Prediction</h1>
      <input className="border p-2 mb-3 w-full" placeholder="Model Name" onChange={(e)=>setModelName(e.target.value)} />
      <input type="file" onChange={(e)=>setFile(e.target.files[0])} className="mb-4" />
      <button onClick={handlePredict} className="bg-green-500 text-white px-4 py-2 rounded">Predict Image</button>

      {result && <pre className="mt-4 p-3 bg-white rounded">{JSON.stringify(result, null, 2)}</pre>}
    </div>
  )
}
