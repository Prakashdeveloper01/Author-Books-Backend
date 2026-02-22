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
        host = CONFIG_SETTINGS.SMTP_HOST
        port = CONFIG_SETTINGS.SMTP_PORT

        logger.info(
            f"Connecting to SMTP server at {host}:{port} (SSL: {CONFIG_SETTINGS.SMTP_SSL}, TLS: {CONFIG_SETTINGS.SMTP_TLS})"
        )

        if CONFIG_SETTINGS.SMTP_SSL:
            server = smtplib.SMTP_SSL(host, port, timeout=10)
        else:
            server = smtplib.SMTP(host, port, timeout=10)
            if CONFIG_SETTINGS.SMTP_TLS:
                server.starttls()

        with server:
            if CONFIG_SETTINGS.SMTP_USER and CONFIG_SETTINGS.SMTP_PASSWORD:
                server.login(CONFIG_SETTINGS.SMTP_USER, CONFIG_SETTINGS.SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"Email sent successfully to {to_email}")
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP Authentication Error: {e}")
        raise e
    except OSError as e:
        logger.error(
            f"Network error when connecting to {CONFIG_SETTINGS.SMTP_HOST}:{CONFIG_SETTINGS.SMTP_PORT}: {e}"
        )
        if e.errno == 101:
            logger.error(
                "Network is unreachable. This often means the outbound port is blocked or variables are missing in Railway Dashboard."
            )
        raise e
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        raise e
