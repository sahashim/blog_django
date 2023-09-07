import base64

from django.core.files.storage import default_storage
from rest_framework_simplejwt.tokens import RefreshToken

from djangoProject4.celery import app
from .utils import generate_otp, send_otp_email
from .models import CustomUser

@app.task
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

def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh':
            str(refresh),
        'access':
            str(refresh.access_token),
        }

@app.task
def validate_otp_task(email,otp):
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return {'error': 'User with this email does not exist.task'}
    print(user.otp)
    if user.otp == otp:
        user.otp = None
        user.save()
        token = get_token_for_user(user)
        refresh = token['refresh']
        access = token['access']
        return {'refresh':refresh,'access':access, 'status':200}
    else:
        return {'error': 'Invalid OTP.task'}










@app.task
def register_user(data):
    print('here222222')
    try:
            image_data = base64.b64decode(data['image'])
            user = CustomUser.objects.create_user(
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                age=data['age'],
                education=['education'],
                bio=data['bio'],
                image=image_data
            )
            return {'message':'task created new user'}

    except Exception as e:
        print(e)
        raise e
