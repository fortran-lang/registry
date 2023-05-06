from base_case import BaseTestClass
from uuid import uuid4

class TestLogin(BaseTestClass):

    def test_successful_login(self):
        """
        Test case to verify the behavior of the system when a user provides the correct login credentials and is able to successfully login to the system.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response code received from the server is not as expected.
        """
        email = "testemail@gmail.com"
        password = "123456"
        username = "testuser"

        signup_data = {
            "email": email,
            "password": password,
            "username": username
        }

        # Create a user first.
        response_for_signup = self.client.post("/auth/signup", data=signup_data)
        self.assertEqual(400, response_for_signup.json["code"])

        login_data = {
            "user_identifier": email,
            "password": password
        }

        # Login with the same user.
        response_for_login = self.client.post("/auth/login", data=login_data)
        self.assertEqual(200, response_for_login.json["code"])
    
    def test_unsuccessful_login(self):
        """
        Test case to verify the behavior of the system when a user provides incorrect login credentials and is unable to login to the system.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response code received from the server is not as expected.
        """
        email = "testemail@gmail.com"
        password = "123456"
        username = "testuser"

        signup_data = {
            "email": email,
            "password": password,
            "username": username
        }

        response_for_signup = self.client.post("/auth/signup", data=signup_data)
        self.assertEqual(200, response_for_signup.json["code"])

        login_data_incorrect_password = {
            "user_identifier": email,
            "password": password+'123',
        }

        login_data_incorrect_email = {
            "user_identifier": "hello"+email,
            "password": password,
        }

        # Login with incorrect password for the same user.
        response_for_login = self.client.post("/auth/login", data=login_data_incorrect_password)
        self.assertEqual(401, response_for_login.json["code"])

        # Login with incorrect email for the same user.
        response_for_login = self.client.post("/auth/login", data=login_data_incorrect_email)
        self.assertEqual(401, response_for_login.json["code"])


    def test_successful_logout(self):
        """
        Test case to verify the behavior of the system when a user successfully logs out of the system.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response code received from the server is not as expected.
        """
        email = "testuser@gmail.com"
        password = "123456"
        username = "testuser"

        data_for_signup = {
            "email": email,
            "password": password,
            "username": username
        }

        response_from_signup = self.client.post("/auth/signup", data=data_for_signup)
        self.assertEqual(200, response_from_signup.json["code"])

        data_for_logout = {
            "uuid": response_from_signup.json["uuid"],
        }

        response_from_logout = self.client.post('/auth/logout', data=data_for_logout)
        self.assertEqual(200, response_from_logout.json["code"])
    
    def test_unsuccessful_logout(self):
        """
        Test case to verify the behavior of the system when a user tries to log out with an invalid UUID.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response code received from the server is not as expected.
        """
        uuid = uuid4().hex

        data = {
            "uuid": uuid,
        }

        response = self.client.post('/auth/logout', data=data)
        self.assertEqual(404, response.json["code"])
