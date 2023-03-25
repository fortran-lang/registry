from base_case import BaseTestClass

class TestSignUp(BaseTestClass):

    def test_successful_signup(self):
        email = "arteevraina@gmail.com"
        password="123456"
        username="arteevraina"

        data = {
            "email": email,
            "password": password,
            "username": username,
        }

        response = self.client.post('/auth/signup', data=data)
        self.assertEqual(200, response.status_code)