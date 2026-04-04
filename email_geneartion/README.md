#  MailGen — AI-Powered Agentic Email Generator & Scheduler

> **Course**: AI Product Development — Phase 3: MVP Development & Demo

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-purple.svg)](https://github.com/joaomdmoura/crewAI)
[![Gemini](https://img.shields.io/badge/Google_Gemini-AI-orange.svg)](https://ai.google.dev/)

---

## 📌 What Problem Does MailGen Solve?

Professionals waste **10–15 minutes per email** context-switching between document viewers, AI tools, email clients, and calendars. Job seekers report spending **45+ minutes** drafting their first application email.

**MailGen reduces this to under 30 seconds** through a multi-agent AI pipeline that reads your document, extracts relevant information, and generates a complete professional email — ready to send or schedule.

---

## ✨ Core Features (MVP)

| Feature | Description |
|---------|-------------|
| 🤖 **AI Email Generation** | Two specialized AI agents (Document Analyzer + Email Writer) work sequentially |
| 📄 **Document Intelligence** | Upload `.txt`, `.pdf`, or `.docx` → AI extracts context |
| ⏰ **Email Scheduling** | Schedule emails for future delivery with APScheduler |
| 📎 **Attachment Support** | Upload files, Google Drive URLs, or use the `Attach_folders` directory |
| 📧 **Gmail Integration** | Secure SMTP sending via Gmail App Passwords |
| 📊 **Scheduling Dashboard** | View, track status, and cancel scheduled emails |
| ⚠️ **Failure Handling** | Validates inputs, catches AI errors, reports failures clearly |
| 📋 **Limitations Page** | Transparent about what the MVP can and cannot do |

---

## 🏗️ Architecture

```
User Input (Topic + Document + Credentials)
        │
        ▼
┌─────────────────────────────┐
│  doc_reader.py              │  Reads .txt / .pdf / .docx
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│  Agent 1: Document Extractor│  Analyzes document, extracts key info
│  (CrewAI + Gemini AI)       │
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│  Agent 2: Email Writer      │  Crafts complete professional email
│  (CrewAI + Gemini AI)       │
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│  email_sender.py (yagmail)  │  Sends via Gmail SMTP
│  + APScheduler (optional)   │  Or schedules for later
└─────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Gmail account with [App Password](https://support.google.com/accounts/answer/185833) enabled
- [Google Gemini API key](https://aistudio.google.com/)

### Setup

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd MailGen-Agentic-Mailer/email_geneartion

# 2. Install dependencies
pip install -e .
# OR using uv:
uv install

# 3. Create .env file
echo "MODEL=gemini/gemini-2.5-flash" > .env
echo "GEMINI_API_KEY=your_api_key_here" >> .env

# 4. Run the web app
python run_flask_app.py
```

Open **http://localhost:5000** in your browser.

### Using the App

1. Enter an **email topic** (e.g., "Job Application for Software Engineer at Google")
2. Optionally **upload a document** (resume, proposal, etc.) for AI analysis
3. Enter **recipient email**, your **Gmail**, and your **App Password**
4. Choose **Send Now** or **Schedule for Later**
5. Click **Generate & Send Email** → AI creates and sends the email

---

## 📁 Project Structure

```
email_geneartion/
├── src/email_geneartion/
│   ├── app.py              # Flask web application (routes, forms, scheduling)
│   ├── crew.py             # CrewAI multi-agent pipeline configuration
│   ├── doc_reader.py       # Document reader (.txt, .pdf, .docx)
│   ├── email_sender.py     # Gmail SMTP sender (yagmail)
│   ├── main.py             # CLI interface
│   ├── config/
│   │   ├── agents.yaml     # AI agent role/goal/backstory definitions
│   │   └── tasks.yaml      # Task descriptions and expected outputs
│   └── templates/
│       ├── base.html       # Base layout (Bootstrap 5)
│       ├── index.html      # Email form page
│       ├── scheduled_emails.html  # Dashboard
│       └── limitations.html      # MVP limitations page
├── docs/                   # Sample documents for testing
├── Attach_folders/         # Default attachment directory
├── pyproject.toml          # Dependencies & build config
├── run_flask_app.py        # Flask launcher
├── start_webapp.bat        # Windows launcher
├── test_scheduler.py       # Scheduler test script
└── .env                    # API keys (not committed)
```

---

## 🧪 Sample Data

The `docs/` folder contains sample documents for testing:

- **`req.txt`** — A job description + user qualifications for a Frontend Developer position

The `Attach_folders/` directory contains sample PDFs that auto-attach to sent emails.

**Why this data is sufficient for MVP**: The primary use case is job applications, and `req.txt` contains a realistic job posting with user info — exactly what a real user would provide.

---

## ⚠️ Known Limitations

| Limitation | Impact | MVP Justification |
|-----------|--------|-------------------|
| In-memory scheduling | Emails lost on restart | Proves concept; DB planned for production |
| Gmail only | No Outlook/Yahoo support | Gmail covers primary audience |
| No email preview/edit | Can't review before send | Tests AI quality assumption directly |
| No user accounts | No history across sessions | MVP tests core value, not user management |
| 15-40 sec processing | Not instant | Still 10× faster than manual workflow |
| English only | No multi-language | Validates core workflow first |

Full details at **http://localhost:5000/limitations** when the app is running.

---

## 🔧 Technical Decisions & Trade-offs

| Decision | Rationale |
|----------|-----------|
| **CrewAI** over single-prompt | Multi-agent separation improves output quality — doc analysis and email writing are distinct skills |
| **Google Gemini** over GPT-4 | Free tier available, fast inference, sufficient quality for email generation |
| **Flask** over Django/FastAPI | Lightweight, fast to build, sufficient for MVP web UI |
| **APScheduler** over Celery | No need for a message broker; in-process scheduling is simpler for MVP |
| **yagmail** over smtplib | Simplified Gmail SMTP; handles auth and attachments cleanly |
| **In-memory storage** over DB | No infrastructure overhead; validates scheduling workflow first |
| **Bootstrap CDN** over custom CSS | Rapid UI development; looks professional without frontend engineering |

---

## 🧪 Testing

```bash
# Test the scheduler independently
python test_scheduler.py

# Test email generation via CLI
crewai run

# Test the web app
python run_flask_app.py
# → http://localhost:5000
```

---

## 📚 Documentation Index

| Document | Purpose |
|----------|---------|
| `README.md` | This file — setup, usage, architecture |
| `PHASE_1_BUSINESS_ANALYSIS.md` | Business viability analysis (market, pricing, competition) |
| `PHASE_1_DOCUMENTATION.md` | Phase 1 technical documentation |
| `FIXES_SUMMARY.md` | Bug fixes changelog |
| `how it works.md` | Comprehensive technical reference |

---

## 📄 License

MIT License — see `how it works.md` for full text.

