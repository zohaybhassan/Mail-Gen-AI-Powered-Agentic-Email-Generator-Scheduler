# Phase 3: Technical Summary — MailGen MVP
*AI Product Development Course*

---

## Slide 1: Product Scope & What We Built

### Problem
Professionals waste **10–15 minutes per email** context-switching between document viewers, AI drafters, email clients, and calendars. Job seekers spend **45+ minutes** overthinking their first application email.

### MVP Solution
An **end-to-end AI email generation system** that reads a document (resume, proposal, etc.), extracts key information via a multi-agent AI pipeline, and sends a polished, professional email — all in **under 30 seconds**.

### What We Built ✅
| Component | Implementation |
|-----------|---------------|
| **Multi-Agent AI Pipeline** | 2 CrewAI agents (Document Extractor → Email Writer) using Google Gemini |
| **Document Intelligence** | Reads `.txt`, `.pdf`, `.docx` — extracts names, skills, dates, context |
| **Web Interface** | Flask app with Bootstrap 5 UI — form-based, no technical knowledge needed |
| **Email Scheduling** | APScheduler with date/time picker, status dashboard, cancel capability |
| **Gmail Integration** | yagmail SMTP with App Password auth, attachment support |
| **Failure Handling** | Input validation, AI error catching, document validation, user-facing errors |
| **Limitations Transparency** | Dedicated `/limitations` page communicating MVP constraints |

### What We Deliberately Did NOT Build ❌
| Feature | Why Excluded |
|---------|-------------|
| Email Preview/Edit before send | Tests AI quality assumption directly |
| User Accounts & History | Core value test doesn't require persistence |
| Multi-language support | English-first validates the workflow |
| Database storage | In-memory proves concept; DB is a scaling decision |
| Email Templates Library | Would bypass the AI generation hypothesis |
| Mobile App | Web UI is responsive; native app is premature |

---

## Slide 2: System Overview & Technical Decisions

### Architecture
```
User → Flask Web UI → doc_reader.py → CrewAI Pipeline → email_sender.py → Gmail
                                          ↓                    ↑
                                    Agent 1: Doc Extractor     |
                                          ↓                    |
                                    Agent 2: Email Writer      |
                                          ↓                    |
                                    generated_email.txt ───────┘
                                                          + APScheduler (optional)
```

### Key Technical Decisions

| Decision | Alternative Considered | Rationale |
|----------|----------------------|-----------|
| **CrewAI multi-agent** | Single LLM prompt | Separation of concerns: doc analysis ≠ email writing. Multi-agent produces measurably better output in testing |
| **Google Gemini** | GPT-4, Claude | Free tier, fast inference, sufficient quality. Avoids $20/mo API cost barrier for an MVP |
| **Flask** | Django, FastAPI, React | Fastest to build a working UI. Jinja2 templates = no frontend build step. Sufficient for MVP validation |
| **APScheduler (in-process)** | Celery + Redis | No external dependencies. Background scheduler runs inside Flask process. Simple and sufficient for demo |
| **yagmail** | smtplib, SendGrid API | 10 lines of code. Handles Gmail auth, MIME, attachments automatically. Perfect MVP simplicity |
| **In-memory dict** | SQLite, PostgreSQL | Zero infrastructure. Validates scheduling UX. Known limitation (documented on `/limitations` page) |
| **Bootstrap CDN** | Tailwind, Custom CSS | Professional UI in minutes. No build tools. Gradient theme looks polished |

### Trade-offs Accepted
- **Processing takes 15–40 sec** due to sequential multi-agent pipeline → Still 10× faster than manual
- **Gmail-only** sending → Covers primary target audience (job seekers, freelancers)
- **No email preview** before send → Forces direct testing of AI quality hypothesis
- **Scheduled emails lost on restart** → Documented transparently, proves UX concept

---

## Slide 3: Limitations, Risks & Assumptions Being Tested

### Known Risks

| Risk | Severity | Mitigation in MVP |
|------|----------|-------------------|
| **AI Hallucination** | Medium | Agent 1 grounds email content in actual document data. No "creative" mode. |
| **Credentials in transit** | Medium | HTTPS recommended for production. App Passwords limit scope. Credentials not stored. |
| **API Dependency** | Low | Gemini API is reliable. Error handling catches API failures and reports to user. |
| **Empty/Bad Documents** | Low | `doc_reader.py` returns error strings; `app.py` validates before processing |

### Assumptions This MVP Tests

| # | Assumption | How MVP Tests It |
|---|-----------|-----------------|
| 1 | **"Users will find AI-generated emails useful enough to send without editing"** | MVP sends directly — if users need to edit, this assumption fails |
| 2 | **"Document-grounded generation produces better emails than generic AI"** | Upload a resume → see if the email references actual skills, experience by name |
| 3 | **"The time savings (10 min → 30 sec) are compelling enough to use a new tool"** | End-to-end flow is timed; user either completes the workflow or abandons |
| 4 | **"Email scheduling adds meaningful value beyond 'send now'"** | Scheduling feature usage can be tracked; validates Phase 1 hypothesis |
| 5 | **"Multi-agent pipeline produces higher quality than single-prompt"** | Agent 1 (analysis) + Agent 2 (writing) vs. a single "write me an email" prompt |

### What Success Looks Like for Phase 4
- Users complete the full flow (upload → generate → send) without confusion
- Generated emails are professional enough to send as-is in >70% of cases
- Scheduling feature is used by at least some users (not ignored entirely)
- Time-to-value is under 2 minutes from first page load to email sent

---

*MailGen — Built with CrewAI, Google Gemini, Flask, and Python*

