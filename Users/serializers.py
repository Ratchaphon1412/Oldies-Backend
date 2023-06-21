from rest_framework import serializers
from .models import UserProfiles
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
        
        
    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class OldiesTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        return token
