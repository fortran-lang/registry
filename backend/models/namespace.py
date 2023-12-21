from datetime import datetime

class Namespace:
    def __init__(self, namespace, description, author, maintainers=[], admins=[], packages=[], created_at=datetime.now(), id=None):
        self.id = id
        self.namespace = namespace
        self.description = description
        self.createdAt = created_at
        self.author = author
        self.maintainers = maintainers
        self.admins = admins
        self.packages = []

    # Create a to_json method.
    def to_json(self):
        return {
            "namespace": self.namespace,
            "description": self.description,
            "createdAt": self.createdAt,
            "author": self.author,
            "maintainers": self.maintainers,
            "admins": self.admins,
            "packages": self.packages,
        }
    
    # Create a from_json method.
    @staticmethod
    def from_json(json_data):
        return Namespace(
            id=json_data["_id"],
            namespace=json_data["namespace"],
            description=json_data["description"],
            created_at=json_data["createdAt"],
            author=json_data["author"],
            maintainers=json_data["maintainers"],
            admins=json_data["admins"],
            packages=json_data["packages"],
        )
    