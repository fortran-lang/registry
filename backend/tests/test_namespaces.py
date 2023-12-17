from base_case import BaseTestClass

class TestNamespaces(BaseTestClass):

    email = "testemail@gmail.com"
    password = "123456"
    username = "testuser"

    test_namespace_data = {
        "namespace": "test_namespace",
        "namespace_description": "test namespace description"
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
            "username": self.username
        }

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

    def test_successful_namespace_creation(self):
        """
        Test case to verify the behaviour of the system when a namespace is created successfully.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response code received from the server is not as expected.
        """

        access_token = self.login()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = self.client.post("/namespaces", data=TestNamespaces.test_namespace_data, headers=headers)
        self.assertEqual(200, response.json["code"])

    def test_creating_existing_namespace(self):
        """
        Test case to verify the behaviour of the system when user tries to create an already existing namespace.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response code received from the server is not as expected.
        """

        access_token = self.login()

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        # Create a namespace entry in the database.
        response = self.client.post("/namespaces", data=TestNamespaces.test_namespace_data, headers=headers)
        self.assertEqual(200, response.json["code"])

        # Try to create the namespace entry with same namespace.
        response = self.client.post("/namespaces", data=TestNamespaces.test_namespace_data, headers=headers)
        self.assertEqual(400, response.json["code"])
    
    def test_create_upload_token_success(self):
        """
        Test case to verify the behaviour of the system when a user tries to generate upload token 
        successfully.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response code received from the server is not as expected.
        """

        access_token = self.login()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        # Create a namespace.
        response = self.client.post("/namespaces", data=TestNamespaces.test_namespace_data, headers=headers)
        self.assertEqual(200, response.json["code"])

        namespace_name = TestNamespaces.test_namespace_data['namespace']

        # Generate a token.
        response = self.client.post(f"/namespaces/{namespace_name}/uploadToken", headers=headers)
        self.assertEqual(200, response.json["code"])

    def test_create_upload_token_unauthorized(self):
        """
        Test case to verify the behaviour of the system when a user who is not a maintainer not an admin 
        of the namespace tries to create an upload token.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response code received from the server is not as expected.
        """

        access_token = self.login()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        # Create a namespace.
        response = self.client.post("/namespaces", data=TestNamespaces.test_namespace_data, headers=headers)
        self.assertEqual(200, response.json["code"])

        namespace_name = TestNamespaces.test_namespace_data['namespace']
        
        # Generate a token.
        response = self.client.post(f"/namespaces/{namespace_name}/uploadToken", headers=headers)
        self.assertEqual(200, response.json["code"])

        # Sign up using a new user.
        new_user_obj = {
            "username": "new_username",
            "password": "new_test_password",
            "email": "newtestemail@gmail.com",
            "user_identifier": "new_username"
        }

        response = self.client.post("/auth/signup", data=new_user_obj)
        self.assertEqual(200, response.json["code"])  

        response_for_login = self.client.post("/auth/login", data=new_user_obj)
        self.assertEqual(200, response_for_login.json["code"]) 
        access_token = response_for_login.json["access_token"]  

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        # Try to generate a token using a new user.
        # This user is not a maintainer nor an admin of the namespace.
        response = self.client.post(f"/namespaces/{namespace_name}/uploadToken", headers=headers)
        self.assertEqual(401, response.json["code"])

    def test_namespace_maintainers_list(self):
        """
        Test case to verify the behaviour of the system when a user tries to get the list of maintainers of a namespace.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response code received from the server is not as expected.
        """

        access_token = self.login()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        # Create a namespace.
        response = self.client.post("/namespaces", data=TestNamespaces.test_namespace_data, headers=headers)
        self.assertEqual(200, response.json["code"])

        namespace_name = TestNamespaces.test_namespace_data['namespace']

        # Get the list of maintainers.
        response = self.client.post(f"/namespaces/{namespace_name}/maintainers", headers=headers)
        self.assertEqual(200, response.json["code"])
        self.assertEqual(1, len(response.json["users"]))

    def test_namespace_admins_list(self):
        """
        Test case to verify the behaviour of the system when a user tries to get the list of admins of a namespace.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response code received from the server is not as expected.
        """

        access_token = self.login()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        # Create a namespace.
        response = self.client.post("/namespaces", data=TestNamespaces.test_namespace_data, headers=headers)
        self.assertEqual(200, response.json["code"])

        namespace_name = TestNamespaces.test_namespace_data['namespace']

        # Get the list of admins.
        response = self.client.post(f"/namespaces/{namespace_name}/admins", headers=headers)
        self.assertEqual(200, response.json["code"])
        self.assertEqual(1, len(response.json["users"]))