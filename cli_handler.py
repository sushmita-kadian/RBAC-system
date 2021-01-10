from actions_and_roles.action_types import ActionTypes
from actions_and_roles.role import Role, RoleManager
from user.base import UserManager
from user.user import User
from user.user_role_manager import UserRoleManager


class HandlerBase:
    def __init__(self, controller):
        self.controller = controller

    def relogin(self):
        username = input('Enter username: ')
        user_details = User.authenticate_username(username)
        if not user_details:
            print('ERROR: Username does not exist in system')
            return

        password = input('Enter password: ')
        if not User.authenticate_password(password, user_details):
            print('ERROR: Incorrect password')
            return

        self.controller.current_user = user_details['username']
        print(f'Hi! You are logged in as {user_details["username"]}')

    def view_all_roles(self):
        all_roles = RoleManager.get_all()
        if not all_roles:
            print('No roles found in system!! Create some')
            return

        for role_details in all_roles.values():
            print(f'Role name ---> {role_details["role_name"]}')
            for action_type, access_level in role_details["role_to_action_mapping"].items():
                print(f'\t\t {action_type} ---> {access_level}')
            print('\n')


class UserCLIHandler(HandlerBase):

    def help(self):
        print("""
            0 -> HELP
            1 -> Login as another user
            2 -> View all roles
            3 -> Request new role
            4 -> View my roles
        """)

    def request_new_role(self):
        print('You can ask to assign a role. This will be accepted/rejected on basis of admin decision')
        role_name = input('Enter role name: ')
        role_object = RoleManager.get_one(role_name)
        if not role_object:
            print(f'ERROR: {role_name} does not exists in system!!')
            return

        user_roles = UserRoleManager.get_one(self.controller.current_user)
        if role_name in user_roles:
            print(f'{role_name} is already assigned to you')
            return

        self.controller.admin.add_request(self.controller.current_user, role_name)
        print('Request successfully sent to admin!!')

    def view_my_roles(self):
        all_assigned_roles = UserRoleManager.get_one(self.controller.current_user)
        if not all_assigned_roles:
            print('No roles assigned!!')
            return
        for role in all_assigned_roles:
            print(f'Role name ---> {role}')


class AdminCLIHandler(HandlerBase):

    def help(self):
        print("""
            0 -> HELP
            1 -> Login as another user
            2 -> View all roles
            3 -> Create a new user
            4 -> Create a new role
            5 -> Edit an existing role
            6 -> Delete an existing role
            7 -> View user request
            8 -> Delete user
            9 -> List all users
            10 -> Assign a role to a user
        """)

    def new_user(self):
        username = input('Enter username: ')
        user_data = User.authenticate_username(username)
        if user_data:
            print(f'{username} already exists in system')
            return

        password = input('Enter password: ')
        retype_password = input('Re-type password: ')
        if password != retype_password:
            print(f'ERROR: {password} and {retype_password} do not match!!')
            return

        User(username, password)
        print('New user successfully created!!')

    def new_role(self):
        role_name = ''

        print('Enter y/n against all prompted actions')

        try:
            while True:
                delete_access = input('DELETE ACCESS: ')
                if delete_access not in ('y', 'n'):
                    print('ERROR: Invalid input: Please enter either `y` or `n`')
                else:
                    role_name += '1' if delete_access == 'y' else '0'
                    break

            while True:
                write_access = input('WRITE ACCESS: ')
                if write_access not in ('y', 'n'):
                    print('ERROR: Invalid input: Please enter either `y` or `n`')
                else:
                    role_name += '1' if write_access == 'y' else '0'
                    break

            while True:
                read_access = input('READ ACCESS: ')
                if read_access not in ('y', 'n'):
                    print('ERROR: Invalid input: Please enter either `y` or `n`')
                else:
                    role_name += '1' if read_access == 'y' else '0'
                    break

        except KeyboardInterrupt:
            print('Returning to main menu!!')
            return

        role_object = RoleManager.get_one(role_name)
        if role_object:
            print('This role already exists in system. Try viewing all roles and then create one')
            return

        delete_access = ActionTypes.DELETE.value if role_name[0] == '1' else ''
        write_access = ActionTypes.WRITE.value if role_name[1] == '1' else ''
        read_access = ActionTypes.READ.value if role_name[2] == '1' else ''

        allowed_actions = [access for access in (delete_access, write_access, read_access) if access]
        Role(role_name, allowed_actions)
        print('New role successfully created!!')

    def edit_role(self):
        print('Keep in mind: Editing role will change role name. Proceeding...')
        role_name = input('Enter role name: ')
        role_details = RoleManager.get_one(role_name)
        if not role_details:
            print('ERROR: No such role exist!! Try listing all roles and then editing')
            return

        new_role_name = ''
        print('Enter y/n against all prompted actions')
        while True:
            delete_access = input('NEW DELETE ACCESS: ')
            if delete_access not in ('y', 'n'):
                print('ERROR: Invalid input: Please enter either `y` or `n`')
            else:
                new_role_name += '1' if delete_access == 'y' else '0'
                break

        while True:
            write_access = input('NEW WRITE ACCESS: ')
            if write_access not in ('y', 'n'):
                print('ERROR: Invalid input: Please enter either `y` or `n`')
            else:
                new_role_name += '1' if write_access == 'y' else '0'
                break

        while True:
            read_access = input('NEW READ ACCESS: ')
            if read_access not in ('y', 'n'):
                print('ERROR: Invalid input: Please enter either `y` or `n`')
            else:
                new_role_name += '1' if read_access == 'y' else '0'
                break

        role_details = RoleManager.get_one(new_role_name)
        if role_details:
            print('ERROR: This role already exists in system. Try viewing all roles and then create one')
            return

        delete_access = ActionTypes.DELETE.value if new_role_name[0] == '1' else ''
        write_access = ActionTypes.WRITE.value if new_role_name[1] == '1' else ''
        read_access = ActionTypes.READ.value if new_role_name[2] == '1' else ''

        allowed_actions = [access for access in (delete_access, write_access, read_access) if access]

        RoleManager.delete(role_name)
        Role(new_role_name, allowed_actions)
        print('Role successfully edited!!')

    def delete_role(self):
        pass

    def view_request(self):
        request = self.controller.admin.fetch_request()
        if not request:
            print('No pending requests. Good Job!!')
            return

        confirmation = input(f'{request["username"]} is asking for role: {request["role_name"]}. '
                             f'Enter y to accept or n to reject')
        if confirmation == 'n':
            print('Request rejected !!')
            return

        self.assign_role_helper(request['username'], request['role_name'])

    def delete_user(self):
        username = input('Enter username: ')
        confirmation = input('This will delete the user from system. Enter yes/no: ')
        if confirmation == 'yes':
            user_data = UserManager.get_one(username)
            if not user_data:
                print('ERROR: No such user found!!')
                return

            UserManager.delete(username)

    def list_users(self):
        all_users = UserManager.get_all()
        all_users.pop(self.controller.admin.username)
        if not all_users:
            print('No users found in system!! Create some')
            return

        for user_detail in all_users.values():
            print(f'Username --> {user_detail["username"]}')

    def assign_role_helper(self, username, role_name):
        UserRoleManager.save(username, role_name)
        print(f'{role_name} successfully assigned to {username}!!')

    def assign_role_to_user(self):
        username = input('Enter username: ')
        user_data = User.authenticate_username(username)
        if not user_data:
            print(f'ERROR: {username} does not exists in system')
            return

        role_name = input('Enter role name: ')
        role_data = RoleManager.get_one(role_name)
        if not role_data:
            print(f'ERROR: {role_name} does not exists in system')
            return

        user_roles = UserRoleManager.get_one(username)
        if role_name in user_roles:
            print(f'{role_name} already assigned to user {username}!!')
            return

        self.assign_role_helper(username, role_name)
