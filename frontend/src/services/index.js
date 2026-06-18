import api from './api';

export const authService = {
  signup: (data) => api.post('/auth/signup', data),
  login: (data) => api.post('/auth/login', data),
  logout: () => api.post('/auth/logout'),
  getMe: () => api.get('/auth/me'),
};

export const candidateService = {
  getProfile: () => api.get('/candidate/profile'),
  createProfile: (data) => api.post('/candidate/profile', data),
  updateProfile: (data) => api.put('/candidate/profile', data),
  uploadResume: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/candidate/resume/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  searchJobs: (params) => api.get('/candidate/jobs', { params }),
  applyJob: (data) => api.post('/candidate/apply', data),
  getApplications: () => api.get('/candidate/applications'),
  getDashboard: () => api.get('/candidate/dashboard'),
  getSkillGap: (jobId) => api.get(`/candidate/skill-gap/${jobId}`),
};

export const recruiterService = {
  registerCompany: (data) => api.post('/recruiter/company', data),
  getCompany: () => api.get('/recruiter/company'),
  updateCompany: (data) => api.put('/recruiter/company', data),
  createJob: (data) => api.post('/recruiter/jobs', data),
  getJobs: () => api.get('/recruiter/jobs'),
  updateJob: (id, data) => api.put(`/recruiter/jobs/${id}`, data),
  deleteJob: (id) => api.delete(`/recruiter/jobs/${id}`),
  getApplicants: (jobId, sortBy = 'match_score') =>
    api.get(`/recruiter/jobs/${jobId}/applicants`, { params: { sort_by: sortBy } }),
  updateApplicationStatus: (id, status) =>
    api.patch(`/recruiter/applications/${id}/status`, { status }),
  scheduleInterview: (data) => api.post('/recruiter/interviews', data),
  getInterviews: () => api.get('/recruiter/interviews'),
  getInterviewQuestions: (data) => api.post('/recruiter/interview-questions', data),
  getAnalytics: () => api.get('/recruiter/analytics'),
};

export const adminService = {
  getAnalytics: () => api.get('/admin/analytics'),
  getTimeToHire: () => api.get('/admin/analytics/time-to-hire'),
  getCompanies: () => api.get('/admin/companies'),
  getCandidates: () => api.get('/admin/candidates'),
  getRecruiters: () => api.get('/admin/recruiters'),
  getJobs: () => api.get('/admin/jobs'),
  getApplications: () => api.get('/admin/applications'),
  getUsers: () => api.get('/admin/users'),
  updateUser: (id, data) => api.put(`/admin/users/${id}`, data),
  deleteUser: (id) => api.delete(`/admin/users/${id}`),
  deleteJob: (id) => api.delete(`/admin/jobs/${id}`),
  getReports: (type) => api.get('/admin/reports', { params: { report_type: type } }),
};

export const pdfService = {
  generateOfferLetter: (data) =>
    api.post('/pdf/offer-letter', data, { responseType: 'blob' }),
  generateExperienceLetter: (data) =>
    api.post('/pdf/experience-letter', data, { responseType: 'blob' }),
  generatePayslip: (data) =>
    api.post('/pdf/payslip', data, { responseType: 'blob' }),
  getOfferTemplates: () => api.get('/pdf/offer-templates'),
};

export const downloadBlob = (blob, filename) => {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
};
