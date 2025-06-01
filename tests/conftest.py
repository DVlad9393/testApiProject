import os

import pytest
import dotenv
dotenv.load_dotenv()

@pytest.fixture(autouse=True)
def envs():
    dotenv.load_dotenv()

@pytest.fixture(scope="session")
def base_url():
    return os.getenv('BASE_URL')