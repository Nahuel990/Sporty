# Strategy and Recommendations

## Why these 2:

**API test: stake validation (TC-02)**
- Stake rules protect the user's money and balance
- API tests are fast and stable, and one parametrized test covers all the boundary values
- It catches BUG-01 (negative stake accepted)

**UI test: place a bet and check the receipt (TC-01)**
- It is the main user journey
- It checks the money values the user sees: stake, odds, payout, balance
- It catches BUG-03 (wrong payout on the receipt)

Other candidates like TC-03 (overdraft) and TC-04 (past matches) are good next steps, but these two cover the most risk first.

## Left as manual

- **Exploratory and visual checks:** things like BUG-10 (scientific notation) need a human eye
- **409 bet in progress(TC-05):** depends on timing, hard to reproduce reliably

## Recommendations

1. **Clarify the spec:** minimum stake (€1.00 vs €1.01), reset balance (USD120 vs €125.50), and where the bet ID and timestamp come from
2. **Run tests in CI:** API tests on every push, UI tests nightly in headless Chrome. Use uv or Poetry to lock dependency versions
3. **Error modal (TC-05):** set up a script that triggers the error (e.g. two bets at the same time for a 409) and run it manually, since it could be flaky in CI
4. **Get upcoming match IDs at runtime:** the tests use a fixed match ID, so once that match is in the past the tests will get 422. Getting an upcoming match from /api/matches keeps the tests running
