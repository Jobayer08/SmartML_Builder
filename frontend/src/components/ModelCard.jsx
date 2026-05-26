export default function ModelCard({ model, onPredict, onDelete }) {
  return (
    <div className="bg-gradient-to-br from-blue-50/80 to-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 border border-blue-100 hover:border-blue-300 hover:scale-[1.02] group">
      <div className="p-5">
        <h3 className="font-bold text-lg mb-2 text-blue-800 group-hover:text-blue-600 transition-colors">
          {model.model_name}
        </h3>
        <div className="text-sm space-y-1.5">
          <p className="text-gray-600">
            <span className="font-semibold text-blue-600">🧠 Type:</span> {model.model_type || 'Unknown'}
          </p>
          <p className="text-gray-600">
            <span className="font-semibold text-blue-600">📈 Accuracy:</span>{' '}
            <span className="font-mono font-medium text-blue-700">
              {model.accuracy ? parseFloat(model.accuracy).toFixed(4) : 'N/A'}
            </span>
          </p>
          <p className="text-gray-600">
            <span className="font-semibold text-blue-600">⏱️ Created:</span> {new Date(model.created_at).toLocaleDateString()}
          </p>
        </div>
        <div className="flex gap-3 mt-4">
          {onPredict && (
            <button 
              onClick={() => onPredict(model.model_name)}
              className="flex-1 bg-gradient-to-r from-blue-500 to-blue-600 text-white text-sm px-4 py-2 rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all duration-200 shadow-sm hover:shadow font-medium"
            >
              🔮 Predict
            </button>
          )}
          {onDelete && (
            <button 
              onClick={() => onDelete(model.id)}
              className="text-red-500 hover:text-red-700 font-semibold text-sm px-3 py-2 rounded-lg hover:bg-red-50 transition-all duration-200"
            >
              🗑️ Delete
            </button>
          )}
        </div>
      </div>
    </div>
  );
}