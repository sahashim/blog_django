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


class check_validate_task(APIView):
    def post(self,request):
        task_id = request.data.get('task_id', '')
        result = validate_otp_task.AsyncResult(task_id)
        if result.ready():
            try:
                data = result.get()
                token = result.get('token')
                status_code = data.get('status')
                return Response({'token': token, 'status': status_code}, status=status_code)

            except Exception as e:
                print(e)
                return Response({'message': 'something went wrong_check'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'Task is still running'}, status=status.HTTP_202_ACCEPTED)


class ValidateOTP(APIView):

    def post(self, request):
        email = request.data.get('email', '')
        otp = request.data.get('otp', '')

        try:
            result = validate_otp_task.delay(email,otp)
            return Response({'task_id': result.id}, status=status.HTTP_202_ACCEPTED)


        except Exception as e:
            print(e)
            return Response({'message':'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)




from users.tasks import register_user
import base64


class RegisterView(APIView):

    def post(self,request):
        try:
            data = request.data
            image_data = data['image'].read()

            image_base64 = base64.b64encode(image_data).decode('utf-8')

            data['image'] = image_base64

            result = register_user.delay(data)

            return Response({
                'data':{},
                'message':'Registration request successful',
            },status=status.HTTP_202_ACCEPTED)
        except Exception as e :
            print('hereeeee')
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


