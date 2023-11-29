from base_case import BaseTestClass
from mongo import client
from server import app
from packages import check_token_expiry
from datetime import datetime
import random


class TestPackages(BaseTestClass):
    def setUp(self):
        app.config["SERVER_NAME"] = "localhost:9090"  # set server to localhost
        self.client = app.test_client()

        # This method is called before each test method
        # Reset or initialize variables here if needed
        self.uuid = None
        self.is_created = False
        self.is_namespace_created = False
        self.email = f"testemail{random.randint(1,100)}@gmail.com"
        self.password = "123456"
        self.username = f"testuser{random.randint(1,100)}"
        self.test_package_data = {
            "package_name": "test_package",
            "package_version": "0.0.1",
            "package_license": "MIT",
        }

        self.test_namespace_data = {
            "namespace": f"test_namespace{random.randint(1,100)}",
            "namespace_description": "Test namespace description",
        }

    def login(self):
        """
        Helper function to signup and login a user.

        Parameters:
        None

        Returns:
        uuid (str): The UUID of the user who successfully logged in.

        Raises:
        AssertionError: If the response code received from the server is not as expected.
        """

        signup_data = {
            "email": self.email,
            "password": self.password,
            "username": self.username,
        }
        if self.is_created:
            return self.uuid
        response_for_signup = self.client.post("/auth/signup", data=signup_data)
        self.assertEqual(200, response_for_signup.json["code"])

        login_data = {"user_identifier": self.email, "password": self.password}

        # Login with the same user.
        response_for_login = self.client.post("/auth/login", data=login_data)
        self.assertEqual(200, response_for_login.json["code"])
        self.is_created = True
        self.uuid = response_for_login.json["uuid"]
        return response_for_login.json["uuid"]

    def upload(self):
        """
        Helper function to upload a package.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response code received from the server is not as expected.
        """
        uuid = self.login()
        self.test_namespace_data["uuid"] = uuid

        # Try to create a namespace.
        if not self.is_namespace_created:
            response = self.client.post("/namespaces", data=self.test_namespace_data)
            self.assertEqual(200, response.json["code"])
            self.is_namespace_created = True

        # Create an upload token for the namespace.
        response = self.client.post(
            f"/namespaces/{self.test_namespace_data['namespace']}/uploadToken",
            data={"uuid": uuid},
        )
        self.assertEqual(200, response.json["code"])

        upload_token = response.json["uploadToken"]

        # Upload the package.
        response = self.client.post(
            "/packages",
            content_type="multipart/form-data",
            data={
                "upload_token": upload_token,
                **self.test_package_data,
                "dry_run": "false",
                "tarball": ("static/registry.tar.gz", "package.tar.gz"),
            },
        )

        response.json["uploadToken"] = upload_token
        return response.json

    def test_successful_package_upload(self):
        """
        Test case to verify the behaviour of the system when a user tries to upload a package successfully.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response code received from the server is not as expected.
        """
        response = self.upload()
        self.assertEqual(200, response["code"])
        print("test_successful_package_upload passed")

    def test_upload_existing_package(self):
        """
        Test case to verify the behaviour of the system when a user tries to upload already existing
        package in the registry.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response code received from the server is not as expected.
        """

        response = self.upload()
        self.assertEqual(200, response["code"])

        response = self.upload()
        self.assertEqual(400, response["code"])
        print("test_upload_existing_package passed")

    def test_incorrect_version_upload(self):
        """
        Test case to verify the behaviour of the system when a user tries to upload a package with
        incorrect version.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response received from the server is not as expected.
        """

        response = self.upload()
        self.assertEqual(200, response["code"])

        self.test_package_data["package_version"] = "somerandomstring"
        # Upload the package again with version change.

        response = self.upload()
        self.assertEqual(400, response["code"])
        print("test_incorrect_version_upload passed")

    def test_invalid_token_upload(self):
        """
        Test case to verify the behaviour of the system if an invalid token is used to upload a package.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response received from the server is not as expected.
        """

        self.test_package_data["upload_token"] = "somerandomtoken123"
        self.test_package_data["package_version"] = "0.0.1"
        response = self.upload()
        self.assertEqual(401, response["code"])
        print("test_invalid_token_upload passed")

    def test_search_package(self):
        """
        Test case to verify the behaviour of the system while searching for a package.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response received from the server is not as expected.
        """

        response = self.upload()
        self.assertEqual(200, response["code"])

        response = self.client.get(
            "/packages", query_string={"query": self.test_package_data["package_name"]}
        )

        self.assertEqual(200, response.json["code"])

        response = self.client.get(
            "/packages", query_string={"query": "somerandompackage"}
        )
        self.assertEqual(200, response.json["code"])
        self.assertEqual([], response.json["packages"])
        print("test_search_package passed")

    def test_get_exisiting_package(self):
        """
        Test case to verify the behaviour of the system while trying to get a package.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response received from the server is not as expected.
        """

        self.upload()
        # Get the package.
        response = self.client.get(
            f"/packages/{self.test_namespace_data['namespace']}/{self.test_package_data['package_name']}"
        )
        self.assertEqual(200, response.json["code"])
        print("test_get_exisiting_package passed")

    def test_get_nonexisting_package(self):
        """
        Test case to verify the behaviour of the system while trying to get non existing package.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response received from the server is not as expected.
        """

        response = self.upload()
        self.assertEqual(200, response["code"])

        response = self.client.get(
            f"/packages/{self.test_namespace_data['namespace']}/test_package_hello_world"
        )
        self.assertEqual(404, response.json["code"])
        print("test_get_nonexisting_package passed")

    def test_get_nonexisting_package_version(self):
        """
        Test case to verify the behaviour of the system while trying to get non existing package version.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response received from the server is not as expected.
        """

        response = self.upload()
        self.assertEqual(200, response["code"])

        response = self.client.get(
            f"/packages/{self.test_namespace_data['namespace']}/{self.test_package_data['package_name']}/2.0.0"
        )
        self.assertEqual(404, response.json["code"])
        print("test_get_nonexisting_package_version passed")

    def test_get_existing_package_version(self):
        """
        Test case to verify the behaviour of the system while trying to get a package using version.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response received from the server is not as expected.
        """

        response = self.upload()
        self.assertEqual(200, response["code"])

        response = self.client.get(
            f"/packages/{self.test_namespace_data['namespace']}/{self.test_package_data['package_name']}/0.0.1"
        )
        self.assertEqual(200, response.json["code"])
        print("test_get_existing_package_version passed")

    def test_package_invalid_license(self):
        """
        Test case to verify the behaviour of the system when a user tries to upload a package with invalid license identifier.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response received from the server is not as expected.
        """

        self.test_package_data["package_license"] = "ABC"
        response = self.upload()

        # Upload the package.
        self.assertEqual(400, response["code"])
        print("test_package_invalid_license passed")

    def test_check_token_expiry(self):
        """
        Test case to unit test the behaviour of the function to check if token is expired or not.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response received is not as expected.
        """
        created_at = datetime(22, 1, 1)
        response = check_token_expiry(created_at)
        self.assertEqual(True, response)

        created_at_now = datetime.now()
        response = check_token_expiry(created_at_now)
        self.assertEqual(False, response)
        print("test_check_token_expiry passed")

    def test_package_maintainers(self):
        """
        Test case to verify the behaviour of the system when a user tries to get the maintainers of a package.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response received from the server is not as expected.
        """

        # create a user
        uuid = self.login()

        # Upload the package.
        response = self.upload()
        self.assertEqual(200, response["code"])

        response = self.client.get(
            f"/packages/{self.test_namespace_data['namespace']}/{self.test_package_data['package_name']}/maintainers",
            data={"uuid": uuid},
        )
        self.assertEqual(200, response.json["code"])
        print("test_package_maintainers passed")
