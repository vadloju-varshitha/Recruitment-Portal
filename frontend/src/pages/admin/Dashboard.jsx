import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';
import Layout from '../../components/Layout';
import Sidebar from '../../components/Sidebar';
import StatCard from '../../components/StatCard';
import LoadingSpinner from '../../components/LoadingSpinner';
import { adminService } from '../../services';

const links = [
  { path: '/admin/dashboard', label: 'Dashboard', icon: '📊' },
  { path: '/admin/users', label: 'Users', icon: '👤' },
  { path: '/admin/companies', label: 'Companies', icon: '🏢' },
  { path: '/admin/jobs', label: 'Jobs', icon: '💼' },
  { path: '/admin/applications', label: 'Applications', icon: '📋' },
  { path: '/admin/reports', label: 'Reports', icon: '📄' },
];

export default function AdminDashboard() {
  const [analytics, setAnalytics] = useState(null);
  const [timeToHire, setTimeToHire] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([adminService.getAnalytics(), adminService.getTimeToHire()])
      .then(([a, t]) => { setAnalytics(a.data); setTimeToHire(t.data); })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const statusData = analytics ? [
    { name: 'Shortlisted', value: analytics.shortlisted_candidates },
    { name: 'Rejected', value: analytics.rejected_candidates },
    { name: 'Hired', value: analytics.hired_candidates },
  ] : [];

  return (
    <Layout sidebar={<Sidebar links={links} />}>
      <h1 className="text-2xl font-bold mb-6">Admin Dashboard</h1>
      {loading ? <LoadingSpinner /> : analytics && (
        <>
          <div className="grid md:grid-cols-4 gap-4 mb-8">
            <StatCard title="Total Jobs" value={analytics.total_jobs} color="primary" />
            <StatCard title="Total Candidates" value={analytics.total_candidates} color="green" />
            <StatCard title="Total Applications" value={analytics.total_applications} color="purple" />
            <StatCard title="Hiring Rate" value={`${analytics.hiring_rate}%`} color="yellow" />
          </div>
          <div className="grid md:grid-cols-3 gap-4 mb-8">
            <StatCard title="Companies" value={analytics.total_companies} />
            <StatCard title="Recruiters" value={analytics.total_recruiters} />
            <StatCard title="Shortlisted" value={analytics.shortlisted_candidates} color="green" />
          </div>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="card">
              <h3 className="font-semibold mb-4">Candidate Pipeline</h3>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={statusData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" fill="#3b82f6" />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div className="card">
              <h3 className="font-semibold mb-4">Time to Hire</h3>
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={timeToHire}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="avg_days" stroke="#3b82f6" name="Avg Days" />
                  <Line type="monotone" dataKey="hires" stroke="#10b981" name="Hires" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </>
      )}
    </Layout>
  );
}
