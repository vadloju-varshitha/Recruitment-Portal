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

export default function CompanyProfile() {
  const [form, setForm] = useState({ company_name: '', description: '', location: '', website: '', industry: '' });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [isNew, setIsNew] = useState(true);
  const [message, setMessage] = useState('');

  useEffect(() => {
    recruiterService.getCompany()
      .then((res) => {
        setForm(res.data);
        setIsNew(false);
      })
      .catch(() => setIsNew(true))
      .finally(() => setLoading(false));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage('');
    try {
      if (isNew) {
        await recruiterService.registerCompany(form);
        setMessage('Company registered successfully!');
        setIsNew(false);
      } else {
        await recruiterService.updateCompany(form);
        setMessage('Company updated successfully!');
      }
    } catch (err) {
      setMessage(err.response?.data?.detail || 'Failed to save');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <Layout sidebar={<Sidebar links={links} />}><LoadingSpinner /></Layout>;

  return (
    <Layout sidebar={<Sidebar links={links} />}>
      <h1 className="text-2xl font-bold mb-6">{isNew ? 'Register Company' : 'Company Profile'}</h1>
      {message && <div className="bg-green-50 text-green-700 p-3 rounded-lg mb-4 text-sm">{message}</div>}
      <div className="card max-w-2xl">
        <form onSubmit={handleSubmit} className="space-y-4">
          {[
            { key: 'company_name', label: 'Company Name' },
            { key: 'location', label: 'Location' },
            { key: 'website', label: 'Website' },
            { key: 'industry', label: 'Industry' },
          ].map((f) => (
            <div key={f.key}>
              <label className="block text-sm font-medium text-gray-700 mb-1">{f.label}</label>
              <input type="text" value={form[f.key] || ''} onChange={(e) => setForm({ ...form, [f.key]: e.target.value })} className="input-field" required={f.key === 'company_name'} />
            </div>
          ))}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea value={form.description || ''} onChange={(e) => setForm({ ...form, description: e.target.value })} className="input-field" rows={4} />
          </div>
          <button type="submit" disabled={saving} className="btn-primary">
            {saving ? 'Saving...' : isNew ? 'Register Company' : 'Update Company'}
          </button>
        </form>
      </div>
    </Layout>
  );
}
