# AI Resume Analyzer & Job Matcher 🚀

An AI-powered full-stack web application that helps job seekers optimize their resumes, find real-time job recommendations, and prepare for technical interviews.

## Features

- 📄 **ATS Resume Analyzer** — Upload your resume and get an ATS compatibility score with matched/missing skills
- 🎨 **Resume Generator** — Build professional resumes using Modern, Corporate, and Two-Column templates and export to PDF
- 💼 **Job Recommendations** — Real-time job listings from Arbeitnow & Remotive APIs matched to your role
- 🧠 **Mock Interview Test** — Timed 20-question tests tailored to your job role and target company
- 🔐 **User Authentication** — Secure JWT-based login and registration

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React.js, Vite, Tailwind CSS |
| Backend | FastAPI (Python) |
| Database | MongoDB Atlas |
| Auth | JWT + Bcrypt |
| NLP | spaCy, scikit-learn, sentence-transformers |
| PDF | xhtml2pdf, ReportLab |

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Mahima-1007/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` folder:
```
MONGO_URI=your_mongodb_atlas_connection_string
SECRET_KEY=your_secret_key
```

Start the backend:
```bash
python -m uvicorn main:app --reload --port 8001
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Open the app
Visit **http://localhost:5173**

## Project Structure

```
AI-Resume-Analyzer/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── routes/
│   │   ├── auth.py
│   │   └── api.py
│   ├── modules/
│   │   ├── ats_analyzer.py
│   │   ├── resume_generator.py
│   │   ├── resume_parser.py
│   │   ├── job_api_service.py
│   │   └── test_awareness.py
│   ├── templates/          # HTML resume templates
│   └── data/               # Question bank JSON
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   └── components/
│   └── package.json
└── README.md
```
