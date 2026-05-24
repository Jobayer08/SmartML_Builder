import { useState } from 'react'
import API from '../api/api'

export default function PredictCSV(){
  const [modelName, setModelName] = useState('')
  const [formData, setFormData] = useState({})
  const [prediction, setPrediction] = useState(null)

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handlePredict = async () => {
    try{
      const res = await API.post('/predict-csv/', { model_name: modelName, data: formData })
      setPrediction(res.data)
    }catch(e){
      alert('Prediction failed')
    }
  }

  return (
    <div className="p-6 max-w-lg mx-auto">
      <h1 className="text-3xl font-bold mb-5">CSV Prediction</h1>
      <input className="border p-2 mb-3 w-full" placeholder="Model Name" onChange={(e)=>setModelName(e.target.value)} />
      <input className="border p-2 mb-3 w-full" name="feature_num" placeholder="feature_num" onChange={handleChange} />
      <input className="border p-2 mb-3 w-full" name="feature_cat" placeholder="feature_cat" onChange={handleChange} />
      <button onClick={handlePredict} className="bg-blue-500 text-white px-4 py-2 rounded">Predict</button>

      {prediction && (
        <div className="mt-5 p-4 border rounded bg-white">
          <h2 className="font-bold">Prediction Result</h2>
          <pre>{JSON.stringify(prediction, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}
