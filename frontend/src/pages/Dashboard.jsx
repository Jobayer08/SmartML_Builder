import DashboardCard from '../components/DashboardCard'

export default function Dashboard(){
  return(
    <div className="ml-64 p-8 pt-24">
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>
      <div className="grid grid-cols-4 gap-6">
        <DashboardCard title="Total Models" value="12" />
        <DashboardCard title="Predictions" value="1,543" />
        <DashboardCard title="Datasets" value="23" />
        <DashboardCard title="API Usage" value="4,300" />
      </div>
    </div>
  )
}
