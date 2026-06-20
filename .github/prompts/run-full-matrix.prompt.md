---
description: 'Run the full balance-impact test matrix using the configured SIC UI and Balance API environment'
tools: ['playwright', 'balance-api', 'jira']
---

You are running the complete balance-impact test matrix against the configured environment.
The matrix source is `test-data/balance-impact-matrix.csv`.
Do not assume subscription IDs are sequential. Use the exact `subscription_id` from each row.

### Step 1 — Read the Test Matrix
Read the file `test-data/balance-impact-matrix.csv`.
Parse every row (skip the header). Each row must contain:
`test_case_id,test_case_name,subscription_id,expected_delta,expected_outcome,jira_issue_key`

### Step 2 — Login Once
Take a browser_snapshot.
If the login overlay is visible, log in with the configured credentials.
Do NOT re-login between rows; keep the session active across the full batch.

### Step 3 — Execute Each Row
For EACH row in the matrix, in order:

a. Call the balance-api tool:
   `get_balance(subscriptionId="${input:subscription_id}")`
   Record the returned value as `initial_balance`.
   If the call fails, set status=ERROR, add a note, and continue to the next row.

b. In the browser, locate the exact test case by `test_case_id` under the appropriate folder.
   Do not assume test cases are grouped sequentially by subscription.
   Right-click the matching test case and click `Run`.

c. Poll the `status-badge` element every 3 seconds until it shows one of:
   `PASS`, `FAIL`, `SIC`, or `ERROR`.
   If still `RUNNING` after 30 seconds, set status=ERROR.

d. Fetch the final balance for the same subscription regardless of status:
   `get_balance(subscriptionId="${input:subscription_id}")`.
   If the status is `PASS`, compute:
   - `balance_delta = final_balance - initial_balance`
   - `delta_match = abs(balance_delta - expected_delta) <= 0.01`
   If status is `FAIL`, `SIC`, or `ERROR`, final_balance may be recorded as null.

e. Update the JIRA issue `jira_issue_key` with:
   - Execution Status
   - Initial Balance
   - Final Balance
   - Balance Delta
   - Expected Delta
   - Delta Match
   - Test Case ID
   - Subscription ID
   - Timestamp

f. Append one summary line for the row:
   `| test_case_id | status | initial | final | delta | expected | match | jira |`

g. Continue to the next row regardless of outcome.

### Step 4 — Final Report
When all rows are complete, output:
- A markdown table with all results.
- Total PASS / FAIL / SIC / ERROR counts.
- Any rows where `delta_match` is false.
- Confirmation that JIRA issues were updated.
