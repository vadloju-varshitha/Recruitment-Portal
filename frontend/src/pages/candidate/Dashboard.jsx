import { useEffect, useState } from 'react';
import Layout from '../../components/Layout';
import Sidebar from '../../components/Sidebar';
import StatCard from '../../components/StatCard';
import StatusBadge from '../../components/StatusBadge';
import LoadingSpinner from '../../components/LoadingSpinner';
import { candidateService } from '../../services';

const links = [
  { path: '/candidate/dashboard', label: 'Dashboard', icon: '📊' },
  { path: '/candidate/profile', label: 'My Profile', icon: '👤' },
  { path: '/candidate/jobs', label: 'Search Jobs', icon: '🔍' },
  { path: '/candidate/applications', label: 'Applications', icon: '📋' },
];

export default function CandidateDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    candidateService.getDashboard()
      .then((res) => setData(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Layout sidebar={<Sidebar links={links} />}><LoadingSpinner /></Layout>;

  return (
    <Layout sidebar={<Sidebar links={links} />}>
      <h1 className="text-2xl font-bold mb-6">Candidate Dashboard</h1>
      <div className="grid md:grid-cols-3 gap-4 mb-8">
        <StatCard title="Total Applications" value={data?.total_applications || 0} color="primary" />
        <StatCard title="Shortlisted" value={data?.status_breakdown?.shortlisted || 0} color="green" />
        <StatCard title="Interviews" value={data?.status_breakdown?.interview || 0} color="purple" />
      </div>

      <div className="card">
        <h2 className="text-lg font-semibold mb-4">Recent Applications</h2>
        {data?.recent_applications?.length === 0 ? (
          <p className="text-gray-500">No applications yet. Start searching for jobs!</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-left text-gray-500">
                  <th className="pb-3 pr-4">Job</th>
                  <th className="pb-3 pr-4">Company</th>
                  <th className="pb-3 pr-4">Status</th>
                  <th className="pb-3">Match</th>
                </tr>
              </thead>
              <tbody>
                {data?.recent_applications?.map((app) => (
                  <tr key={app.application_id} className="border-b last:border-0">
                    <td className="py-3 pr-4 font-medium">{app.job_title}</td>
                    <td className="py-3 pr-4">{app.company_name}</td>
                    <td className="py-3 pr-4"><StatusBadge status={app.status} /></td>
                    <td className="py-3">{app.match_score}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </Layout>
  );
}
