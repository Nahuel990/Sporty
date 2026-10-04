import pytest

from api_client import ApiClient


@pytest.fixture
def api():
    client = ApiClient()
    yield client
    client.session.close()


@pytest.fixture
def reset_balance(api):
    api.reset_balance().raise_for_status()
