from .config import SMTP_SERVER, SMTP_PORT, EMAIL, PASSWORD, RECIPIENT_EMAIL
import smtplib
from fastapi import HTTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import logging
from jinja2 import Environment, FileSystemLoader
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, "email_template.html")
env = Environment(loader=FileSystemLoader(current_dir))
template = env.get_template("email_template.html")
logger = logging.getLogger(__name__)


def send_email(form_data):
    try:
        current_datetime = datetime.datetime.now()
        formatted_datetime = f" {current_datetime.strftime('%H:%M:%S')} ; {current_datetime.strftime('%Y-%m-%d')}"
        email_content = template.render(
            formatted_datetime=formatted_datetime,
            firstName=form_data.firstName,
            lastName=form_data.lastName,
            phone=form_data.phone,
            email=form_data.email,
            telegram=form_data.telegram,
            info=form_data.info
        )
        msg = MIMEMultipart("alternative")
        msg['From'] = EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = "New Contact Form Submission"
        part = MIMEText(email_content, "html")
        msg.attach(part)
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, RECIPIENT_EMAIL, msg.as_string())
        return {"message": "Email has been sent successfully"}
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
