from base_case import BaseTestClass

class TestNamespaces(BaseTestClass):
    test_user_data = {
        "email": "testemail@gmail.com",
        "password": "testpassword",
        "username": "testuser",
    }

    test_namespace_data = {
        "namespace": "test_namespace",
        "namespace_description": "test namespace description"
    }

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

        response = self.client.post("/auth/signup", data=TestNamespaces.test_user_data)
        self.assertEqual(200, response.json["code"])

        uuid = response.json["uuid"]
        TestNamespaces.test_namespace_data["uuid"] = uuid

        response = self.client.post("/namespaces", data=TestNamespaces.test_namespace_data)
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

        response = self.client.post("/auth/signup", data=TestNamespaces.test_user_data)
        self.assertEqual(200, response.json["code"])

        uuid = response.json["uuid"]
        TestNamespaces.test_namespace_data["uuid"] = uuid

        # Create a namespace entry in the database.
        response = self.client.post("/namespaces", data=TestNamespaces.test_namespace_data)
        self.assertEqual(200, response.json["code"])

        # Try to create the namespace entry with same namespace.
        response = self.client.post("/namespaces", data=TestNamespaces.test_namespace_data)
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

        response = self.client.post("/auth/signup", data=TestNamespaces.test_user_data)
        self.assertEqual(200, response.json["code"])

        uuid = response.json["uuid"]
        TestNamespaces.test_namespace_data["uuid"] = uuid

        # Create a namespace.
        response = self.client.post("/namespaces", data=TestNamespaces.test_namespace_data)
        self.assertEqual(200, response.json["code"])

        namespace_name = TestNamespaces.test_namespace_data['namespace']

        # Generate a token.
        response = self.client.post(f"/namespaces/{namespace_name}/uploadToken", data={"uuid": uuid})
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
        response = self.client.post("/auth/signup", data=TestNamespaces.test_user_data)
        self.assertEqual(200, response.json["code"])

        uuid = response.json["uuid"]
        TestNamespaces.test_namespace_data["uuid"] = uuid

        # Create a namespace.
        response = self.client.post("/namespaces", data=TestNamespaces.test_namespace_data)
        self.assertEqual(200, response.json["code"])

        namespace_name = TestNamespaces.test_namespace_data['namespace']
        
        # Generate a token.
        response = self.client.post(f"/namespaces/{namespace_name}/uploadToken", data={"uuid": uuid})
        self.assertEqual(200, response.json["code"])

        # Sign up using a new user.
        new_user_obj = {
            "username": "new_username",
            "password": "new_test_password",
            "email": "newtestemail@gmail.com"
        }

        response = self.client.post("/auth/signup", data=new_user_obj)
        self.assertEqual(200, response.json["code"])
        new_uuid = response.json["uuid"]

        # Try to generate a token using a new user.
        # This user is not a maintainer nor an admin of the namespace.
        response = self.client.post(f"/namespaces/{namespace_name}/uploadToken", data={"uuid": new_uuid})
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

        response = self.client.post("/auth/signup", data=TestNamespaces.test_user_data)
        self.assertEqual(200, response.json["code"])

        uuid = response.json["uuid"]
        TestNamespaces.test_namespace_data["uuid"] = uuid

        # Create a namespace.
        response = self.client.post("/namespaces", data=TestNamespaces.test_namespace_data)
        self.assertEqual(200, response.json["code"])

        namespace_name = TestNamespaces.test_namespace_data['namespace']

        # Get the list of maintainers.
        response = self.client.post(f"/namespaces/{namespace_name}/maintainers", data={"uuid": uuid})
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

        response = self.client.post("/auth/signup", data=TestNamespaces.test_user_data)
        self.assertEqual(200, response.json["code"])

        uuid = response.json["uuid"]
        TestNamespaces.test_namespace_data["uuid"] = uuid

        # Create a namespace.
        response = self.client.post("/namespaces", data=TestNamespaces.test_namespace_data)
        self.assertEqual(200, response.json["code"])

        namespace_name = TestNamespaces.test_namespace_data['namespace']

        # Get the list of admins.
        response = self.client.post(f"/namespaces/{namespace_name}/admins", data={"uuid": uuid})
        self.assertEqual(200, response.json["code"])
        self.assertEqual(1, len(response.json["users"]))