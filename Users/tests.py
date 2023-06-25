from django.test import TestCase

# Create your tests here.

class UserAPIVIewTest(TestCase):
    
    def test_signup_api_view_password_validate(self):
        url = reversed('users:register')
        body = {
            "username":"ratchaphon1412",
            "email":"test456@gmail.com",
            "password":"111"  
            }
        response = self.client.post(url,body,format='json')
        self.assertEqual(response.status_code,400)
