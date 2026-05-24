export default function PredictionCard({ prediction }){
  return (
    <div className="bg-white p-4 rounded shadow hover:shadow-lg transition">
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-bold text-lg">{prediction.model_name}</h3>
        <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">
          {new Date(prediction.created_at).toLocaleTimeString()}
        </span>
      </div>
      <div className="text-sm text-gray-600 space-y-1">
        <p><strong>Prediction:</strong> {JSON.stringify(prediction.prediction)}</p>
        {prediction.confidence && (
          <p><strong>Confidence:</strong> {(prediction.confidence * 100).toFixed(2)}%</p>
        )}
      </div>
    </div>
  )
}
