import { useEffect, useState } from 'react';
import Layout from '../../components/Layout';
import Sidebar from '../../components/Sidebar';
import LoadingSpinner from '../../components/LoadingSpinner';
import { candidateService } from '../../services';

const links = [
  { path: '/candidate/dashboard', label: 'Dashboard', icon: '📊' },
  { path: '/candidate/profile', label: 'My Profile', icon: '👤' },
  { path: '/candidate/jobs', label: 'Search Jobs', icon: '🔍' },
  { path: '/candidate/applications', label: 'Applications', icon: '📋' },
];

export default function JobSearch() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState({ query: '', location: '', experience: '' });
  const [applying, setApplying] = useState(null);
  const [skillGap, setSkillGap] = useState(null);
  const [message, setMessage] = useState('');

  const fetchJobs = () => {
    setLoading(true);
    candidateService.searchJobs(search)
      .then((res) => setJobs(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchJobs(); }, []);

  const handleApply = async (jobId) => {
    setApplying(jobId);
    setMessage('');
    try {
      const res = await candidateService.applyJob({ job_id: jobId });
      setMessage(`Applied successfully! Match score: ${res.data.match_score}%`);
      fetchJobs();
    } catch (err) {
      setMessage(err.response?.data?.detail || 'Application failed');
    } finally {
      setApplying(null);
    }
  };

  const handleSkillGap = async (jobId) => {
    try {
      const res = await candidateService.getSkillGap(jobId);
      setSkillGap(res.data);
    } catch (err) {
      setMessage(err.response?.data?.detail || 'Failed to analyze');
    }
  };

  return (
    <Layout sidebar={<Sidebar links={links} />}>
      <h1 className="text-2xl font-bold mb-6">Search Jobs</h1>

      <div className="card mb-6">
        <div className="grid md:grid-cols-4 gap-4">
          <input placeholder="Job title or keyword" value={search.query} onChange={(e) => setSearch({ ...search, query: e.target.value })} className="input-field" />
          <input placeholder="Location" value={search.location} onChange={(e) => setSearch({ ...search, location: e.target.value })} className="input-field" />
          <input placeholder="Experience" value={search.experience} onChange={(e) => setSearch({ ...search, experience: e.target.value })} className="input-field" />
          <button onClick={fetchJobs} className="btn-primary">Search</button>
        </div>
      </div>

      {message && <div className="bg-blue-50 text-blue-700 p-3 rounded-lg mb-4 text-sm">{message}</div>}

      {loading ? <LoadingSpinner /> : (
        <div className="space-y-4">
          {jobs.length === 0 ? (
            <p className="text-gray-500 text-center py-8">No jobs found.</p>
          ) : jobs.map((job) => (
            <div key={job.job_id} className="card">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-lg font-semibold">{job.title}</h3>
                  <p className="text-sm text-gray-500">{job.company_name} · {job.location}</p>
                  <p className="text-sm text-gray-600 mt-2 line-clamp-2">{job.description}</p>
                  {job.required_skills && (
                    <p className="text-xs text-primary-600 mt-2">Skills: {job.required_skills}</p>
                  )}
                  <div className="flex gap-4 mt-2 text-xs text-gray-500">
                    {job.salary && <span>💰 {job.salary}</span>}
                    {job.experience && <span>📅 {job.experience}</span>}
                  </div>
                </div>
                <div className="flex flex-col gap-2 ml-4">
                  <button onClick={() => handleApply(job.job_id)} disabled={applying === job.job_id} className="btn-primary text-sm whitespace-nowrap">
                    {applying === job.job_id ? 'Applying...' : 'Apply Now'}
                  </button>
                  <button onClick={() => handleSkillGap(job.job_id)} className="btn-secondary text-sm whitespace-nowrap">
                    Skill Gap
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {skillGap && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" onClick={() => setSkillGap(null)}>
          <div className="card max-w-lg w-full" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-lg font-semibold mb-2">Skill Gap Analysis - {skillGap.job_title}</h3>
            <p className="text-2xl font-bold text-primary-600 mb-4">{skillGap.match_percentage}% Match</p>
            <div className="space-y-2 text-sm">
              <p><strong>Matched:</strong> {skillGap.matched_skills?.join(', ') || 'None'}</p>
              <p><strong>Missing:</strong> {skillGap.missing_skills?.join(', ') || 'None'}</p>
              <div className="mt-4">
                <strong>Recommendations:</strong>
                <ul className="list-disc ml-5 mt-1">
                  {skillGap.recommendations?.map((r, i) => <li key={i}>{r}</li>)}
                </ul>
              </div>
            </div>
            <button onClick={() => setSkillGap(null)} className="btn-secondary mt-4">Close</button>
          </div>
        </div>
      )}
    </Layout>
  );
}
