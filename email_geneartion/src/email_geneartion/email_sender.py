import smtplib
from email.message import EmailMessage
import mimetypes
import os

def send_email(subject, body, to_email, from_email, app_password, attachments=None):
    """
    Send an email via Gmail SMTP using standard smtplib.
    
    Args:
        subject: Email subject line
        body: Email body text
        to_email: Recipient email address
        from_email: Sender's Gmail address
        app_password: 16-character Gmail App Password
        attachments: Optional list of file paths to attach
    
    Raises:
        Exception: If email sending fails (with descriptive message)
    """
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        msg.set_content(body)

        if attachments:
            for filepath in attachments:
                if not os.path.exists(filepath):
                    continue
                ctype, encoding = mimetypes.guess_type(filepath)
                if ctype is None or encoding is not None:
                    ctype = 'application/octet-stream'
                maintype, subtype = ctype.split('/', 1)
                
                with open(filepath, 'rb') as f:
                    msg.add_attachment(f.read(),
                                       maintype=maintype,
                                       subtype=subtype,
                                       filename=os.path.basename(filepath))

        # Connect to Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(from_email, app_password)
            smtp.send_message(msg)
            
        print(f"✅ Email sent successfully to {to_email}")
        
    except smtplib.SMTPAuthenticationError as e:
        raise Exception(f"Gmail authentication failed. Please check your email and App Password. Details: {e}")
    except Exception as e:
        error_msg = str(e).lower()
        if "connection" in error_msg or "smtp" in error_msg:
            raise Exception(f"Could not connect to Gmail SMTP. Check your internet connection. Details: {e}")
        else:
            raise Exception(f"Failed to send email: {e}")

