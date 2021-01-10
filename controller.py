"""
controller module for all initialisations and controlling further command inputs
"""


import random

from actions_and_roles.action_types import ActionTypes
from actions_and_roles.role import Role
from cli_handler import UserCLIHandler, AdminCLIHandler
from user.admin import Admin


class Controller:

    def __init__(self):
        """
        ~ Create an admin user
        ~ Initialise few roles
        """
        self.admin = Admin()
        self.current_user = self.admin.username
        Controller.generate_random_roles()
        self.admin_cli_handler = AdminCLIHandler(self)
        self.user_cli_handler = UserCLIHandler(self)
        self.user_to_action_mapping = {
            'admin': {
                0: self.admin_cli_handler.help,
                1: self.admin_cli_handler.relogin,
                2: self.admin_cli_handler.view_all_roles,
                3: self.admin_cli_handler.new_user,
                4: self.admin_cli_handler.new_role,
                5: self.admin_cli_handler.edit_role,
                6: self.admin_cli_handler.delete_role,
                7: self.admin_cli_handler.view_request,
                8: self.admin_cli_handler.delete_user,
                9: self.admin_cli_handler.list_users,
                10: self.admin_cli_handler.assign_role_to_user
            },
            'user': {
                0: self.user_cli_handler.help,
                1: self.user_cli_handler.relogin,
                2: self.user_cli_handler.view_all_roles,
                3: self.user_cli_handler.request_new_role,
                4: self.user_cli_handler.view_my_roles
            }
        }

        print(f"""\n\n
            Hi! You are logged in as {self.admin.username}
            Enter 0(numerical zero) for help
            Enter Ctrl+C to exit!
        """)

    @staticmethod
    def generate_random_roles():
        """
        Generate 3 random roles out of 8 possibilities(as of now because of only three action types)
        So we can denote them as 000 or 001 or 110 or 111 where each bit denotes if it's 1 it has access for it and 0
        for otherwise. First bit represents DELETE, second bit represents WRITE and third one for READ

        :return: list of random roles generated
        """

        role_names = set()
        roles_size = 0
        while roles_size != 3:
            role_name = ''
            for i in range(3):
                role_name += random.choice(['0', '1'])
            if role_name not in role_names:
                role_names.add(role_name)
                roles_size += 1

        for role_name in role_names:
            delete_access = ActionTypes.DELETE.value if role_name[0] == '1' else ''
            write_access = ActionTypes.WRITE.value if role_name[1] == '1' else ''
            read_access = ActionTypes.READ.value if role_name[2] == '1' else ''

            allowed_actions = [access for access in (delete_access, write_access, read_access) if access]
            Role(role_name, allowed_actions)

    def run(self):
        while True:
            try:
                print('\n\n')
                command = input()
                if not command:
                    continue
                command = int(command)
                active_user_username = 'admin' if self.current_user == self.admin.username else 'user'
                action = self.user_to_action_mapping[active_user_username].get(command)
                if action:
                    action()
                else:
                    print(f'ERROR: Not a valid command. Please try again')
            except KeyboardInterrupt:
                print(f'Make up for your mind for god"s sake')
                exit(0)
            except ValueError:
                print('ERROR: Not a valid integer command. Please try again')
