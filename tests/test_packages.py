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
