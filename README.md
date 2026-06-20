# Dummy Test Environment — Quick Start

A self-contained sandbox to validate your Copilot + Playwright MCP + Balance API MCP setup before pointing it at the real app.

---

## What's in here

```
dummy-api/
  server.js                      ← Node.js Balance API (runs on :3001)
dummy-ui/
  index.html                     ← Simulated Cloud GUI test runner
.github/
  copilot-instructions.md        ← Standing rules for the agent
  prompts/
    run-single-test.prompt.md    ← Playbook for one test case
    run-full-matrix.prompt.md    ← Flow for config-page-driven balance validation
.vscode/
  mcp.json                       ← Wires playwright + balance-api into VS Code
```

---

## Step 1 — Start the dummy Balance API

```bash
cd dummy-api
node server.js
```

You should see:
```
✅  Dummy Balance API running at http://localhost:3001
```

Verify it's working: open http://localhost:3001/balance?subscriptionId=SUB-1001 in your browser.
Expected response:
```json
{ "subscriptionId": "SUB-1001", "balance": 500.0, "currency": "USD" }
```

---

## Step 2 — Open the dummy UI

Open `dummy-ui/index.html` directly in Chrome/Edge.  
You can do this from the terminal:

```bash
# Mac
open dummy-ui/index.html

# Windows
start dummy-ui/index.html

# Or just drag the file into a browser tab
```

The login overlay will appear. Credentials:
- **Username:** `testuser`
- **Password:** `Test@1234`

Once logged in, you'll see two test folders in the sidebar. Right-click any test case to see the context menu with a Run option.

---

## Step 3 — Open the workspace in VS Code

```bash
code .
```

Check that `.vscode/mcp.json` is present. VS Code will pick it up automatically.

---

## Step 4 — Verify all MCP servers are visible in Copilot

1. Open Copilot Chat (Ctrl+Shift+I or ⌘⇧I).
2. Switch to **Agent** mode.
3. Click **Configure Tools** (the tools icon).
4. Confirm you see tools from: `playwright` and `balance-api`.

If `playwright` tools aren't listed, open Command Palette → `MCP: List Servers` → Start playwright.

---

## Step 5 — Test the Balance API MCP in isolation

In Copilot Chat (agent mode), type:

> "Use the balance-api tool to get the balance for subscription SUB-1001"

Expected: the agent calls `get_balance("SUB-1001")` and shows balance 500.00.

---

## Step 6 — Test Playwright MCP in isolation

In Copilot Chat (agent mode), type:

> "Navigate to file:///[full path to dummy-ui/index.html] and take a snapshot. Tell me what elements you see."

Replace `[full path]` with the actual path. The agent should return an accessibility tree showing the login overlay elements.

---

## Step 7 — Run a single test case end to end

In Copilot Chat, type `/run-single-test` (VS Code will show the prompt file).

When prompted, enter:
- testCaseId: `TC-101`
- subscriptionId: `SUB-1001`
- expectedDelta: `50`

Watch the agent:
1. Fetch the initial balance for the specified subscription.
2. Log in to the dummy UI if needed.
3. Expand the test folder and right-click the matching test case.
4. Click Run and poll the `status-badge`.
5. Fetch the final balance after execution.
6. Compute the actual delta and compare it to the expected delta.

---

## Step 8 — Run the balance validation flow

In Copilot Chat, type `/run-full-matrix`.

The agent will:
- open the configuration page URL and extract `msisdn`
- call the balance API using that `msisdn`
- execute the matching SIC test case in the UI
- record the initial and final balance
- compare actual balance impact to expected delta
- report PASS / FAIL / SIC / ERROR counts

### Notes
- `msisdn` is sourced from the configuration page, not from a CSV or Excel file.
- Expected delta values may be provided as part of the test input or from the config page context.

### Expected behavior
- The agent reads `msisdn` from the config page.
- The agent calls the balance API URL with that `msisdn`.
- The agent runs the SIC test case and captures the final balance.
- The agent compares the actual delta to the expected delta.

### Example results
Expected output includes a table summarizing each test and counts of PASS / FAIL / SIC / ERROR.

---

## Reset balances between runs

If you run the matrix multiple times, balances will have shifted from the first run.
Reset them before re-running:

```bash
curl http://localhost:3001/reset
```

Or open http://localhost:3001/reset in your browser.

---

## Dummy credentials reference

| Thing          | Value                          |
|----------------|-------------------------------|
| UI login user  | `testuser`                    |
| UI login pass  | `Test@1234`                   |
| API base URL   | `http://localhost:3001`        |
| API auth       | not validated locally (any value works) |

---

## What to confirm before switching to the real app

- [ ] Playwright MCP can log in to the real Cloud GUI app using the same snapshot → click flow.
- [ ] The real Balance API base URL and token are configured in `.vscode/mcp.json` inputs.
- [ ] The test case names/IDs in the tree match your real test case definitions exactly.
- [ ] Balance delta tolerance (currently ±0.01) is appropriate for your currency precision.
