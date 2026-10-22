# Testing

> Consolidated from: `test_case.md` (Week 6), `bug_log.md`, and the uploaded `tests/test_simulation_engine.py`.

## 1. Approach
4-tier framework: **Normal, Boundary, Invalid, Financial consistency** (plus workflow). *Technical pass* = no exceptions on valid input, state changes correctly; *financial consistency* = results match the approved formulas ([financial_logic.md](financial_logic.md)).

Run from the repository root:
```bash
python -m unittest discover tests
```
(`src/__init__.py` must exist because the tests import `from src.simulation_engine import MarginEngine, HouseType, MarginStatus`.)

## 2. What the committed test file contains (4 tests)
| Test | Verifies | Matches formal case |
|---|---|---|
| `test_case_1_high_leverage_wipeout_with_penalty` | ₩10m, 4×, 400 shares @ ₩100,000, −20 % → ratio 6.25 %, `MARGIN_CALL`, liquidation: gross ₩32m, penalty ₩1.6m, net ₩30.4m, remaining debt 0, final cash ₩400,000, account marked liquidated | T09 (and T02 set-up) |
| `test_case_2_cash_only_safe_position` | ₩50m cash, 500 shares, −10 % → equity ₩45m, no debt, `HEALTHY`, solvent | Week 4 case 2 / T01 |
| `test_bank_savings_workflow` | Deposit ₩10m to savings → cash ₩10m, savings ₩10m, equity ₩20m | T10 (deposit part) |
| `test_settlement_delay_holding_pen` | Tick 50 order not delivered at 70, delivered at 80; tick 200 order delivered on entering Phase 2 | T11 |

## 3. Formal test specification (`test_case.md`)
| ID | Category | Input | Expected | Recorded status |
|---|---|---|---|---|
| T01 | Normal | $10,000 cash, buy 10 @ $500 | Cash $5,000, debt 0, equity $10,000, ratio 200 %, `HEALTHY` | PASS |
| T02 | Normal | $10,000, 4×, buy 400 @ $100 | Debt $30,000, equity $10,000, leverage 4.0×, ratio 25 %, `NORMAL` | PASS |
| T03 | Boundary | Price −6.25 % ($93.75) | Ratio exactly 20.00 %, `WARNING`, no liquidation | PASS |
| T04 | Boundary | Price −6.26 % ($93.74) | Ratio 19.9914 %, `MARGIN_CALL`, immediate liquidation | PASS |
| T05 | Invalid | Buy $50,000 with $40,000 power | Rejected (`False`), state unchanged | PASS |
| T06 | Invalid | Sell 50 shares not owned | Rejected; no short selling | PASS |
| T07 | Invalid | Negative quantity | `ValueError` | PASS |
| T08 | Invalid | Buy after liquidation | `RuntimeError` | PASS |
| T09 | Financial | ₩10m, debt ₩30m, −20 %, 5 % penalty | Final cash ₩400k | PASS |
| T10 | Financial | $4,000 savings, stocks −50 % | Savings stay $4,000 | PASS |
| T11 | Workflow | Orders at tick 50 and 200 | Delivered at tick 80 / on Phase 2 entry | PASS |
| T12 | Workflow | Savings $5,000, reserve $2,000, withdraw $4,000 | Rejected | PASS |

`test_case.md` records `Ran 14 tests … OK`. Boundary derivation: ratio = 1 − Debt ÷ Stock → S = $30,000 ÷ 0.80 = $37,500 → $93.75 (−6.25 %).

## 4. Reproducibility gap — action needed
- The uploaded test file has **4 tests**, while `test_case.md` and the README claim **14 tests / 12 cases** (names such as `test_t08_post_liquidation_lockout`). T03–T08 and T12 are not in the file I could see. Commit the latest test file or correct the claim.
- `src/simulation_engine.py` was not part of the uploaded files, so I could not execute the suite; `[TODO: paste a fresh console run with date and commit hash]`.
- The settlement boundary is “tick < 150” in the engine/tests but “≤ 150” in one contribution file.

## 5. Defects found and fixed (Week 6)
| ID | Severity | Issue | Verified by |
|---|---|---|---|
| BUG-01 | Critical | Orders after tick 150 never delivered at Phase 2 | `test_settlement_delay_holding_pen`, `test_t11…` |
| BUG-02 | Critical | `margin_multiplier` uninitialised → crash on margin BUY | `test_t02…` + regression |
| BUG-03 | Major | Float artefacts (e.g. 24.9999999994 %) in HUD/API | Visual check |
| BUG-04 | Major | Orders accepted after liquidation | `test_t08_post_liquidation_lockout` |
| BUG-05 | Major | Cash-only ratio displayed 200 % (ambiguity) | Test comment + docs |
| BUG-06 | Minor | Background PNGs in repo root | Repo check |

Sign-off recorded: 6 logged / 6 verified, 0 open blockers, scope freeze at Checkpoint 6.

## 6. Other gaps
- Test and bug logs name **roles**, not members — `[TODO: map to names]`.
- The repo root still listed `bg_base.png` / `bg_reveal.png` when checked, although BUG-06 says they moved to `assets/`.
- No recorded UI/end-to-end check on the live build, and no test of the scenario CSV (e.g. continuity at session boundaries, see [data_and_sources.md](data_and_sources.md) §6) — `[TODO]`.
