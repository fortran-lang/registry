import io
from base_case import BaseTestClass

class TestPackages(BaseTestClass):

    test_user_data = {
        "email": "testemail@gmail.com",
        "password": "testpassword",
        "username": "testuser",
    }
    
    test_package_data = {
        "name": "test_package",
        "namespace": "test_namespace",
        "version": "0.0.1",
        "license": "test_license",
        "copyright": "test_copyright",
        "description": "test_description",
        "namespace_description": "test_namespace_description",
        "tags": "test_tags",
        "dependencies": "test_dependencies",
    }

    @staticmethod
    def generate_tarball():
        # Create a file object to upload
        file_contents = b'Test file contents'
        tarball = io.BytesIO(file_contents)
        tarball.name = 'test.tar.gz'

        return tarball

   
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

        response = self.client.post("/auth/signup", data=TestPackages.test_user_data)
        self.assertEqual(200, response.json["code"])

        uuid = response.json["uuid"]

        TestPackages.test_package_data["uuid"] = uuid
        TestPackages.test_package_data["tarball"] = TestPackages.generate_tarball()

        response = self.client.post("/packages", data=TestPackages.test_package_data)
        self.assertEqual(200, response.json["code"])

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

        response = self.client.post("/auth/signup", data=TestPackages.test_user_data)
        self.assertEqual(200, response.json["code"])

        uuid = response.json["uuid"]
        
        TestPackages.test_package_data["uuid"] = uuid
        TestPackages.test_package_data["tarball"] = TestPackages.generate_tarball()

        response = self.client.post("/packages", data=TestPackages.test_package_data)
        self.assertEqual(200, response.json["code"])

        TestPackages.test_package_data["tarball"] = TestPackages.generate_tarball()

        response = self.client.post("/packages", data=TestPackages.test_package_data)
        self.assertEqual(400, response.json["code"])

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

        response = self.client.post("/auth/signup", data=TestPackages.test_user_data)
        self.assertEqual(200, response.json["code"])

        uuid = response.json["uuid"]

        TestPackages.test_package_data["uuid"] = uuid
        TestPackages.test_package_data["tarball"] = TestPackages.generate_tarball()

        response = self.client.post("/packages", data=TestPackages.test_package_data)
        self.assertEqual(200, response.json["code"])

        TestPackages.test_package_data["tarball"] = TestPackages.generate_tarball()

        # Make the previous one previous to the correct one.
        TestPackages.test_package_data["version"] = "0.0.0"

        response = self.client.post("/packages", data=TestPackages.test_package_data)

        self.assertEqual(400, response.json["code"])

    def test_unauthorized_upload(self):
        """
        Test case to verify the behaviour of the system if an unauthorized user tries to upload a version
        of a package.

        Parameters:
        None

        Returns:
        None

        Raises:
        AssertionError: If the response received from the server is not as expected.
        """

        response = self.client.post("/auth/signup", data=TestPackages.test_user_data)
        self.assertEqual(200, response.json["code"])

        uuid = response.json["uuid"]
        
        TestPackages.test_package_data["uuid"] = uuid
        TestPackages.test_package_data["tarball"] = TestPackages.generate_tarball()

        response = self.client.post("/packages", data=TestPackages.test_package_data)
        self.assertEqual(200, response.json["code"])
        
        # Sign up with different credentials.
        response = self.client.post("/auth/signup", data={
            "email": "test@gmail.com",
            "password": "testpassword",
            "username": "testusername"
        })
        self.assertEqual(200, response.json["code"])

        uuid = response.json["uuid"]

        TestPackages.test_package_data["uuid"] = uuid
        TestPackages.test_package_data["tarball"] = TestPackages.generate_tarball()
        TestPackages.test_package_data["version"] = "0.0.2"

        response = self.client.post("/packages", data=TestPackages.test_package_data)
        self.assertEqual(401, response.json["code"])

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

        response = self.client.post("/auth/signup", data=TestPackages.test_user_data)
        self.assertEqual(200, response.json["code"])

        uuid = response.json["uuid"]

        TestPackages.test_package_data["uuid"] = uuid
        TestPackages.test_package_data["tarball"] = TestPackages.generate_tarball()

        response = self.client.post("/packages", data=TestPackages.test_package_data)
        self.assertEqual(200, response.json["code"])

        response = self.client.get("/packages", query_string={
            "query": TestPackages.test_package_data["name"]
        })

        self.assertEqual(200, response.json["code"])

        response = self.client.get("/packages", query_string={
            "query": "somerandompackage"
        })

        self.assertEqual(200, response.json["code"])

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

        response = self.client.post("/auth/signup", data=TestPackages.test_user_data)
        self.assertEqual(200, response.json["code"])

        uuid = response.json["uuid"]

        TestPackages.test_package_data["uuid"] = uuid
        TestPackages.test_package_data["tarball"] = TestPackages.generate_tarball()

        response = self.client.post("/packages", data=TestPackages.test_package_data)
        self.assertEqual(200, response.json["code"])      

        response = self.client.get("/packages/test_namespace/test_package")

        self.assertEqual(200, response.json["code"])

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
        
        response = self.client.post("/auth/signup", data=TestPackages.test_user_data)
        self.assertEqual(200, response.json["code"])

        response = self.client.get("/packages/test_namespace/test_package")
        self.assertEqual(404, response.json["code"])