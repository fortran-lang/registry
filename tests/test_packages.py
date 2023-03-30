import io
from base_case import BaseTestClass

class TestPackages(BaseTestClass):
    
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

        email = "testemail@gmail.com"
        password="123456"
        username="testuser"

        data = {
            "email": email,
            "password": password,
            "username": username,
        }

        response = self.client.post("/auth/signup", data=data)
        uuid = response.json["uuid"]

        name = "test_package"
        namespace = "test_namespace"
        version = "1.0.0"
        license = "test_license"
        copyright = "test_copyright"
        description = "test_description"
        namespace_description = "test_namespace_description"
        tags = "test_tags"
        dependencies = "test_dependencies"

        # Create a file object to upload
        file_contents = b'Test file contents'
        tarball = io.BytesIO(file_contents)
        tarball.name = 'test.tar.gz'

        package_data = {
            "name": name,
            "namespace": namespace,
            "version": version,
            "license": license,
            "copyright": copyright,
            "description": description,
            "namespace_description": namespace_description,
            "tags": tags,
            "dependencies": dependencies,
            "uuid": uuid,
            "tarball": tarball
        }

        response = self.client.post("/packages", data=package_data)
        self.assertEqual(200, response.json["code"])