import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import CONFIG_SETTINGS
import logging

logger = logging.getLogger(__name__)


def send_email(to_email: str, subject: str, html_content: str):
    """
    Send an HTML email using SMTP configuration from settings.
    """
    try:
        if not CONFIG_SETTINGS.SMTP_HOST:
            logger.warning("SMTP settings not configured. Email not sent.")
            return

        msg = MIMEMultipart()
        msg["From"] = (
            f"{CONFIG_SETTINGS.EMAILS_FROM_NAME} <{CONFIG_SETTINGS.EMAILS_FROM_EMAIL}>"
        )
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(html_content, "html"))

        # Connect to SMTP server
        # Note: If SSL is required from start, use SMTP_SSL.
        # Here we assume STARTTLS pattern if TLS is True, or plain/SSL based on port/config usually.
        # Adjusting logic to be robust.

        if CONFIG_SETTINGS.SMTP_SSL:
            server = smtplib.SMTP_SSL(
                CONFIG_SETTINGS.SMTP_HOST, CONFIG_SETTINGS.SMTP_PORT
            )
        else:
            server = smtplib.SMTP(CONFIG_SETTINGS.SMTP_HOST, CONFIG_SETTINGS.SMTP_PORT)
            if CONFIG_SETTINGS.SMTP_TLS:
                server.starttls()

        with server:
            if CONFIG_SETTINGS.SMTP_USER and CONFIG_SETTINGS.SMTP_PASSWORD:
                server.login(CONFIG_SETTINGS.SMTP_USER, CONFIG_SETTINGS.SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"Email sent to {to_email}")
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP Authentication Error: {e}")
        error_msg = str(e)
        if "Application-specific password required" in error_msg:
            logger.error(
                "GMAIL AUTH ERROR: You need an App Password. Go to https://myaccount.google.com/apppasswords"
            )
        raise e
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        raise e
