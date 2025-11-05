import smtplib
from email.mime.text import MIMEText
from app.config import settings


async def send_reset_email(email: str, token: str):
    reset_link = f"http://92.118.115.96/reset-password?token={token}"

    msg = MIMEText(f"Для восстановления пароля перейдите по ссылке:\n{reset_link}")
    msg["Subject"] = "Восстановление пароля"
    msg["From"] = settings.SMTP_USER
    msg["To"] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        print(f"Email sent to {email}")
    except Exception as e:
        print(f"Email send error: {e}")
