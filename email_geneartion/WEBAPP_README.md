# AI Email Generator Web Application

A Flask-based web application that uses CrewAI to generate professional emails with automatic scheduling capabilities.

## Features

- 🤖 **AI-Powered Email Generation**: Uses CrewAI agents to analyze documents and generate professional emails
- ⏰ **Email Scheduling**: Schedule emails to be sent at specific times
- 📎 **File Upload Support**: Upload documents (.txt, .pdf, .docx) for content analysis
- 📧 **Gmail Integration**: Send emails directly through Gmail with app passwords
- 📋 **Email Management**: View, cancel, and track scheduled emails
- 🎨 **Modern UI**: Beautiful, responsive web interface

## Installation

1. **Install Python Dependencies**:
   ```bash
   pip install flask flask-wtf wtforms apscheduler python-dateutil
   ```

2. **Or install all dependencies using the project file**:
   ```bash
   pip install -e .
   ```

## Usage

### Option 1: Using the Batch File (Windows)
Double-click `start_webapp.bat` to start the application.

### Option 2: Using Python
```bash
python run_flask_app.py
```

### Option 3: Using the Flask App Directly
```bash
cd src
python -m email_geneartion.app
```

## Accessing the Application

1. Open your web browser
2. Navigate to `http://localhost:5000`
3. Fill in the email form:
   - **Email Topic**: What the email is about
   - **Upload Document**: Optional document to analyze
   - **Recipient Email**: Who to send the email to
   - **Your Gmail**: Your Gmail address
   - **App Password**: Your Gmail app password ([How to generate](https://support.google.com/accounts/answer/185833))
   - **Send Option**: Send now or schedule for later

## Email Scheduling

1. Select "Schedule for Later" in the send option
2. Choose your desired date and time
3. The email will be automatically generated and sent at the scheduled time
4. View all scheduled emails in the "Scheduled Emails" page
5. Cancel scheduled emails if needed

## Gmail App Password Setup

1. Go to your Google Account settings
2. Enable 2-Factor Authentication
3. Go to "App passwords" section
4. Generate a new app password for "Mail"
5. Use this 16-character password in the web application

## File Structure

```
src/email_geneartion/
├── app.py                 # Main Flask application
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Main form page
│   └── scheduled_emails.html  # Scheduled emails page
├── static/              # Static files (CSS, JS)
├── crew.py             # CrewAI configuration
├── email_sender.py     # Email sending functionality
├── doc_reader.py       # Document reading utilities
└── main.py             # Original CLI version

uploads/                 # Uploaded files storage
Attach_folders/         # Default attachments folder
```

## API Endpoints

- `GET /` - Main email form
- `POST /send_email` - Process email form and send/schedule email
- `GET /scheduled_emails` - View scheduled emails page
- `GET /api/scheduled_emails` - JSON API for scheduled emails
- `GET /cancel_email/<id>` - Cancel a scheduled email

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're in the correct directory and all dependencies are installed
2. **Gmail Authentication**: Ensure you're using an app password, not your regular Gmail password
3. **File Upload Issues**: Check that the uploaded file is in a supported format (.txt, .pdf, .docx)
4. **Scheduling Issues**: Ensure the scheduled time is in the future

### Dependencies

- Flask: Web framework
- Flask-WTF: Form handling
- WTForms: Form validation
- APScheduler: Background job scheduling
- yagmail: Gmail email sending
- PyPDF2: PDF file reading
- python-docx: Word document reading
- CrewAI: AI agent framework

## Security Notes

- Email credentials are not stored permanently
- File uploads are stored temporarily in the uploads folder
- Use strong app passwords for Gmail
- Run the application in a secure environment for production use

## Development

To modify the application:

1. Edit `app.py` for backend functionality
2. Modify templates in `templates/` for UI changes
3. Update `crew.py` for AI agent behavior
4. Customize email generation in the task configurations

## License

This project is part of the CrewAI email generation system.

