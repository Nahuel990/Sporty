import re

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import BASE_URL, USER_ID

ODDS_BUTTON_ID = "odds-{match}-{outcome}"
ODDS_VALUE = (By.CSS_SELECTOR, ".oddsButtonValue")
STAKE_INPUT = (By.ID, "bet-slip-stake-input")
PLACE_BET_BUTTON = (By.ID, "bet-slip-place-bet")
BET_SLIP_ITEMS = (By.CSS_SELECTOR, "#bet-slip .betSelectionCard")
RECEIPT = (By.CSS_SELECTOR, ".modalPanel")
RECEIPT_MATCH = (By.ID, "modal-success-match")
RECEIPT_STAKE = (By.ID, "modal-success-stake")
RECEIPT_ODDS = (By.ID, "modal-success-odds")
RECEIPT_PAYOUT = (By.ID, "modal-success-payout")
CLOSE_RECEIPT_BUTTON = (By.ID, "modal-success-close")
BALANCE = (By.ID, "header-balance")


def to_number(text):
    return float(re.search(r"-?\d+(\.\d+)?", text.replace(",", "")).group())


class BetPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        self.driver.get(f"{BASE_URL}/?user-id={USER_ID}")
        self.wait.until(EC.visibility_of_element_located(BALANCE))

    def select_odds(self, match, outcome):
        locator = (By.ID, ODDS_BUTTON_ID.format(match=match, outcome=outcome.lower()))
        button = self.wait.until(EC.element_to_be_clickable(locator))
        odds = to_number(button.find_element(*ODDS_VALUE).text)
        button.click()
        return odds

    def enter_stake(self, value):
        field = self.wait.until(EC.visibility_of_element_located(STAKE_INPUT))
        field.clear()
        field.send_keys(str(value))

    def place_bet(self):
        self.wait.until(EC.element_to_be_clickable(PLACE_BET_BUTTON)).click()

    def get_receipt_values(self):
        self.wait.until(EC.visibility_of_element_located(RECEIPT))
        return {
            "match": self._text(RECEIPT_MATCH),
            "stake": to_number(self._text(RECEIPT_STAKE)),
            "odds": to_number(self._text(RECEIPT_ODDS)),
            "payout": to_number(self._text(RECEIPT_PAYOUT)),
        }

    def close_receipt(self):
        self.wait.until(EC.element_to_be_clickable(CLOSE_RECEIPT_BUTTON)).click()
        self.wait.until(EC.invisibility_of_element_located(RECEIPT))

    def get_balance(self):
        return to_number(self._text(BALANCE))

    def is_bet_slip_empty(self):
        try:
            self.wait.until(lambda d: not d.find_elements(*BET_SLIP_ITEMS))
            return True
        except TimeoutException:
            return False

    def _text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text
