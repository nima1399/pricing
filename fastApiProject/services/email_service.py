import smtplib, ssl
from decouple import config

class EmailManager:
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = config("SENDER_EMAIL")
    password = config("SENDER_EMAIL_PASSWORD")

    @classmethod
    def send_email(cls, email: str, subject: str, message: str):
        message = f"Subject: {subject}\n\n{message}"

        context = ssl.create_default_context()
        with smtplib.SMTP(cls.smtp_server, cls.port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(cls.sender_email, cls.password)
            server.sendmail(cls.sender_email, email, message)