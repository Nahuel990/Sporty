
# Test Plan: Single Bet Placement // Sporty QA Bet

Scope: single bets on upcoming football matches, desktop Chrome, UI and APINot covered: live bets, multi-bets, mobile
I prioritised anything that touches money or the bet record

---

## TC-01: Place a valid bet and check the receipt
Priority: Critical

Risk: main flow of the app. If the receipt or balance is wrong, the user's bet record is wrong
Steps:
1. Reset balance (125.50)
2. Pick home odds on an upcoming match
3. Stake 2
4. Place bet
5. Check receipt, close it

Expected:
- Slip shows payout (stake x odd)
- Receipt has bet ID, match (home team first), selection, stake, payout, time
- Balance decrese(header and slip)
- Slip is empty after closing

---

## TC-02: Stake limits
Priority: Critical

Risk: bad stake values can mess up balances
Steps: try these stakes:
0.99, 1.00, 100.00, 100.01, -10, 0, 1.005, abc
(remove validation from input=id bet-slip-stake-input)

Expected:
- 1.00 and 100.00 work
- 0.99 gives "Minimum stake is €1.00" / 422 (api)
- 10001 gives "Maximum stake is €100.00" / 422 (api)
- the rest rejected, balance doesn't change

---

## TC-03: Can't bet more than the balance
Priority: Critical

Risk: users betting money they don't have
Steps:
1. Reset balance
2. Bet 100
3. Without refreshing, bet 77
4. Try the same in the API

Expected:
- Balance shows 25.5 after the first bet
- Second bet blocked with "Insufficient balance" / 422
- Balance never goes below 0

---

## TC-04: Only upcoming matches
Priority: High

Risk: betting on games that already finished
Steps:
1. Check match dates in the list
2. Try to bet on a past match (UI and API)

Expected: only upcoming matches listed, past ones rejected

---

## TC-05: Error modal
Priority: High

Risk: Rebet could place the bet twice
Steps:
1. Place a bet until it fails
2. Click Rebet
3. Fail again, click Close
4. Fail again, click X

Expected:
- Title "Something went wrong"
- Rebet retries, bet placed only once
- Close and X clear the slip

---

## TC-06: Odds filter
Priority: Medium

Risk: users don't see matches they should
Steps:
1. Min 6.60, max 10.00
2. Min 5.00, max 2.00

Expected:
- 6.60 odds are shown
- min > max gives an error
- match count updates

---

## Exploratory testing

Time box: about 1 hour, UI in Chrome and API in Bruno

Areas to explore:
- Stake field: long numbers, leading zeros, decimals, negative values, pasting text
- Placing several bets in a row without refreshing the page
- Balance: does the header and slip update after each bet and after a reset
- Receipt: compare every value with the bet slip and the match list
- Odds and date filters: edge values, invalid ranges, match count
- API: bad JSON, wrong types, missing fields, missing header, wrong method

Anything found here goes in the bug reports file.

---

## Spec questions and assumptions

Things in the spec that are unclear. I wrote down what I assumed for testing

1. Minimum stake: the validation table says €1.01, but the business rules and the UI message say €1.00
   Assumed: €1.00 is valid.

2. The place-bet response has no bet ID or timestamp, but the receipt must show both.
   Assumed: the UI generates them. Needs confirming, because the receipt should match a real saved bet

3. Matches only have kickoffDate (no time) and no status field
   Assumed: a match is upcoming if its date is today or later. Not clear how matches on today's date are handled

4. "Extra fields may be ignored by the API" doesn't say if they should be rejected or not.
   Assumed: ignoring them is fine

5. 409 "bet already in progress" isn't explained (how long it lasts, what the UI should show)
   Assumed: a second bet sent at the same time should get 409 and only one bet is placed.

6. Reset balance goes to the "initial configured value", which isn't stated in the spec.
   Assumed: €125.50, from the assignment (API resets to 120)
