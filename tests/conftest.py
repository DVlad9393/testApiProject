import dotenv
dotenv.load_dotenv()

import os
import httpx

from sqlalchemy import text
from microservice.db import users_db
from microservice.database.engine import engine
from microservice.database.users import get_users_from_db
import pytest

@pytest.fixture(scope="session", autouse=True)
def envs():
    dotenv.load_dotenv()

@pytest.fixture(scope="session")
def base_url():
    return os.getenv('BASE_URL')

@pytest.fixture(scope="session")
def total_users():
    return len(get_users_from_db())

@pytest.fixture(scope="session")
def fill_test_data(base_url):
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE userdata RESTART IDENTITY CASCADE;"))
        conn.commit()

    api_users = []
    for user in users_db.values():
        data = user.model_dump()
        response = httpx.post(f"{base_url}/api/users/", json=data)
        api_users.append(response.json())

    yield
    for user in api_users:
        httpx.delete(f"{base_url}/api/users/{user['id']}")