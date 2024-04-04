from django.core.mail import send_mail, get_connection
from django.conf import settings
from CoWinApp import EmailException
import random


def send_mail_using_smtp(otp, email_data):
    try:
        connection = get_connection(
            backend=settings.EMAIL_BACKEND,
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
        )
        message_with_otp = f"Your OTP is: {otp}. Please use this OTP to reset your password."
        send_mail(
            subject=email_data.get("subject"),
            message="",
            html_message=message_with_otp,
            from_email=email_data.get("from_email"),
            recipient_list=email_data.get("recipient"),
            connection=connection,
            fail_silently=False,
        )
    except Exception as exc:
        raise EmailException(exc)

