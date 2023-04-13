from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ImproperlyConfigured

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import json

from .models import User, Interest
from .functions import code_generator
from .serializers import InterestsSimpleSerializer, UserDetailsSerializer, UserUpdateSerializer

with open("secret.json") as f:
    secret = json.loads(f.read())

def get_secret(secret_name, secrets=secret):
    try:
        return secrets[secret_name]
    except:
        msg = "The variable %s does not exist" % secret_name
        raise ImproperlyConfigured(msg)

class RegisterView(APIView):

    def post(self, request):

        user = User()

        email = request.data.get('email')
        password = request.data.get('password')
        full_name = request.data.get('full_name')
        code_register = code_generator()

        # Verify if the user needs to be created or it is already registered
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'password':make_password(password),
                'full_name':full_name,
                'code_register':code_register
            }
        )

        if not created:
            return Response({'ok':'false', 'msg':'A user with this email is already registered'}, status=status.HTTP_409_CONFLICT)
        else:

            # Send code to confirm account
            subject = 'Account Confirmation'
            message = '<div><h4 style="text-align: center;"> Code Verification:</h4><p style="text-align: center;">'+str(code_register)+'</p></div>'
            sender = settings.EMAIL_SENDER

            # Send email
            send_mail(subject, message, sender, [email,], html_message=message)

            return Response({'ok':'true', 'msg':'A code has been sent to your email address. Please enter it here, in order to activate your account','userId':user.id}, status=status.HTTP_200_OK)


class VerifyAccountView(APIView):

    def post(self, request):

        code_verification = request.data.get('code')
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(id=user_id, code_register = code_verification)
            user.code_register = None
            user.is_active = True
            user.save()
            return Response({'ok':'true', 'msg':'Account was validated correctly. You can now log in!'}, status=status.HTTP_200_OK)
        except:
            return Response({'ok':'false', 'msg':'A user associated with this code, does not exists'}, status=status.HTTP_401_UNAUTHORIZED)

class UserDetailsView(APIView):

    permission_classes = [IsAuthenticated,]

    def get(self, request):

        jwt_authenticator = JWTAuthentication()

        response = jwt_authenticator.authenticate(request)

        if response is not None:
            user, token = response
            serializer = UserDetailsSerializer(user, context={'request':request})
            return Response({
                'ok': True,
                'userDetails':serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'ok': False,
                'msg': 'Invalid Token'
            }, status=status.HTTP_401_UNAUTHORIZED)

class UpdateUserView(RetrieveUpdateAPIView):

    permission_classes = [IsAuthenticated,]

    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()

class UpdateUserInformationView(RetrieveAPIView):

    permission_classes = [IsAuthenticated,]

    serializer_class = UserDetailsSerializer
    queryset = User.objects.all()

class UpdatePassWordRequestView(APIView):

    def post(self, request):

        userEmail = request.data.get('email')

        try:
            user = User.objects.get(email=userEmail)

            code = code_generator()

            user.code_register = code

            user.save()

            # Send email to update password
            subject = 'Update Password'
            message = '<div><h4 style="text-align: center;"> Update Password Link:</h4><p style="text-align: center;"><a style="text-decoration: none;" href="'+get_secret('UPDATE_PASSWORD_BASE_URL')+str(code)+'">Click Here to Follow The Link</a></p></div>'
            sender = settings.EMAIL_SENDER

            # Send email
            send_mail(subject, message, sender, [userEmail,], html_message=message)

            return Response({'ok':True, 'msg':'We have sent you a link to your email so you can change your password'}, status=status.HTTP_200_OK)     
        except:
            return Response({'ok':False, 'msg':'Email address does not exist'}, status=status.HTTP_400_BAD_REQUEST)

class VerifyCode(APIView):

    def post(self, request):

        code = request.data.get('code')

        try:
             user = User.objects.get(code_register=code)

             return Response({
                'ok': True,
                'msg': 'Code is valid'
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'ok': False,
                'msg': 'Code is not valid'
            }, status=status.HTTP_400_BAD_REQUEST)

class UpdatePasswordView(APIView):

    def post(self, request):

        code = request.data.get('code')

        new_password = request.data.get('newPassword')


        try:
            # find user by code
            user = User.objects.get(code_register=code)
            user.password = make_password(new_password)

            user.code_register = None

            user.save()

            return Response({
                'ok': True,
                'msg': 'Your password has been successfully updated'
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'ok': False,
                'msg': 'Invalid Code'
            }, status=status.HTTP_400_BAD_REQUEST)

""" Intersts views """
class ListInterstsView(ListAPIView):

    serializer_class = InterestsSimpleSerializer
    queryset = Interest.objects.all()
    

