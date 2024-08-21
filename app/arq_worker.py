import os

from arq import Worker
from arq.connections import RedisSettings, create_pool, ArqRedis
from dotenv import load_dotenv
from fastapi_mail import MessageSchema, FastMail, ConnectionConfig
from pydantic import EmailStr

load_dotenv()


async def get_redis_pool():
    return await create_pool(RedisSettings(host='localhost'))

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=os.getenv("USE_CREDENTIALS") == "True",
    VALIDATE_CERTS=os.getenv("VALIDATE_CERTS") == "True")


async def send_confirmation_email(ctx, email: EmailStr, username: str, token: str):
    message = MessageSchema(
        subject="Confirm your registration",
        recipients=[email],
        body=f"Hello {username},\n\nPlease confirm your registration by clicking the following link: http://127.0.0.1:8000/user/confirm?token={token}",
        subtype="plain"
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        return "Email sent successfully"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

async def send_reset_password_email(ctx, email: str, username: str, token: str):
    message = MessageSchema(
        subject="Reset your password",
        recipients=[email],
        body=f"Hello {username},\n\nPlease reset your password by clicking the following link: http://127.0.0.1:8000/user/reset-password?token={token}",
        subtype="plain"
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        return "Email sent successfully"
    except Exception as e:
        return f"Failed to send email: {str(e)}"


redis_url = "redis://redis:6379/0"
class WorkerSettings:
    functions = [send_confirmation_email, send_reset_password_email]
    redis_settings = RedisSettings(host="redis")


if __name__ == '__main__':
    redis = ArqRedis.from_url("redis://redis:6379/0")
    worker = Worker(WorkerSettings)
    worker.run()