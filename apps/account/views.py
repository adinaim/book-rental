from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    UserRegistrationSerializer, 
    PasswordChangeSerializer, 
    RestorePasswordSerializer,
    ResetPasswordSerializer
    )


User = get_user_model()

class RegistrationView(APIView):
    @swagger_auto_schema(request_body=UserRegistrationSerializer) 
    def post(self, request: Request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):  
            serializer.save()
            return Response(
                'Thanks for registration. Activate your account via link in your email.',
                status=status.HTTP_201_CREATED
                )

class AccountActivationView(APIView):
    def get(self, request, activation_code): 
        user = User.objects.filter(activation_code=activation_code).first()
        if not user:
            return Response(
                'Page not found.' ,
                status=status.HTTP_404_NOT_FOUND
                )
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response(
            'Account activated. You can login now.',
            status=status.HTTP_200_OK
            )

class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request:Request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'Your password has been changed.',
                status = status.HTTP_200_OK
            )

class RestorePasswordView(APIView):
    def post(self, request: Request):
        serializer = RestorePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_code()
            return Response(
                'Code for restoring your password has been sent ot your email.',
                status=status.HTTP_200_OK
            )

class ResetPasswordView(APIView):
    def post(self, request: Request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'Your password has been restored.',
                status=status.HTTP_200_OK
            )

class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def destroy(self, request: Request):
        username = request.user.username
        User.objects.get(username=username).delete()
        return Response(
            'Your account has been deleted.',
            status=status.HTTP_204_NO_CONTENT
        )