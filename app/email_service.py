# Mail
from aiosmtplib import SMTP
from email.message import EmailMessage
import smtplib
from .config import settings

def send_email(subject, body):
    try:
        message = EmailMessage()
        message["From"] = settings.EMAIL_FROM
        message["Subject"] = subject
        message["To"] = settings.EMAIL_TO
        message.set_content(body)
        with smtplib.SMTP(settings.SMTP_SERVER,settings.SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            smtp.send_message(message)

    except Exception as e:
        print("Email error:", e)