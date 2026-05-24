export default function DatasetCard({ dataset, onDelete }){
  return (
    <div className="bg-white p-4 rounded shadow hover:shadow-lg transition">
      <h3 className="font-bold text-lg mb-2">{dataset.dataset_name}</h3>
      <div className="text-sm text-gray-600 space-y-1">
        <p><strong>Type:</strong> {dataset.file_type}</p>
        <p><strong>Uploaded:</strong> {new Date(dataset.created_at).toLocaleDateString()}</p>
        <p><strong>Size:</strong> {(dataset.file_size / 1024).toFixed(2)} KB</p>
      </div>
      {onDelete && (
        <button 
          onClick={() => onDelete(dataset.id)}
          className="mt-3 text-red-600 text-sm hover:text-red-800 font-bold"
        >
          Delete
        </button>
      )}
    </div>
  )
}
