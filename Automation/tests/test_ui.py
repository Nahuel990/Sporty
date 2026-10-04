import pytest

from pages.bet_page import BetPage

pytestmark = pytest.mark.usefixtures("reset_balance")

MATCH = "premier-league-chelsea-liverpool-2026-12-01"
HOME_TEAM = "Chelsea"
AWAY_TEAM = "Liverpool"
STAKE = 10


def test_place_single_bet_shows_correct_receipt(driver):
    """Chosen because it is the main user journey and checks the money
    values the user sees."""
    page = BetPage(driver)
    page.open()
    balance_before = page.get_balance()

    odds = page.select_odds(MATCH, "HOME")
    page.enter_stake(STAKE)
    page.place_bet()

    receipt = page.get_receipt_values()
    assert receipt["stake"] == pytest.approx(10.00)
    assert receipt["odds"] == pytest.approx(odds)
    assert receipt["payout"] == pytest.approx(STAKE * odds, abs=0.01)
    assert receipt["match"].index(HOME_TEAM) < receipt["match"].index(AWAY_TEAM)

    page.close_receipt()
    assert page.get_balance() == pytest.approx(balance_before - STAKE)
    assert page.is_bet_slip_empty()
