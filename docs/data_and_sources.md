# Data, Assumptions and Sources

> Consolidates `Market_Dataset.md`, `INPUT_DICTIONARY.md`, `ASSUMPTIONS.md`, `SOURCE_USE_MAP.md`, scenario datasets and audits, and the latest dual-scenario portfolio optimization results (22 October 2026).

## 1. Files and Evidence Map

| File / Artifact | Content and Purpose | Status |
|---|---|---|
| [`data/market_scenario_1.csv`](../data/market_scenario_1.csv) | Scenario 1: 50 assets × 1,800 ticks | Corrected; QA PASS |
| [`data/market_scenario_2.csv`](../data/market_scenario_2.csv) | Scenario 2: alternative deterministic market path | Corrected; QA PASS |
| [`data/audit/market_scenario_audit_1.xlsm`](../data/audit/market_scenario_audit_1.xlsm) | Scenario 1 audit workbook | Historical audit; verify formulas against final phase-wide rule |
| [`data/audit/market_scenario_audit_2.xlsx`](../data/audit/market_scenario_audit_2.xlsx) | Scenario 2 audit workbook | Historical audit; verify formulas against final phase-wide rule |
| [`analysis/best_case.py`](../analysis/best_case.py) | Whole-share Dynamic Programming and staggered MILP optimizer | Executed for both scenarios |
| [`analysis/best_case_calibration_targets_3x_20x_100x.md`](../analysis/best_case_calibration_targets_3x_20x_100x.md) | Optimization methodology and target calibration | Updated |
| [`analysis/whole_share_srlp_summary.csv`](../analysis/whole_share_srlp_summary.csv) | Combined scenario-by-tier results | Generated |
| [`analysis/whole_share_srlp_cycles.csv`](../analysis/whole_share_srlp_cycles.csv) | Optimized trading cycles | Generated |
| [`analysis/whole_share_srlp_buy_allocations.csv`](../analysis/whole_share_srlp_buy_allocations.csv) | Asset selections and whole-share BUY allocations | Generated |
| [`analysis/whole_share_srlp_margin_audit.csv`](../analysis/whole_share_srlp_margin_audit.csv) | Margin-ratio verification | Generated |
| [`analysis/target_calibration_3x_20x_100x.csv`](../analysis/target_calibration_3x_20x_100x.csv) | Property-target feasibility by scenario and leverage | Generated |
| [`analysis/scenario_tier_comparison.csv`](../analysis/scenario_tier_comparison.csv) | Cross-scenario performance comparison | Generated |
| [`analysis/target_robustness_both_scenarios.csv`](../analysis/target_robustness_both_scenarios.csv) | Target attainment across both scenarios | Generated |

**Data schema:** Each CSV contains six metadata columns (`Scenario`, `Global_Second`, `Phase`, `Phase_Name`, `Phase_Second`, `Market_State`) and 50 numeric asset-price columns. The optimizer converts raw prices using a divisor of **1,400**. SK Hynix was renamed **Vintrumite**.

## 2. Scenario Structure and Dataset Validation

Each scenario contains **1,800 ticks**, divided into six **300-tick phases**. Every phase has a 150-tick AM session and a 150-tick PM session.

The finalized market-data rules are:

1. **Phase price limits:** For each asset, all prices within a phase must remain between **70% and 130%** of the phase-opening price. The reference price does not reset at PM.
2. **AM/PM continuity:** Prices must match at ticks 150–151, 450–451, 750–751, 1050–1051, 1350–1351 and 1650–1651.
3. **Phase continuity:** Prices must match at ticks 300–301, 600–601, 900–901, 1200–1201 and 1500–1501.
4. **Data integrity:** All 50 asset prices must be numeric, positive and non-missing; `Global_Second` must run consecutively from 1 to 1,800.

The former interpretation of **±30% per 150-tick half-session**, allowing compounded movements of +69%/−51% per phase, is obsolete.

| Phase | Global Ticks | Intended Market Behavior |
|---|---|---|
| 1 — Fake Positive News | 1–300 | Misleading positive signals |
| 2 — True Positive News | 301–600 | Improving confidence and supported rallies |
| 3 — Bull Market | 601–900 | Sustained positive movements |
| 4 — Strong Growth (FOMO) | 901–1200 | Rising speculative exposure |
| 5 — Market Euphoria | 1201–1500 | Euphoric rallies and bull traps |
| 6 — Negative Shock | 1501–1800 | Market reversal and liquidation pressure |

### 2.1 Scenario 1

The original primary drivers are **Samsung Electronics, Vintrumite, KODEX Leverage, KODEX Semiconductor and TIGER Semiconductor TOP10**. Other assets provide diversification, decoy opportunities and contrasting price movements.

The original dataset contained abnormal price jumps, notably at ticks **1650–1651 and 1680–1681**. These were corrected while preserving the intended phase-level behavior.

The corrected Scenario 1 passed the final structural, continuity, phase-limit and numeric validation checks.

### 2.2 Scenario 2

Scenario 2 introduces an alternative market path with different asset drivers, volatility patterns and trading opportunities.

The original dataset contained AM/PM discontinuities and price cells formatted as text with thousands separators. These problems were corrected without changing the intended market-price values during numeric normalization.

Both finalized datasets passed the validation stage of `best_case.py`:

| Validation | Scenario 1 | Scenario 2 |
|---|---|---|
| 1,800 ticks × 50 assets | PASS | PASS |
| AM/PM continuity (300 checks) | PASS | PASS |
| Phase-boundary continuity (250 checks) | PASS | PASS |
| Phase-wide ±30% limits (300 checks) | PASS | PASS |
| Numeric and positive prices | PASS | PASS |

These checks confirm compliance with the specified data constraints, not real-world market realism or game-engine integration.

## 3. Best-Case Optimization and House-Target Calibration

### 3.1 Optimization Assumptions

The updated `best_case.py` evaluates both market scenarios using:

- **Concentrated Dynamic Programming (DP):** Sequential leveraged trades, with reinvestment after settlement.
- **Staggered Re-Leveraging MILP:** Additional BUY orders within profitable cycles, using newly available margin capacity.

| Parameter | Value |
|---|---|
| Initial Capital | $10,000 |
| Assets / Ticks | 50 / 1,800 |
| Price Divisor | 1,400 |
| Fixed Leverage Tiers | 2×, 3×, 4× |
| Share Quantities | Whole shares |
| Settlement Delay | 75 ticks |
| Maintenance-Margin Trigger | ≤20% |
| Survival Margin | ≥20.001% |
| MILP Time Limit | 60 seconds per cycle |
| MILP Relative Gap Target | 0.1% |

The optimizer assumes complete knowledge of future prices (**perfect foresight**) and does not model trading fees, spreads, slippage or limited order-book liquidity.

Individual MILP cycles are optimized around DP-selected trading windows; the full-session strategy is **not proven globally optimal**.

### 3.2 Latest Optimization Results (22 October 2026)

| Scenario | Leverage | Concentrated DP | Staggered MILP | Final Equity |
|---|---|---:|---:|---:|
| Scenario 1 | 2× | 25.007857× | **31.534604×** | $315,346.04 |
| Scenario 1 | 3× | 85.517668× | **156.869452×** | $1,568,694.52 |
| Scenario 1 | 4× | 257.709480× | **491.696973×** | $4,916,969.73 |
| Scenario 2 | 2× | 103.427759× | **137.817680×** | $1,378,176.80 |
| Scenario 2 | 3× | 545.345477× | **1,127.322099×** | $11,273,220.99 |
| Scenario 2 | 4× | 2,249.165859× | **5,990.443600×** | $59,904,436.00 |

Staggered re-leveraging outperformed concentrated DP in all six scenario-tier combinations.

Scenario 2 produced substantially higher optimized wealth than Scenario 1, suggesting different attainable upside under the two deterministic market paths.

**Solver qualification:** Scenario 1 at 2× leverage had one cycle with a **0.195264% MIP gap**, exceeding the configured 0.1% tolerance. Its solution remains feasible but is not certified optimal to that tolerance. All other tested cycles reported successful MILP convergence under the configured stopping criteria.

### 3.3 Property Targets and Attainment

The game uses three property targets:

| Target | Multiple | Required Final Equity |
|---|---:|---:|
| **Small House** | 3× | $30,000 |
| **Normal House** | 20× | $200,000 |
| **ToLam Villa** | 100× | $1,000,000 |

**Target attainment under the staggered optimizer:**

| Scenario | Leverage | 3× | 20× | 100× |
|---|---|---|---|---|
| Scenario 1 | 2× | PASS | PASS | BELOW |
| Scenario 1 | 3× | PASS | PASS | PASS |
| Scenario 1 | 4× | PASS | PASS | PASS |
| Scenario 2 | 2× | PASS | PASS | PASS |
| Scenario 2 | 3× | PASS | PASS | PASS |
| Scenario 2 | 4× | PASS | PASS | PASS |

The 3× and 20× targets are reached in every tested combination. The 100× target is reached at 3× and 4× leverage in both scenarios, and at 2× leverage in Scenario 2.

Scenario 1 at 2× leverage reaches **31.534604×**, below the 100× threshold.

These findings establish **attainment by the tested optimized strategies**, not ordinary-player success probabilities or proof that an unmet target is mathematically impossible.

Historical benchmarks such as 109×, 156× and 785.81× from previous dataset versions should not replace the current results.

## 4. Input Dictionary

| Variable | Meaning | Format / Source | Affects |
|---|---|---|---|
| `assigned_scenario_id` | Selects Scenario 1 or 2 | System-generated | Market prices and portfolio outcomes |
| `initial_capital` | Starting wealth | $10,000 in optimizer | Equity, buying power and targets |
| `fixed_price_path` | Asset-price path for each tick | 1,800 × 50 CSV data | Portfolio valuation and margin checks |
| `target_house_type` | Selected property reward | Small / Normal / ToLam Villa | Target evaluation |
| `property_target_value` | Final-equity requirement | 3× / 20× / 100× initial capital | Target progress |
| `margin_tier` | Selected leverage | 1× cash; 2× / 3× / 4× margin | Exposure and debt |
| `orders` | BUY, SELL, quantity and asset | Player input; whole shares | Portfolio and settlement |
| `bank_savings` | Funds allocated to savings | Player choice | Cash allocation |
| `savings_return_rate` | Savings credit assumption | +4.75% per AM/PM session | Savings balance |

## 5. Assumptions and Limitations

| # | Assumption | Implication |
|---|---|---|
| 1 | Deterministic market-price paths | Players may memorize patterns across repeated games |
| 2 | ±30% per full 300-tick phase | Synthetic price-limit rule, not a reconstruction of Korean exchange rules |
| 3 | Continuous AM/PM and phase boundaries | Prevents artificial one-tick price gaps |
| 4 | Full trade execution at stated prices | Ignores spreads, market impact and partial fills |
| 5 | Property targets of 3× / 20× / 100× | Educational reward thresholds rather than actual housing prices |
| 6 | Maintenance margin of 20% | Simplified game-specific risk rule |
| 7 | Bank Savings earns 4.75% per session | Accelerated synthetic savings return |
| 8 | Perfect-foresight portfolio optimization | Best-case benchmark, not expected player performance |
| 9 | Optimizer settlement delay of 75 ticks | Must match the implemented game engine |

The current optimizer does **not** incorporate Bank Savings returns into its stock-portfolio optimization.

## 6. Final Issues and Verification Tasks

| Priority | Remaining Issue | Required Action |
|---|---|---|
| **Critical** | Optimizer uses 75-tick settlement, while an earlier engine specification reported 30 ticks | Confirm and align the final implemented settlement rule |
| **High** | Optimizer uses perfect foresight | Conduct player testing to assess practical target difficulty |
| **High** | Scenario 2 produces substantially higher optimized wealth than Scenario 1 | Evaluate whether this difference is appropriate for gameplay balance |
| **Medium** | Legacy audit workbooks and documentation may still reference ±30% per half-session | Align formulas and explanations with the 300-tick phase rule |
| **Medium** | Scenario 1, 2× MILP cycle exceeds target gap | Rerun with tighter solver settings if an optimality certificate is required |
| **Medium** | Dataset and optimizer integration with the final game build | Confirm actual committed versions and add GitHub commit/PR evidence |
| **Medium** | Historical source-map inconsistencies | Reconcile maintenance-margin values, crisis dates and circuit-breaker descriptions |

Scenario 1 discontinuities, Scenario 2 numeric formatting and dual-scenario optimizer execution have been addressed in the latest reported runs.

## 7. Source–Use Map

| Source | Use | Qualification |
|---|---|---|
| Korean market and margin-crisis background sources | Educational context and scenario narrative | Synthetic price paths are not historical market reconstructions |
| [Scenario 1](../data/market_scenario_1.csv) and [Scenario 2](../data/market_scenario_2.csv) | Deterministic game-price inputs | Both passed the latest reported data-validation checks |
| [Scenario 1 Audit](../data/audit/market_scenario_audit_1.xlsm) and [Scenario 2 Audit](../data/audit/market_scenario_audit_2.xlsx) | Historical dataset verification | Workbook formulas should be checked against the final phase-wide rules |
| [`analysis/best_case.py`](../analysis/best_case.py) | Quantitative portfolio optimization | Perfect foresight; 75-tick settlement assumption |
| [Optimization Summary](../analysis/whole_share_srlp_summary.csv) and [Target Calibration](../analysis/target_calibration_3x_20x_100x.csv) | Leverage and target feasibility evidence | Optimizer results are not player-success probabilities |
| Brokerage margin materials | Inspiration for teaching mechanics | In-game thresholds are simplified project assumptions |
| Industry and company news themes | Asset behavior and narrative development | Contextual inputs, not live market-price feeds |

Some historical sources in `SOURCE_USE_MAP.md` still require complete URLs and consistent publication dates before final submission.

## 8. Scope Decision

The MVP market data exclude USD/KRW rates, institutional market-maker parameters, foreign-fund flows, central-bank reserve variables, additional leveraged-market indicators, real-time price feeds and detailed market microstructure.

These exclusions are deliberate simplifications to keep the simulation focused on **portfolio decisions, leverage, margin safety, liquidation risk and financial target attainment**.
