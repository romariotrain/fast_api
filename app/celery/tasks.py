# import os
#
# from celery import shared_task
# from dotenv import load_dotenv
# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
# from pydantic import EmailStr
# from asgiref.sync import async_to_sync
#
#
# from app.celery_app import app
#
# load_dotenv()
#
# class ConnectionConfig:
#     MAIL_USERNAME = os.getenv("MAIL_USERNAME")
#     MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
#     MAIL_FROM = os.getenv("MAIL_FROM")
#     MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
#     MAIL_SERVER = os.getenv("MAIL_SERVER")
#     MAIL_STARTTLS = os.getenv("MAIL_STARTTLS") == "True"
#     MAIL_SSL_TLS = os.getenv("MAIL_SSL_TLS") == "True"
#     USE_CREDENTIALS = os.getenv("USE_CREDENTIALS") == "True"
#     VALIDATE_CERTS = os.getenv("VALIDATE_CERTS") == "True"
#
#
# @app.task
# def send_confirmation_email(email: EmailStr, username: str, token: str):
#     message = MessageSchema(
#         subject="Confirm your registration",
#         recipients=[email],
#         body=f"Hello {username},\n\nPlease confirm your registration by clicking the following link: http://http://127.0.0.1:8000/user/confirm?token={token}",
#         subtype="plain"
#     )
#
#     fm = FastMail(conf)
#     try:
#         async_to_sync(fm.send_message)(message)
#         return "Email sent successfully"
#     except Exception as e:
#         return f"Failed to send email: {str(e)}"
#
#
# @app.task
# def send_reset_password_email(email: str, username: str, token: str):
#     message = MessageSchema(
#         subject="Reset your password",
#         recipients=[email],
#         body=f"Hello {username},\n\nPlease reset your password by clicking the following link: http://127.0.0.1:8000/user/reset-password?token={token}",
#         subtype="plain"
#     )
#
#     fm = FastMail(conf)
#     async_to_sync(fm.send_message)(message)
#     return "Email sent successfully"