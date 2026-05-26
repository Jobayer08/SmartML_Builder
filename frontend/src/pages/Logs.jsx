import { useEffect, useState } from 'react'
import API from '../api/api'

export default function Logs(){
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const res = await API.get('/api-usage')
        setLogs(Array.isArray(res.data) ? res.data : [])
      } catch (e) {
        setError('Failed to load logs')
        console.error(e)
      }
      setLoading(false)
    }

    fetchLogs()
  }, [])

  return(
    <div className="ml-64 p-8 pt-24 min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-extrabold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
          📋 Activity Logs
        </h1>
        <p className="text-blue-500 mt-2">Track API requests and prediction activity</p>
      </div>

      {/* Main Card */}
      <div className="bg-gradient-to-br from-white to-blue-50/50 rounded-xl shadow-md border border-blue-200 overflow-hidden">
        <div className="bg-gradient-to-r from-blue-500 to-blue-600 px-6 py-4">
          <p className="text-white font-medium flex items-center gap-2">
            📊 API Request History
            <span className="ml-auto text-sm bg-white/20 px-2 py-1 rounded">
              {logs.length} {logs.length === 1 ? 'request' : 'requests'}
            </span>
          </p>
        </div>
        
        <div className="p-6">
          <p className="text-blue-600 mb-4 flex items-center gap-2">
            🔍 API requests and prediction activity for your account appear below
          </p>

          {loading && (
            <div className="flex items-center justify-center py-12">
              <div className="text-center">
                <div className="w-10 h-10 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-3"></div>
                <p className="text-blue-600 text-sm">Loading activity logs...</p>
              </div>
            </div>
          )}

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-600 text-sm flex items-center gap-2">
                ❌ {error}
              </p>
            </div>
          )}

          {!loading && !error && logs.length === 0 && (
            <div className="mb-4 p-6 bg-blue-50 border border-blue-200 rounded-lg text-center">
              <div className="text-4xl mb-3">📭</div>
              <p className="text-blue-600 font-medium">No logs found yet</p>
              <p className="text-blue-400 text-sm mt-1">
                Perform a prediction or other action to generate activity
              </p>
            </div>
          )}

          {!loading && logs.length > 0 && (
            <div className="mt-4 overflow-x-auto">
              <table className="min-w-full text-left text-sm">
                <thead>
                  <tr className="border-b-2 border-blue-200 bg-blue-50/50">
                    <th className="py-3 px-4 font-semibold text-blue-800 rounded-tl-lg">
                      🕐 Time
                    </th>
                    <th className="py-3 px-4 font-semibold text-blue-800">
                      🔗 Endpoint
                    </th>
                    <th className="py-3 px-4 font-semibold text-blue-800">
                      📡 Method
                    </th>
                    <th className="py-3 px-4 font-semibold text-blue-800 rounded-tr-lg">
                      👤 User ID
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {logs.map((log, index) => (
                    <tr 
                      key={log.id || `${log.endpoint}-${log.created_at}`} 
                      className={`border-b border-blue-100 hover:bg-blue-50/50 transition-colors duration-150 ${
                        index % 2 === 0 ? 'bg-white' : 'bg-blue-50/30'
                      }`}
                    >
                      <td className="py-3 px-4 text-gray-700 font-mono text-xs">
                        {log.created_at || 'N/A'}
                      </td>
                      <td className="py-3 px-4">
                        <span className="text-blue-700 font-medium">
                          {log.endpoint || 'N/A'}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-semibold ${
                          log.method === 'GET' ? 'bg-green-100 text-green-700' :
                          log.method === 'POST' ? 'bg-blue-100 text-blue-700' :
                          log.method === 'PUT' ? 'bg-yellow-100 text-yellow-700' :
                          log.method === 'DELETE' ? 'bg-red-100 text-red-700' :
                          'bg-gray-100 text-gray-700'
                        }`}>
                          {log.method || 'N/A'}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-gray-600 font-mono text-xs">
                        {log.user_id ?? 'N/A'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              
              {/* Optional: Export Button */}
              <div className="mt-6 pt-4 border-t border-blue-200 flex justify-end">
                <button 
                  onClick={() => {
                    const csv = logs.map(log => `${log.created_at},${log.endpoint},${log.method},${log.user_id}`).join('\n')
                    const blob = new Blob([`Time,Endpoint,Method,User ID\n${csv}`], { type: 'text/csv' })
                    const url = URL.createObjectURL(blob)
                    const a = document.createElement('a')
                    a.href = url
                    a.download = `logs-${new Date().toISOString().slice(0,19)}.csv`
                    a.click()
                    URL.revokeObjectURL(url)
                  }}
                  className="text-sm bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-all duration-200 shadow-sm hover:shadow flex items-center gap-2"
                >
                  📥 Export CSV
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
      
      {/* Optional: Filter Section */}
      {!loading && logs.length > 0 && (
        <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-gradient-to-br from-blue-50/80 to-white rounded-lg border border-blue-200 p-4">
            <p className="text-blue-600 text-sm font-semibold mb-1">Total Requests</p>
            <p className="text-2xl font-bold text-blue-800">{logs.length}</p>
          </div>
          <div className="bg-gradient-to-br from-blue-50/80 to-white rounded-lg border border-blue-200 p-4">
            <p className="text-blue-600 text-sm font-semibold mb-1">GET Requests</p>
            <p className="text-2xl font-bold text-blue-800">
              {logs.filter(l => l.method === 'GET').length}
            </p>
          </div>
          <div className="bg-gradient-to-br from-blue-50/80 to-white rounded-lg border border-blue-200 p-4">
            <p className="text-blue-600 text-sm font-semibold mb-1">POST Requests</p>
            <p className="text-2xl font-bold text-blue-800">
              {logs.filter(l => l.method === 'POST').length}
            </p>
          </div>
        </div>
      )}
    </div>
  )
}