# Agent Runbook for SIC Balance Impact Tests

## Overview
This repo includes an agent-driven test automation flow for the dummy SIC GUI and Balance API.
The agent reads a matrix of test cases, records the initial balance for each subscription, executes the UI test, captures the final balance, and compares the expected balance impact.

## Recommended file structure

```
.github/prompts/run-single-test.prompt.md
.github/prompts/run-full-matrix.prompt.md
.vscode/mcp.json
dummy-api/server.js
dummy-ui/index.html
scripts/convert_excel_to_csv.py
test-data/balance-impact-matrix.csv
```

## Required tools
- Node.js
- Python 3.10+
- `mcp-server` package for the Balance API MCP
- `playwright` package for Playwright MCP
- GitHub Copilot licensed and enabled

## Setup steps

1. Clone the repository:
   ```bash
   git clone https://github.com/balaramireddy2025/Rating-Test-Automation.git
   cd Rating-Test-Automation
   ```

2. Install Python dependencies:
   ```bash
   python -m pip install --upgrade pip
   python -m pip install mcp-server httpx playwright pandas openpyxl
   python -m playwright install
   ```

3. Prepare the test matrix.
   - If your source is Excel, save it as CSV in `test-data/balance-impact-matrix.csv`.
   - Or use the helper script:
     ```bash
     python scripts/convert_excel_to_csv.py test-data/balance-impact-matrix.xlsx test-data/balance-impact-matrix.csv
     ```

4. Configure `.vscode/mcp.json` for your real API and MCP servers.
   - Set `BALANCE_API_BASE_URL` and `BALANCE_API_TOKEN`.
   - Optionally configure JIRA and Confluence servers if your flow updates issues/pages.

5. Start the dummy Balance API server:
   ```bash
   cd dummy-api
   node server.js
   ```

6. Start the dummy UI web server:
   ```bash
   cd ../dummy-ui
   python -m http.server 8080
   ```

7. Open the repository in VS Code:
   ```bash
   code .
   ```

8. Confirm the MCP tools are available in Copilot Chat:
   - `playwright`
   - `balance-api`
   - `jira` (if configured)

## How to run tests

### Single test
1. Open Copilot Chat in Agent mode.
2. Type `/run-single-test`.
3. Provide the requested values.

### Full matrix
1. Open Copilot Chat in Agent mode.
2. Type `/run-full-matrix`.
3. The agent will process every row in `test-data/balance-impact-matrix.csv`.

## Excel to CSV guidance

The agent reads a CSV matrix. Most teams should export the Excel sheet using Excel:
- File → Save As → CSV UTF-8
- Place the file in `test-data/balance-impact-matrix.csv`

If you want to keep the Excel file source, use `scripts/convert_excel_to_csv.py`.

## Matrix format

The CSV file must include these columns:

- `test_case_id`
- `test_case_name`
- `subscription_id`
- `expected_delta`
- `expected_outcome`
- `jira_issue_key`

Example:

```
TC-101,Recharge Promo Bonus,SUB-1001,50.00,PASS,QA-201
TC-102,Data Pack Deduction,SUB-1002,-20.00,PASS,QA-202
```

## Notes for production migration
- Replace dummy UI URL with the real Cloud GUI login page.
- Use the real API base URL and token.
- Update prompt instructions if the real UI navigation or login flow differs.
- Store production credentials securely, not in source control.
