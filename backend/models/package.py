class Package:
    def __init__(self, name, namespace, description, homepage, repository, 
                    copyright, license, created_at, updated_at, author, maintainers, keywords, is_deprecated, versions=[], id=None,
                        malicious_report={}, is_verified=False, is_malicious=False, security_status="No security issues found", ratings={"users": {}, "avg_ratings": 0}):
        self.id = id
        self.name = name
        self.namespace = namespace
        self.description = description
        self.homepage = homepage
        self.repository = repository
        self.copyright = copyright
        self.license = license
        self.created_at = created_at
        self.updated_at = updated_at
        self.author = author
        self.maintainers = maintainers
        self.keywords = keywords
        self.is_deprecated = is_deprecated
        self.versions = versions
        self.malicious_report  = malicious_report
        self.is_verified = is_verified
        self.is_malicious = is_malicious
        self.security_status = security_status
        self.downloads_stats = {}
        self.ratings = ratings

        # Ensure that versions list only contains instances of Version class
        for v in self.versions:
            if not isinstance(v, Version):
                raise ValueError("All elements in 'versions' list must be of Version type.")

    # Create a to_json method.
    def to_json(self):
        # Convert versions to JSON.
        versions_json = [v.to_json() for v in self.versions]

        # Convert maintainers to a list of strings
        maintainers_json = [str(maintainer) for maintainer in self.maintainers]


        return {
            "id": str(self.id),
            "name": self.name,
            "namespace": self.namespace,
            "description": self.description,
            "homepage": self.homepage,
            "repository": self.repository,
            "copyright": self.copyright,
            "license": self.license,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "author": self.author,
            "maintainers": maintainers_json,
            "keywords": self.keywords,
            "is_deprecated": self.is_deprecated,
            "versions": versions_json,
            "malicious_report": self.malicious_report,
            "is_verified": self.is_verified,
            "is_malicious": self.is_malicious,
            "security_status": self.security_status,
            "ratings": self.ratings,
        }
    
    # Create a from_json method.
    @staticmethod
    def from_json(json_data):
        # Extract the 'versions' list from the JSON data
        versions_data = json_data.get("versions", [])

        # Convert each version JSON data to a Version object
        versions = [Version.from_json(v_data) for v_data in versions_data]

        return Package(
            id=str(json_data.get("_id")),
            name=json_data.get("name"),
            namespace=json_data.get("namespace"),
            description=json_data.get("description"),
            homepage=json_data.get("homepage"),
            repository=json_data.get("repository"),
            copyright=json_data.get("copyright"),
            license=json_data.get("license"),
            created_at=json_data.get("created_at"),
            updated_at=json_data.get("updated_at"),
            author=json_data.get("author"),
            maintainers=json_data.get("maintainers"),
            keywords=json_data.get("keywords"),
            is_deprecated=json_data.get("is_deprecated"),
            versions=versions,
            malicious_report=json_data.get("malicious_report"),
            is_verified=json_data.get("is_verified"),
            is_malicious=json_data.get("is_malicious"),
            security_status=json_data.get("security_status"),
            ratings=json_data.get("ratings"),
        )
    
class Version:
    def __init__(self, version, tarball, dependencies, created_at, is_deprecated, download_url, is_verified=False):
        self.version = version
        self.tarball = tarball
        self.dependencies = dependencies
        self.created_at = created_at
        self.is_deprecated = is_deprecated
        self.download_url = download_url
        self.is_verified = is_verified

    # Create a to_json method.
    def to_json(self):
        return {
            "version": self.version,
            "tarball": self.tarball,
            "dependencies": self.dependencies,
            "created_at": self.created_at,
            "is_deprecated": self.is_deprecated,
            "download_url": self.download_url,
            "is_verified": self.is_verified,
        }
    
    # Create a from_json method.
    @staticmethod
    def from_json(json_data):
        return Version(
            version=json_data.get("version"),
            tarball=json_data.get("tarball"),
            dependencies=json_data.get("dependencies"),
            created_at=json_data.get("created_at"),
            is_deprecated=json_data.get("is_deprecated"),
            download_url=json_data.get("download_url"),
            is_verified=json_data.get("is_verified"),
        )