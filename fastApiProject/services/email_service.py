import re
import smtplib
from decouple import config
import ssl
from logger import logger


class EmailManager:
    port = 587  # For starttls2
    smtp_server = "smtp.gmail.com"
    sender_email = config("SENDER_EMAIL")
    password = config("SENDER_EMAIL_PASSWORD")

    @classmethod
    def send_email(cls, email: str, subject: str, message: str):
        message = f"Subject: {subject}\n\n{message}"

        if not cls.is_valid_email(email):
            raise ValueError(f"Invalid email address: {email}")

        context = ssl.create_default_context()
        logger.info(
            f"Email : Sending to {email} | Subject: {subject} | Message: {message}"
        )
        with smtplib.SMTP(cls.smtp_server, cls.port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(cls.sender_email, cls.password)
            server.sendmail(cls.sender_email, email, message)

        logger.info(
            f"Email : Sent to {email} | Subject: {subject} | Message: {message}"
        )

    @staticmethod
    def is_valid_email(email):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_regex, email) is not None
