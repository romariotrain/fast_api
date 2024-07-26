from celery_app import celery_app
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr

conf = ConnectionConfig(
    MAIL_USERNAME="romanmorozevich1@gamil.com",
    MAIL_PASSWORD="Roma2003!",
    MAIL_FROM="romanmorozevich1@gamil.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


@celery_app.task
def send_confirmation_email(email: EmailStr, username: str, token: str):
    message = MessageSchema(
        subject="Confirm your registration",
        recipients=[email],
        body=f"Hello {username},\n\nPlease confirm your registration by clicking the following link: http://example.com/confirm?token={token}",
        subtype="plain"
    )

    fm = FastMail(conf)
    fm.send_message(message)