import os
import pytest
import dotenv

ENV_TO_DOTENV = {
    "dev": "test_env/.env.dev",
    "stage": "test_env/.env.stage",
    "prod": "test_env/.env.prod",
}

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Test environment: dev/stage/prod",
    )

@pytest.fixture(scope="session", autouse=True)
def load_env(pytestconfig):
    env = pytestconfig.getoption("env")
    dotenv_path = ENV_TO_DOTENV.get(env, ".env")
    if os.path.exists(dotenv_path):
        dotenv.load_dotenv(dotenv_path, override=True)
    else:
        raise RuntimeError(f"Cannot find dotenv file for env '{env}': {dotenv_path}")

@pytest.fixture(scope="session")
def base_url(load_env):
    return os.environ["BASE_URL"]

@pytest.fixture(scope="session")
def engine(load_env):
    from microservice.database.engine import get_engine
    return get_engine()

@pytest.fixture(scope="session")
def total_users(engine, load_env):
    from microservice.database.users import get_users_from_db
    return len(get_users_from_db())

@pytest.fixture(scope="session")
def fill_test_data(base_url, engine, load_env):
    from sqlalchemy import text
    from microservice.db import users_db
    import httpx

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

@pytest.fixture
def users_api_client(base_url, load_env):
    from tests.api.user_api_client import UsersApiClient
    return UsersApiClient(base_url)