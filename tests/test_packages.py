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

        # Create a file object to upload
        file_contents = b'Test file contents'
        tarball = io.BytesIO(file_contents)
        tarball.name = 'test.tar.gz'

        TestPackages.test_package_data["tarball"] = tarball

        response = self.client.post("/packages", data=TestPackages.test_package_data)
        self.assertEqual(200, response.json["code"])
