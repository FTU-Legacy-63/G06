# Data, Assumptions and Sources

> Consolidates `Market_Dataset.md`, `INPUT_DICTIONARY.md`, `ASSUMPTIONS.md`, `SOURCE_USE_MAP.md`, `Solution_Structure.md`, scenario data/audits, the Data Gatherer's contribution record, and the latest **Scenario 1** whole-share optimizer run. Values marked **provisional** must be reconciled against the committed final datasets and game engine.

## 1. Files and evidence map

| File / artifact | Content and purpose | Status / action |
|---|---|---|
| [`data/market_scenario_1.csv`](../data/market_scenario_1.csv) | Scenario 1; 50 tradable assets × 1,800 ticks and six metadata columns | Used as input to the latest optimizer run; **Phase 6 tick 1650→1651 issue unresolved** |
| [`data/market_scenario_2.csv`](../data/market_scenario_2.csv) | Scenario 2; alternative deterministic path, same structure | **Replace/verify** using validated `market_scenario_2_PHASE30_FIXED.csv`; do not assume the repository copy is updated |
| `data/audit/market_scenario_audit_1.xlsm` | Historical Scenario 1 audit workbook, including a session-based check | Legacy audit logic must be updated to **phase-wide** ±30% |
| `data/audit/market_scenario_audit_2.xlsx` | Original Scenario 2 market and data-audit sheets | Historical baseline; its original 150-tick reference calculations do not establish final rule compliance |
| `market_scenario_2_PHASE30_FIXED.csv` | Rebuilt Scenario 2 price data; intended 300-tick ±30% rule and AM/PM continuity | Prepared outside repo; upload as the authoritative Scenario 2 CSV after review |
| `market_scenario_2_PHASE30_AUDIT.csv` | Per-asset/per-phase checks associated with the rebuilt Scenario 2 | Preserve as evidence; link to final committed copy |
| `build_market_scenario_2.py` | Reproducible scenario-correction and validation script | Preserve beside audit; code should be rerunnable |
| [`analysis/best_case.py`](../analysis/best_case.py) | Concentrated DP plus whole-share staggered MILP for leverage tiers 2×/3×/4× | Latest results below; verify this repo script is the target-calibration revision |
| `whole_share_srlp_summary.csv`, `whole_share_srlp_cycles.csv`, `whole_share_srlp_buy_allocations.csv`, `whole_share_srlp_margin_audit.csv` | Outputs of latest Scenario 1 run | Attach to repo and link in the final contribution map |
| `target_calibration_3x_20x_100x.csv` | Target achievement, coverage and gaps computed from actual optimizer results | Latest generated output; attach to repo |
| `best_case_portfolio_combos.csv`, `best_case_portfolio_summary.csv` | Earlier-generation portfolio tests | Historical comparisons only, not current calibration |

**Data schema.** The market CSVs use the metadata columns `Scenario`, `Global_Second`, `Phase`, `Phase_Name`, `Phase_Second`, and `Market_State`, followed by 50 numeric price columns (unscaled prices). Within the optimizer, trade prices are the raw numeric price divided by **1,400**. The asset formerly named SK Hynix is **Vintrumite** in the intended final dataset.

## 2. Scenario structure and dataset validation

Each scenario contains 1,800 ticks and six **300-tick phases**, each split into AM (150 ticks) and PM (150 ticks). The phase-wide rules are:

1. For every asset and phase, let `P_open` be that asset's price at the **first tick of the phase**. Every price in both AM and PM must satisfy `0.70 × P_open ≤ P_t ≤ 1.30 × P_open` (subject only to documented numeric rounding tolerance). The price reference **does not reset at PM**.
2. **AM/PM continuity:** `P_150 = P_151`, `P_450 = P_451`, `P_750 = P_751`, `P_1050 = P_1051`, `P_1350 = P_1351`, `P_1650 = P_1651` for each asset.
3. **Phase boundary continuity** under the current agreed specification: `P_300 = P_301`, `P_600 = P_601`, `P_900 = P_901`, `P_1200 = P_1201`, `P_1500 = P_1501` for each asset.
4. Price fields must parse as numeric, remain positive, and contain no missing values. `Global_Second` must run consecutively from 1 through 1,800.

The price cap is per **entire phase**, not per half-session; statements that a new ±30% band begins at PM, or that a phase permits +69%/−51% from sequential session caps, are obsolete.

| Phase | Global ticks | Intended behavior |
|---|---|---|
| 1 — Fake Positive News | 1–300 | Early uncertainty, misleading positive signals |
| 2 — True Positive News | 301–600 | Improving confidence and supported rallies |
| 3 — Bull Market | 601–900 | Sustained positive moves and opportunities |
| 4 — Strong Growth (FOMO) | 901–1200 | Rising speculative exposure |
| 5 — Market Euphoria | 1201–1500 | Euphoric rallies, decoys and bull traps |
| 6 — Negative Shock | 1501–1800 | Reversal, falling prices, margin/liquidation pressure |

### 2.1 Scenario 1

The originally documented primary drivers are **Samsung Electronics, Vintrumite, KODEX Leverage, KODEX Semiconductor, and TIGER Semiconductor TOP10**; other assets provide contrasting patterns and decoy opportunities. Historical dataset notes reported cumulative driver appreciation through tick 1500 and a synchronized Phase 6 crash. **Do not treat the earlier quoted phase statistics as certified final values until Scenario 1 is corrected and re-audited.**

**Open critical issue:** In the previously reviewed Scenario 1 CSV, all 50 assets jump at tick **1650→1651**. A reported example is Vintrumite **1,932,051 → 2,636,174**. This violates the final AM/PM continuity rule and may materially inflate late Phase 6 optimization gains. The final committed Scenario 1 must be fixed and the entire benchmark rerun before the numbers in Section 3 are promoted to official targets evidence.

### 2.2 Scenario 2

The original Excel/CSV contained widespread discontinuities at AM→PM boundaries and, in an earlier CSV representation, price cells with thousands separators that were read as text. A revised CSV, `market_scenario_2_PHASE30_FIXED.csv`, and audit, `market_scenario_2_PHASE30_AUDIT.csv`, were produced using a reproducible script.

The prior correction run **reported** the following results (these are outputs of that correction step, not an independent fresh repository validation):

| Scenario 2 correction check | Reported result |
|---|---:|
| AM/PM equal-price checks | 300/300 PASS (50 assets × 6 boundaries) |
| Phase boundary equal-price checks | 250/250 PASS (50 × 5 boundaries) |
| Phase-wide ±30% limit checks | 300/300 PASS (50 × 6 phases) |
| Largest discrepancy in phase-end return vs old dataset | 0.00336 percentage points |

**Release requirement:** Inspect the actual committed CSV, rerun the script/audit, and ensure the game controller loads that version. Scenario 2 **portfolio optimization/target feasibility has not yet been rerun**, so no Scenario 2 best-case wealth ceiling is established here.

## 3. Best-case optimization and house-target calibration — Scenario 1 (provisional)

### 3.1 Assumptions implemented in the supplied optimizer

| Parameter | Current optimizer value |
|---|---|
| Initial equity | **$10,000** |
| Scenario | `market_scenario_1.csv` |
| Assets / ticks | 50 / 1,800 |
| Price divisor | 1,400 |
| Fixed leveraged tiers | 2×, 3×, 4×; cash 1× not optimized in this latest script |
| Quantity | **Whole shares only** |
| Settlement delay | **75 ticks**, both for earliest resale after BUY and for reuse of proceeds after SELL |
| Maintenance trigger | Margin ratio ≤20% |
| Survival floor | **20.001%**, strictly above trigger |
| Staggered optimization | Per-cycle MILP; 60-second time limit, relative gap target 0.1% |
| Model omissions | Fees, spreads, slippage, order-book depth, constrained liquidity |

`Margin Ratio = Equity / Gross Portfolio Value`. The optimizer uses future market prices (**perfect foresight**) and selects concentrated DP cycles first, then solves staggered purchases within those cycles. Consequently, solver-optimal individual cycles **do not imply a globally optimal full-session trading schedule**.

### 3.2 Latest actual results provided (22 October 2026)

| Fixed tier | Concentrated DP equity | DP multiple | Staggered equity | Staggered multiple | Gain over DP |
|---|---:|---:|---:|---:|---:|
| **2×** | $421,954.90 | **42.195490×** | $452,245.75 | **45.224575×** | **+7.18%** |
| **3×** | $1,688,823.79 | **168.882379×** | $2,038,144.72 | **203.814472×** | **+20.68%** |
| **4×** | $5,621,206.12 | **562.120612×** | $7,858,115.33 | **785.811533×** | **+39.79%** |

All ten MILP cycles per tier were reported as optimal within configured tolerance. Reported minimum maintenance ratios were **48.4672%**, **31.2896%**, and **22.7008%** respectively. These figures describe the tested optimized paths, not ordinary-player performance.

### 3.3 Target ladder and benchmark attainment

| Target | Multiple | Equity required from $10,000 |
|---|---:|---:|
| **Small House** | **3×** | **$30,000** |
| **Normal House** | **20×** | **$200,000** |
| **ToLam Villa** | **100×** | **$1,000,000** |

| Fixed tier | Staggered multiple | 3× target | 20× target | 100× target |
|---|---:|---|---|---|
| **2×** | 45.224575× | PASS | PASS | BELOW |
| **3×** | 203.814472× | PASS | PASS | PASS* |
| **4×** | 785.811533× | PASS | PASS | PASS |

`*`The **3× 100× PASS** depends on the tenth trading cycle (tick 1650→1725), which overlaps the known faulty Scenario 1 boundary. It **must not** be used to prove that players can reach 100× on a corrected dataset. The 4× path crosses 100× during cycle 9 (before the final cycle), but the full 4× result still requires revalidation against corrected data.

**First target-reaching cycle in this run:**

| Fixed tier | Reaches 3× | Reaches 20× | Reaches 100× |
|---|---|---|---|
| 2× | Cycle 4 (3.129080×) | Cycle 9 (21.664542×) | Not reached |
| 3× | Cycle 4 (5.275689×) | Cycle 7 (28.370480×) | Cycle 10 (203.814472×; **boundary-sensitive**) |
| 4× | Cycle 3 (3.949156×) | Cycle 5 (23.072560×) | Cycle 9 (247.494533×) |

**Interpretation:** These are **feasible strategies found under the modeled assumptions**. They do not estimate a player's probability of reaching a house target and do not establish that a particular tier is *necessary* for ordinary players. The legacy 109× / 156× results and other historical benchmarks belong only to earlier optimizer/dataset generations and should not be reused as the current run's ceiling.

## 4. Input dictionary

| Variable | Meaning | Format / source | Affects |
|---|---|---|---|
| `assigned_scenario_id` | Selects the fixed market path | Scenario 1 or 2; system | Data selection, portfolio outcomes |
| `initial_capital` | Starting player capital | $10,000 **in current optimizer**; confirm game configuration | Equity, buying power, target values |
| `fixed_price_path` | Price array consumed every tick | CSV: 1,800 × 50 | Mark-to-market, alerts, liquidation checks |
| `target_house_type` | Chosen reward threshold | Small / Normal / ToLam Villa | Target selection |
| `property_target_value` | Required wealth | Target multiple × initial capital | Target progress and outcome |
| `margin_tier` | Chosen leverage | Cash 1×; margin 2×/3×/4× | Exposure, debt, margin health |
| `orders` | Buy, sell, hold, ticker, quantity | Player input; whole shares | Cash, shares, settlement, margin debt |
| `bank_savings` | Cash assigned to savings | Player / game input | Allocation and liquidity |
| `savings_return_rate` | Savings credit assumption | +4.75% per completed AM/PM session **per earlier project specification** | Savings balance; verify engine implementation |

## 5. Assumptions and limitations

| # | Assumption | Why it matters / limitation |
|---|---|---|
| 1 | Deterministic scripted market paths | Replaying a scenario permits memorizing prices and optimal trade windows |
| 2 | **±30% relative to each 300-tick phase opening price** | Synthetic teaching rule, not a claim about real Korean exchange limits |
| 3 | AM closing price = PM opening price; adjacent phases continuous | Avoids artificial one-tick wealth creation or liquidation |
| 4 | 100% fills and unlimited liquidity at tick price | Ignores spreads, impact, partial fills and forced-sale execution costs |
| 5 | House targets fixed at **3× / 20× / 100×** | Synthetic goal difficulty; not actual housing prices |
| 6 | Maintenance trigger at 20%; fixed leverage tiers 2×/3×/4× | Broker practice differs; actual in-game implementation must match |
| 7 | Savings credited +4.75% per AM/PM session under prior specification | Deliberately accelerated, unrealistic real-world deposit return |
| 8 | Optimizer uses future price path and per-cycle constraints | Best-case exercise, not a behavioral or realistic expected-return prediction |
| 9 | Optimizer settlement delay is 75 ticks | **Conflict to resolve:** previously reported game engine uses 30 ticks |

## 6. Final issues and verification tasks

| Priority | Issue | Required evidence / action |
|---|---|---|
| **Critical** | Scenario 1 tick **1650→1651** jump violates continuity; the latest optimizer profits in cycle 10 | Rebuild Scenario 1 preserving 300-tick price limit and continuity; rerun and replace target comparison |
| **Critical** | **75-tick optimizer** settlement vs **30-tick engine** reported elsewhere | Confirm actual production rule, align optimizer + documentation, then rerun all tiers |
| **High** | Original Scenario 2 CSV had AM/PM jumps and comma-formatted prices | Upload final numeric `market_scenario_2_PHASE30_FIXED.csv`; rerun `market_scenario_2_PHASE30_AUDIT.csv` checks; verify deployed loader |
| **High** | Scenario 2 best-case strategy and target attainability not measured after data correction | Run the same optimizer on validated Scenario 2; compare targets by tier |
| **Medium** | Legacy audit workbook uses 150-tick reference and old text says ±30% per half-session | Update workbook formulas and other documentation to **300-tick reference** |
| **Medium** | Legacy numeric claims: 109×/156× and 217.45× | Label historical results or replace in input dictionary, contribution, README, and difficulty notes |
| **Medium** | Ownership and source citation inconsistency | Agree final Data Gatherer/Mechanism Designer ownership, link commits, reconcile source map and dates |

## 7. Source–use map

| Source | Use | Qualification |
|---|---|---|
| Background Korean market/margin news (references in older `SOURCE_USE_MAP.md`) | Learning context and scripted-news themes | Synthetic scenarios are **not historical price reconstructions**; verify exact external citation/dates before citing |
| Scenario datasets, audit workbooks and `build_market_scenario_2.py` | Market paths and validation evidence | Use final committed versions; distinguish legacy and repaired files |
| [`analysis/best_case.py`](../analysis/best_case.py) and `whole_share_srlp_*` outputs | Return ceilings, leverage sensitivity and house-target feasibility | Perfect foresight; Phase 6 discontinuity and settlement mismatch pending |
| Brokerage margin materials identified in old source map | Inspiration for margin teaching mechanics | Simulation thresholds are standardized game assumptions, not provider-specific claims |
| Industry and company news themes (AI/memory, EV batteries, ETF descriptions) | Scenario narrative and decoy/player-signal design | Context rather than formula-driven live price feeds |

**External references:** Some earlier source-map entries have no verifiable URLs in this document; add exact links before final submission. Earlier files also conflict on crisis date, maintenance margin (20% versus 30%), and whether circuit breakers are implemented. Do not silently claim these have been resolved.

## 8. Scope decision

The MVP market data exclude foreign-exchange rates, institutional market-maker and foreign-fund-flow parameters, central-bank-reserve variables, extra leveraged-market indicators, real-time feeds and microstructure depth. These are intentional teaching-model boundaries and should remain explicit in the final README.


Cũ:
# Data, Assumptions and Sources

> Consolidated from: `Market_Dataset.md`, `INPUT_DICTIONARY.md`, `ASSUMPTIONS.md`, `SOURCE_USE_MAP.md`, `Solution_Structure.md`, `best_case_base_for_target_3x_10x_100x.md`, `best_case.py`, the scenario CSVs and audit workbooks, and the Data Gatherer's contribution file.

## 1. Files
| File | Content | Used by |
|---|---|---|
| [data/market_scenario_1.csv](../data/market_scenario_1.csv) | Scenario 1: 50 assets × 1,800 s + 6 metadata columns | Engine / game controller; benchmark optimiser |
| `../data/market_scenario_2.csv` | Scenario 2: same structure, different price paths | Engine (alternative scenario) |
| `data/market_scenario_1_plot.png` | Price-index plot of Scenario 1 (second 1 = 100) | Documentation |
| `data/audit/market_scenario_audit_1.xlsm` | Sheets *Market Scenario*, *Data Audit* (1,800 rows, per-ticker Δ %), *Data Audit checked* (600 rows = 50 tickers × 12 AM/PM sessions, reference price and 70 % floor) | Validation of session limits |
| `data/audit/market_scenario_audit_2.xlsx` | *Market Scenario*, *Data Audit* | Validation |
| `analysis/best_case.py` | Whole-share benchmark optimiser (outputs `whole_share_srlp_summary/cycles/buy_allocations/margin_audit.csv` and an xlsx) | Target calibration |
| `best_case_portfolio_combos.csv`, `best_case_portfolio_summary.csv` | Earlier benchmark outputs cited by the Data Gatherer | Target calibration (earlier generation) |

Columns of both CSVs: `Scenario, Global_Second, Phase, Phase_Name, Phase_Second, Market_State` followed by 50 ticker price columns (KRW); `Market_State` is `TRADING` for all rows. The asset formerly named SK Hynix is called **Vintrumite** (naming change only).

## 2. Structure and validation (script re-check of the uploaded CSVs)
| Check | Scenario 1 | Scenario 2 |
|---|---|---|
| Rows × tickers / price cells | 1,800 × 50 / 90,000 | 1,800 × 50 / 90,000 |
| Missing / non-positive prices | 0 / 0 | 0 / 0 |
| `Global_Second` = 1…1,800 in order; no duplicate headers | Yes | Yes |
| Price columns stored as numbers | Yes | **No — 49 of 50 columns are text with thousands separators (e.g. `"154,126.40"`)** |
| Prices within ±30 % of the session-open reference | 0 violations (150 s sessions) | not checked (text format) |

Average change of the 50 assets from the first to the last second of each phase:

| Phase | Scenario 1 | Scenario 2 |
|---|---|---|
| 1 Fake Positive News | −0.3 % | +1.8 % |
| 2 True Positive News | −0.1 % | −1.0 % |
| 3 Bull Market | +1.5 % | −1.3 % |
| 4 Strong Growth (FOMO) | +1.2 % | +3.0 % |
| 5 Market Euphoria | +2.4 % | +1.1 % |
| 6 Negative Shock | −20.5 % (range −30.0 % … −6.2 %) | −13.5 % (range −20.2 % … +5.0 %) |

Scenario 1 drivers at second 1,500 versus second 1: TIGER Semiconductor TOP10 1.96×, Samsung Electronics 1.89×, Vintrumite 1.82×, KODEX Leverage 1.74×, KODEX Semiconductor 1.70× (next best asset 1.10×). Vintrumite: 1,447,000 → 2,636,174 (sec 1,500) → 1,845,322 (sec 1,800).

**Drivers:** Vintrumite, Samsung Electronics, KODEX Leverage, KODEX Semiconductor, TIGER Semiconductor TOP10 (delayed). **Decoys:** other assets with temporary spikes and reversals.

| Phase | Name | Seconds | Intended behaviour |
|---|---|---|---|
| 1 | Fake Positive News | 1–300 | Early uncertainty, decoy spikes |
| 2 | True Positive News | 301–600 | Fundamentals validate rally |
| 3 | Bull Market | 601–900 | Broad rally |
| 4 | Strong Growth (FOMO) | 901–1200 | Rapid surge, peak borrowing |
| 5 | Market Euphoria | 1201–1500 | Peak, fakeouts, bull traps |
| 6 | Negative Shock | 1501–1800 | Systemic crash |

Each phase = AM (first 150 s) + PM (last 150 s) session; ±30 % limit from each session's reference price.

## 3. Benchmarks and target calibration
| Generation | Result | Source |
|---|---|---|
| Earlier | Cash 2.92×–5.20×, 2× 7.02×–21.27×, 3× 14.72×–72.84×, 4× 27.99×–217.45× | `best_case_portfolio_summary.csv` |
| Current optimiser | Concentrated dynamic programming **≈ 109×** ($1.09 m); staggered re-leveraging **≈ 156×** ($1.56 m), +43.1 % | `best_case.py`, benchmark note |

`best_case.py`: $10,000 start, tiers 2×/3×/4×, whole shares, maintenance trigger ≤ 20 % with survival floor ≥ 20.001 %, 75 s settlement delay, MILP (SciPy) per cycle with 60 s limit and 0.1 % gap. The benchmark is best-case under perfect foresight, not a typical player result. Target ladder: 3× / 20× / 100× (≈ 1.9 %, 12.8 %, 64.1 % of 156×). Only Scenario 1 has been benchmarked.

## 4. Input dictionary
| Variable | Meaning | Format | Source | Affects |
|---|---|---|---|---|
| `assigned_scenario_id` | Random scenario; sets capital and price path | 1 or 2 | System | `initial_capital`, `fixed_price_path` |
| `initial_capital` | Starting cash | $10,000 / ₩20,000,000 baseline | System | Net worth, buying power |
| `fixed_price_path` | 1,800 s × 50 assets | CSV | Team dataset | Revaluation, alerts |
| `target_house_type` | Difficulty | Small / Normal / ToLam Villa | User | Target value, ending |
| `property_target_value` | Equity needed to win | multiplier × capital | Calculated | Progress, win/loss |
| `margin_tier` | Leverage tier | Cash 1×, 2×, 3×, 4× | User | Buying power, debt, liquidation |
| `orders` | Buy / Sell / Hold, ticker, volume, margin toggle | categorical + numeric | User | Cash, shares, debt, equity |
| `bank_savings` | Funds in savings | numeric | User / system | Liquidity |
| `savings_return_rate` | 4.75 % per completed AM/PM session | constant | System | Savings balance |

## 5. Assumptions
| # | Assumption | Main risk |
|---|---|---|
| 1 | Instant liquidity at tick price | Real fire sales suffer slippage |
| 2 | Deterministic 1,800 s scripted paths; two scenarios | Replays allow memorising peaks |
| 3 | Fixed 3× / 20× / 100× targets | Real property prices do not scale with capital |
| 4 | 100 % fill, unlimited volume | No partial fills / depth |
| 5 | ±30 % per AM/PM session limit, reset each session (+69 % / −51 % per phase) | Not exact exchange rules |
| 6 | Fixed 20 % maintenance margin | Brokers vary |
| 7 | Bank Savings +4.75 % per session | Amplified, unrealistic rate |

Player-facing disclosure sentences for each assumption are in the original `ASSUMPTIONS.md` (archive).

## 6. Data issues to resolve before submission
1. **Scenario 1, second 1,651:** all 50 assets jump up at the start of the Phase 6 PM session (mean +30 %, minimum +11.5 %); for example Vintrumite goes 1,932,051 → 2,636,174, back to its second-1,500 level. As a result drivers end Phase 6 at −30.0 % versus second 1,500, while the plot and the docs describe roughly −50 % to −57 %. Check the committed CSV against the plot and the audit workbook.
2. **Session-boundary jumps elsewhere:** Scenario 2 shows single-second moves up to +40 % at seconds 451, 751, 1,051 and 1,351 and a mean +16.6 % at 1,651; Scenario 1 has smaller jumps at the same boundaries. Confirm these are intended reference resets.
3. **Scenario 2 number format:** text values with commas will break CSV parsing in the engine or benchmark script — re-export as plain numbers.
4. **Scenario 2 calibration:** not yet benchmarked; starting prices differ from Scenario 1 for some tickers (e.g. Vintrumite 209,016.5 vs 1,447,000). Confirm that targets stay feasible.
5. **Benchmark generations:** 217.45× (Input Dictionary) versus ≈ 156× / 109× (optimiser) — update the Input Dictionary and difficulty text; `best_case.py` writes `whole_share_srlp_*` files, not the `best_case_portfolio_*` names cited elsewhere.
6. **Settlement delay:** 75 s in the optimiser versus 30 ticks in the engine.

## 7. Source–use map
| Source | Use | Limitation / modification |
|---|---|---|
| Korean margin-crisis price action (source map: April 2023) | Problem evidence, cascade baseline | Compressed from weeks to 1,800 s; intensified; circuit breakers omitted |
| Optimisation runs (`best_case.py`, `best_case_portfolio_*.csv`) | Wealth ceilings, target multiples | Perfect timing, frictionless execution |
| Korean brokerage margin rules (e.g. Kiwoom Securities) | Basis for 2×/3×/4× tiers and maintenance margin | Standardised to three tiers and one rule |
| Company news themes (AI memory demand, HBM, ASML collaboration, KODEX product descriptions) | Phase 1 news script | Context only; does not alter the synthetic prices |

`[TODO: add URLs/citations; SOURCE_USE_MAP lists none.]` Other inconsistencies: source map says maintenance margin **30 %** (everywhere else 20 %); crisis dated April 2023 vs mid-2026 elsewhere; `Market_Dataset` mentions circuit breakers in Phase 6, the source map says they are omitted; dataset documentation ownership differs between files (Nguyên vs Khánh).

## 8. Scope decision
Excluded from the MVP data: USD/KRW rates, institutional market-maker parameters, foreign-fund flows, central-bank reserves, extra leveraged-market indicators.
