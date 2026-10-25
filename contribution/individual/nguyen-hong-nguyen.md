# Nguyễn Hồng Nguyên — Individual Footprint

*Data gatherer · Quantitative calibration*

## My main responsibility
Owned the construction and validation of the two market-scenario datasets and the quantitative calibration of portfolio benchmarks, leverage tiers and property targets. Provided data-based feedback on margin risk, settlement, phase price limits and Bank Savings; the Mechanism Designer owns the formal financial rules.

## My concrete outputs
- Market data: two deterministic scenarios, each with 50 assets × 1,800 ticks across six phases, with distinct drivers, temporary spikes, decoys and late-game downside
- Data validation: corrected Scenario 1 and Scenario 2 price paths; checked AM/PM continuity, adjacent-phase continuity and ±30% limits measured from the beginning of each full 300-tick phase
- Audit evidence: `market_scenario_audit_1.xlsm` and `market_scenario_audit_2.xlsx`, supported by dataset correction and QA checks
- Portfolio optimization: whole-share concentrated DP and staggered re-leveraging MILP for 2× / 3× / 4× margin tiers, run on both corrected scenarios
- Latest staggered wealth multiples (Scenario 1): **31.5346× / 156.8695× / 491.6970×** for 2× / 3× / 4×; Scenario 2: **137.8177× / 1,127.3221× / 5,990.4436×**, respectively
- Property targets: calibrated Small House **3×**, Normal House **20×** and ToLam Villa **100×**; the optimizer reaches all three targets in both scenarios at 3× and 4× leverage, while Scenario 1 at 2× remains below 100×
- Documentation: market assumptions, validation, optimization methodology and target-calibration evidence; aligned the player-facing ticker name **SK Hynix → Vintrumite**

## Evidence links
- [data/market_scenario_1.csv](../../data/market_scenario_1.csv) and [data/market_scenario_2.csv](../../data/market_scenario_2.csv) (final market datasets)
- [data/audit/market_scenario_audit_1.xlsm](../../data/audit/market_scenario_audit_1.xlsm) and [data/audit/market_scenario_audit_2.xlsx](../../data/audit/market_scenario_audit_2.xlsx) (audit workbooks)
- [analysis/best_case.py](../../analysis/best_case.py) and [analysis/best_case_calibration_targets_3x_20x_100x.md](../../analysis/best_case_calibration_targets_3x_20x_100x.md) (optimizer and calibration explanation)
- [analysis/output/combined/](../../analysis/output/) (combined optimization, margin-audit and target-calibration outputs; link applies after committing the output directory)
- [docs/data_and_sources.md](../../docs/data_and_sources.md) (data assumptions, constraints and QA)
- Original evidence: [Hồng_Nguyên_CONTRIBUTIONS.md](../evidence/Hồng_Nguyên_CONTRIBUTIONS.md)

## How my work is used
The game engine reads a selected scenario's price path every tick to revalue holdings and expose the effects of trading, leverage and market shocks on equity and margin safety. The Mechanism Designer defines the financial rules, the Technical Developer implements them, and my datasets and optimization outputs support scenario testing and target calibration.

## Integration, testing and revision
Both corrected datasets passed the 1,800-tick / 50-asset checks, AM/PM and phase-boundary continuity, and the phase-wide ±30% price caps. I reran the whole-share DP and staggered MILP across both scenarios and compared 3× / 20× / 100× target attainment. In Scenario 1 at 2× leverage, one MILP cycle ended above the 0.1% target gap (0.195264%), so not all cycles were proven optimal to tolerance. 

## Remaining limitation
The optimizer assumes advance knowledge of future prices and therefore does not estimate typical player success rates or establish a global wealth optimum. Its 75-tick settlement assumption should be reconciled with the implemented game engine, and the scenario datasets, audit workbooks and result files should be checked against their final committed versions.
