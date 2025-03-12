from datetime import datetime

from logger import logger
from services.django_service import DjangoService
from services.email_service import EmailManager


class MessageHandler:
    @classmethod
    def handle_message(cls, message):
        time = datetime.fromtimestamp(int(message.value['timestamp'])).strftime("%Y-%m-%d %H:%M:%S")
        emails = DjangoService.get_emails(message.key)
        email_message = f"New {message.key} price: {message.value['price']} in time {time}"
        for email in emails:
            EmailManager.send_email(
                email=email, subject=message.key, message=email_message
            )
