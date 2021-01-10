from user.base import UserBase
from utils import CustomQueue


class Admin(UserBase):
    def __init__(self):
        """
        Initialize Admin user with `admin` username and `admin` password
        Always keep initialization of admin user with this settings here so only one change across all places is
        required in future
        """

        super().__init__(username='admin', password='admin')
        self.requests = CustomQueue()

    def fetch_request(self):
        return self.requests.get() if not self.requests.empty() else None

    def add_request(self, username, role_name):
        self.requests.put({
            'username': username,
            'role_name': role_name
        })
