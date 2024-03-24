from base_case import BaseTestClass
import os
from dotenv import load_dotenv

load_dotenv()


class TestSignUp(BaseTestClass):

    def test_successful_signup(self):
        """
        Test case to verify the behavior of the system when a user provides the correct information and is able to successfully signup to the system.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response code received from the server is not as expected.
        """
        email = "testemail@gmail.com"
        password="123456"
        username="testuser"

        data = {
            "email": email,
            "password": password,
            "username": username,
        }

        response = self.client.post("/auth/signup", data=data)
        self.assertEqual(200, response.json["code"])

    def test_signup_without_data(self):
        """
        Test case to verify the behavior of the system when a user tries to sign up without providing all the required information such as email, password, or username.

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

        data_without_email = {
            "email": "",
            "password" : password,
            "username": username
        }

        data_without_password = {
            "email": email,
            "password": "",
            "username": username
        }

        data_without_username = {
            "email": email,
            "password": password,
            "username": ""
        }

        response_for_email = self.client.post("/auth/signup", data=data_without_email)
        self.assertEqual(400, response_for_email.json["code"])

        response_for_password = self.client.post("/auth/signup", data=data_without_password)
        self.assertEqual(400, response_for_password.json["code"])

        response_for_username = self.client.post("/auth/signup", data=data_without_username)
        self.assertEqual(400, response_for_username.json["code"])

    def test_signup_already_existing_user(self):
        """
        Test case to verify the behavior of the system when a user tries to sign up with an email, username, and password that already exists in the system.

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

        # Create a new user first.
        data = {
            "email": email,
            "password": password,
            "username": username,
        }

        response = self.client.post("/auth/signup", data=data)
        self.assertEqual(200, response.json["code"])

        # Try to signup again with the same user.
        response = self.client.post("/auth/signup", data=data)
        self.assertEqual(400, response.json["code"])

    def test_successful_sudo_signup(self):
        """
        Test case to verify the signup of a sudo user.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response code received from the server is not as expected.
        """
        email = "testuser@gmail.com"
        password = os.getenv("SUDO_PASSWORD")
        username = "testuser"

        data = {
            "email": email,
            "password": password,
            "username": username,
        }

        response = self.client.post('/auth/signup', data=data)
        self.assertEqual(200, response.status_code)
        return response.json