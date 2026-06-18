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

export default function Interviews() {
  const [interviews, setInterviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    recruiterService.getInterviews()
      .then((res) => setInterviews(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return (
    <Layout sidebar={<Sidebar links={links} />}>
      <h1 className="text-2xl font-bold mb-6">Scheduled Interviews</h1>
      {loading ? <LoadingSpinner /> : interviews.length === 0 ? (
        <div className="card text-center py-8 text-gray-500">No interviews scheduled.</div>
      ) : (
        <div className="space-y-4">
          {interviews.map((iv) => (
            <div key={iv.interview_id} className="card">
              <h3 className="font-semibold">{iv.candidate_name}</h3>
              <p className="text-sm text-gray-500">{iv.job_title}</p>
              <div className="flex gap-4 mt-2 text-sm">
                <span>📅 {iv.date}</span>
                <span>🕐 {iv.time}</span>
              </div>
              {iv.meeting_link && (
                <a href={iv.meeting_link} target="_blank" rel="noreferrer" className="text-primary-600 text-sm hover:underline mt-2 inline-block">
                  Join Meeting
                </a>
              )}
              {iv.notes && <p className="text-xs text-gray-400 mt-2">{iv.notes}</p>}
            </div>
          ))}
        </div>
      )}
    </Layout>
  );
}
