import { useEffect, useState } from 'react';
import Layout from '../../components/Layout';
import Sidebar from '../../components/Sidebar';
import LoadingSpinner from '../../components/LoadingSpinner';
import { recruiterService } from '../../services';

const links = [
  { path: '/recruiter/dashboard', label: 'Dashboard', icon: '📊' },
  { path: '/recruiter/company', label: 'Company', icon: '🏢' },
  { path: '/recruiter/jobs', label: 'Jobs', icon: '💼' },
  { path: '/recruiter/applicants', label: 'Applicants', icon: '👥' },
  { path: '/recruiter/interviews', label: 'Interviews', icon: '📅' },
];

export default function JobManagement() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editId, setEditId] = useState(null);
  const [form, setForm] = useState({
    title: '', description: '', requirements: '', required_skills: '', salary: '', experience: '', location: '',
  });
  const [message, setMessage] = useState('');

  const fetchJobs = () => {
    recruiterService.getJobs()
      .then((res) => setJobs(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchJobs(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editId) {
        await recruiterService.updateJob(editId, form);
        setMessage('Job updated!');
      } else {
        await recruiterService.createJob(form);
        setMessage('Job posted!');
      }
      setShowForm(false);
      setEditId(null);
      setForm({ title: '', description: '', requirements: '', required_skills: '', salary: '', experience: '', location: '' });
      fetchJobs();
    } catch (err) {
      setMessage(err.response?.data?.detail || 'Failed');
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Delete this job?')) return;
    await recruiterService.deleteJob(id);
    fetchJobs();
  };

  const handleEdit = (job) => {
    setForm({
      title: job.title, description: job.description, requirements: job.requirements || '',
      required_skills: job.required_skills || '', salary: job.salary || '',
      experience: job.experience || '', location: job.location || '',
    });
    setEditId(job.job_id);
    setShowForm(true);
  };

  return (
    <Layout sidebar={<Sidebar links={links} />}>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Job Management</h1>
        <button onClick={() => { setShowForm(true); setEditId(null); }} className="btn-primary">Post New Job</button>
      </div>
      {message && <div className="bg-green-50 text-green-700 p-3 rounded-lg mb-4 text-sm">{message}</div>}

      {showForm && (
        <div className="card mb-6">
          <h3 className="font-semibold mb-4">{editId ? 'Edit Job' : 'New Job Posting'}</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid md:grid-cols-2 gap-4">
              <input placeholder="Job Title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} className="input-field" required />
              <input placeholder="Location" value={form.location} onChange={(e) => setForm({ ...form, location: e.target.value })} className="input-field" />
              <input placeholder="Salary" value={form.salary} onChange={(e) => setForm({ ...form, salary: e.target.value })} className="input-field" />
              <input placeholder="Experience Required" value={form.experience} onChange={(e) => setForm({ ...form, experience: e.target.value })} className="input-field" />
            </div>
            <input placeholder="Required Skills (comma separated: Python, SQL, ML)" value={form.required_skills} onChange={(e) => setForm({ ...form, required_skills: e.target.value })} className="input-field" />
            <textarea placeholder="Description" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} className="input-field" rows={3} required />
            <textarea placeholder="Requirements" value={form.requirements} onChange={(e) => setForm({ ...form, requirements: e.target.value })} className="input-field" rows={2} />
            <div className="flex gap-2">
              <button type="submit" className="btn-primary">{editId ? 'Update' : 'Post Job'}</button>
              <button type="button" onClick={() => setShowForm(false)} className="btn-secondary">Cancel</button>
            </div>
          </form>
        </div>
      )}

      {loading ? <LoadingSpinner /> : (
        <div className="space-y-4">
          {jobs.map((job) => (
            <div key={job.job_id} className="card flex justify-between items-start">
              <div>
                <h3 className="font-semibold">{job.title}</h3>
                <p className="text-sm text-gray-500">{job.location} · {job.salary}</p>
                <p className="text-xs text-primary-600 mt-1">Skills: {job.required_skills}</p>
                <span className={`badge mt-2 ${job.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                  {job.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
              <div className="flex gap-2">
                <button onClick={() => handleEdit(job)} className="btn-secondary text-sm">Edit</button>
                <button onClick={() => handleDelete(job.job_id)} className="btn-danger text-sm">Delete</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </Layout>
  );
}
