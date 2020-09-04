from django.shortcuts import render
from rest_framework import generics, status, views
from .serializers import RegisterSerializer, SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer, EmailVerificationSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError 
# smart_str, force_str, smart_bytes,thi sensures we sending conventional data that human can read/understnd
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
#all this utils will help in encoding the user token

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util

# Create your views here.

#register view
class RegisterView(generics.GenericAPIView):
    renderer_classes = (UserRenderer,) #rederer mapping 
    serializer_class = RegisterSerializer #mapping it to the serializer class in serializer.py
   

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user) #this help send data to serializer so we can go ahead to validate
        
        serializer.is_valid(raise_exception=True) 
        #this will run a method called validate from the serializer class in the serializer.py 
        #incase not valid, raise exception

        serializer.save() #this will run the save method from the serializer class in the serializer.py 
        
        user_data = serializer.data

        #setting up the token for a user but first we need to call the user
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token #this give us two tokens, the refresh and access token
        #after this token, create utils.py and create class utils to help us send email
        

        
            #note: we want the user to click the link in their email and the link should
            #be able bring them back to our app using the domain
        

        current_site = get_current_site(request).domain #requesting the domain url

        relativeLink = reverse('email-verify')
        #this will take the url name in the urls pattern and giving us the path
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        #this will get only the access token not th refrsh token
        email_body = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}
         #this will not return a protocol witn the domain
        #we nned to constuct a protocol thats why we concatinate http
        #also set the url pattern that will take them to a page when they click the email link
        #first set the api view before the url pattern

        #Sending the email using the send_email method without initiating the class intself
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)

# api view for verify email... map it to a url pattern
class VerifyEmail(views.APIView):
    # use generics.GenericAPIView  to see that the field shows in swagger
    #then change it to views.APIView to be able to have a field where the token will be entered 
    #this will give us access to a field though afdditional config is needed
    serializer_class = EmailVerificationSerializer #mapping it to the serializer class 
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
        #this is the addtional config for having the token field but import openapi and auto_schema
        #copy and paste the token sent to verify email into the token field in swagger to test it out
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token') 
       #getting the token sent to the email then decoding it to see which user was encodded
       #  in it
        try:
            payload = jwt.decode(token, settings.SECRET_KEY) #import settings
            #the secret key in settings.py is used to mmake tokens for the user
            #this is done by adding it to the user_id
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    renderer_classes = (UserRenderer,) #rederer mapping 

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#this will handle the token  creation and sending the toke to th user email
class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))#creating the id for user but in hashed format
            #with the above, we just encode the user id then below will create the token for the user
            token = PasswordResetTokenGenerator().make_token(user)#creating a token for the user
            #this will make sure the token used wont be available for another user so they wont change someonese password
 
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                #reverse will get us the link where the user will be going like after cliking the token in theri email
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
                #this means we are setting the reverselink to password-reset-confirm, 
                # that is the url the will handle the request when the user clicks our genrated token 
            absurl = 'http://'+current_site + relativeLink #adding http to the token
            email_body = 'Hello, \n Use link below to reset your password  \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


#this will be a get request which handles the request when the user clicks the token in their email
class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64)) #using smart_str to make it readible by human
            user = User.objects.get(id=id) #getting the id of the user clicking the link in the email
            
            #checking if a user has used a specific token before so they dont use it again .. reqquest new one
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        #incase user tempered with the token
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)


#handling the new password entry
class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
