# 🤖 MailGen - AI-Powered Agentic Email Generator & Scheduler

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Latest-purple.svg)](https://github.com/joaomdmoura/crewAI)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A sophisticated, AI-powered email generation and scheduling system that leverages **CrewAI** framework with **Google Gemini AI** to automatically generate professional, context-aware emails. Features a beautiful Flask web interface with email scheduling capabilities, document analysis, and attachment management.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [API Endpoints](#api-endpoints)
- [Technologies Used](#technologies-used)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Overview

**MailGen** is an intelligent email generation system that uses multi-agent AI architecture to create professional, personalized emails. The system analyzes uploaded documents, extracts relevant information, and crafts well-structured emails that are ready to send. Whether you need to send job applications, meeting requests, follow-ups, or any other type of professional communication, MailGen handles it all.

### Key Capabilities

- **AI-Powered Content Generation**: Uses CrewAI with Google Gemini AI to understand context and generate professional emails
- **Multi-Agent Architecture**: Two specialized AI agents work together - one for document analysis, another for email composition
- **Smart Scheduling**: Schedule emails for future delivery with APScheduler
- **Document Intelligence**: Supports `.txt`, `.pdf`, and `.docx` files for content extraction
- **Flexible Attachment Handling**: Upload files directly or use the `Attach_folders` directory
- **Gmail Integration**: Secure email sending via Gmail SMTP with App Password authentication
- **Beautiful Web UI**: Modern, responsive Flask-based interface with real-time feedback
- **Scheduling Dashboard**: Manage, view, and cancel scheduled emails

## 🏗️ Architecture

### Multi-Agent System (CrewAI)

MailGen uses a **two-agent architecture** powered by CrewAI:

```
┌─────────────────────────────────────────────────────────┐
│                    User Input                           │
│  (Topic, Document, Email Details, Attachments)          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Agent 1: Document Extractor                │
│  Role: Intelligent Document Analyst                     │
│  Task: Analyze uploaded document and extract key info   │
│  Output: Structured summary of important details        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Agent 2: Email Writer                      │
│  Role: Professional Email Generator                     │
│  Task: Craft complete, professional email               │
│  Input: Extracted info + Topic                          │
│  Output: Subject line + Complete email body             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│            Email Delivery System                        │
│  • Send immediately via Gmail SMTP                      │
│  • Schedule for future delivery (APScheduler)           │
│  • Attach files from uploads or Attach_folders          │
└─────────────────────────────────────────────────────────┘
```

### System Components

1. **Flask Web Application** (`app.py`)
   - Handles HTTP requests and form submissions
   - Manages file uploads and validation
   - Controls email scheduling and delivery

2. **CrewAI Orchestrator** (`crew.py`)
   - Configures and manages AI agents
   - Coordinates task execution
   - Ensures sequential processing

3. **Document Reader** (`doc_reader.py`)
   - Supports multiple file formats (.txt, .pdf, .docx)
   - Extracts text content for AI analysis

4. **Email Sender** (`email_sender.py`)
   - Handles Gmail SMTP authentication
   - Manages attachment inclusion
   - Sends emails securely

5. **Scheduler** (APScheduler integration)
   - Background job scheduling
   - Automatic email delivery at specified times
   - Job management and cancellation

## ✨ Features

### 🌐 Web Interface
- **Beautiful, Responsive Design**: Modern UI built with Bootstrap 5
- **Intuitive Forms**: Easy-to-use interface for email configuration
- **Real-time Feedback**: Flash messages for success/error notifications
- **Mobile-Friendly**: Works seamlessly on desktop, tablet, and mobile

### 🤖 AI-Powered Generation
- **Context-Aware**: Understands document content and email purpose
- **Professional Tone**: Generates formal, well-structured emails
- **Smart Extraction**: Identifies names, dates, purposes, and key details
- **No Placeholders**: Generates complete emails ready to send

### ⏰ Advanced Scheduling
- **Date/Time Picker**: Visual calendar for easy scheduling
- **Background Execution**: Emails sent automatically at scheduled time
- **Timezone Support**: Handles timezone conversions properly
- **Status Tracking**: Monitor scheduled, sent, failed, and cancelled emails
- **Cancellation**: Cancel scheduled emails before they're sent

### 📄 Document Analysis
- **Multiple Formats**: .txt, .pdf, .docx support
- **Intelligent Parsing**: Extracts relevant information automatically
- **Context Understanding**: AI agents understand document structure and content

### 📎 Attachment Management
- **Form Upload**: Upload multiple files directly through the web interface
- **URL Downloads**: Provide Google Drive or direct download links
- **Folder-Based**: Place files in `Attach_folders` for automatic inclusion
- **Flexible Storage**: Uploaded files stored in `uploads/` directory

### 📧 Gmail Integration
- **Secure Authentication**: Uses Gmail App Passwords (not regular password)
- **SMTP Protocol**: Reliable email delivery via yagmail
- **Attachment Support**: Seamlessly includes all specified files

### 📊 Management Dashboard
- **View Scheduled Emails**: See all pending scheduled emails
- **Email Status**: Track if emails are scheduled, sent, failed, or cancelled
- **Debug Tools**: Access scheduler debug information
- **Test Functionality**: Built-in scheduler testing endpoint

## 📁 Project Structure

```
MailGen-Agentic-Mailer/
│
├── email_geneartion/                # Main project directory
│   │
│   ├── src/
│   │   └── email_geneartion/       # Source code
│   │       ├── app.py              # Flask web application (405 lines)
│   │       ├── main.py             # CLI interface (121 lines)
│   │       ├── crew.py             # CrewAI agent & task configuration
│   │       ├── doc_reader.py       # Document reading utilities
│   │       ├── email_sender.py     # Email sending via Gmail
│   │       ├── send_final_email.py # Email delivery helper
│   │       │
│   │       ├── config/             # AI agent configuration
│   │       │   ├── agents.yaml     # Agent definitions & prompts
│   │       │   └── tasks.yaml      # Task descriptions & outputs
│   │       │
│   │       ├── templates/          # HTML templates (Jinja2)
│   │       │   ├── base.html       # Base layout template
│   │       │   ├── index.html      # Main email form (177 lines)
│   │       │   └── scheduled_emails.html  # Scheduling dashboard
│   │       │
│   │       └── tools/              # Custom CrewAI tools
│   │           ├── __init__.py
│   │           └── custom_tool.py
│   │
│   ├── docs/                       # Sample documents for testing
│   ├── Attach_folders/             # Default attachment directory
│   ├── uploads/                    # Uploaded files storage
│   ├── knowledge/                  # Knowledge base (if applicable)
│   │
│   ├── pyproject.toml              # Project dependencies & metadata
│   ├── .env                        # Environment variables (API keys)
│   ├── .gitignore                  # Git ignore rules
│   │
│   ├── run_flask_app.py            # Flask app launcher script
│   ├── start_webapp.bat            # Windows batch file to start app
│   ├── test_scheduler.py           # Scheduler testing script
│   │
│   ├── generated_email.txt         # Last generated email (output)
│   ├── report.md                   # AI LLMs comprehensive report
│   ├── README.md                   # Original project README
│   ├── WEBAPP_README.md            # Web app specific README
│   └── FIXES_SUMMARY.md            # Bug fixes documentation
│
└── README.md                       # This comprehensive README

```

### Key Files Explained

#### **app.py** (Flask Web Application)
The heart of the web interface. Contains:
- `EmailForm`: Flask-WTF form with validation
- `convert_google_drive_url()`: Converts Google Drive share links to direct downloads
- `download_file_from_url()`: Downloads files from provided URLs
- `generate_email_content()`: Invokes CrewAI to generate email
- `send_scheduled_email()`: Scheduled job function for email delivery
- Route handlers for `/`, `/send_email`, `/scheduled_emails`, `/cancel_email/<id>`, `/debug/scheduler`

#### **crew.py** (CrewAI Configuration)
Defines the multi-agent system:
- `doc_extractor`: Agent that analyzes documents
- `email_writer`: Agent that crafts emails
- `extract_doc_task`: Task for document analysis
- `generate_email_task`: Task for email generation
- Sequential processing workflow

#### **agents.yaml** & **tasks.yaml**
Configuration files that define agent behaviors, roles, goals, backstories, and task descriptions.

#### **main.py** (CLI Interface)
Command-line interface for the application:
- `run()`: Main CLI execution flow
- `train()`: Train the AI agents
- `replay()`: Replay past tasks
- `test()`: Test the AI agents

## 🚀 Installation

### Prerequisites

- **Python 3.10 or higher** (Tested with 3.10 - 3.13)
- **Gmail account** with 2-Factor Authentication enabled
- **Google Gemini API key** ([Get one here](https://aistudio.google.com/))

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd MailGen-Agentic-Mailer/email_geneartion
```

### Step 2: Install Dependencies

#### Option 1: Using uv (Recommended)
```bash
uv install
```

#### Option 2: Using pip
```bash
pip install -r requirements.txt
```

#### Option 3: Install from pyproject.toml
```bash
pip install -e .
```

### Step 3: Set Up Environment Variables

Create a `.env` file in the `email_geneartion` directory:

```env
MODEL=gemini/gemini-2.5-flash
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

**Important**: Replace `your_actual_gemini_api_key_here` with your real API key from Google AI Studio.

### Step 4: Set Up Gmail App Password

1. Go to [Google Account Security Settings](https://myaccount.google.com/security)
2. Enable **2-Factor Authentication** if not already enabled
3. Navigate to **App Passwords** section
4. Generate a new app password for "Mail"
5. Save the 16-character password (you'll need it when using the app)

### Dependencies

The project requires the following Python packages:

```
crewai[tools] >= 0.140.0, < 1.0.0
yagmail >= 0.15.0
PyPDF2 >= 3.0.0
python-docx >= 0.8.11
flask >= 2.0.0
flask-wtf >= 1.0.0
wtforms >= 3.0.0
email-validator >= 2.0.0
apscheduler >= 3.10.0
python-dateutil >= 2.8.0
```

## ⚙️ Configuration

### AI Agent Configuration

Edit `src/email_geneartion/config/agents.yaml` to customize agent behavior:

```yaml
doc_extractor:
  role: Intelligent Document Analyst
  goal: Extract key information from the uploaded document related to the given topic.
  backstory: You are a skilled document analyst who specializes in quickly understanding 
    the context and summarizing documents to extract relevant facts, such as names, 
    dates, reasons, and requests.

email_writer:
  role: Professional Email Generator
  goal: Craft a clear and context-aware email using the user's topic and extracted details.
  backstory: You're an expert email writer known for generating concise and well-structured 
    emails. You turn fragmented or raw input into polished, formal messages.
```

### Task Configuration

Edit `src/email_geneartion/config/tasks.yaml` to customize task descriptions:

```yaml
extract_doc_task:
  description: >
    Read and analyze the document content provided in the doc_text input.
    Extract all key information relevant to the email topic: {topic}
  expected_output: >
    A structured summary of extracted information from the document
  agent: doc_extractor

generate_email_task:
  description: >
    Write a professional, complete email using the topic: {topic} 
    and the extracted document information.
  expected_output: >
    A polished, formal email including subject, greeting, complete body, and proper closing.
    No placeholders should exist.
  agent: email_writer
```

## 💻 Usage

### Web Interface (Recommended)

#### Option 1: Windows Batch File
Double-click `start_webapp.bat` to launch the application.

#### Option 2: Python Script
```bash
cd email_geneartion
python run_flask_app.py
```

#### Option 3: Direct Module Execution
```bash
cd email_geneartion/src
python -m email_geneartion.app
```

The application will start on `http://localhost:5000`

### Using the Web Application

1. **Open your browser** and navigate to `http://localhost:5000`

2. **Fill in the Email Form**:
   - **Email Topic**: What is this email about? (e.g., "Job Application for Senior Developer")
   - **Upload Document** (Optional): Upload a .txt, .pdf, or .docx file containing information for the email
   - **Upload Attachments** (Optional): Select files to attach to the email
   - **Attachment URL** (Optional): Provide a Google Drive link or direct download URL
   - **Recipient Email**: Who should receive the email
   - **Your Gmail**: Your Gmail address
   - **Gmail App Password**: Your 16-character app password (NOT your regular password)
   - **Send Option**: 
     - "Send Now" - Send immediately
     - "Schedule for Later" - Pick a date and time

3. **Submit the Form**:
   - Click "Generate & Send Email"
   - The AI will analyze your document (if provided)
   - Generate a professional email
   - Send it immediately or schedule it for later

4. **View Scheduled Emails**:
   - Navigate to `http://localhost:5000/scheduled_emails`
   - See all pending scheduled emails
   - Cancel emails if needed

### Command Line Interface (CLI)

For advanced users or automation:

```bash
cd email_geneartion
crewai run
# OR
python -m email_geneartion.main
```

Follow the prompts:
1. Enter email topic
2. Provide document path (e.g., `docs/application.txt`)
3. Enter recipient email
4. Enter your Gmail address
5. Enter Gmail App Password

The generated email will be saved to `generated_email.txt` and sent automatically.

## 🔍 How It Works

### Detailed Workflow

1. **User Input Collection**
   - User fills out the web form with email details
   - Uploads optional document for content analysis
   - Selects attachments (form upload, URL, or Attach_folders)
   - Chooses to send now or schedule for later

2. **Document Processing**
   - If document is uploaded, it's saved to the `uploads/` directory
   - `doc_reader.py` reads the file based on extension (.txt, .pdf, .docx)
   - Text content is extracted and prepared for AI analysis

3. **AI Agent Processing (CrewAI)**
   
   **Step 1 - Document Extraction**:
   - `doc_extractor` agent receives the document text
   - Analyzes content in context of the email topic
   - Extracts key information: names, dates, purposes, requests, etc.
   - Produces a structured summary
   
   **Step 2 - Email Generation**:
   - `email_writer` agent receives the extracted information
   - Uses the email topic and extracted details
   - Crafts a complete, professional email
   - Includes subject line, greeting, body, and closing
   - Ensures no placeholders or missing information
   - Output is saved to `generated_email.txt`

4. **Email Preparation**
   - Subject line is extracted from generated content
   - Body is formatted properly
   - Attachments are collected:
     - Files uploaded via form
     - Files downloaded from URLs (Google Drive, etc.)
     - Files in `Attach_folders/` directory

5. **Delivery or Scheduling**
   
   **If "Send Now"**:
   - Email is sent immediately via Gmail SMTP
   - Confirmation message displayed to user
   
   **If "Schedule for Later"**:
   - Email details are stored with a unique ID
   - APScheduler creates a background job
   - Job is scheduled for the specified date/time
   - At the scheduled time, the job executes and sends the email
   - Status is updated to "sent" or "failed"

6. **Status Tracking**
   - All scheduled emails are stored in memory (dictionary)
   - Users can view scheduled emails in the dashboard
   - Users can cancel scheduled emails before they're sent
   - Debug endpoints provide scheduler status information

### AI Agents in Detail

**Agent 1: Document Extractor**
- **Role**: Intelligent Document Analyst
- **Goal**: Extract key information relevant to the email topic
- **Capabilities**:
  - Understands context and document structure
  - Identifies important names, dates, facts, requests
  - Summarizes lengthy documents into key points
  - Provides structured output for the email writer

**Agent 2: Email Writer**
- **Role**: Professional Email Generator
- **Goal**: Craft clear, context-aware, professional emails
- **Capabilities**:
  - Uses extracted information and topic to compose emails
  - Generates appropriate subject lines
  - Creates proper email structure (greeting, body, closing)
  - Ensures professional tone and formatting
  - Replaces any placeholders with actual information
  - Produces ready-to-send emails

### Example Workflow

**Scenario**: Applying for a job

1. User uploads their resume (PDF)
2. Sets topic to "Job Application for Frontend Developer at Tech Corp"
3. Provides recipient as "hr@techcorp.com"
4. Provides their Gmail credentials

**AI Processing**:
1. `doc_extractor` reads the resume and extracts:
   - Your name
   - Your skills (React, JavaScript, TypeScript)
   - Your experience (5 years)
   - Your education
   - Previous companies

2. `email_writer` uses this information to generate:
   ```
   Subject: Application for Frontend Developer Position

   Dear Hiring Manager,

   I am writing to express my strong interest in the Frontend Developer position 
   at Tech Corp. With 5 years of professional experience in developing modern web 
   applications using React, JavaScript, and TypeScript, I am confident I can 
   contribute effectively to your team.

   [... detailed body with specific accomplishments ...]

   I have attached my resume for your review. I would welcome the opportunity to 
   discuss how my experience and skills align with your needs.

   Thank you for considering my application.

   Best regards,
   [Your Name]
   ```

3. Email is sent with resume attached

## 🔌 API Endpoints

### Web Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Main email form page |
| `/send_email` | POST | Process email form and send/schedule email |
| `/scheduled_emails` | GET | View scheduled emails dashboard |
| `/cancel_email/<id>` | GET | Cancel a scheduled email by ID |
| `/debug/scheduler` | GET | Get scheduler status and debug info |
| `/test_scheduler` | GET | Test scheduler with a 10-second job |

### API Response Examples

**GET `/debug/scheduler`**
```json
{
  "running": true,
  "jobs_count": 3,
  "scheduled_emails_count": 3,
  "jobs": [
    {
      "id": "email_a1b2c3d4...",
      "next_run_time": "2025-02-14T10:30:00+00:00",
      "trigger": "date[2025-02-14 10:30:00 UTC]"
    }
  ]
}
```

**GET `/test_scheduler`**
```json
{
  "message": "Test scheduled successfully. Check console in 10 seconds.",
  "scheduled_for": "2025-02-13T19:09:05"
}
```

## 🛠️ Technologies Used

### Backend
- **Python 3.10+**: Core programming language
- **Flask 2.0+**: Web framework
- **Flask-WTF**: Form handling and validation
- **WTForms**: Form validation
- **APScheduler 3.10+**: Background job scheduling
- **yagmail**: Gmail email sending

### AI & Machine Learning
- **CrewAI**: Multi-agent AI framework
- **Google Gemini AI**: Language model (gemini-2.5-flash)
- **LangChain**: LLM orchestration (via CrewAI)

### Document Processing
- **PyPDF2**: PDF file reading
- **python-docx**: Word document reading
- **Built-in text processing**: .txt file reading

### Frontend
- **Bootstrap 5**: CSS framework
- **Font Awesome**: Icons
- **JavaScript**: Dynamic form interactions
- **Jinja2**: Template engine

### Utilities
- **python-dateutil**: Date/time parsing
- **email-validator**: Email validation
- **requests**: HTTP requests for file downloads (in app.py)

## 🐛 Troubleshooting

### Common Issues

#### 1. **ModuleNotFoundError**

**Problem**: Python can't find the email_geneartion module

**Solution**:
```bash
# Make sure you're in the correct directory
cd email_geneartion

# Reinstall dependencies
pip install -e .
# OR
uv install
```

#### 2. **Invalid API Key Error**

**Problem**: Gemini API key is not recognized

**Solution**:
- Check your `.env` file exists in `email_geneartion/` directory
- Verify the API key has no extra spaces or newlines
- Ensure the format is: `GEMINI_API_KEY=your_key_here`
- Get a new key from [Google AI Studio](https://aistudio.google.com/)

#### 3. **Gmail Authentication Failed**

**Problem**: Cannot send emails via Gmail

**Solutions**:
- ✅ Use App Password, NOT your regular Gmail password
- ✅ Ensure 2-Factor Authentication is enabled on your Google Account
- ✅ Check that the app password is exactly 16 characters
- ✅ Go to [Google App Passwords](https://myaccount.google.com/apppasswords) to generate a new one
- ✅ Check Gmail security settings for blocked sign-in attempts

#### 4. **File Upload Errors**

**Problem**: Document upload fails

**Solutions**:
- Verify the file format is .txt, .pdf, or .docx
- Check file size (very large files may cause issues)
- Ensure proper file permissions
- Check that the `uploads/` directory exists and is writable

#### 5. **Scheduled Emails Not Sending**

**Problem**: Scheduled emails don't send at the specified time

**Solutions**:
- Check the scheduler status at `http://localhost:5000/debug/scheduler`
- Verify the scheduled time is in the future
- Ensure the Flask app is still running (scheduler stops when app stops)
- Check console output for error messages
- Run the test scheduler: `python test_scheduler.py`

**Note**: Scheduled emails are stored in **memory only**. If you restart the Flask app, all pending scheduled emails will be lost.

#### 6. **"Send Now" Validation Error**

**Problem**: Form requires date/time even when "Send Now" is selected

**Solution**: This has been fixed in the current version. If you still see this:
- Clear your browser cache
- Ensure JavaScript is enabled
- Check `FIXES_SUMMARY.md` for details

#### 7. **Google Drive Link Not Working**

**Problem**: Attachment from Google Drive URL fails

**Solutions**:
- Ensure the Google Drive link is a **share link**
- Make sure the file has public access or "Anyone with the link can view"
- The system converts share links to direct download links automatically
- Test with a direct download URL first to verify the feature works

### Debug Endpoints

Use these URLs for debugging:

- **Main App**: `http://localhost:5000`
- **Scheduled Emails Dashboard**: `http://localhost:5000/scheduled_emails`
- **Scheduler Debug Info**: `http://localhost:5000/debug/scheduler`
- **Test Scheduler**: `http://localhost:5000/test_scheduler`

### Testing the Scheduler

Run the standalone test script:

```bash
cd email_geneartion
python test_scheduler.py
```

This will:
1. Check scheduler status
2. Schedule a test job for 10 seconds in the future
3. Verify the job executes

### Logs and Output

Check the console output for detailed information:
- AI agent processing steps
- Email generation progress
- Scheduler job creation and execution
- Email sending status
- Error messages with stack traces

## 🧪 Testing

### Test the Scheduler

```bash
python test_scheduler.py
```

### Test Email Generation (CLI)

```bash
crewai run
```

### Test the Web App

1. Start the app: `python run_flask_app.py`
2. Open browser: `http://localhost:5000`
3. Fill in a test email with a short topic and upload a sample document
4. Use your own email as both sender and recipient
5. Select "Send Now" to test immediate sending
6. Try "Schedule for Later" with a time 2 minutes in the future
7. Check the scheduled emails page to verify it appears
8. Wait for the scheduled time and verify the email is sent

## 📚 Additional Documentation

- **README.md**: Original project documentation (in `email_geneartion/`)
- **WEBAPP_README.md**: Web application specific guide
- **FIXES_SUMMARY.md**: Bug fixes and improvements changelog
- **report.md**: Comprehensive AI/LLM trends report (sample document)

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**: Edit code, add features, fix bugs
4. **Test thoroughly**: Ensure everything works
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Areas for Contribution

- **Database Integration**: Replace in-memory scheduled emails with persistent storage (SQLite, PostgreSQL)
- **Authentication**: Add user accounts and authentication
- **Email Templates**: Create reusable email templates
- **More AI Models**: Support for other LLMs (GPT-4, Claude, etc.)
- **Enhanced UI**: Improve the web interface with more features
- **Email Preview**: Preview generated emails before sending
- **Attachment Preview**: View attachments before sending
- **Email History**: Track sent emails with a history page
- **Notifications**: Email or push notifications for scheduled emails
- **Multi-language Support**: Generate emails in different languages
- **Docker Support**: Containerize the application

## 📝 License

This project is open source and available under the **MIT License**.

```
MIT License

Copyright (c) 2025 MailGen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

## 🙏 Acknowledgments

- **CrewAI** - For the amazing multi-agent framework
- **Google Gemini** - For powerful AI capabilities
- **Flask** - For the excellent web framework
- **Bootstrap** - For beautiful UI components
- **APScheduler** - For reliable job scheduling

## 📞 Support

For issues, questions, or feature requests:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the [Additional Documentation](#additional-documentation)
3. Check the debug endpoints for system status
4. Open an issue on GitHub
5. Review existing issues for similar problems

## 🎯 Roadmap

### Planned Features

- ✅ AI-powered email generation
- ✅ Document analysis (.txt, .pdf, .docx)
- ✅ Email scheduling with APScheduler
- ✅ Web interface with Flask
- ✅ Gmail integration
- ⬜ Persistent database for scheduled emails
- ⬜ User authentication and accounts
- ⬜ Email templates library
- ⬜ Email preview before sending
- ⬜ Email history and analytics
- ⬜ Multi-language email generation
- ⬜ Support for more email providers (Outlook, SendGrid)
- ⬜ API for programmatic access
- ⬜ Mobile app
- ⬜ Browser extension

---

**Made with ❤️ using AI and Python**

**Star ⭐ this repo if you find it helpful!**
