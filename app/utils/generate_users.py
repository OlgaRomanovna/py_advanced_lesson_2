from faker import Faker

from app.database.users import create_user
from app.models.User import User


async def generate_users(num_users):
    fake = Faker()

    for _ in range(num_users):
        user = User(
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            avatar=fake.image_url(),
        )
        await create_user(user)

