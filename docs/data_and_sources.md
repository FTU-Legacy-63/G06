# Data, Assumptions and Sources

> Consolidated from: `Market_Dataset.md`, `INPUT_DICTIONARY.md`, `ASSUMPTIONS.md`, `SOURCE_USE_MAP.md`, `Solution_Structure.md`, `best_case_base_for_target_3x_10x_100x.md`, `best_case.py`, the scenario CSVs and audit workbooks, and the Data Gatherer's contribution file.

## 1. Files
| File | Content | Used by |
|---|---|---|
| [data/market_scenario_1.csv](data/market_scenario_1.csv) | Scenario 1: 50 assets × 1,800 s + 6 metadata columns | Engine / game controller; benchmark optimiser |
| `data/market_scenario_2.csv` | Scenario 2: same structure, different price paths | Engine (alternative scenario) |
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
