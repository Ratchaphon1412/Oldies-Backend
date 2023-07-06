#REST FRAMEWORK
from rest_framework.views import APIView,Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

#Utils
from django.utils.http import urlsafe_base64_decode
from .utils import *
from django.shortcuts import redirect


#Models
from Users import exceptions,models,serializers
from django.contrib.auth.models import update_last_login

# Create your views here.

class Register(APIView):
    def post (self,request):
        serializer = serializers.UserProfilesSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            EmailVerify.send_email_token(serializer.data['email'],serializer.instance)
            return Response(status=201,data={'status':'success',
                                            'messege':'Account Created',
                                            'username':serializer.data['username'],
            })
        else:
            raise exceptions.BadRequestBody
   

class AuthenticationJWT(APIView):
    
    def get(self,request):
        user,token = JWTAuthentication().authenticate(request)
        if token is not None:
           return Response(serializers.UserProfilesSerializer(user).data)
     
        
    

class VerifyEmail(APIView):
    def post(self,request):
        try:
            
            uid = urlsafe_base64_decode(request.data.get("uid")).decode()
            user = models.UserProfiles.objects.get(id=uid)
            user.is_email_verified = True
            user.save()
            
        except:
            raise exceptions.VerifyEmailError
        return Response(status=200,data={'status':'Verify success'})
    
class OldiesTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.OldiesTokenObtainPairSerializer   

class GoogleURL(APIView):
    def get(self,request):
        url = f'https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri=http://localhost:8000/api/auth/google/callback/&response_type=code&scope=https://www.googleapis.com/auth/userinfo.email%20https://www.googleapis.com/auth/userinfo.profile&prompt=select_account&access_type=offline'
        return redirect(url)


class GoogleOauthView(APIView):
    def get(self,request):
        serializer_class = serializers.GoogleOauthSerializer(data=request.GET)
        serializer_class.is_valid(raise_exception=True)
        
        validated_data = serializer_class.validated_data
        code = validated_data.get('code')
        
        access_token = GoogleOauth.google_get_access_token(code)
        
        user_data = GoogleOauth.get_google_user_data(access_token)
        
        
        
        profile_serializer = serializers.UserProfilesSerializer(data=user_data)
        if models.UserProfiles.objects.filter(email=user_data['email']).exists():
            user = models.UserProfiles.objects.get(email=user_data['email'])
            update_last_login(None,user)
            jwt = RefreshToken.for_user(user)
            
            return Response(status=200,data={'access':str(jwt.access_token),'refresh':str(jwt)})
        else:
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()
            jwt = RefreshToken.for_user(profile_serializer.instance)
            update_last_login(None,profile_serializer.instance)
            return Response(status=200,data={'access':str(jwt.access_token),'refresh':str(jwt)})
        
class FacebookURL(APIView):
    def get(self,request):
        url = f'https://www.facebook.com/v17.0/dialog/oauth?client_id={settings.FACEBOOK_ID}&redirect_uri=http://localhost:8000/api/auth/facebook/callback/&state={"odies_oauth=ABC"}&scope=public_profile,email'
        
        return redirect(url)
    
class FacebookOauthView(APIView):
    def get(self,request):
        serializer_class= serializers.FacebookOauthSerializer(data=request.GET)
        serializer_class.is_valid(raise_exception=True)
        validated_data = serializer_class.validated_data
        code = validated_data.get('code')
        profile = FacebookOauth.facebook_get_accesstoken(code)
        
        profile_serializer = serializers.UserProfilesSerializer(data=profile)
        if models.UserProfiles.objects.filter(email=profile['email']).exists():
            user = models.UserProfiles.objects.get(email=profile['email'])
            update_last_login(None,user)
            jwt = RefreshToken.for_user(user)
            
            return Response(status=200,data={'access':str(jwt.access_token),'refresh':str(jwt)})
        else:
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()
            jwt = RefreshToken.for_user(profile_serializer.instance)
            update_last_login(None,profile_serializer.instance)
            return Response(status=200,data={'access':str(jwt.access_token),'refresh':str(jwt)})
             
       
    
    