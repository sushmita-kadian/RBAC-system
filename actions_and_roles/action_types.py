from enum import Enum


class ActionTypes(Enum):
    """
    Enum class to keep constant action types
    This way addition of new roles and deletion of existing roles will be easy
    """

    READ = 'READ'
    WRITE = 'WRITE'
    DELETE = 'DELETE'

    @staticmethod
    def get_all_keys():
        return list(ActionTypes.__members__.keys())

    @staticmethod
    def get_all_values():
        return [key.value for key in ActionTypes]
