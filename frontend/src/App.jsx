import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import Home from './pages/Home';
import Login from './pages/Login';
import Signup from './pages/Signup';
import CandidateDashboard from './pages/candidate/Dashboard';
import CandidateProfile from './pages/candidate/Profile';
import JobSearch from './pages/candidate/JobSearch';
import Applications from './pages/candidate/Applications';
import RecruiterDashboard from './pages/recruiter/Dashboard';
import CompanyProfile from './pages/recruiter/Company';
import JobManagement from './pages/recruiter/Jobs';
import Applicants from './pages/recruiter/Applicants';
import Interviews from './pages/recruiter/Interviews';
import AdminDashboard from './pages/admin/Dashboard';
import AdminUsers, { AdminCompanies, AdminJobs, AdminApplications, AdminReports } from './pages/admin/AdminPages';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />

          <Route path="/candidate/dashboard" element={<ProtectedRoute roles={['candidate']}><CandidateDashboard /></ProtectedRoute>} />
          <Route path="/candidate/profile" element={<ProtectedRoute roles={['candidate']}><CandidateProfile /></ProtectedRoute>} />
          <Route path="/candidate/jobs" element={<ProtectedRoute roles={['candidate']}><JobSearch /></ProtectedRoute>} />
          <Route path="/candidate/applications" element={<ProtectedRoute roles={['candidate']}><Applications /></ProtectedRoute>} />

          <Route path="/recruiter/dashboard" element={<ProtectedRoute roles={['recruiter']}><RecruiterDashboard /></ProtectedRoute>} />
          <Route path="/recruiter/company" element={<ProtectedRoute roles={['recruiter']}><CompanyProfile /></ProtectedRoute>} />
          <Route path="/recruiter/jobs" element={<ProtectedRoute roles={['recruiter']}><JobManagement /></ProtectedRoute>} />
          <Route path="/recruiter/applicants" element={<ProtectedRoute roles={['recruiter']}><Applicants /></ProtectedRoute>} />
          <Route path="/recruiter/interviews" element={<ProtectedRoute roles={['recruiter']}><Interviews /></ProtectedRoute>} />

          <Route path="/admin/dashboard" element={<ProtectedRoute roles={['admin']}><AdminDashboard /></ProtectedRoute>} />
          <Route path="/admin/users" element={<ProtectedRoute roles={['admin']}><AdminUsers /></ProtectedRoute>} />
          <Route path="/admin/companies" element={<ProtectedRoute roles={['admin']}><AdminCompanies /></ProtectedRoute>} />
          <Route path="/admin/jobs" element={<ProtectedRoute roles={['admin']}><AdminJobs /></ProtectedRoute>} />
          <Route path="/admin/applications" element={<ProtectedRoute roles={['admin']}><AdminApplications /></ProtectedRoute>} />
          <Route path="/admin/reports" element={<ProtectedRoute roles={['admin']}><AdminReports /></ProtectedRoute>} />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
