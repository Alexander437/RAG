import smtplib

from email.message import EmailMessage
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.db import SQLAlchemyUserDatabase

from backend.auth.models import User
from backend.database import get_async_session
from backend.settings import settings


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


def get_email_verification_template(username: str):
    email = EmailMessage()
    email['Subject'] = 'Example app'
    email['From'] = settings.SMTP_CONFIG.user
    email['To'] = settings.SMTP_CONFIG.user
    email.set_content(
        f"Hello {username}!"
    )
    return email


def send_email_verification(username: str):
    email = get_email_verification_template(username)
    with smtplib.SMTP(settings.SMTP_CONFIG.host, settings.SMTP_CONFIG.port) as server:
        server.starttls()  # only for mail.ru
        server.login(settings.SMTP_CONFIG.user, settings.SMTP_CONFIG.password)
        server.send_message(email)
