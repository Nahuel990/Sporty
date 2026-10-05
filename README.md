# Sporty

QA assignment for the Single Bet Placement feature.

- `TestPlan/` - test plan
- `Bugs/` - bug reports with evidence
- `Automation/` - API and UI tests (Python, pytest, Selenium, requests)
- `Strategy/` - test plan

## Setup

Requires Python 3 and Chrome.

```bash
cd Automation
pip install -r requirements.txt
```

## Run

```bash
export BASE_URL="https://qae-assignment-tau.vercel.app"
export USER_ID="<your-user-id>"

pytest tests/test_api.py   
pytest tests/test_ui.py    
pytest                     
```

An HTML report is saved to `Automation/reports/report.html`.

## Extra tools

- `pytest-html` - HTML test report
- `webdriver-manager` - downloads the matching chromedriver

## Known failures

Both tests fail because of real bugs:

- `test_api.py` with stake `-10` - BUG-01, negative stake is accepted
- `test_ui.py` - BUG-03, receipt payout is stake x 2 instead of stake x odds

## Scaling

This project uses a plain `requirements.txt` to keep it simple. For a larger project, a tool like `uv` or `Poetry` would be a better fit: it pins every dependency (including sub-dependencies) in a lock file, so all machines and CI runs use the exact same versions.

Other improvements for a larger project:

- Run tests in CI on every push
- Use pytest markers to run API and UI tests separately
- Run tests in parallel with xdist
- Mark known bugs with xfail so the run stays green and links to the bug ID


