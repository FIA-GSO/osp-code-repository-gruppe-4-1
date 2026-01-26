import uuid

from database.models import User


class Authenticated:
    def __init__(self, user_record: User):
        self.record = user_record
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return str(self.record.id)


def generate_token():
    return str(uuid.uuid4())