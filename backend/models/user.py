from datetime import datetime

class User:
    def __init__(self, username, email, password, uuid, 
                    lastLogout=None, is_verified=False, new_email='', 
                        login_at=None, created_at=datetime.now(), roles=[], author_of=[], id=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.lastLogout = lastLogout
        self.loginAt = login_at
        self.createdAt = created_at
        self.uuid = uuid
        self.isVerified = is_verified
        self.newEmail = new_email
        self.roles = roles
        self.authorOf = author_of

    # Create a to json method.
    def to_json(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'lastLogout': self.lastLogout,
            'loginAt': self.loginAt,
            'createdAt': self.createdAt,
            'uuid': self.uuid,
            'isVerified': self.isVerified,
            'newEmail': self.newEmail,
            'roles': self.roles,
            'authorOf': self.authorOf
        }
    
    # Create a from json method.
    @staticmethod
    def from_json(json_data):
        return User(
            id=json_data.get('_id'),
            username=json_data.get('username'),
            email=json_data.get('email'),
            password=json_data.get('password'),
            lastLogout=json_data.get('lastLogout'),
            login_at=json_data.get('loginAt'),
            created_at=json_data.get('createdAt'),
            uuid=json_data.get('uuid'),
            is_verified=json_data.get('isVerified'),
            new_email=json_data.get('newEmail'),
            roles=json_data.get('roles'),
            author_of=json_data.get('authorOf')
        )