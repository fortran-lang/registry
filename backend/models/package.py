class Package:
    def __init__(self, name, namespace, description, homepage, repository, 
                    copyright, license, createdAt, updatedAt, author, maintainers, tags, isDeprecated, versions=[], id=None):
        self.id = id
        self.name = name
        self.namespace = namespace
        self.description = description
        self.homepage = homepage
        self.repository = repository
        self.copyright = copyright
        self.license = license
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.author = author
        self.maintainers = maintainers
        self.tags = tags
        self.isDeprecated = isDeprecated
        self.versions = versions

        # Ensure that versions list only contains instances of Version class
        for v in self.versions:
            if not isinstance(v, Version):
                raise ValueError("All elements in 'versions' list must be of Version type.")

    # Create a to_json method.
    def to_json(self):
        # Convert versions to JSON.
        versions_json = [v.to_json() for v in self.versions]

        return {
            "name": self.name,
            "namespace": self.namespace,
            "description": self.description,
            "homepage": self.homepage,
            "repository": self.repository,
            "copyright": self.copyright,
            "license": self.license,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
            "author": self.author,
            "maintainers": self.maintainers,
            "tags": self.tags,
            "isDeprecated": self.isDeprecated,
            "versions": versions_json
        }
    
    # Create a from_json method.
    @staticmethod
    def from_json(json_data):
        # Extract the 'versions' list from the JSON data
        versions_data = json_data["versions"]

        # Convert each version JSON data to a Version object
        versions = [Version.from_json(v_data) for v_data in versions_data]

        return Package(
            id=json_data["_id"],
            name=json_data["name"],
            namespace=json_data["namespace"],
            description=json_data["description"],
            homepage=json_data["homepage"],
            repository=json_data["repository"],
            copyright=json_data["copyright"],
            license=json_data["license"],
            createdAt=json_data["createdAt"],
            updatedAt=json_data["updatedAt"],
            author=json_data["author"],
            maintainers=json_data["maintainers"],
            tags=json_data["tags"],
            isDeprecated=json_data["isDeprecated"],
            versions=versions
        )
    
class Version:
    def __init__(self, version, tarball, dependencies, createdAt, isDeprecated, download_url):
        self.version = version
        self.tarball = tarball
        self.dependencies = dependencies
        self.createdAt = createdAt
        self.isDeprecated = isDeprecated
        self.download_url = download_url

    # Create a to_json method.
    def to_json(self):
        return {
            "version": self.version,
            "tarball": self.tarball,
            "dependencies": self.dependencies,
            "createdAt": self.createdAt,
            "isDeprecated": self.isDeprecated,
            "download_url": self.download_url
        }
    
    # Create a from_json method.
    @staticmethod
    def from_json(json_data):
        return Version(
            version=json_data["version"],
            tarball=json_data["tarball"],
            dependencies=json_data["dependencies"],
            createdAt=json_data["createdAt"],
            isDeprecated=json_data["isDeprecated"],
            download_url=json_data["download_url"]
        )