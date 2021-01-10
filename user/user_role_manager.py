from collections import defaultdict
import copy


class UserRoleDB:
    db = defaultdict(set)

    @classmethod
    def save(cls, username, role_name):
        cls.db[username].add(role_name)

    @classmethod
    def get_one(cls, user):
        return cls.db.get(user, set())

    @classmethod
    def get_all(cls):
        return copy.deepcopy(cls.db)

    @classmethod
    def delete(cls, user):
        return cls.db.pop(user, None)


class UserRoleManager:

    @classmethod
    def save(cls, user, role):
        UserRoleDB.save(user, role)

    @classmethod
    def get_one(cls, user):
        return UserRoleDB.get_one(user)

    @classmethod
    def get_all(cls):
        return UserRoleDB.get_all()

    @classmethod
    def delete(cls, user):
        return UserRoleDB.delete(user)
