# Financial Logic

> Consolidated from: `Solution_Structure.md`, `Project_Proposal.md` (risk engine), `ASSUMPTIONS.md` (6–7), `INPUT_DICTIONARY.md` (margin tiers, targets), `MIDTERM_REVIEW.md` (Week 4 logic, margin-call price), `SAMPLE_INPUT_OUTPUT.md`, `test_case.md`. Implemented in [`src/simulation_engine.py`](../src/simulation_engine.py).

**Logic chain:** Leverage blindness → inexperienced investor → manage a leveraged portfolio → scenario, capital, target, margin tier, orders, price path → portfolio / debt / equity / leverage / margin calculations → net worth, target progress, liquidation status → player adjusts leverage and trades.

## 1. State variables
| Variable | Definition |
|---|---|
| Liquid cash | Uninvested funds |
| Bank Savings | Safe allocation outside the stock market |
| Gross exposure (stock value) | Σ Shares_i × Current price_i |
| Margin debt | Borrowed amount |
| Net equity | Liquid cash + Bank Savings + Gross exposure − Margin debt |
| Effective leverage | Gross exposure ÷ Net equity |
| Margin ratio | Net equity ÷ Gross exposure (stock value) |
| Property target value | Initial capital × house multiplier |
| Target progress % | Net equity ÷ Property target value × 100 |

*The proposal's formula omits Bank Savings; the Solution Structure, Feature Map and test T10 include it. This document follows the latter (see §9).*

## 2. Order mechanics
`Required cash = Order cost ÷ Margin multiplier` · `New margin debt = Order cost − Required cash`
Orders are validated (sufficient purchasing power, sufficient shares to sell, positive quantity; no short selling) and rejected otherwise. Fill is immediate at the current tick price and unlimited in volume (Assumptions 1, 4).

## 3. Margin tiers
| Tier | Buying power | Max debt per $1 equity | Initial margin ratio | Price fall to 20 % margin call | Theoretical equity wipeout |
|---|---|---|---|---|---|
| Cash 1.0× | 1× | 0 | 100 % | n/a | −100 % (no debt) |
| 2× | 2× | 1× | 50 % | **−37.50 %** | −50 % |
| 3× | 3× | 2× | 33.3 % | **−16.67 %** | −33.3 % |
| 4× | 4× | 3× | 25 % | **−6.25 %** | −25 % |

Margin-call stock value = Debt ÷ 0.80. Margin-call price (single security) = Margin debt ÷ [Shares × (1 − Maintenance margin)].

## 4. Risk states and enforcement
| State | Condition | Action |
|---|---|---|
| Safe | Effective leverage ≤ 2.5× (margin ratio ≥ 40 %) | Normal play |
| Margin Warning (amber) | 2.5× < leverage < 5.0× | Warning banner; prompts voluntary de-risking |
| Maintenance breach → Forced liquidation | Leverage ≥ 5.0× **or** margin ratio below 20 % | Fire-sale of 100 % of open stock holdings at current tick price, repay debt, apply **5 % penalty** on gross proceeds |
| Solvency check | Net equity ≤ 0 | Account wipeout / game over |

After liquidation the account is locked: further orders raise an error (BUG-04 fix). Test T03/T04 pin the engine behaviour at the boundary: exactly 20.00 % → `WARNING`, no liquidation; 19.99 % → `MARGIN_CALL` and immediate liquidation.

**Engine reference** (`MarginEngine`, from `tests/test_simulation_engine.py`): constructor defaults `maintenance_margin_ratio = 0.20`, `liquidation_penalty_pct = 0.05`; `execute_order(ticker, action, shares, price, use_margin, current_tick, current_phase)`; `deposit_to_savings`; `process_deliveries`; `evaluate(prices)` → portfolio value, equity, margin ratio, margin status (`HEALTHY`, `MARGIN_CALL`, …), solvency; `trigger_forced_liquidation(prices)` → gross proceeds, penalty, net proceeds, remaining debt, final cash.

## 5. Other rules
| Rule | Value |
|---|---|
| Bank Savings return | **+4.75 % after each completed AM/PM session**, compounded: `Savings(t+1) = Savings(t) × 1.0475`. Deliberately amplified for gameplay |
| Settlement (T+0.5) | (boundary: engine/tests use tick < 150; one contribution file says ≤ 150) Order before tick 150 → delivered in the same phase 30 ticks later (tick 50 → tick 80); order at/after tick 150 → pending, delivered on entering Phase 2. Pending shares stay exposed to price moves but cannot be sold |
| Session price limit | ±30 % from each AM/PM session reference price, reset every session. Compounded phase limits: **+69 % / −51 %** |
| Emergency reserve | Bank Savings withdrawals above the free (non-reserved) amount are rejected (T12) |
| Time | 1,800 s, 6 phases × 300 s, one price tick per second |

## 6. Property targets and benchmarks
Targets are fixed multiples of initial capital: **Small House 3×, Normal House 20×, ToLam Villa 100×**. They were calibrated against best-case benchmarks of Scenario 1, which exist in two generations:

| Benchmark | Cash 1× | 2× | 3× | 4× | Source |
|---|---|---|---|---|---|
| Earlier summary (`best_case_portfolio_summary.csv`, Input Dictionary) | 2.92×–5.20× | 7.02×–21.27× | 14.72×–72.84× | 27.99×–217.45× | Week 3 |
| Whole-share optimiser (`best_case.py`, benchmark note) | — | — | — | **≈ 109×** concentrated DP, **≈ 156×** staggered re-leveraging (from $10,000) | Week 6 |

Optimiser rules (from `best_case.py`): tiers 2×/3×/4×, whole shares only, 20 % maintenance (survival floor 20.001 %), prices ÷ 1,400 to USD, settlement delay of **75 s** between sell and reuse of cash, MILP per cycle.

| Target | Share of the 156× benchmark | Intended difficulty |
|---|---|---|
| 3× (Small House) | ≈ 1.9 % | Basic — cash only |
| 20× (Normal House) | ≈ 12.8 % | Intermediate — 2×–3× margin |
| 100× (ToLam Villa) | ≈ 64.1 % | Expert — 4× margin with near-perfect timing |

Endings: Small House → *Normie*; Normal House → *Middle-class stability*; ToLam Villa → *Extravagant luxury*; liquidation → *Wipeout*. *The benchmark note lists the basic target as 2× (file name says 3×/10×/100×); the product uses 3×/20×/100×.*

## 7. Worked examples
**A. 4× boundary (T02–T04).** Capital $10,000; buy 400 @ $100 = $40,000; debt $30,000; ratio 25 %. At $93.75: stock $37,500, equity $7,500, ratio 20.00 % (no liquidation). At $93.74: stock $37,496, equity $7,496, ratio 19.9914 % → liquidation.

**B. High-leverage wipeout (T09).** ₩10m capital, ₩40m position, ₩30m debt, −20 % shock: stock ₩32m, equity ₩2m, ratio 6.25 %. Penalty 5 % × ₩32m = ₩1.6m; net proceeds ₩30.4m; repay ₩30m; final cash **₩0.4m**.

**C. Cash only (Week 4 case 2, T01, T10).** ₩50m cash position, −10 %: equity ₩45m, no debt, no margin call. A $4,000 Bank Savings deposit stays $4,000 when stocks fall 50 %.

**D. Narrative cases (Sample I/O).** ToLam Villa + 4× held into Phase 6 (≈ −49 % to −51 % after session limits) → margin ratio falls through 20 % after a ≈ 6.25 % drop → forced liquidation, possible zero/negative equity. Small House + cash, rotated into Bank Savings before Phase 6 → solvent at ≈ $29,247 (2.92×), just under the 3× target.

## 8. Explainability
Every outcome traces to a decision: `Margin tier → Leverage → Position size → Price move → P&L → Equity → Margin ratio → Liquidation risk`. The debrief explains *why* the state changed rather than only showing the result.

## 9. Items to reconcile (documents disagree)
| Topic | Conflict | Suggested resolution |
|---|---|---|
| Net equity | Proposal excludes Bank Savings; Solution Structure / Feature Map / T10 include it | Use inclusive definition everywhere |
| Maintenance threshold | `ASSUMPTIONS` / tests: 20 %; `SOURCE_USE_MAP`: “30 %” | Correct source map to 20 % (or explain) |
| Boundary rule | Assumptions: “reaches or falls below 20 %”; tests: exactly 20.00 % is not liquidated | State “below 20 %” |
| Warning level | Solution Structure: leverage > 2.5×; engine test T02 shows 4× (25 % ratio) as `NORMAL`, 20 % as `WARNING` | Confirm engine warning threshold and align doc |
| Phase 6 drop | −57 % (docs), −48.7 % / −51 % (sample cases), ≈ −50 % (scenario plot) vs −30.0 % for drivers in the scenario 1 CSV (a +30 % jump at second 1651 — see data_and_sources §6) | Re-check the CSV, then state one figure with its basis |
| Settlement delay | Engine/tests: 30 ticks (tick 50 → 80); `best_case.py`: 75 s | Align benchmark with the engine or explain |
| Benchmark ceiling | 217.45× (Input Dictionary) vs ≈ 156× (new optimiser); target ladder 2×/20×/100× vs 3×/20×/100× | Pick the current benchmark and update the Input Dictionary |
| Week 4 targets (2× / 8×) and `initial_margin_ratio` inputs | Superseded by 3/20/100× and margin tiers | Treated as history in [revision_summary.md](revision_summary.md) |
