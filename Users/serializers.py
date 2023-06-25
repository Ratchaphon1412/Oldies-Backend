from rest_framework import serializers
from .models import UserProfiles
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import redirect
from urllib.parse import urlencode
from django.conf import settings
from .exceptions import *

class UserProfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfiles
        fields = '__all__'
        extra_kwargs = {
            'password':{'write_only':True},
            'last_login':{'write_only':True},
            'is_superuser':{'write_only':True},
            'is_staff':{'write_only':True},
            'groups':{'write_only':True},
            'user_permissions':{'write_only':True},
        }
        

        
    def validate(self,data):
        if UserProfiles.objects.filter(email=data['email']).exists():
            if data['service'] == 'Local':
                raise NotAcceptableCreateAccount
        if data['service'] == 'Local':
            if data['password'] is not None:
                try:
                    validate_password(password=data['password'],user=UserProfiles)
                except Exception as e:
                    raise PasswordErrorCommon(e)
        
           
        return data
        
        
    def create(self,validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

class OldiesTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):
        if user.is_email_verified:
            token = super().get_token(user)
            # Add custom claims
            token['email'] = user.email
        else:
            raise EmailNotVerified
        
        return token


class GoogleOauthSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=255,required=False)
    error = serializers.CharField(max_length=255,required=False)

    def validate(self,data):
        if data.get('error') is not None:
            login_url = f'{settings.BASE_FRONTEND_URL}login'
            params = urlencode({'error': data.get('error')})
            return redirect(f'{login_url}?{params}')
        
        return data
        
        