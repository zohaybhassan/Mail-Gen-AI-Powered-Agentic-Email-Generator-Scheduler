@echo off
echo Starting AI Email Generator Web Application...
echo.
echo Features:
echo - AI-powered email generation
echo - Document upload and analysis
echo - Email scheduling with APScheduler
echo - Automatic attachment handling
echo.
echo Debug URLs:
echo - Main App: http://localhost:5000
echo - Scheduled Emails: http://localhost:5000/scheduled_emails
echo - Scheduler Debug: http://localhost:5000/debug/scheduler
echo - Test Scheduler: http://localhost:5000/test_scheduler
echo.
cd /d "%~dp0"
python run_flask_app.py
pause

