"""
Standalone email sender utility.
Reads the last generated email from generated_email.txt and sends it.

Usage:
    Set environment variables or pass credentials at runtime.
    python -m email_geneartion.send_final_email
"""

import os
from email_sender import send_email

def send_generated_email(your_email: str, app_password: str, receiver_email: str):
    """Send the last generated email from generated_email.txt"""
    
    if not os.path.exists("generated_email.txt"):
        print("❌ No generated email found. Run the crew first.")
        return
    
    with open("generated_email.txt", "r", encoding="utf-8") as f:
        email_content = f.read()

    lines = email_content.strip().splitlines()
    subject = lines[0].replace("Subject: ", "") if lines[0].lower().startswith("subject") else "Email from CrewAI"
    body = "\n".join(lines[1:]).strip()

    send_email(subject, body, receiver_email, your_email, app_password)


if __name__ == "__main__":
    sender = input("Your Gmail address: ").strip()
    password = input("Gmail App Password: ").strip()
    recipient = input("Recipient email: ").strip()
    
    if not all([sender, password, recipient]):
        print("❌ All fields are required.")
    else:
        send_generated_email(sender, password, recipient)
