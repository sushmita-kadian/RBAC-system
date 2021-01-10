import copy

from utils import CaesarCipher


class UserDB:
    db = {}

    @classmethod
    def save(cls, username, user):
        cls.db[username] = user

    @classmethod
    def get_one(cls, username):
        return cls.db.get(username)

    @classmethod
    def get_all(cls):
        return copy.deepcopy(cls.db)

    @classmethod
    def delete(cls, username):
        return cls.db.pop(username, None)


class UserManager:

    @classmethod
    def save(cls, username, user_object):
        UserDB.save(username, user_object.to_dict())

    @classmethod
    def get_one(cls, username):
        return UserDB.get_one(username)

    @classmethod
    def get_all(cls):
        return UserDB.get_all()

    @classmethod
    def delete(cls, username):
        return UserDB.delete(username)


class UserBase:
    def __init__(self, username, password):
        self.username = username
        self.password = CaesarCipher.encrypt(password)

        UserManager.save(username, self)

    @staticmethod
    def authenticate_username(username):
        return UserManager.get_one(username)

    @staticmethod
    def authenticate_password(password, user_object):
        is_authentic = False
        encrypted_password = CaesarCipher.encrypt(password)
        if encrypted_password == user_object['password']:
            is_authentic = True

        return is_authentic

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password
        }
