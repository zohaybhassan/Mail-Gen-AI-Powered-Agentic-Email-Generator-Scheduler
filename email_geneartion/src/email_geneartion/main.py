#!/usr/bin/env python
import sys
import warnings
import os
import glob
from datetime import datetime
from email_geneartion.crew import EmailGeneartion  # keep typo to match folder
from email_geneartion.email_sender import send_email
from email_geneartion.doc_reader import read_document

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    print("Enter the info you want to send an email about:")
    topic = input("➤ ")

    print("Enter path to the document with info (e.g., email_geneartion/docs/info.txt):")
    doc_path = input("➤ ")

    print("Enter recipient's email address:")
    to_email = input("➤ ")

    print("Enter your Gmail address:")
    from_email = input("➤ ")

    print("Enter your 16-character Gmail app password:")
    app_password = input("➤ ")

    doc_text = read_document(doc_path)

    # Automatically get all attachments from Attach_folders
    attachments = []
    attach_folder = "Attach_folders"
    if os.path.exists(attach_folder):
        for file in os.listdir(attach_folder):
            file_path = os.path.join(attach_folder, file)
            if os.path.isfile(file_path):
                attachments.append(file_path)

    inputs = {
        "topic": topic,
        "doc_text": doc_text,
        "current_year": str(datetime.now().year)
    }

    try:
        EmailGeneartion().crew().kickoff(inputs=inputs)

        with open("generated_email.txt", "r", encoding="utf-8") as f:
            email_content = f.read().strip()

        # Extract subject and body properly
        lines = email_content.splitlines()
        subject = "Generated Email"
        body_lines = []
        
        # Find subject line and separate it from body
        for i, line in enumerate(lines):
            if line.lower().startswith("subject:"):
                subject = line.replace("Subject:", "").replace("subject:", "").strip()
                # Skip empty lines after subject
                start_idx = i + 1
                while start_idx < len(lines) and not lines[start_idx].strip():
                    start_idx += 1
                body_lines = lines[start_idx:]  # Rest of the content is body
                break
        else:
            # If no subject line found, use entire content as body
            body_lines = lines
            
        # Join body lines and clean up
        body = "\n".join(body_lines).strip()
        
        # Remove any remaining "Subject:" text that might be in the body
        if body.lower().startswith("subject:"):
            body_lines = body.split('\n')[1:]
            body = "\n".join(body_lines).strip()

        # Only attach files from Attach_folders directory
        send_email(subject, body, to_email, from_email, app_password, attachments=attachments)

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    doc_text = read_document("sample_docs/sample.txt")

    inputs = {
        "topic": "Training Email",
        "doc_text": doc_text,
        "current_year": str(datetime.now().year)
    }

    try:
        EmailGeneartion().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    try:
        EmailGeneartion().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    doc_text = read_document("sample_docs/sample.txt")

    inputs = {
        "topic": "Testing Email",
        "doc_text": doc_text,
        "current_year": str(datetime.now().year)
    }

    try:
        EmailGeneartion().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

