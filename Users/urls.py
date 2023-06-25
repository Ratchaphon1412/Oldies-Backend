from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django.urls import path,include
from .views import *



urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', OldiesTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/',AuthenticationJWT.as_view(),name='auth_verify'),
    path('verify/email/',VerifyEmail.as_view(),name='verify_email'),
    path('auth/google/',GoogleOauthView.as_view(),name='login-with-google'),

]
