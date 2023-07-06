from django.conf import settings
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .exceptions import EmailErrorSend
from django.urls import reverse
from .exceptions import *
import requests



class EmailVerify:
    def send_email_token(email,user):
        
       try:
           
            subject = "Your Account need to be verified"
            message = f'Click on the link to verify http://localhost:3000/verify/email/{user.username}/{urlsafe_base64_encode(force_bytes(user.id))}'
            
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail( subject, message, email_from, recipient_list )
       except:
           raise EmailErrorSend 
   
class GoogleOauth:
    def google_get_access_token(code):
        
        domain = settings.BASE_BACKEND_URL
        api_uri = reverse('login-with-google')
        redirect_uri = f'{domain}{api_uri}'
        data = {
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRETE,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }

        response = requests.post('https://oauth2.googleapis.com/token', data=data)
      
        
        if not response.ok:
            raise GoogleOauthAccessTokenError
        access_token = response.json()['access_token']
        
        return access_token
    
    def get_google_user_data(access_token):
        response = requests.get('https://www.googleapis.com/oauth2/v3/userinfo',params={'access_token':access_token})
        
        if not response.ok:
            raise GoogleOauthGetUserDataError
        response_json = response.json()
        profile = {
            'email':response_json['email'],
            'username':response_json['name'],
            'is_email_verified':response_json['email_verified'],
            'profile':response_json['picture'],
            'service':'Google',
        }
        
        return profile
    
class FacebookOauth:
    def facebook_get_accesstoken(code):
        secrete_key = settings.FACEBOOK_SECRETE
        client_id = settings.FACEBOOK_ID
        response = requests.get(f"https://graph.facebook.com/v17.0/oauth/access_token?client_id={client_id}&redirect_uri=http://localhost:8000/api/auth/facebook/callback/&client_secret={secrete_key}&code={code}")
        access_token = response.json()['access_token']
        
        response_profile = requests.get(f"https://graph.facebook.com/me?access_token={access_token}&fields=id,name,email,picture.width(500).height(500)")
        response_profile = response_profile.json()
        profile={
            'email':response_profile['email'],
            'username':response_profile['name'],
            'is_email_verified':True,
            'profile':response_profile['picture']['data']['url'],
            'service':'Facebook'
        }
        
        return profile
  
        
        
        
        
