# Testing and Verification Specification

This document details the test framework, formal test case coverage, automated test suite, and defect resolution history for Free Fall 2.0.

---

## 1. Testing Framework and Methodology

The project uses a **4-tier testing framework** to ensure the simulation is both technically operational and financially explainable:

1. **Normal Execution:** Standard order execution, cash purchasing, leveraged purchasing, and debt accumulation.
2. **Boundary Analysis:** Exact mathematical thresholds for maintenance margin warnings (20.00%) versus forced liquidation triggers (< 20.00%).
3. **Invalid Input Handling:** Over-leveraging rejections, unowned stock short-sale blocks, negative quantity errors, and post-liquidation order lockouts.
4. **Financial Consistency:** Accounting identities, leverage caps, 5% liquidation penalty deductions, safe haven bank isolation, and T+0.5 settlement delivery queues.

All unit tests run via Python's standard `unittest` framework from the repository root:
```bash
python -m unittest discover tests
```
*Current test run: 66 tests across 6 modules, 100% passing.*

---

## 2. Test Suite Architecture (66 Automated Tests)

The test suite in `tests/` is organized into modular files:

| Test Module | Test Count | Scope & Verifications |
|---|---|---|
| [`tests/test_simulation_engine.py`](../tests/test_simulation_engine.py) | 8 | Core engine mechanics: 4× wipeout with 5% penalty, cash solvency, Safe Haven Bank balance isolation, T+0.5 intra-phase deliveries, mid-phase liquidation detection. |
| [`tests/test_week6_integration.py`](../tests/test_week6_integration.py) | 10 | Formal cases T01–T10: cash trading, 4× leverage, 20.00% exact boundary, 19.9914% liquidation trigger, purchasing power limits, short-sale rejection. |
| [`tests/test_bug_fixes_5_to_11.py`](../tests/test_bug_fixes_5_to_11.py) | 7 | Fixes for mid-phase liquidation checks, live tick delivery progression, and bank withdrawal limits. |
| [`tests/test_critical_bugs_c1_to_c5.py`](../tests/test_critical_bugs_c1_to_c5.py) | 7 | Server-authoritative pricing (anti-spoofing), phase transition boundaries, and state consistency. |
| [`tests/test_moderate_and_visual_fixes.py`](../tests/test_moderate_and_visual_fixes.py) | 12 | Margin multiplier propagation, zero-cash validations, liquidation UI button locking, and layout rules. |
| [`tests/test_complete_bug_report_45.py`](../tests/test_complete_bug_report_45.py) | 22 | Comprehensive regression suite, phase start-tick alignment, and 100% parity between `index.html` and `web/index.html`. |

---

## 3. Formal Test Cases (T01–T12)

The 12 formal test specifications define core financial and operational compliance:

| ID | Category | Inputs | Expected Output | Status |
|:---:|:---:|---|---|:---:|
| **T01** | Normal | Capital $10,000, 1.0× Cash, BUY 10 shares @ $500. | Cash: $5,000; Debt: $0; Equity: $10,000; Margin Ratio: 200%; Status: `HEALTHY`. | **PASS** |
| **T02** | Normal | Capital $10,000, 4.0× Tier, BUY 400 shares @ $100 ($40,000 cost). | Cash: $0; Debt: $30,000; Equity: $10,000; Leverage: 4.0×; Margin Ratio: 25.0%; Status: `NORMAL`. | **PASS** |
| **T03** | Boundary | Position $40,000, Debt $30,000. Price drops −6.25% to $93.75. | Position = $37,500; Equity = $7,500; Margin Ratio = **20.00%**; Status: `WARNING`; Liquidation: NOT triggered. | **PASS** |
| **T04** | Boundary | Position $40,000, Debt $30,000. Price drops −6.26% to $93.74. | Position = $37,496; Equity = $7,496; Margin Ratio = **19.9914%** (< 20.00%); Status: `MARGIN_CALL`; Liquidation: Triggered immediately. | **PASS** |
| **T05** | Invalid | Capital $10,000, 4× Tier ($40,000 max power). BUY 500 shares @ $100 ($50,000). | Order returns `False`. Balances unchanged. | **PASS** |
| **T06** | Invalid | Owns 0 shares. Submit SELL order for 50 shares. | Order returns `False`. Balances unchanged; short selling blocked. | **PASS** |
| **T07** | Invalid | BUY order with negative quantity: `shares = -10.0`. | Engine raises `ValueError`. | **PASS** |
| **T08** | Invalid | Submit order after account liquidation. | Engine raises `RuntimeError("Account is liquidated. Trading is disabled.")`. | **PASS** |
| **T09** | Financial | Capital ₩10m, Debt ₩30m, −20% shock (Position ₩32m), 5% penalty. | Gross proceeds ₩32m; penalty ₩1.6m; net proceeds ₩30.4m; debt repaid ₩30m; final cash **₩400,000**. | **PASS** |
| **T10** | Financial | $4,000 deposited in Bank Savings. Stock market plunges −50%. | Savings balance remains $4,000 (immune to stock collapse). | **PASS** |
| **T11** | Workflow | Orders placed at tick 50 (T < 150) and tick 200 (T $\ge$ 150). | Tick 50 order delivers at tick 80 (T+30); tick 200 order delivers upon Phase 2 entry. | **PASS** |
| **T12** | Workflow | Savings $5,000, reserve locked at $2,000. Withdraw $4,000. | Withdrawal rejected (only $3,000 free above reserve). Balance stays $5,000. | **PASS** |

---

## 4. Mathematical Derivations of Boundary Cases

### Maintenance Margin Threshold (T03 vs T04)
The broker maintenance margin requirement is $20.00\%$ ($\text{Maintenance Margin Ratio} = 0.20$):
$$\text{Margin Ratio} = \frac{\text{Stock Value} - \text{Debt}}{\text{Stock Value}} = 1 - \frac{\text{Debt}}{\text{Stock Value}}$$
$$0.20 = 1 - \frac{\$30,000}{\text{Stock Value}} \implies \text{Stock Value} = \frac{\$30,000}{0.80} = \$37,500$$
$$\text{Share Price} = \frac{\$37,500}{400} = \$93.75 \quad (\text{Exact drop of } -6.25\%)$$

- **At \$93.75 (T03):** Equity = $\$7,500$, Margin Ratio = $20.00\%$. The position is on the boundary; status changes to `WARNING`, but liquidation is **not triggered**.
- **At \$93.74 (T04):** A further one-cent decline yields Stock Value = $\$37,496$, Equity = $\$7,496$, Margin Ratio = $19.9914\% < 20.00\%$. Status shifts to `MARGIN_CALL`, and the engine immediately executes forced liquidation.

---

## 5. Defect Triage and Resolution History

All six critical and major defects identified during Week 6 testing clinics were resolved and verified:

| Bug ID | Severity | Component | Issue Description | Fixed By | Verified By | Resolution Summary |
|:---:|:---:|---|---|---|---|---|
| **BUG-01** | Critical | `simulation_engine.py` | Orders placed after tick 150 remained stuck in `pending_queue` across phase boundaries. | Nguyễn Quang Minh | Trần Hữu Dụ | Decoupled phase advancement check from tick-threshold check in `process_deliveries`. |
| **BUG-02** | Critical | `simulation_engine.py` | Uninitialized `margin_multiplier` caused runtime attribute errors during BUY orders. | Nguyễn Quang Minh | Triệu Đức Lương | Explicitly initialized multiplier in engine constructor and mapped order tier inputs. |
| **BUG-03** | Major | `index.html` | Floating-point division produced trailing decimal artifacts (e.g. 24.9999999994%). | Triệu Đức Lương | Trần Hữu Dụ | Enforced `.toFixed(2)` formatting across all HUD gauges and API response serializations. |
| **BUG-04** | Major | `simulation_engine.py` | Engine accepted trades after liquidation occurred. | Nguyễn Quang Minh | Cáp Phan Quang Khánh | Added an explicit guard check throwing `RuntimeError` if `self.state.is_liquidated` is True. |
| **BUG-05** | Major | `simulation_engine.py` | Cash-only positions displayed a 200% margin ratio, confusing players. | Nguyễn Quang Minh | Trần Hữu Dụ | Standardized cash-only margin ratio representation to cap at 100% `HEALTHY`. |
| **BUG-06** | Minor | Repository Root | Background PNG images cluttered the root directory. | Nguyễn Quang Minh | Full Group | Moved all visual assets to `assets/` and updated image references. |

---

## 6. Execution Verification

Fresh console output from the root repository run:
```text
======================================================================
python -m unittest discover tests
..................................................................
----------------------------------------------------------------------
Ran 66 tests in 2.829s

OK
```
All tests pass cleanly on Python 3.10 through 3.14 without warnings or external library dependencies.
