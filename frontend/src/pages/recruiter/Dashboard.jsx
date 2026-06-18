import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import Layout from '../../components/Layout';
import Sidebar from '../../components/Sidebar';
import StatCard from '../../components/StatCard';
import LoadingSpinner from '../../components/LoadingSpinner';
import { recruiterService } from '../../services';

const links = [
  { path: '/recruiter/dashboard', label: 'Dashboard', icon: '📊' },
  { path: '/recruiter/company', label: 'Company', icon: '🏢' },
  { path: '/recruiter/jobs', label: 'Jobs', icon: '💼' },
  { path: '/recruiter/applicants', label: 'Applicants', icon: '👥' },
  { path: '/recruiter/interviews', label: 'Interviews', icon: '📅' },
];

const COLORS = ['#3b82f6', '#10b981', '#ef4444', '#f59e0b', '#8b5cf6', '#6366f1'];

export default function RecruiterDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    recruiterService.getAnalytics()
      .then((res) => setData(res.data))
      .catch((err) => setError(err.response?.data?.detail || 'Register your company first'))
      .finally(() => setLoading(false));
  }, []);

  const chartData = data ? Object.entries(data.applications_by_status || {}).map(([name, value]) => ({ name, value })) : [];

  return (
    <Layout sidebar={<Sidebar links={links} />}>
      <h1 className="text-2xl font-bold mb-6">Recruiter Dashboard</h1>
      {error && <div className="bg-yellow-50 text-yellow-700 p-3 rounded-lg mb-4">{error}</div>}
      {loading ? <LoadingSpinner /> : data && (
        <>
          <div className="grid md:grid-cols-4 gap-4 mb-8">
            <StatCard title="Total Jobs" value={data.total_jobs} color="primary" />
            <StatCard title="Active Jobs" value={data.active_jobs} color="green" />
            <StatCard title="Applications" value={data.total_applications} color="purple" />
            <StatCard title="Hiring Rate" value={`${data.hiring_rate}%`} color="yellow" />
          </div>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="card">
              <h3 className="font-semibold mb-4">Applications by Status</h3>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" fill="#3b82f6" />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div className="card">
              <h3 className="font-semibold mb-4">Status Distribution</h3>
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie data={chartData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
                    {chartData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </>
      )}
    </Layout>
  );
}
