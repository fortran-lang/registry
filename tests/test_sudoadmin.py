from base_case import BaseTestClass
import os
from dotenv import load_dotenv

load_dotenv()

class TestSudoadmin(BaseTestClass):

    def test_successfull_sudo_signup(self):
        email = "henilp105@gmail.com"
        password = os.getenv("SUDO_PASSWORD")
        username = "henil"

        data = {
            "email": email,
            "password": password,
            "username": username,
        }

        response = self.client.post('/auth/signup', data=data)
        self.assertEqual(200, response.status_code)
    
    def test_unsuccessfull_sudo_signup(self):   # a regular signup will take place instead of sudo signup
        email = "henilp105@gmail.com"
        password = "12345678"
        username = "henil"

        data = {
            "email": email,
            "password": password,
            "username": username,
        }

        response = self.client.post('/auth/signup', data=data)
        self.assertEqual(200, response.status_code)