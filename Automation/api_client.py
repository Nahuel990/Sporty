import requests

from config import BASE_URL, USER_ID


class ApiClient:
    def __init__(self, base_url=BASE_URL, user_id=USER_ID, timeout=10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"x-user-id": user_id})

    def get_balance(self):
        return self.session.get(f"{self.base_url}/api/balance", timeout=self.timeout)

    def reset_balance(self):
        return self.session.post(f"{self.base_url}/api/reset-balance", timeout=self.timeout)

    def place_bet(self, match_id, selection, stake):
        body = {"matchId": match_id, "selection": selection, "stake": stake}
        return self.session.post(f"{self.base_url}/api/place-bet", json=body, timeout=self.timeout)
