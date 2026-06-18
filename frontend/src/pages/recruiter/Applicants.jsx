import { useEffect, useState } from 'react';
import Layout from '../../components/Layout';
import Sidebar from '../../components/Sidebar';
import StatusBadge from '../../components/StatusBadge';
import MatchScore from '../../components/MatchScore';
import LoadingSpinner from '../../components/LoadingSpinner';
import { recruiterService, pdfService, downloadBlob } from '../../services';

const links = [
  { path: '/recruiter/dashboard', label: 'Dashboard', icon: '📊' },
  { path: '/recruiter/company', label: 'Company', icon: '🏢' },
  { path: '/recruiter/jobs', label: 'Jobs', icon: '💼' },
  { path: '/recruiter/applicants', label: 'Applicants', icon: '👥' },
  { path: '/recruiter/interviews', label: 'Interviews', icon: '📅' },
];

export default function Applicants() {
  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState('');
  const [applicants, setApplicants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [questions, setQuestions] = useState(null);
  const [showInterview, setShowInterview] = useState(null);
  const [interviewForm, setInterviewForm] = useState({ date: '', time: '', meeting_link: '', notes: '' });
  const [showOffer, setShowOffer] = useState(null);
  const [offerForm, setOfferForm] = useState({ salary: '', start_date: '', position: '', template: 'standard' });

  useEffect(() => {
    recruiterService.getJobs()
      .then((res) => {
        setJobs(res.data);
        if (res.data.length > 0) setSelectedJob(res.data[0].job_id);
      })
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (!selectedJob) return;
    recruiterService.getApplicants(selectedJob)
      .then((res) => setApplicants(res.data))
      .catch(console.error);
  }, [selectedJob]);

  const updateStatus = async (appId, status) => {
    await recruiterService.updateApplicationStatus(appId, status);
    const res = await recruiterService.getApplicants(selectedJob);
    setApplicants(res.data);
  };

  const getQuestions = async (candidateId) => {
    const res = await recruiterService.getInterviewQuestions({ job_id: Number(selectedJob), candidate_id: candidateId });
    setQuestions(res.data);
  };

  const scheduleInterview = async () => {
    await recruiterService.scheduleInterview({
      candidate_id: showInterview.candidate_id,
      job_id: Number(selectedJob),
      ...interviewForm,
    });
    setShowInterview(null);
    setInterviewForm({ date: '', time: '', meeting_link: '', notes: '' });
    const res = await recruiterService.getApplicants(selectedJob);
    setApplicants(res.data);
  };

  const generateOffer = async () => {
    const res = await pdfService.generateOfferLetter({
      candidate_id: showOffer.candidate_id,
      job_id: Number(selectedJob),
      ...offerForm,
    });
    downloadBlob(res.data, `offer_letter_${showOffer.candidate_id}.pdf`);
    setShowOffer(null);
  };

  return (
    <Layout sidebar={<Sidebar links={links} />}>
      <h1 className="text-2xl font-bold mb-6">Applicants</h1>

      <div className="mb-4">
        <select value={selectedJob} onChange={(e) => setSelectedJob(e.target.value)} className="input-field max-w-md">
          {jobs.map((j) => <option key={j.job_id} value={j.job_id}>{j.title}</option>)}
        </select>
      </div>

      {loading ? <LoadingSpinner /> : applicants.length === 0 ? (
        <div className="card text-center py-8 text-gray-500">No applicants for this job.</div>
      ) : (
        <div className="space-y-4">
          {applicants.map((app, idx) => (
            <div key={app.application_id} className="card">
              <div className="flex justify-between items-start mb-3">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs bg-gray-100 px-2 py-0.5 rounded">#{idx + 1}</span>
                    <h3 className="font-semibold">{app.candidate_name}</h3>
                  </div>
                  <p className="text-sm text-gray-500">{app.candidate_email}</p>
                  <p className="text-xs text-gray-400 mt-1">Skills: {app.candidate_skills}</p>
                </div>
                <StatusBadge status={app.status} />
              </div>
              <MatchScore score={app.match_score} breakdown={app.match_breakdown} />
              <div className="flex flex-wrap gap-2 mt-4">
                <button onClick={() => updateStatus(app.application_id, 'shortlisted')} className="btn-primary text-xs">Shortlist</button>
                <button onClick={() => updateStatus(app.application_id, 'rejected')} className="btn-danger text-xs">Reject</button>
                <button onClick={() => updateStatus(app.application_id, 'on_hold')} className="btn-secondary text-xs">Hold</button>
                <button onClick={() => setShowInterview(app)} className="btn-secondary text-xs">Schedule Interview</button>
                <button onClick={() => getQuestions(app.candidate_id)} className="btn-secondary text-xs">AI Questions</button>
                <button onClick={() => setShowOffer(app)} className="btn-secondary text-xs">Offer Letter</button>
              </div>
            </div>
          ))}
        </div>
      )}

      {questions && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" onClick={() => setQuestions(null)}>
          <div className="card max-w-lg w-full max-h-[80vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            <h3 className="font-semibold mb-2">AI Interview Questions</h3>
            <p className="text-sm text-gray-500 mb-4">{questions.job_title} · {questions.candidate_name}</p>
            <ol className="list-decimal ml-5 space-y-2 text-sm">
              {questions.questions.map((q, i) => <li key={i}>{q}</li>)}
            </ol>
            <button onClick={() => setQuestions(null)} className="btn-secondary mt-4">Close</button>
          </div>
        </div>
      )}

      {showInterview && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" onClick={() => setShowInterview(null)}>
          <div className="card max-w-md w-full" onClick={(e) => e.stopPropagation()}>
            <h3 className="font-semibold mb-4">Schedule Interview - {showInterview.candidate_name}</h3>
            <div className="space-y-3">
              <input type="date" value={interviewForm.date} onChange={(e) => setInterviewForm({ ...interviewForm, date: e.target.value })} className="input-field" />
              <input type="time" value={interviewForm.time} onChange={(e) => setInterviewForm({ ...interviewForm, time: e.target.value })} className="input-field" />
              <input placeholder="Meeting Link" value={interviewForm.meeting_link} onChange={(e) => setInterviewForm({ ...interviewForm, meeting_link: e.target.value })} className="input-field" />
              <textarea placeholder="Notes" value={interviewForm.notes} onChange={(e) => setInterviewForm({ ...interviewForm, notes: e.target.value })} className="input-field" rows={2} />
            </div>
            <div className="flex gap-2 mt-4">
              <button onClick={scheduleInterview} className="btn-primary">Schedule</button>
              <button onClick={() => setShowInterview(null)} className="btn-secondary">Cancel</button>
            </div>
          </div>
        </div>
      )}

      {showOffer && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" onClick={() => setShowOffer(null)}>
          <div className="card max-w-md w-full" onClick={(e) => e.stopPropagation()}>
            <h3 className="font-semibold mb-4">Generate Offer Letter</h3>
            <div className="space-y-3">
              <input placeholder="Position" value={offerForm.position} onChange={(e) => setOfferForm({ ...offerForm, position: e.target.value })} className="input-field" />
              <input placeholder="Salary" value={offerForm.salary} onChange={(e) => setOfferForm({ ...offerForm, salary: e.target.value })} className="input-field" />
              <input placeholder="Start Date" value={offerForm.start_date} onChange={(e) => setOfferForm({ ...offerForm, start_date: e.target.value })} className="input-field" />
              <select value={offerForm.template} onChange={(e) => setOfferForm({ ...offerForm, template: e.target.value })} className="input-field">
                <option value="standard">Standard</option>
                <option value="executive">Executive</option>
                <option value="intern">Internship</option>
              </select>
            </div>
            <div className="flex gap-2 mt-4">
              <button onClick={generateOffer} className="btn-primary">Generate PDF</button>
              <button onClick={() => setShowOffer(null)} className="btn-secondary">Cancel</button>
            </div>
          </div>
        </div>
      )}
    </Layout>
  );
}
