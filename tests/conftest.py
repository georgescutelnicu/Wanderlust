import pytest
from main import app
import os


@pytest.fixture
def flask_app():
    secret_key = os.environ.get('SECRET_KEY')
    if secret_key is None:
        raise ValueError("SECRET_KEY environment variable is not set")

    app.config.update(
        TESTING=True,
        SECRET_KEY=secret_key
    )
    with app.app_context():
        yield app


@pytest.fixture
def client(flask_app):
    with flask_app.test_client() as client:
        yield client
