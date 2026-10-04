import pytest

from config import MATCH_ID

pytestmark = pytest.mark.usefixtures("reset_balance")


@pytest.mark.parametrize("stake, expected_status", [
    (1.00, 200),
    (100.00, 200),
    (0.99, 422),
    (100.01, 422),
    (-10, 422),
    (0, 422),
    (1.005, 422),
    ("abc", 422),
])
def test_place_bet_stake_validation(api, stake, expected_status):
    """Chosen because stake validation protects user money and balances,
    and API checks are fast and stable."""
    balance_before = api.get_balance().json()["balance"]

    response = api.place_bet(MATCH_ID, "HOME", stake)
    assert response.status_code == expected_status

    balance_after = api.get_balance().json()["balance"]
    if expected_status == 422:
        assert balance_after == balance_before
    else:
        assert balance_after == pytest.approx(balance_before - stake)
