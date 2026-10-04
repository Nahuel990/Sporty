# Bug Reports

Environment: Chrome (latest), desktop
User: <something-something>
API tested with Bruno

---

## BUG-01: Negative stake is accepted and increases the balance

**Severity:** Critical

**Steps:**
1. POST /api/place-bet with header x-user-id
2. Body: {"matchId":"premier-league-manutd-chelsea","selection":"AWAY","stake":-1.999999999999999}
3. GET /api/balance

**Expected:** 422, stake rejected (spec 4.1: min €1.00). Balance unchanged.

**Actual:** 200 "Bet placed successfully". Payout is negative and balance goes up to 1000000000000121.9.

**Business impact:** Any user can give themselves unlimited money through the API.

**Evidence:** Bugs/Evidence

---

## BUG-02: User can bet more than their balance (overdraft)

**Severity:** Critical

**Steps:**
1. Reset balance (€125.50)
2. In the UI, select odds and place a bet of €100.00
3. Without refreshing, place a second bet of €77.00 so the total is more than the balance
4. Refresh the page

**Expected:** Second bet is blocked with "Insufficient balance" (spec 4.1, UI + API).

**Actual:** Both bets are accepted. Balance is not updated in the UI after the first bet, and the API doesn't check the balance. After refresh, "Insufficient balance" appears, but the bet was already placed. Balance is €-57.00.

**Business impact:** Users can stake money they don't have.

**Evidence:**  Bugs/Evidence

---

## BUG-03: Receipt shows payout as stake x 2 instead of stake x odds

**Severity:** High

**Steps:**
1. Select PSG vs Marseille, away (7.50)
2. Enter stake €1. Bet slip shows €7.50
3. Place bet

**Expected:** Receipt payout €7.50 (spec 2.4, must match the bet slip).

**Actual:** Receipt shows €2.00. The API returns the correct payout, so the bug is in the UI only.

**Business impact:** The user's record of what they're owed is wrong, which leads to disputes and loss of trust.

**Evidence:**  Bugs/Evidence

---

## BUG-04: Past matches are shown and can be bet on

**Severity:** High

**Steps:**
1. Open the app
2. Look at the match list under "Upcoming Football Matches"
3. Place a bet on a match tagged PAST (UI or API)

**Expected:** Only upcoming matches are listed. Bets on past matches are rejected (spec 1: pre-match only).

**Actual:** Matches tagged PAST (27 Feb, 1 Mar...) are listed and bets on them are accepted (e.g. premier-league-manutd-chelsea via API).

**Business impact:** Users can bet on games that are already finished, when the result is known.

**Evidence:**  Bugs/Evidence

---

## BUG-05: Malformed JSON returns 500 instead of 400

**Severity:** Medium

**Steps:**
1. POST /api/place-bet with body {hi: "jo"} (invalid JSON)

**Expected:** 400 malformed payload (spec 5.3).

**Actual:** 500.

**Business impact:** Bad input crashes the endpoint instead of being handled. Noise in monitoring, possible stability risk.

**Evidence:**  Bugs/Evidence

---

## BUG-06: Stake precision check can be bypassed

**Severity:** Medium

**Steps:**
1. POST /api/place-bet with stake 1.999999999999999

**Expected:** 422 invalid precision (spec 4.1: max 2 decimals).

**Actual:** 200, bet accepted. Note that 1.22222 is correctly rejected, so the check only fails for values close to 2 decimals.

**Business impact:** Invalid amounts get stored, which can cause rounding errors in balances and payouts.

**Evidence:**  Bugs/Evidence

---

## BUG-07: API returns currency USD instead of EUR

**Severity:** Medium

**Steps:**
1. POST /api/place-bet with a valid bet
2. Check "currency" in the response

**Expected:** "EUR" (spec 3 and 5.3).

**Actual:** "USD".

**Business impact:** Wrong currency in records, confusing for users and a problem for reporting.

**Evidence:**  Bugs/Evidence

---

## BUG-08: Odds filter accepts min greater than max

**Severity:** Medium

**Steps:**
1. Open the Odds filter
2. Set min 6.20, max 2.63
3. Click Apply

**Expected:** Invalid range rejected with a clear message (spec 2.6).

**Actual:** Filter is applied with no error. The list is empty.

**Business impact:** Users get an empty or confusing list with no explanation.

**Evidence:**  Bugs/Evidence

---

## BUG-09: Odds filter min is not inclusive

**Severity:** Medium

**Steps:**
1. Open the Odds filter
2. Set min 6.60
3. Apply

**Expected:** Matches with 6.60 odds are shown (spec 2.6: inclusive).

**Actual:** Matches with 6.60 are hidden. They only appear with min 6.59.

**Business impact:** Users miss matches they filtered for.

**Evidence:** Bugs/Evidence

---

## BUG-10: Stake field accepts unlimited digits and shows scientific notation

**Severity:** Low

**Steps:**
1. Select any odds
2. Type a very long number in the stake field (e.g. 99999999999999999999999999999999)

**Expected:** Input is limited, totals stay readable.

**Actual:** Input is accepted. Total Stake shows €1e+32, Payout shows €3.35e+32. Max stake message appears and Place Bet is disabled, so the bet can't be placed.

**Business impact:** Looks broken and unprofessional, but no financial risk.

**Evidence:**  Bugs/Evidence
