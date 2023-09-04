from celery import shared_task
from .utils import generate_otp, send_otp_email
from .models import CustomUser

@shared_task
def send_otp_email_task(email):
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return {'error': 'User with this email does not exist.'}

    otp = generate_otp()
    user.otp = otp
    user.save()
    send_otp_email(email, otp)
    return {'message': 'OTP has been sent to your email.'}