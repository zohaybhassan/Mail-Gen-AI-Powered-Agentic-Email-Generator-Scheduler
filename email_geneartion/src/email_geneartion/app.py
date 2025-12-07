from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, DateTimeLocalField, PasswordField
from wtforms.validators import DataRequired, Email, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta
import os
import json
import uuid
import atexit
import requests
from urllib.parse import urlparse
from werkzeug.utils import secure_filename
from .crew import EmailGeneartion
from .doc_reader import read_document
from .email_sender import send_email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ATTACH_FOLDER'] = 'Attach_folders'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['ATTACH_FOLDER'], exist_ok=True)

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Store scheduled emails
scheduled_emails = {}

class EmailForm(FlaskForm):
    topic = StringField('Email Topic', validators=[DataRequired()], render_kw={"placeholder": "What is this email about?"})
    to_email = StringField('Recipient Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "recipient@example.com"})
    from_email = StringField('Your Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "your@gmail.com"})
    app_password = PasswordField('Gmail App Password', validators=[DataRequired()], render_kw={"placeholder": "16-character app password"})
    document = FileField('Document (for content)', validators=[Optional(), FileAllowed(['txt', 'pdf', 'docx'], 'Only txt, pdf, and docx files are allowed!')])
    attachments = FileField('Attachments (optional)', validators=[Optional(), FileAllowed(['pdf', 'docx', 'txt', 'jpg', 'png', 'xlsx'], 'File type not allowed!')])
    attachment_url = StringField('Attachment URL (optional)', validators=[Optional()], render_kw={"placeholder": "https://example.com/document.pdf"})
    send_now = SelectField('Send Option', choices=[('now', 'Send Now'), ('schedule', 'Schedule for Later')], default='now')
    send_time = DateTimeLocalField('Send Time', validators=[Optional()], format='%Y-%m-%dT%H:%M')

def convert_google_drive_url(url):
    """Convert Google Drive share link to direct download URL and extract filename"""
    try:
        # Pattern: https://drive.google.com/file/d/{FILE_ID}/view?...
        if 'drive.google.com' in url and '/file/d/' in url:
            file_id = url.split('/file/d/')[1].split('/')[0]
            # Get file metadata to retrieve the actual filename
            try:
                api_url = f"https://drive.google.com/uc?id={file_id}&export=json"
                response = requests.get(api_url, timeout=10)
                # This won't work directly, but we'll use a different approach
            except:
                pass
            return f"https://drive.google.com/uc?id={file_id}&export=download", file_id
        return url, None
    except:
        return url, None

def download_file_from_url(url, save_folder):
    """Download a file from URL and save it locally"""
    try:
        print(f"📥 Downloading file from URL: {url}")
        
        # Convert Google Drive link to direct download URL
        converted_url, file_id = convert_google_drive_url(url)
        print(f"📥 Converted URL: {converted_url}")
        
        # Send request to download the file with proper headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(converted_url, timeout=30, headers=headers, allow_redirects=True)
        response.raise_for_status()
        
        # Extract filename from URL or Content-Disposition header
        filename = None
        
        # Try to get filename from Content-Disposition header (most reliable)
        if 'content-disposition' in response.headers:
            content_disposition = response.headers['content-disposition']
            if 'filename=' in content_disposition:
                filename = content_disposition.split('filename=')[1].strip('"\'')
        
        # Fallback: Extract from URL
        if not filename:
            parsed_url = urlparse(converted_url.split('?')[0])  # Remove query parameters
            filename = os.path.basename(parsed_url.path)
        
        # Determine file extension from content-type
        content_type = response.headers.get('content-type', 'application/octet-stream').split(';')[0]
        ext_map = {
            'application/pdf': '.pdf',
            'application/msword': '.doc',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
            'application/vnd.ms-excel': '.xls',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
            'image/jpeg': '.jpg',
            'image/png': '.png',
            'text/plain': '.txt',
            'text/csv': '.csv',
            'application/zip': '.zip',
        }
        
        # If still no filename or no extension, generate one based on content type
        if not filename or '.' not in filename:
            ext = ext_map.get(content_type, '.tmp')
            filename = f"attachment_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
        else:
            # If filename exists but extension doesn't match content-type, add the correct extension
            current_ext = os.path.splitext(filename)[1].lower()
            if not current_ext or current_ext == '.tmp':
                ext = ext_map.get(content_type, '.tmp')
                if ext != '.tmp':
                    filename = os.path.splitext(filename)[0] + ext
        
        # Secure the filename
        filename = secure_filename(filename)
        filepath = os.path.join(save_folder, filename)
        
        # Save the file
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ File downloaded successfully: {filename}")
        return filepath
        
    except requests.exceptions.Timeout:
        raise Exception("Download timeout: URL took too long to respond (>30 seconds)")
    except requests.exceptions.ConnectionError:
        raise Exception("Connection error: Unable to connect to the URL")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise Exception("File not found (404): Check if the URL is correct")
        elif e.response.status_code == 403:
            raise Exception("Access denied (403): Make sure the file is publicly shared")
        elif e.response.status_code == 401:
            raise Exception("Authentication required (401): File may require login to access")
        else:
            raise Exception(f"HTTP error {e.response.status_code}: {e}")
    except Exception as e:
        raise Exception(f"Failed to download file from URL: {str(e)}")

def generate_email_content(topic, doc_text):
    """Generate email content using CrewAI"""
    try:
        inputs = {
            "topic": topic,
            "doc_text": doc_text,
            "current_year": str(datetime.now().year)
        }
        
        print(f"🤖 Generating email for topic: {topic}")
        EmailGeneartion().crew().kickoff(inputs=inputs)
        
        # Read generated email
        with open("generated_email.txt", "r", encoding="utf-8") as f:
            email_content = f.read().strip()
        
        # Extract subject and body
        lines = email_content.splitlines()
        subject = "Generated Email"
        body_lines = []
        
        for i, line in enumerate(lines):
            if line.lower().startswith("subject:"):
                subject = line.replace("Subject:", "").replace("subject:", "").strip()
                start_idx = i + 1
                while start_idx < len(lines) and not lines[start_idx].strip():
                    start_idx += 1
                body_lines = lines[start_idx:]
                break
        else:
            body_lines = lines
            
        body = "\n".join(body_lines).strip()
        
        return subject, body
        
    except Exception as e:
        print(f"❌ Error generating email: {e}")
        return f"Error generating email: {str(e)}", "Please try again or contact support."

def send_scheduled_email(email_data):
    """Function to send scheduled emails"""
    try:
        print(f"📧 Sending scheduled email to: {email_data['to_email']}")
        
        # Generate email content
        subject, body = generate_email_content(email_data['topic'], email_data['doc_text'])
        
        # Send email
        send_email(
            subject=subject,
            body=body,
            to_email=email_data['to_email'],
            from_email=email_data['from_email'],
            app_password=email_data['app_password'],
            attachments=email_data.get('attachments', [])
        )
        
        print(f"✅ Scheduled email sent successfully to {email_data['to_email']}")
        
        # Update status in scheduled_emails
        if email_data['id'] in scheduled_emails:
            scheduled_emails[email_data['id']]['status'] = 'sent'
            scheduled_emails[email_data['id']]['sent_at'] = datetime.now().isoformat()
                
    except Exception as e:
        print(f"❌ Error sending scheduled email: {e}")
        if email_data['id'] in scheduled_emails:
            scheduled_emails[email_data['id']]['status'] = 'failed'
            scheduled_emails[email_data['id']]['error'] = str(e)

@app.route('/')
def index():
    form = EmailForm()
    return render_template('index.html', form=form)

@app.route('/send_email', methods=['POST'])
def send_email_route():
    form = EmailForm()
    
    if form.validate_on_submit():
        try:
            print(f"📝 Processing email request...")
            
            # Handle document upload for content
            doc_text = ""
            if form.document.data:
                doc_file = form.document.data
                doc_filename = secure_filename(doc_file.filename)
                doc_path = os.path.join(app.config['UPLOAD_FOLDER'], doc_filename)
                doc_file.save(doc_path)
                doc_text = read_document(doc_path)
                print(f"📄 Document uploaded: {doc_filename}")
            
            # Handle attachments
            attachments = []
            if form.attachments.data:
                attach_file = form.attachments.data
                attach_filename = secure_filename(attach_file.filename)
                attach_path = os.path.join(app.config['ATTACH_FOLDER'], attach_filename)
                attach_file.save(attach_path)
                attachments.append(attach_path)
                print(f"📎 Attachment saved: {attach_filename}")
            
            # Handle attachment URL
            if form.attachment_url.data and form.attachment_url.data.strip():
                try:
                    url_attachment_path = download_file_from_url(form.attachment_url.data, app.config['ATTACH_FOLDER'])
                    attachments.append(url_attachment_path)
                except Exception as e:
                    print(f"❌ Error downloading attachment from URL: {e}")
                    flash(f'❌ Failed to download attachment from URL: {str(e)}', 'error')
                    return render_template('index.html', form=form)
            
            # Prepare email data
            email_data = {
                'id': datetime.now().strftime('%Y%m%d_%H%M%S'),
                'topic': form.topic.data,
                'doc_text': doc_text,
                'to_email': form.to_email.data,
                'from_email': form.from_email.data,
                'app_password': form.app_password.data,
                'attachments': attachments,
                'created_at': datetime.now().isoformat()
            }
            
            if form.send_now.data == 'now':
                # Send immediately
                print("📧 Sending email immediately...")
                subject, body = generate_email_content(form.topic.data, doc_text)
                
                send_email(
                    subject=subject,
                    body=body,
                    to_email=form.to_email.data,
                    from_email=form.from_email.data,
                    app_password=form.app_password.data,
                    attachments=attachments
                )
                
                flash('✅ Email sent successfully!', 'success')
                
            else:
                # Schedule email
                if not form.send_time.data:
                    flash('❌ Please select a send time for scheduled emails.', 'error')
                    return render_template('index.html', form=form)
                
                send_time = form.send_time.data
                if send_time <= datetime.now():
                    flash('❌ Send time must be in the future.', 'error')
                    return render_template('index.html', form=form)
                
                print(f"⏰ Scheduling email for: {send_time}")
                
                email_data.update({
                    'scheduled_time': send_time.isoformat(),
                    'status': 'scheduled'
                })
                
                # Add to scheduler
                job = scheduler.add_job(
                    func=send_scheduled_email,
                    trigger=DateTrigger(run_date=send_time),
                    args=[email_data],
                    id=email_data['id']
                )
                
                # Store in scheduled emails dictionary
                scheduled_emails[email_data['id']] = email_data
                
                flash(f'⏰ Email scheduled for {send_time.strftime("%Y-%m-%d %H:%M")}!', 'success')
            
            return redirect(url_for('index'))
            
        except Exception as e:
            print(f"❌ Error processing email: {e}")
            flash(f'❌ Error: {str(e)}', 'error')
            return render_template('index.html', form=form)
    
    # Form validation failed
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'❌ {field}: {error}', 'error')
    
    return render_template('index.html', form=form)

@app.route('/scheduled_emails')
def view_scheduled_emails():
    return render_template('scheduled_emails.html', emails=scheduled_emails)

@app.route('/cancel_email/<email_id>')
def cancel_email(email_id):
    """Cancel a scheduled email"""
    if email_id in scheduled_emails:
        # Remove from scheduler
        try:
            scheduler.remove_job(email_id)
        except:
            pass  # Job might have already been executed or removed
        
        # Update status
        scheduled_emails[email_id]['status'] = 'cancelled'
        scheduled_emails[email_id]['cancelled_at'] = datetime.now().isoformat()
        
        flash(f'✅ Email scheduled for {scheduled_emails[email_id]["to_email"]} has been cancelled.', 'success')
    else:
        flash('❌ Email not found.', 'error')
    
    return redirect(url_for('view_scheduled_emails'))

@app.route('/debug/scheduler')
def debug_scheduler():
    """Debug endpoint to check scheduler status"""
    jobs = scheduler.get_jobs()
    return jsonify({
        'running': scheduler.running,
        'jobs_count': len(jobs),
        'jobs': [{'id': job.id, 'next_run': str(job.next_run_time)} for job in jobs],
        'scheduled_emails_count': len(scheduled_emails),
        'scheduled_emails': scheduled_emails
    })

@app.route('/test_scheduler')
def test_scheduler():
    """Test endpoint to verify scheduler is working"""
    test_time = datetime.now() + timedelta(seconds=10)
    
    def test_function():
        print(f"🎯 [{datetime.now()}] Test scheduler job executed successfully!")
    
    job = scheduler.add_job(
        func=test_function,
        trigger=DateTrigger(run_date=test_time),
        id=f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    
    return jsonify({
        'message': f'Test job scheduled for {test_time}',
        'job_id': job.id
    })

if __name__ == '__main__':
    print("🚀 Starting AI Email Generator Web Application...")
    print("📧 Access the application at: http://localhost:5000")
    print("⏰ Features include:")
    print("   - AI-powered email generation")
    print("   - Document upload and analysis") 
    print("   - Email scheduling")
    print("   - Automatic attachment handling")
    print("\n" + "="*50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

# Export the app for external use
__all__ = ['app']