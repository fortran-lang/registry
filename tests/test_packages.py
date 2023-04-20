import io
from base_case import BaseTestClass
from packages import check_token_expiry
from datetime import datetime

class TestPackages(BaseTestClass):

    test_user_data = {
        "email": "testemail@gmail.com",
        "password": "testpassword",
        "username": "testuser",
    }
    
    test_package_data = {
        "package_name": "test_package",
        "package_version": "0.0.1",
        "package_license": "MIT",
    }

    test_namespace_data = {
        "namespace": "test_namespace",
        "namespace_description": "Test namespace description"
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

        TestPackages.test_namespace_data["uuid"] = uuid

        # Try to create a namespace.
        response = self.client.post("/namespaces", data=TestPackages.test_namespace_data)
        self.assertEqual(200, response.json["code"])

        # Create an upload token for the namespace.
        response = self.client.post(f"/namespaces/{TestPackages.test_namespace_data['namespace']}/uploadToken", 
            data={
            "uuid": uuid
            }
        )
        self.assertEqual(200, response.json["code"])

        upload_token = response.json["uploadToken"]
        TestPackages.test_package_data["upload_token"] = upload_token
        TestPackages.test_package_data["tarball"] = TestPackages.generate_tarball()

        # Upload a package.
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

        TestPackages.test_namespace_data["uuid"] = uuid

        # Try to create a namespace.
        response = self.client.post("/namespaces", data=TestPackages.test_namespace_data)
        self.assertEqual(200, response.json["code"])

        # Create an upload token for the namespace.
        response = self.client.post(f"/namespaces/{TestPackages.test_namespace_data['namespace']}/uploadToken", 
            data={
            "uuid": uuid
            }
        )
        self.assertEqual(200, response.json["code"])

        upload_token = response.json["uploadToken"]
        TestPackages.test_package_data["upload_token"] = upload_token
        TestPackages.test_package_data["tarball"] = TestPackages.generate_tarball()

        # Upload the package.
        response = self.client.post("/packages", data=TestPackages.test_package_data)
        self.assertEqual(200, response.json["code"])

        TestPackages.test_package_data["tarball"] = TestPackages.generate_tarball()

        # Upload the package again.
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

        TestPackages.test_namespace_data["uuid"] = uuid

        # Try to create a namespace.
        response = self.client.post("/namespaces", data=TestPackages.test_namespace_data)
        self.assertEqual(200, response.json["code"])

        # Create an upload token for the namespace.
        response = self.client.post(f"/namespaces/{TestPackages.test_namespace_data['namespace']}/uploadToken", 
            data={
            "uuid": uuid
            }
        )
        self.assertEqual(200, response.json["code"])

        upload_token = response.json["uploadToken"]
        TestPackages.test_package_data["upload_token"] = upload_token
        TestPackages.test_package_data["tarball"] = TestPackages.generate_tarball()

        # Upload the package.
        response = self.client.post("/packages", data=TestPackages.test_package_data)
        self.assertEqual(200, response.json["code"])

        TestPackages.test_package_data["tarball"] = TestPackages.generate_tarball()
        
        # Upload the package again with version change.
        response = self.client.post("/packages", data={**TestPackages.test_package_data, "package_version": "somerandomstring"})

        self.assertEqual(400, response.json["code"])

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

        response = self.client.post("/auth/signup", data=TestPackages.test_user_data)
        self.assertEqual(200, response.json["code"])

        uuid = response.json["uuid"]

        TestPackages.test_namespace_data["uuid"] = uuid

        upload_token = "someinvalidrandomstring"
        TestPackages.test_package_data["upload_token"] = upload_token
        TestPackages.test_package_data["tarball"] = TestPackages.generate_tarball()

        # Upload the package.
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

        TestPackages.test_namespace_data["uuid"] = uuid

        # Try to create a namespace.
        response = self.client.post("/namespaces", data=TestPackages.test_namespace_data)
        self.assertEqual(200, response.json["code"])

        # Create an upload token for the namespace.
        response = self.client.post(f"/namespaces/{TestPackages.test_namespace_data['namespace']}/uploadToken", 
            data={
            "uuid": uuid
            }
        )
        self.assertEqual(200, response.json["code"])

        upload_token = response.json["uploadToken"]
        TestPackages.test_package_data["upload_token"] = upload_token
        TestPackages.test_package_data["tarball"] = TestPackages.generate_tarball()

        # Upload the package.
        response = self.client.post("/packages", data=TestPackages.test_package_data)
        self.assertEqual(200, response.json["code"])

        response = self.client.get("/packages", query_string={
            "query": TestPackages.test_package_data["package_name"]
        })

        self.assertEqual(200, response.json["code"])

        response = self.client.get("/packages", query_string={
            "query": "somerandompackage"
        })
        self.assertEqual(200, response.json["code"])
        self.assertEqual([], response.json["packages"])

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

        TestPackages.test_namespace_data["uuid"] = uuid

        # Try to create a namespace.
        response = self.client.post("/namespaces", data=TestPackages.test_namespace_data)
        self.assertEqual(200, response.json["code"])

        # Create an upload token for the namespace.
        response = self.client.post(f"/namespaces/{TestPackages.test_namespace_data['namespace']}/uploadToken", 
            data={
            "uuid": uuid
            }
        )
        self.assertEqual(200, response.json["code"])

        upload_token = response.json["uploadToken"]
        TestPackages.test_package_data["upload_token"] = upload_token
        TestPackages.test_package_data["tarball"] = TestPackages.generate_tarball()

        # Upload the package.
        response = self.client.post("/packages", data=TestPackages.test_package_data)
        self.assertEqual(200, response.json["code"])

        # Get the package.
        response = self.client.get(f"/packages/{TestPackages.test_namespace_data['namespace']}/{TestPackages.test_package_data['package_name']}")
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

        uuid = response.json["uuid"]

        TestPackages.test_namespace_data["uuid"] = uuid

        # Try to create a namespace.
        response = self.client.post("/namespaces", data=TestPackages.test_namespace_data)
        self.assertEqual(200, response.json["code"])

        # Create an upload token for the namespace.
        response = self.client.post(f"/namespaces/{TestPackages.test_namespace_data['namespace']}/uploadToken", 
            data={
            "uuid": uuid
            }
        )
        self.assertEqual(200, response.json["code"])

        response = self.client.get(f"/packages/{TestPackages.test_namespace_data['namespace']}/test_package")
        self.assertEqual(404, response.json["code"])

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
        response = self.client.post("/auth/signup", data=TestPackages.test_user_data)
        self.assertEqual(200, response.json["code"])

        uuid = response.json["uuid"]

        TestPackages.test_namespace_data["uuid"] = uuid

        # Try to create a namespace.
        response = self.client.post("/namespaces", data=TestPackages.test_namespace_data)
        self.assertEqual(200, response.json["code"])

        # Create an upload token for the namespace.
        response = self.client.post(f"/namespaces/{TestPackages.test_namespace_data['namespace']}/uploadToken", 
            data={
            "uuid": uuid
            }
        )
        self.assertEqual(200, response.json["code"])

        upload_token = response.json["uploadToken"]
        TestPackages.test_package_data["upload_token"] = upload_token
        TestPackages.test_package_data["tarball"] = TestPackages.generate_tarball()

        # Upload the package.
        response = self.client.post("/packages", data=TestPackages.test_package_data)
        self.assertEqual(200, response.json["code"])

        response = self.client.get(f"/packages/{TestPackages.test_namespace_data['namespace']}/{TestPackages.test_package_data['package_name']}/2.0.0")
        self.assertEqual(404, response.json["code"])

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

        response = self.client.post("/auth/signup", data=TestPackages.test_user_data)
        self.assertEqual(200, response.json["code"])

        uuid = response.json["uuid"]

        TestPackages.test_namespace_data["uuid"] = uuid

        # Try to create a namespace.
        response = self.client.post("/namespaces", data=TestPackages.test_namespace_data)
        self.assertEqual(200, response.json["code"])

        # Create an upload token for the namespace.
        response = self.client.post(f"/namespaces/{TestPackages.test_namespace_data['namespace']}/uploadToken", 
            data={
            "uuid": uuid
            }
        )
        self.assertEqual(200, response.json["code"])

        upload_token = response.json["uploadToken"]
        TestPackages.test_package_data["upload_token"] = upload_token
        TestPackages.test_package_data["tarball"] = TestPackages.generate_tarball()

        # Upload the package.
        response = self.client.post("/packages", data=TestPackages.test_package_data)
        self.assertEqual(200, response.json["code"])

        response = self.client.get(f"/packages/{TestPackages.test_namespace_data['namespace']}/{TestPackages.test_package_data['package_name']}/0.0.1")
        self.assertEqual(200, response.json["code"])

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

        response = self.client.post("/auth/signup", data=TestPackages.test_user_data)
        self.assertEqual(200, response.json["code"])

        uuid = response.json["uuid"]

        TestPackages.test_namespace_data["uuid"] = uuid

        # Try to create a namespace.
        response = self.client.post("/namespaces", data=TestPackages.test_namespace_data)
        self.assertEqual(200, response.json["code"])

        # Create an upload token for the namespace.
        response = self.client.post(f"/namespaces/{TestPackages.test_namespace_data['namespace']}/uploadToken", 
            data={
            "uuid": uuid
            }
        )
        self.assertEqual(200, response.json["code"])

        upload_token = response.json["uploadToken"]
        TestPackages.test_package_data["upload_token"] = upload_token
        TestPackages.test_package_data["tarball"] = TestPackages.generate_tarball()        

        # Upload the package.
        response = self.client.post("/packages", data={**TestPackages.test_package_data, "package_license": "ABC"})
        self.assertEqual(400, response.json["code"])

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