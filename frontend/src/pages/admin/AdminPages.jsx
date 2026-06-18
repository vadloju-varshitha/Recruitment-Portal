import { useEffect, useState } from 'react';
import Layout from '../../components/Layout';
import Sidebar from '../../components/Sidebar';
import StatusBadge from '../../components/StatusBadge';
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

export default function AdminUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    adminService.getUsers()
      .then((res) => setUsers(res.data))
      .finally(() => setLoading(false));
  }, []);

  const handleDelete = async (id) => {
    if (!confirm('Delete this user?')) return;
    await adminService.deleteUser(id);
    setUsers(users.filter((u) => u.id !== id));
  };

  return (
    <Layout sidebar={<Sidebar links={links} />}>
      <h1 className="text-2xl font-bold mb-6">Manage Users</h1>
      {loading ? <LoadingSpinner /> : (
        <div className="card overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b text-left text-gray-500">
                <th className="pb-3 pr-4">Name</th>
                <th className="pb-3 pr-4">Email</th>
                <th className="pb-3 pr-4">Role</th>
                <th className="pb-3">Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id} className="border-b last:border-0">
                  <td className="py-3 pr-4 font-medium">{u.name}</td>
                  <td className="py-3 pr-4">{u.email}</td>
                  <td className="py-3 pr-4 capitalize">{u.role}</td>
                  <td className="py-3">
                    <button onClick={() => handleDelete(u.id)} className="btn-danger text-xs">Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Layout>
  );
}

export function AdminCompanies() {
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    adminService.getCompanies().then((res) => setCompanies(res.data)).finally(() => setLoading(false));
  }, []);

  return (
    <Layout sidebar={<Sidebar links={links} />}>
      <h1 className="text-2xl font-bold mb-6">All Companies</h1>
      {loading ? <LoadingSpinner /> : (
        <div className="grid md:grid-cols-2 gap-4">
          {companies.map((c) => (
            <div key={c.company_id} className="card">
              <h3 className="font-semibold">{c.company_name}</h3>
              <p className="text-sm text-gray-500">{c.location} · {c.industry}</p>
              <p className="text-sm text-gray-600 mt-2">{c.description}</p>
            </div>
          ))}
        </div>
      )}
    </Layout>
  );
}

export function AdminJobs() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    adminService.getJobs().then((res) => setJobs(res.data)).finally(() => setLoading(false));
  }, []);

  const handleDelete = async (id) => {
    if (!confirm('Delete this job?')) return;
    await adminService.deleteJob(id);
    setJobs(jobs.filter((j) => j.job_id !== id));
  };

  return (
    <Layout sidebar={<Sidebar links={links} />}>
      <h1 className="text-2xl font-bold mb-6">All Jobs</h1>
      {loading ? <LoadingSpinner /> : (
        <div className="space-y-4">
          {jobs.map((j) => (
            <div key={j.job_id} className="card flex justify-between">
              <div>
                <h3 className="font-semibold">{j.title}</h3>
                <p className="text-sm text-gray-500">{j.company_name} · {j.location}</p>
              </div>
              <button onClick={() => handleDelete(j.job_id)} className="btn-danger text-sm">Delete</button>
            </div>
          ))}
        </div>
      )}
    </Layout>
  );
}

export function AdminApplications() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    adminService.getApplications().then((res) => setApplications(res.data)).finally(() => setLoading(false));
  }, []);

  return (
    <Layout sidebar={<Sidebar links={links} />}>
      <h1 className="text-2xl font-bold mb-6">All Applications</h1>
      {loading ? <LoadingSpinner /> : (
        <div className="card overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b text-left text-gray-500">
                <th className="pb-3 pr-4">Candidate</th>
                <th className="pb-3 pr-4">Job</th>
                <th className="pb-3 pr-4">Company</th>
                <th className="pb-3 pr-4">Status</th>
                <th className="pb-3">Match</th>
              </tr>
            </thead>
            <tbody>
              {applications.map((a) => (
                <tr key={a.application_id} className="border-b last:border-0">
                  <td className="py-3 pr-4">{a.candidate_name}</td>
                  <td className="py-3 pr-4">{a.job_title}</td>
                  <td className="py-3 pr-4">{a.company_name}</td>
                  <td className="py-3 pr-4"><StatusBadge status={a.status} /></td>
                  <td className="py-3">{a.match_score}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Layout>
  );
}

export function AdminReports() {
  const [report, setReport] = useState(null);
  const [type, setType] = useState('summary');
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    setLoading(true);
    try {
      const res = await adminService.getReports(type);
      setReport(res.data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout sidebar={<Sidebar links={links} />}>
      <h1 className="text-2xl font-bold mb-6">Reports</h1>
      <div className="card mb-6 flex gap-4 items-end">
        <div>
          <label className="block text-sm font-medium mb-1">Report Type</label>
          <select value={type} onChange={(e) => setType(e.target.value)} className="input-field">
            <option value="summary">Summary Report</option>
            <option value="hiring">Hiring Report</option>
          </select>
        </div>
        <button onClick={generate} disabled={loading} className="btn-primary">
          {loading ? 'Generating...' : 'Generate Report'}
        </button>
      </div>
      {report && (
        <div className="card">
          <pre className="text-sm overflow-x-auto whitespace-pre-wrap">{JSON.stringify(report, null, 2)}</pre>
        </div>
      )}
    </Layout>
  );
}
