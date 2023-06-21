from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView,Response
from Users import exceptions,models,serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.

class Register(APIView):
    def post (self,request):
        try:
            check_user = models.UserProfiles.objects.filter(email=request.data['email'])
            if check_user.count() > 0:
                raise exceptions.NotAcceptableCreateAccount
            
            serializer = serializers.UserProfilesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            
            return Response(status=201,data={'status':'success',
                                             'messege':'Account Created',
                                            'username':serializer.data['username'],
            })
        except exceptions.NotAcceptableCreateAccount as e:
            raise e
        except:
            raise exceptions.BadRequestBody

class AuthenticationJWT(APIView):
    
    def get(self,request):
        user,token = JWTAuthentication().authenticate(request)
        if token is not None:
            
           return Response(serializers.UserProfilesSerializer(user).data)
        else:
            print("no token is provided in the header or the header is missing")
        return Response(status=200,data={'status':'success'})

    
class OldiesTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.OldiesTokenObtainPairSerializer   
