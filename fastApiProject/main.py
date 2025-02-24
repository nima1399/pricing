import smtplib, ssl
from decouple import config

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = config("SENDER_EMAIL")
receiver_email = "hekmatinima@gmail.com"
password = config("SENDER_EMAIL_PASSWORD")
message = """\
Subject: Hi there

This message is sent from Python."""

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)


# from fastapi import FastAPI
#
# app = FastAPI()
#
# @app.on_event("startup")
# async def startup_event():
#     asyncio.create_task(consume())