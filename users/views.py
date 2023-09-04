from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from .serializers import RegisterSerializer, EditSerializer, ChangePasswordSerializer
from .utils import generate_otp, send_otp_email
from .models import CustomUser
from .tasks import send_otp_email_task


class LoginWithOTP(APIView):
    permission_classes = {IsAuthenticated,}
    def post(self, request):
        email = request.data.get('email', '')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        otp = generate_otp()
        user.otp = otp
        user.save()
        send_otp_email(email, otp)
        return Response({'message': 'OTP has been sent to your email.'}, status=status.HTTP_200_OK)


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh':
            str(refresh),
        'access':
            str(refresh.access_token),
        }


class ValidateOTP(APIView):

    def post(self, request):
        email = request.data.get('email', '')
        otp = request.data.get('otp', '')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        print(user.otp)
        if user.otp == otp:
            user.otp = None
            user.save()

            token = get_token_for_user(user)

            return Response(token , status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)




class RegisterView(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = RegisterSerializer(data= data)
            if not serializer.is_valid():
                print('not serializer valid')
                return Response({'data': serializer.errors,
                     'message':'something went wrong',
                 },status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'data':{},
                'message':'your account is created'
            },status=status.HTTP_201_CREATED)
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


