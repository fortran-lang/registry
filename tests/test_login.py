from base_case import BaseTestClass

class TestLogin(BaseTestClass):

    def test_successfull_login(self):
        email = "arteevraina@gmail.com"
        password="123456"

        data = {
            "email": email,
            "password": password,
        }

        response = self.client.post('/auth/login', data=data)
        self.assertEqual(200, response.status_code)
    
    def test_unsuccessfull_login(self):
        email = "artv@gmail.com"
        password="123456"

        data = {
            "email": email,
            "password": password,
        }

        response = self.client.post('/auth/login', data=data)
        self.assertEqual(401, response.status_code)