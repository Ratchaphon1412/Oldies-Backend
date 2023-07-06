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
    path('auth/google/',GoogleURL.as_view(),name='google_url'),
    path('auth/google/callback/',GoogleOauthView.as_view(),name='login-with-google'),
    path('auth/facebook/',FacebookURL.as_view(),name="facebook_url"),
    path('auth/facebook/callback/',FacebookOauthView.as_view(),name="facebook_url")

]
