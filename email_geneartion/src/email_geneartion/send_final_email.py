from email_sender import send_email

# Read generated email from CrewAI output
with open("generated_email.txt", "r", encoding="utf-8") as f:
    email_content = f.read()

# You can extract subject from first line (if your email content has one)
lines = email_content.strip().splitlines()
subject = lines[0].replace("Subject: ", "") if lines[0].lower().startswith("subject") else "Email from CrewAI"
body = "\n".join(lines)

# YOUR credentials
your_email = "mahadrehman04@gmail.com"
app_password = "vxrx aoxt bmas dqbi"
receiver_email = "i220792@nu.edu.pk"

# Send
send_email(subject, body, receiver_email, your_email, app_password)
