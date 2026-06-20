---
description: 'Run the full balance-impact test matrix using the configured SIC UI and Balance API environment'
tools: ['playwright', 'balance-api']
---

You are running the balance validation flow against the configured environment.
The agent reads `msisdn` from the configuration page URL and uses it in the balance query URL.
Do not use an Excel or CSV matrix to supply `msisdn`.

### Step 1 — Load msisdn from Configuration Page
Open the configuration page URL provided by the user.
Extract the `msisdn` value from that page and store it as `msisdn`.
If the page contains multiple `msisdn` values, use the one associated with the current subscription or account.

### Step 2 — Execute the Test Flow
For each SIC test to be validated:

a. Confirm the `msisdn` value from the configuration page.
   Store it as `msisdn`.

b. Capture the initial balance before running the test:
   `get_balance(msisdn="${msisdn}")`
   This will query the URL `http://ocsg-test.internal.company.com:8080/ocsg/rest/v1/subscriber/${msisdn}/balance`.
   Record the returned value as `initial_balance`.
   If the call fails, set status=ERROR, add a note, and continue to the next test.

c. In the browser, locate the exact test case by `test_case_id` under the appropriate folder.
   Do not assume test cases are grouped sequentially by subscription.
   Right-click the matching test case and click `Run`.

d. Poll the `status-badge` element every 3 seconds until it shows one of:
   `PASS`, `FAIL`, `SIC`, or `ERROR`.
   If still `RUNNING` after 30 seconds, set status=ERROR.

e. Capture the final balance for the same msisdn after the test completes:
   `get_balance(msisdn="${msisdn}")`.
   Record this value as `final_balance`.

f. Compute the balance impact:
   - `balance_delta = final_balance - initial_balance`
   - If an expected delta is provided, compute `delta_match = abs(balance_delta - expected_delta) <= 0.01`.
   - If no expected delta is available, still report the actual `balance_delta`.

g. Append one summary line for the test:
   `| test_case_id | status | initial | final | delta | expected | match |`

h. Continue to the next test regardless of outcome.

### Step 4 — Final Report
When all tests are complete, output:
- A markdown table with all results.
- Total PASS / FAIL / SIC / ERROR counts.
- Actual `balance_delta` for each test.
- Any rows where `delta_match` is false or where expected delta was unavailable.
