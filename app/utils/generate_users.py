from faker import Faker

from app.database.users import create_user
from app.models.User import User


def generate_users(num_users):
    fake = Faker()

    for _ in range(num_users):
        user = User(
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            avatar=fake.image_url(),
        )
        return create_user(user)

