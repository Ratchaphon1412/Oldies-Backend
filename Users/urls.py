from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django.urls import path,include
from .views import Register,OldiesTokenObtainPairView,AuthenticationJWT



urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', OldiesTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/',AuthenticationJWT.as_view(),name='auth_verify')

]
