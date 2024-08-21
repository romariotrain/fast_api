import os

from dotenv import load_dotenv

load_dotenv()

# Вывод переменных окружения для проверки
print("MAIL_USERNAME:", os.getenv("MAIL_USERNAME"))
print("MAIL_PASSWORD:", os.getenv("MAIL_PASSWORD"))
print("MAIL_FROM:", os.getenv("MAIL_FROM"))
print("MAIL_PORT:", os.getenv("MAIL_PORT"))
print("MAIL_SERVER:", os.getenv("MAIL_SERVER"))
print("MAIL_STARTTLS:", os.getenv("MAIL_STARTTLS"))
print("MAIL_SSL_TLS:", os.getenv("MAIL_SSL_TLS"))
print("USE_CREDENTIALS:", os.getenv("USE_CREDENTIALS"))
print("VALIDATE_CERTS:", os.getenv("VALIDATE_CERTS"))
print("SQLALCHEMY_DATABASE_URL:", os.getenv("SQLALCHEMY_DATABASE_URL"))