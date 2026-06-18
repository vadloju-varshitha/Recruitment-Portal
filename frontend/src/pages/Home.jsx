import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div className="min-h-[calc(100vh-4rem)]">
      <section className="bg-gradient-to-br from-primary-600 to-primary-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-4">Corporate Recruitment & Placement Portal</h1>
          <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
            Connect top talent with leading companies. AI-powered matching, seamless hiring, and comprehensive analytics.
          </p>
          <div className="flex gap-4 justify-center">
            <Link to="/signup" className="bg-white text-primary-700 px-6 py-3 rounded-lg font-semibold hover:bg-primary-50 transition">
              Get Started
            </Link>
            <Link to="/login" className="border border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white/10 transition">
              Sign In
            </Link>
          </div>
        </div>
      </section>

      <section className="py-16 max-w-7xl mx-auto px-4">
        <h2 className="text-3xl font-bold text-center mb-12">Platform Features</h2>
        <div className="grid md:grid-cols-3 gap-8">
          {[
            { title: 'For Candidates', desc: 'Build profiles, upload resumes, search jobs, and track applications with AI match scores.', icon: '👤' },
            { title: 'For Recruiters', desc: 'Post jobs, manage applicants, schedule interviews, and access hiring analytics.', icon: '🏢' },
            { title: 'For Admins', desc: 'Oversee the entire platform, manage users, generate reports, and monitor metrics.', icon: '⚙️' },
          ].map((f) => (
            <div key={f.title} className="card text-center">
              <div className="text-4xl mb-4">{f.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{f.title}</h3>
              <p className="text-gray-600">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
