from base_case import BaseTestClass
from uuid import uuid4

class TestLogout(BaseTestClass):

    def test_successfull_logout(self):
        email = "arteevraina@gmail.com"
        password="123456"

        data = {
            "email": email,
            "password": password,
        }

        response = self.client.post('/auth/login', data=data)

        data = {
            "uuid": response.json["uuid"],
        }


        response = self.client.post('/auth/login', data=data)
        self.assertEqual(200, response.status_code)
    
    def test_unsuccessfull_logout(self):
        uuid = uuid4().hex

        data = {
            "uuid": uuid,
        }

        response = self.client.post('/auth/logout', data=data)
        self.assertEqual(404, response.status_code)