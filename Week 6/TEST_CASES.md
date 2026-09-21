# TEST CASES

## 1. Purpose

This document verifies that the integrated Free Fall 2.0 MVP operates consistently with the financial rules, market dataset, and user flow defined by the team.

Testing focuses on four areas:

1. **Core Trading Flow** — Buy, Sell, portfolio updates, and settlement.
2. **Margin & Financial Logic** — leverage, debt, equity, margin ratio, and forced liquidation.
3. **Market Data Validation** — price paths, session limits, and scenario integrity.
4. **Input & Boundary Handling** — invalid orders and critical financial thresholds.

A test is marked as:

- ✅ **PASS** — Actual result matches the expected result.
- ❌ **FAIL** — Actual result differs from the expected result.
- ⬜ **NOT TESTED** — Test has not yet been executed.


# 2. Testing Assumptions

| Parameter | Rule |
|---|---|
| Initial Capital | $10,000 |
| Leverage Tiers | 1×, 2×, 3×, 4× |
| Maintenance Margin | 20% |
| Margin Call | Triggered when Margin Ratio ≤ 20% |
| Forced Liquidation | Immediate after Margin Call |
| Liquidation Penalty | 5% |
| Market Universe | 50 assets |
| Number of Phases | 6 |
| Phase Duration | 300 ticks |
| Total Simulation | 1,800 ticks |
| AM Session | Phase Tick 1–150 |
| PM Session | Phase Tick 151–300 |
| Settlement | T+0.5 |
| Bank Savings Yield | 4.75% |
| Session Price Limit | ±30% |


# 3. Core Trading Tests

These tests verify whether the basic player interaction flow works correctly.

| ID | Test Case | Test Procedure | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| T01 | Cash Purchase | Select 1× leverage and buy a stock with sufficient cash. | Order executes. Cash decreases and stock holdings increase. No Margin Debt is created. | — | ⬜ |
| T02 | Leveraged Purchase | Select 2×, 3×, or 4× leverage and execute a valid purchase. | Position is created and the financed portion is recorded as Margin Debt. | — | ⬜ |
| T03 | Normal Sale | Sell shares currently held by the player. | Holdings decrease correctly and sale proceeds enter the settlement process. | — | ⬜ |
| T04 | T+0.5 Settlement | Sell shares during the AM session and continue to PM. | Proceeds become available according to the defined T+0.5 settlement rule. | — | ⬜ |
| T05 | Bank Savings | Transfer available funds into Bank Savings. | Available cash decreases and Bank Savings balance increases by the same amount. | — | ⬜ |
| T06 | Full Game Flow | Complete the simulation from initial setup through Phase 6. | Player reaches a valid final state without breaking the core flow. | — | ⬜ |


# 4. Margin & Financial Logic Tests

These tests verify the core financial engine of Free Fall 2.0.

| ID | Test Case | Test Procedure | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| F01 | Gross Exposure | Open one or more stock positions. | Gross Exposure equals the total market value of stock positions. | — | ⬜ |
| F02 | Margin Debt | Execute a leveraged purchase. | Margin Debt equals the financed portion of the position. | — | ⬜ |
| F03 | Net Equity | Create a portfolio with Margin Debt. | Net Equity = Cash + Portfolio Value − Margin Debt. | — | ⬜ |
| F04 | Effective Leverage | Create a leveraged portfolio. | Effective Leverage = Gross Exposure / Net Equity. | — | ⬜ |
| F05 | Margin Ratio | Revalue a leveraged portfolio after a price movement. | Margin Ratio = Net Equity / Stock Portfolio Value. | — | ⬜ |
| F06 | Margin Above Threshold | Maintain Margin Ratio above 20%. | No forced liquidation occurs. | — | ⬜ |
| F07 | Margin at Threshold | Reduce Margin Ratio to exactly 20%. | Margin Call is triggered and Forced Liquidation occurs immediately. | — | ⬜ |
| F08 | Margin Below Threshold | Reduce Margin Ratio below 20%. | Margin Call is triggered and Forced Liquidation occurs immediately. | — | ⬜ |
| F09 | Liquidation Penalty | Trigger Forced Liquidation. | Liquidated portfolio is charged the defined 5% penalty. | — | ⬜ |
| F10 | Post-Liquidation State | Observe account immediately after liquidation. | Positions, debt, equity, and liquidation status update consistently. | — | ⬜ |


# 5. Boundary & Invalid Input Tests

These tests verify that the system handles edge cases correctly.

| ID | Test Case | Test Procedure | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| B01 | 20.01% Margin Ratio | Create a state where Margin Ratio = 20.01%. | Position remains active. | — | ⬜ |
| B02 | 20.00% Margin Ratio | Create a state where Margin Ratio = 20.00%. | Immediate Forced Liquidation. | — | ⬜ |
| B03 | 19.99% Margin Ratio | Create a state where Margin Ratio = 19.99%. | Immediate Forced Liquidation. | — | ⬜ |
| B04 | Exact Buying Power | Submit an order equal to available Buying Power. | Order is accepted. | — | ⬜ |
| I01 | Exceed Buying Power | Submit an order exceeding available Buying Power. | Order is rejected and account state remains unchanged. | — | ⬜ |
| I02 | Sell More Than Holdings | Attempt to sell more shares than currently owned. | Order is rejected. | — | ⬜ |
| I03 | Zero Quantity | Submit an order with Quantity = 0. | Order is rejected. | — | ⬜ |
| I04 | Negative Quantity | Submit an order with Quantity < 0. | Order is rejected. | — | ⬜ |


# 6. Market Data Validation

Market data is tested separately from the simulation engine because the price paths are deterministic inputs to the game.

## 6.1 Dataset Structure

| Test | Expected Result | Actual Result | Status |
|---|---|---|---|
| 50 assets are present | 50 assets | — | ⬜ |
| Six phases are present | Phase 1–6 | — | ⬜ |
| Each phase contains 300 ticks | 300 ticks | — | ⬜ |
| Total simulation contains 1,800 ticks | 1,800 ticks | — | ⬜ |
| No missing price observations | 0 missing values | — | ⬜ |


## 6.2 Session Price Limit

Each asset is tested against the ±30% session price constraint.

For every price observation:

**Price Change (%) = (Current Price / Session Reference Price) − 1**

Valid range:

**−30% ≤ Price Change ≤ +30%**

Therefore:

- +30.00% → Valid
- −30.00% → Valid
- +30.01% → Breach
- −30.01% → Breach

The `market_scenario_audit.xlsx` workbook is used to automatically calculate the percentage movement of each asset and highlight any observation outside the permitted range.

| ID | Test | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| D01 | AM Session Price Limit | No asset exceeds ±30% relative to AM reference price. | — | ⬜ |
| D02 | PM Session Price Limit | No asset exceeds ±30% relative to PM reference price. | — | ⬜ |
| D03 | Scenario 1 Integrity | Scenario 1 passes the complete dataset audit. | — | ⬜ |
| D04 | Scenario 2 Integrity | Scenario 2 passes the complete dataset audit. | — | ⬜ |


# 7. Quantitative Calibration Tests

These tests verify that the market dataset produces the intended financial difficulty and achievable wealth range.

| ID | Test | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| Q01 | 1× Benchmark | Reproduce the best-case result under Cash / 1× strategy. | Result matches benchmark model. | — | ⬜ |
| Q02 | 2× Benchmark | Reproduce the best-case result under 2× leverage. | Result matches benchmark model. | — | ⬜ |
| Q03 | 3× Benchmark | Reproduce the best-case result under 3× leverage. | Result matches benchmark model. | — | ⬜ |
| Q04 | 4× Benchmark | Reproduce the best-case result under 4× leverage. | Result matches benchmark model. | — | ⬜ |
| Q05 | Phase 6 Crash | Verify the designed synchronized crash behavior in Phase 6. | Crash magnitude and direction match the calibrated scenario. | — | ⬜ |
| Q06 | Property Target Feasibility | Compare benchmark wealth with 3×, 20×, and 100× targets. | Targets remain consistent with the intended difficulty structure. | — | ⬜ |


# 8. Manual Financial Verification

Automated outputs should be cross-checked against at least one manually calculated portfolio.

### Example — 2× Leverage

Assume:

- Initial Equity = $10,000
- Gross Exposure = $20,000
- Margin Debt = $10,000

### Net Equity

Net Equity = Gross Exposure − Margin Debt

Net Equity = $20,000 − $10,000 = $10,000

### Effective Leverage

Effective Leverage = Gross Exposure / Net Equity

Effective Leverage = $20,000 / $10,000 = 2.00×

### Margin Ratio

Margin Ratio = Net Equity / Gross Exposure

Margin Ratio = $10,000 / $20,000 = 50%

### Expected Output

| Metric | Expected Value | Game Output | Match? |
|---|---:|---:|---|
| Gross Exposure | $20,000 | — | ⬜ |
| Margin Debt | $10,000 | — | ⬜ |
| Net Equity | $10,000 | — | ⬜ |
| Effective Leverage | 2.00× | — | ⬜ |
| Margin Ratio | 50.00% | — | ⬜ |
| Margin Call | No | — | ⬜ |


# 9. Test Ownership

Testing responsibilities follow the existing project roles.

| Test Area | Primary Responsibility |
|---|---|
| Trading engine and order execution | Technical Developer & Engine Architect |
| Margin Call and Forced Liquidation implementation | Technical Developer & Engine Architect |
| T+0.5 implementation | Technical Developer & Engine Architect |
| Invalid input handling | Technical Developer & Engine Architect |
| Market dataset integrity | Data Gatherer & Quantitative Calibration |
| ±30% price-limit audit | Data Gatherer & Quantitative Calibration |
| Best-case portfolio benchmarks | Data Gatherer & Quantitative Calibration |
| Scenario and user-flow consistency | Scenario Designer & Content Lead |
| Financial-rule verification | Coordinator & Mechanism Designer |
| UI state and visual feedback | UI/UX & Frontend Interface Designer |


# 10. Bug Handling

If a test fails:

1. Record the failed test ID.
2. Record the expected and actual results.
3. Add the issue to `BUG_LOG.md`.
4. Assign the issue to the responsible member.
5. Apply the required fix.
6. Re-run the same test.
7. Mark the test as **PASS** only after successful re-verification.


# 11. Completion Criteria

Week 6 testing is considered complete when:

- the core trading flow can be completed;
- financial calculations match the documented formulas;
- the 20% maintenance margin rule works correctly;
- Forced Liquidation executes correctly;
- Scenario 1 and Scenario 2 pass market-data validation;
- major invalid inputs are handled safely;
- critical bugs affecting the core flow are resolved or documented; and
- test results are recorded with reproducible evidence.
