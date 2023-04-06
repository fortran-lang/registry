from base_case import BaseTestClass

class TestNamespaces(BaseTestClass):
    test_user_data = {
        "email": "testemail@gmail.com",
        "password": "testpassword",
        "username": "testuser",
    }

    test_namespace_data = {
        "namespace": "test_namespace",
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

