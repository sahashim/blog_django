import base64

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from .serializers import RegisterSerializer, EditSerializer, ChangePasswordSerializer
from .utils import generate_otp, send_otp_email
from .models import CustomUser
from .tasks import *


class LoginWithOTP(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        send_otp_email_task.delay(email)  # Delay the task execution asynchronously

        return Response({'message': 'OTP task has been scheduled.'}, status=status.HTTP_200_OK)





class ValidateOTP(APIView):

    def post(self, request):
        email = request.data.get('email', '')
        otp = request.data.get('otp', '')

        try:
            result = validate_otp_task(email,otp)
            return Response(result , status=status.HTTP_200_OK)

        except Exception as e:
            return Response({},status=status.HTTP_400_BAD_REQUEST)



from users.tasks import register_user
from django.core.files.storage import default_storage
class RegisterView(APIView):

    def post(self,request):
        try:
            data = request.data
            result = register_user(data)

            return Response({
                'data':{},
                'message':'Registration request successful',
            },status=status.HTTP_202_ACCEPTED)
        except Exception as e :
            print(e)
            return Response({
                'data':{},
                'message':'something went wrong',
            },status=status.HTTP_400_BAD_REQUEST)



class EditView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EditSerializer
    lookup_field = 'pk'




class ChangePasswordView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


