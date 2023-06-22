from django.conf import settings
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .exceptions import EmailErrorSend




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
   


