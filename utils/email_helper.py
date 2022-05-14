import os
import email, smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from utils.app_config import app_environment

def send_email_attachment(receiver_email, subject, body, file_path):
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = app_environment["sender_email"]
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Open PDF file in binary mode
    with open(file_path, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    filename = os.path.basename(file_path)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    with smtplib.SMTP(app_environment["smtp_server"], app_environment["smtp_port"]) as server:
        server.login(app_environment["smtp_user_name"], app_environment["smtp_password"])
        server.sendmail(app_environment["sender_email"], receiver_email, text)

def send_email_text(receiver_email, subject, body):
    from_mail = 'bot@nftiply.co'
    #  Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = from_mail
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    text = message.as_string()

    with smtplib.SMTP(app_environment["smtp_server"], app_environment["smtp_port"]) as server:
        server.login(app_environment["smtp_user_name"], app_environment["smtp_password"])
        server.sendmail(from_mail, receiver_email, text)