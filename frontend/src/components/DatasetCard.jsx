export default function DatasetCard({ dataset }) {
  return (
    <div className="bg-gradient-to-br from-blue-50/80 to-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 cursor-pointer border border-blue-100 hover:border-blue-300 hover:scale-[1.02] group">
      <div className="p-5">
        <h3 className="font-bold text-lg mb-2 text-blue-800 group-hover:text-blue-600 transition-colors">
          {dataset.dataset_name}
        </h3>
        <div className="text-sm space-y-1.5">
          <p className="text-gray-600">
            <span className="font-semibold text-blue-600">📊 Type:</span> {dataset.dataset_type || 'Unknown'}
          </p>
          <p className="text-gray-600">
            <span className="font-semibold text-blue-600">📅 Uploaded:</span> {new Date(dataset.created_at).toLocaleDateString()}
          </p>
          <p className="text-gray-600">
            <span className="font-semibold text-blue-600">💾 Size:</span> {dataset.file_size_mb ? `${dataset.file_size_mb.toFixed(2)} MB` : 'N/A'}
          </p>
        </div>
      </div>
    </div>
  );
}