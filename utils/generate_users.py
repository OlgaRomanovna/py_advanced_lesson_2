import json
import os
from faker import Faker


def generate_users(num_users):
    fake = Faker()
    users = []

    for i in range(1, num_users + 1):
        user = {
            "id": i,
            "email": fake.email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "avatar": fake.image_url()
        }
        users.append(user)

    root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    filename = os.path.join(root_directory, 'users.json')

    with open(filename, 'w') as file:
        json.dump(users, file, indent=2)

