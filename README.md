# Corporate Recruitment & Placement Portal

A full-stack recruitment platform combining LinkedIn-style profiles, Naukri-style job search, and ATS (Applicant Tracking System) features.

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| Frontend | React, Tailwind CSS, React Router, Axios, Recharts |
| Backend | FastAPI, SQLAlchemy, JWT, Pydantic |
| Database | PostgreSQL |
| Deployment | Vercel (frontend), Render (backend) |

## Features

### Authentication
- Signup, Login, Logout with JWT tokens
- Role-based access: Admin, Recruiter, Candidate

### Candidate
- Profile management with resume upload (PDF)
- Education, skills, projects, experience
- Job search and apply
- Application status tracking
- AI skill-gap analysis

### Recruiter
- Company registration and profile
- Job posting, editing, deletion
- Applicant management sorted by AI match score
- Shortlist, reject, hold candidates
- Interview scheduling
- AI-generated interview questions (Gemini API)
- Analytics dashboard with Recharts

### Admin
- View/manage all users, companies, jobs, applications
- Platform analytics and time-to-hire charts
- Report generation

### AI Features
- Skill-based candidate ranking with match percentage
- Score breakdown (matched/missing skills)
- Resume parsing (PyPDF2 + keyword extraction)
- Skill-gap analysis with recommendations
- AI interview questions (Gemini API with fallback)

### PDF Generation (ReportLab)
- Offer letters (3 templates: standard, executive, intern)
- Experience letters
- Payslips

### Notifications
- Email: application submitted, shortlisted, rejected, interview scheduled, offer letter
- Telegram: shortlisted, interview scheduled, offer letter

## Project Structure

```
M3/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   ├── pdf_generator/
│   ├── email_service/
│   └── telegram_service/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── contexts/
│   └── vercel.json
└── docker-compose.yml
```

## Quick Start

### 1. Start PostgreSQL

```bash
docker-compose up -d
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings

uvicorn main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

**Default Admin:** `admin@portal.com` / `admin123`

### 3. Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

App: http://localhost:5173

## Environment Variables

### Backend (.env)

| Variable | Description |
|----------|-------------|
| DATABASE_URL | PostgreSQL connection string |
| SECRET_KEY | JWT secret key |
| SMTP_* | Email notification settings |
| TELEGRAM_BOT_TOKEN | Telegram bot token |
| TELEGRAM_CHAT_ID | Telegram chat ID |
| GEMINI_API_KEY | Google Gemini API key |

### Frontend (.env)

| Variable | Description |
|----------|-------------|
| VITE_API_URL | Backend API URL |

## Deployment

### Frontend (Vercel)

1. Push to GitHub
2. Import project in Vercel, set root to `frontend/`
3. Set `VITE_API_URL` to your Render backend URL

### Backend (Render)

1. Create Web Service, root directory: `backend/`
2. Build: `pip install -r requirements.txt`
3. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add PostgreSQL database and set `DATABASE_URL`
5. Set all environment variables from `.env.example`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/signup | Register user |
| POST | /api/auth/login | Login |
| GET | /api/auth/me | Current user |
| GET | /api/candidate/jobs | Search jobs |
| POST | /api/candidate/apply | Apply for job |
| POST | /api/recruiter/jobs | Create job |
| GET | /api/recruiter/jobs/{id}/applicants | View applicants |
| GET | /api/admin/analytics | Platform analytics |
| POST | /api/pdf/offer-letter | Generate offer letter |

Full API documentation at `/docs` when running the backend.

## Match Score Example

**Job Skills:** Python, SQL, Machine Learning  
**Candidate Skills:** Python, SQL, Java  
**Match Score:** 66% (2 of 3 matched)

## License

MIT
