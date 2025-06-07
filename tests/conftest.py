import os
from microservice.db import users_db
import pytest
import dotenv
dotenv.load_dotenv()

@pytest.fixture(autouse=True)
def envs():
    dotenv.load_dotenv()

@pytest.fixture(scope="session")
def base_url():
    return os.getenv('BASE_URL')

@pytest.fixture(scope="session")
def total_users():
    return len(users_db)