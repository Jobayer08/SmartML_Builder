import { useEffect, useState } from 'react'
import DashboardCard from '../components/DashboardCard'
import API from '../api/api'

export default function Dashboard(){
  const [stats, setStats] = useState({ total_models: 0, total_predictions: 0, total_datasets: 0 })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const token = localStorage.getItem('token')
        const datasetsRes = await API.get(`/my-datasets?token=${token}`)
        const modelsRes = await API.get(`/my-models?token=${token}`)
        const predictionsRes = await API.get(`/my-predictions?token=${token}`)
        
        setStats({
          total_models: modelsRes.data?.total_models || modelsRes.data?.length || 0,
          total_predictions: predictionsRes.data?.length || 0,
          total_datasets: datasetsRes.data?.length || 0
        })
      } catch (e) {
        console.error('Error fetching stats:', e)
      }
      setLoading(false)
    }
    fetchStats()
  }, [])

  return(
    <div className="ml-64 p-8 pt-24 min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-extrabold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
          📊 Dashboard
        </h1>
        <p className="text-blue-500 mt-2">Welcome back! Here's an overview of your ML workspace</p>
      </div>
      
      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-blue-600 font-medium">Loading your stats...</p>
          </div>
        </div>
      ) : (
        <>
          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <DashboardCard title="Total Models" value={stats.total_models} />
            <DashboardCard title="Predictions" value={stats.total_predictions} />
            <DashboardCard title="Datasets" value={stats.total_datasets} />
            <DashboardCard title="API Usage" value="—" />
          </div>
          
          {/* Optional: Recent Activity Section */}
          <div className="mt-12">
            <h2 className="text-2xl font-bold text-blue-800 mb-4">📈 Recent Activity</h2>
            <div className="bg-white/50 backdrop-blur-sm rounded-xl border border-blue-200 p-6">
              <p className="text-blue-600 text-center">
                Track your model performance and predictions here
              </p>
              {/* You can add recent predictions or models list here */}
            </div>
          </div>
        </>
      )}
    </div>
  )
}