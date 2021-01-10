import copy

from actions_and_roles.action_types import ActionTypes
from exceptions.exceptions import InvalidActionTypesException


class RoleDB:
    db = {}

    @classmethod
    def save(cls, role_name, role):
        cls.db[role_name] = role

    @classmethod
    def get_one(cls, role_name):
        return cls.db.get(role_name)

    @classmethod
    def get_all(cls):
        return copy.deepcopy(cls.db)

    @classmethod
    def delete(cls, role_name):
        return cls.db.pop(role_name, None)


class RoleManager:

    @classmethod
    def save(cls, role_name, role_object):
        RoleDB.save(role_name, role_object.to_dict())

    @classmethod
    def get_one(cls, role_name):
        return RoleDB.get_one(role_name)

    @classmethod
    def get_all(cls):
        return RoleDB.get_all()

    @classmethod
    def delete(cls, role_name):
        RoleDB.delete(role_name)


class Role:

    def __init__(self, role_name: str, action_types: list = None):
        """
        Create a new role with action

        :param action_types: list of action types for which role is to be created
        """

        if action_types is None:
            action_types = []

        invalid_action_types = Role.validate_action_type(action_types)
        if invalid_action_types:
            raise InvalidActionTypesException(f'Invalid action types: {invalid_action_types} provided')

        self.role_name = role_name
        self.role_to_action_mapping = {}
        for action_type in ActionTypes:
            self.role_to_action_mapping[action_type.value] = True if action_type.value in action_types else False

        RoleManager.save(self.role_name, self)

    @staticmethod
    def validate_action_type(action_types: list):
        """
        validate whether action types provided is valid or not. For now it will only check that whether names provided
        are same or not.

        :return: list of all invalid action types provided
        """

        difference = set(action_types).difference(set(ActionTypes.get_all_values()))
        return list(difference)

    def to_dict(self):
        return {
            'role_name': self.role_name,
            'role_to_action_mapping': self.role_to_action_mapping
        }
