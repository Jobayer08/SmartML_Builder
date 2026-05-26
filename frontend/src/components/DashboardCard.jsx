export default function DashboardCard({ title, value }) {
  return (
    <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl shadow-lg p-6 border border-blue-200 transition-all duration-300 hover:shadow-xl hover:scale-[1.02]">
      <h2 className="text-blue-600 text-sm font-semibold uppercase tracking-wide">
        {title}
      </h2>
      <p className="text-4xl font-extrabold text-blue-800 mt-3">
        {value}
      </p>
    </div>
  );
}