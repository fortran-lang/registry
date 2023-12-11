from base_case import BaseTestClass
from uuid import uuid4

class TestLogin(BaseTestClass):

    email = "testemail@gmail.com"
    password = "123456"
    username = "testuser"

    def test_successful_login(self):
        """
        Test case to verify the behavior of the system when a user provides the correct login credentials and is able to successfully login to the system.

        Parameters:
        None

        Returns:
        access_token (str): The access_token of the user who successfully logged in.

        Raises:
        AssertionError: If the response code received from the server is not as expected.
        """

        signup_data = {
            "email": self.email,
            "password": self.password,
            "username": self.username
        }

        # Create a user first.
        response_for_signup = self.client.post("/auth/signup", data=signup_data)
        self.assertEqual(200, response_for_signup.json["code"])

        login_data = {
            "user_identifier": self.email,
            "password": self.password
        }

        # Login with the same user.
        response_for_login = self.client.post("/auth/login", data=login_data)
        self.assertEqual(200, response_for_login.json["code"]) 
        return response_for_login.json["access_token"]
    
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

        self.test_successful_login()

        login_data_incorrect_password = {
            "user_identifier": self.email,
            "password": self.password+'123',
        }

        login_data_incorrect_email = {
            "user_identifier": "hello"+self.email,
            "password": self.password,
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

        access_token = self.test_successful_login()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response_from_logout = self.client.post('/auth/logout', headers=headers)
        self.assertEqual(200, response_from_logout.json["code"])