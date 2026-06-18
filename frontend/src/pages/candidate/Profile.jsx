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

export default function CandidateProfile() {
  const [profile, setProfile] = useState({
    headline: '', skills: '', education: '', experience: '', projects: '', phone: '', location: '',
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');
  const [resumeFile, setResumeFile] = useState(null);

  useEffect(() => {
    candidateService.getProfile()
      .then((res) => setProfile({
        headline: res.data.headline || '',
        skills: res.data.skills || '',
        education: res.data.education || '',
        experience: res.data.experience || '',
        projects: res.data.projects || '',
        phone: res.data.phone || '',
        location: res.data.location || '',
      }))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage('');
    try {
      await candidateService.updateProfile(profile);
      setMessage('Profile updated successfully!');
    } catch {
      await candidateService.createProfile(profile);
      setMessage('Profile created successfully!');
    } finally {
      setSaving(false);
    }
  };

  const handleResumeUpload = async () => {
    if (!resumeFile) return;
    setSaving(true);
    try {
      const res = await candidateService.uploadResume(resumeFile);
      setMessage(`Resume uploaded! Extracted skills: ${res.data.parsed_data?.skills?.join(', ') || 'None'}`);
      if (res.data.parsed_data?.skills?.length && !profile.skills) {
        setProfile({ ...profile, skills: res.data.parsed_data.skills.join(', ') });
      }
    } catch (err) {
      setMessage(err.response?.data?.detail || 'Upload failed');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <Layout sidebar={<Sidebar links={links} />}><LoadingSpinner /></Layout>;

  return (
    <Layout sidebar={<Sidebar links={links} />}>
      <h1 className="text-2xl font-bold mb-6">My Profile</h1>
      {message && <div className="bg-green-50 text-green-700 p-3 rounded-lg mb-4 text-sm">{message}</div>}

      <div className="grid lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 card">
          <form onSubmit={handleSave} className="space-y-4">
            {[
              { key: 'headline', label: 'Headline', type: 'text' },
              { key: 'phone', label: 'Phone', type: 'text' },
              { key: 'location', label: 'Location', type: 'text' },
              { key: 'skills', label: 'Skills (comma separated)', type: 'textarea' },
              { key: 'education', label: 'Education', type: 'textarea' },
              { key: 'experience', label: 'Experience', type: 'textarea' },
              { key: 'projects', label: 'Projects', type: 'textarea' },
            ].map((field) => (
              <div key={field.key}>
                <label className="block text-sm font-medium text-gray-700 mb-1">{field.label}</label>
                {field.type === 'textarea' ? (
                  <textarea
                    value={profile[field.key]}
                    onChange={(e) => setProfile({ ...profile, [field.key]: e.target.value })}
                    className="input-field"
                    rows={3}
                  />
                ) : (
                  <input
                    type="text"
                    value={profile[field.key]}
                    onChange={(e) => setProfile({ ...profile, [field.key]: e.target.value })}
                    className="input-field"
                  />
                )}
              </div>
            ))}
            <button type="submit" disabled={saving} className="btn-primary">
              {saving ? 'Saving...' : 'Save Profile'}
            </button>
          </form>
        </div>

        <div className="card h-fit">
          <h3 className="font-semibold mb-4">Upload Resume (PDF)</h3>
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setResumeFile(e.target.files[0])}
            className="mb-4 text-sm"
          />
          <button onClick={handleResumeUpload} disabled={!resumeFile || saving} className="btn-primary w-full">
            Upload & Parse Resume
          </button>
          <p className="text-xs text-gray-500 mt-2">Uses PyPDF2 to extract skills and keywords automatically.</p>
        </div>
      </div>
    </Layout>
  );
}
