import yagmail

def send_email(subject, body, to_email, from_email, app_password, attachments=None):
    """
    Send an email via Gmail SMTP using yagmail.
    
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
        yag = yagmail.SMTP(from_email, app_password)
        yag.send(to=to_email, subject=subject, contents=body, attachments=attachments)
        print(f"✅ Email sent successfully to {to_email}")
    except Exception as e:
        error_msg = str(e).lower()
        if "authentication" in error_msg or "password" in error_msg:
            raise Exception(f"Gmail authentication failed. Please check your email and App Password. Details: {e}")
        elif "connection" in error_msg or "smtp" in error_msg:
            raise Exception(f"Could not connect to Gmail SMTP. Check your internet connection. Details: {e}")
        else:
            raise Exception(f"Failed to send email: {e}")

