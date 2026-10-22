# Nguyễn Hồng Nguyên — Individual Footprint

*Data gatherer · Quantitative calibration*

## My main responsibility

My role was to **construct and validate the deterministic market environment** used by Free Fall 2.0 and to **quantitatively test the game's financial difficulty**. The educational goal is to help inexperienced investors understand how leverage, market volatility, changing equity and margin liquidation interact—not merely to maximize simulated profits. My work translates this goal into price paths, investable alternatives and reproducible feasibility tests for the three house targets.

I also provided **quantitative feedback** during the team's design of margin tiers, liquidation, market-price constraints and Bank Savings. The Mechanism Designer retains ownership of the formal game financial formulas and rule specification; my contribution in that area is data-based testing, calibration and collaborative revision rather than sole financial-engine authorship.

## My concrete outputs

| Workstream | My contribution | Player/product value |
|---|---|---|
| **Market scenario construction** | Prepared two deterministic scenarios, each with **50 assets × 1,800 ticks**, six phases and AM/PM structure | Provides a consistent, replayable environment for choosing assets and seeing portfolio outcomes |
| **Driver and decoy behavior** | Differentiated sustained rallies, temporary spikes, sector/asset contrasts and late-game downside | Forces players to distinguish momentum from misleading signals, rather than select an obvious universal winner |
| **Scenario 2 dataset revision** | Identified abnormal AM→PM jumps; produced a corrected CSV, reproducible script and an audit output for **±30% per full 300-tick phase**, AM/PM continuity and adjacent-phase continuity | Reduces artificial gains/losses caused by discontinuous market inputs |
| **Portfolio benchmark testing** | Assessed whole-share concentrated DP and staggered re-leveraging across fixed 2×, 3×, 4× margin tiers, using the market dataset | Measures how leverage, timing and reinvestment change attainable equity |
| **Property-target calibration** | Updated feasibility comparisons for **Small House 3×, Normal House 20× and ToLam Villa 100×** using actual optimizer output | Tests whether game goals are feasible rather than arbitrarily chosen |
| **Collaborative financial-mechanic review** | Provided quantitative feedback on margin health, liquidation exposure, settlement assumptions, market constraints and Bank Savings | Helps the Mechanism Designer align financial rules with market-data outcomes |
| **Ticker naming and documentation** | Maintained naming alignment, including the change **SK Hynix → Vintrumite** | Keeps player-facing labels and code/data references consistent |

### Latest Scenario 1 calibration results (22 October 2026)

Under the **current optimizer's assumptions** ($10,000 start, whole shares, price divisor 1,400, settlement delay 75 ticks, maintenance threshold 20%, survival floor 20.001%), the user-provided run reports:

| Margin tier | Concentrated DP | Staggered re-leveraging | 3× | 20× | 100× |
|---|---:|---:|---|---|---|
| **2×** | **42.195490×** | **45.224575×** | PASS | PASS | BELOW |
| **3×** | **168.882379×** | **203.814472×** | PASS | PASS | PASS* |
| **4×** | **562.120612×** | **785.811533×** | PASS | PASS | PASS |

**These results are provisional.** A suspected discontinuity at **Scenario 1 tick 1650→1651** materially affects the final trading cycle, especially the 3× path's crossing of 100×. They demonstrate what the current optimizer finds on the current price file, **not** actual player success probabilities or final validated game difficulty.

## Evidence links

- [Scenario datasets and validation inputs](../../data/) — attach and verify the final Scenario 1/2 CSVs.
- [Data, assumptions, calibration and outstanding QA](../../docs/data_and_sources.md) — detailed data and method summary.
- [`analysis/best_case.py`](../../analysis/best_case.py) — whole-share DP and staggered MILP code; verify the committed version includes target calibration.
- `market_scenario_2.csv` — Scenario 2 data **(add verified repo path)**.
- `market_scenario_2_audit.xlsx` — Scenario 2 audit **(add verified repo path)**.
- `build_market_scenario_2.py` — scripted correction/validation **(add verified repo path)**.
- `whole_share_srlp_summary.csv`, `whole_share_srlp_cycles.csv`, `whole_share_srlp_buy_allocations.csv`, `whole_share_srlp_margin_audit.csv` — latest optimizer results **(add verified repo links)**.
- `target_calibration_3x_20x_100x.csv` — updated target-attainment comparison **(add verified repo link)**.
- [Original midterm contribution evidence](../evidence/Hồng_Nguyên_CONTRIBUTIONS.md) — ownership and earlier target-calibration rationale; check actual filename before publishing.

**GitHub commits / PRs:** *[Add actual commit or PR links documenting dataset generation, validation, review and integration. Do not invent links.]*

## How my work is used

The game reads the selected scenario's price path each tick to revalue holdings and expose the consequences of BUY/SELL/holding and leverage decisions. My datasets supply the changing market conditions, while the benchmark analysis evaluates whether target requirements are reachable under the model. Players therefore observe **market volatility → equity changes → margin health → possible liquidation**, with different asset behavior making their choices consequential.

The benchmark is a **calibration diagnostic**, not a player-facing promise of wealth: it uses complete knowledge of future price movements that players do not possess.

## Integration, testing and revision

My calibration workflow is:

`Market price path → Data-integrity audit → Portfolio optimization → Leverage/wealth outcomes → 3× / 20× / 100× target assessment → Design feedback`

For Scenario 2, the earlier original data exhibited widespread AM→PM price gaps. The revised data and its audit were prepared to enforce **one ±30% band per 300-tick phase**, rather than resetting the band at the 150-tick midpoint. The correction run reported all 300 AM/PM equal-price checks, 250 adjacent-phase boundary checks and 300 phase-cap checks as passing. **Integration of that particular revised CSV into the final game build remains to be confirmed with a repository commit and loader/test evidence.**

For Scenario 1, a current review has surfaced a Phase 6 price discontinuity; the benchmark results therefore remain **provisional** until the dataset, optimizer and game engine use consistent final rules.

## Remaining limitations and next actions

1. **Correct Scenario 1 tick 1650→1651** and rerun 2×/3×/4× optimization; the current final-cycle returns are potentially inflated.
2. **Reconcile settlement:** supplied `best_case.py` uses **75 ticks**, whereas another engine note reports **30 ticks**. Calibrate against the actual final game rule.
3. **Run Scenario 2 optimization** on the validated **numeric** final CSV; Scenario 2's market-data correction is not the same as completing target calibration.
4. **Verify integration evidence:** attach final CSVs, audit, output files and actual commit/PR links; confirm the deployed game reads the same dataset version.
5. **Keep model limitations explicit:** deterministic prices, perfect-foresight optimizer, no transaction costs/slippage and simplified liquidity.

**Individual contribution statement:** My contribution is not simply collecting stock prices. I created and validated a structured market environment and used reproducible portfolio analysis to test whether the game meaningfully exposes players to the trade-off between return, leverage, margin safety and liquidation risk.

Cũ:
# Nguyễn Hồng Nguyên — Individual Footprint

*Data gatherer · Quantitative calibration*

## My main responsibility
Owned the market scenario datasets and the quantitative calibration of targets and margin tiers; contributed quantitative feedback to the margin, session-limit and Bank Savings rules.

## My concrete outputs
- Scenario datasets: 50 assets × 1,800 s across six phases (AM/PM sessions), drivers and decoys, synchronised Phase 6 crash; Scenario 1 and Scenario 2 files
- Portfolio combination tests and benchmark summaries for Cash / 2× / 3× / 4×
- Calibration of Small / Normal / ToLam Villa targets and the margin-tier structure
- Audit workbooks (session reference prices and 70 % floors)
- Renamed SK Hynix to Vintrumite

## Evidence links
- [data/](../../data)
- [docs/data_and_sources.md](../../docs/data_and_sources.md)
- Original evidence: [HONG_NGUYEN_CONTRIBUTIONS.md](../evidence/Hồng_Nguyên_CONTRIBUTIONS.md)

## How my work is used
The engine reads the price paths every tick; the benchmarks show that targets are achievable with discipline but exposed to the Phase 6 crash.

## Integration, testing and revision
Calibration loop: price paths → portfolio tests → leverage outcomes → wealth ceilings → target thresholds. Data is loaded by [src/game_controller.py](../../src/game_controller.py). `[TODO: link commits]`

## Remaining limitation
Scenario 2 still needs calibration and benchmark re-runs (stated next step); a re-check of the CSVs found a ≈ +30 % jump at second 1,651 in Scenario 1 and text-formatted numbers in Scenario 2 — see [data_and_sources.md](../../docs/data_and_sources.md) §6.

> Short version of [evidence/HONG_NGUYEN_CONTRIBUTIONS.md](../evidence/Hồng_Nguyên_CONTRIBUTIONS.md). **Nguyễn Hồng Nguyên should review, correct and sign off.**
