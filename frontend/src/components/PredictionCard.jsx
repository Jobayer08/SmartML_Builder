export default function PredictionCard({ prediction }) {
  return (
    <div className="bg-gradient-to-br from-blue-50/80 to-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 border border-blue-100 hover:border-blue-300 hover:scale-[1.02] group">
      <div className="p-5">
        <div className="flex justify-between items-start mb-3">
          <h3 className="font-bold text-lg text-blue-800 group-hover:text-blue-600 transition-colors">
            🤖 {prediction.model_name}
          </h3>
          <span className="text-xs bg-gradient-to-r from-blue-100 to-blue-200 text-blue-700 px-3 py-1 rounded-full font-medium shadow-sm">
            🕐 {new Date(prediction.created_at).toLocaleTimeString()}
          </span>
        </div>
        <div className="text-sm space-y-2">
          <div className="bg-blue-50/50 rounded-lg p-3 border border-blue-100">
            <p className="text-gray-600">
              <span className="font-semibold text-blue-600">🎯 Prediction:</span>{' '}
              <span className="font-mono font-medium text-blue-800">
                {JSON.stringify(prediction.prediction)}
              </span>
            </p>
          </div>
          {prediction.confidence && (
            <div className="flex items-center justify-between bg-white/50 rounded-lg p-2 px-3">
              <span className="font-semibold text-blue-600">📊 Confidence:</span>
              <div className="flex items-center gap-2">
                <div className="w-24 h-2 bg-blue-100 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-gradient-to-r from-blue-500 to-blue-600 rounded-full transition-all duration-500"
                    style={{ width: `${(prediction.confidence * 100).toFixed(2)}%` }}
                  ></div>
                </div>
                <span className="font-bold text-blue-700 text-sm">
                  {(prediction.confidence * 100).toFixed(2)}%
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}