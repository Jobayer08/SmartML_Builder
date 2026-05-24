export default function ModelCard({ model, onPredict, onDelete }){
  return (
    <div className="bg-white p-4 rounded shadow hover:shadow-lg transition">
      <h3 className="font-bold text-lg mb-2">{model.model_name}</h3>
      <div className="text-sm text-gray-600 space-y-1">
        <p><strong>Type:</strong> {model.model_type || 'Unknown'}</p>
        <p><strong>Accuracy:</strong> {model.accuracy ? parseFloat(model.accuracy).toFixed(4) : 'N/A'}</p>
        <p><strong>Created:</strong> {new Date(model.created_at).toLocaleDateString()}</p>
      </div>
      <div className="flex gap-2 mt-3">
        {onPredict && (
          <button 
            onClick={() => onPredict(model.model_name)}
            className="flex-1 bg-blue-500 text-white text-sm px-3 py-1 rounded hover:bg-blue-600"
          >
            Predict
          </button>
        )}
        {onDelete && (
          <button 
            onClick={() => onDelete(model.id)}
            className="text-red-600 text-sm hover:text-red-800 font-bold"
          >
            Delete
          </button>
        )}
      </div>
    </div>
  )
}
