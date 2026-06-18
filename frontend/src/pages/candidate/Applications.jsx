import { useEffect, useState } from 'react';
import Layout from '../../components/Layout';
import Sidebar from '../../components/Sidebar';
import StatusBadge from '../../components/StatusBadge';
import MatchScore from '../../components/MatchScore';
import LoadingSpinner from '../../components/LoadingSpinner';
import { candidateService } from '../../services';

const links = [
  { path: '/candidate/dashboard', label: 'Dashboard', icon: '📊' },
  { path: '/candidate/profile', label: 'My Profile', icon: '👤' },
  { path: '/candidate/jobs', label: 'Search Jobs', icon: '🔍' },
  { path: '/candidate/applications', label: 'Applications', icon: '📋' },
];

export default function Applications() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    candidateService.getApplications()
      .then((res) => setApplications(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return (
    <Layout sidebar={<Sidebar links={links} />}>
      <h1 className="text-2xl font-bold mb-6">My Applications</h1>
      {loading ? <LoadingSpinner /> : applications.length === 0 ? (
        <div className="card text-center py-8 text-gray-500">No applications yet.</div>
      ) : (
        <div className="space-y-4">
          {applications.map((app) => (
            <div key={app.application_id} className="card">
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h3 className="font-semibold text-lg">{app.job_title}</h3>
                  <p className="text-sm text-gray-500">{app.company_name}</p>
                </div>
                <StatusBadge status={app.status} />
              </div>
              <MatchScore score={app.match_score} breakdown={app.match_breakdown} />
              <p className="text-xs text-gray-400 mt-2">
                Applied: {app.created_at ? new Date(app.created_at).toLocaleDateString() : 'N/A'}
              </p>
            </div>
          ))}
        </div>
      )}
    </Layout>
  );
}
