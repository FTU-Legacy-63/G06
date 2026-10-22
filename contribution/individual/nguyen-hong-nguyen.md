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
- Original evidence: [HONG_NGUYEN_CONTRIBUTIONS.md]([contribution/evidence/Hồng_Nguyên_CONTRIBUTIONS.md](https://github.com/FTU-Legacy-63/G06/blob/432e72fb3704ada67889956f9a55187bf45839b8/contribution/evidence/H%E1%BB%93ng_Nguy%C3%AAn_CONTRIBUTIONS.md))

## How my work is used
The engine reads the price paths every tick; the benchmarks show that targets are achievable with discipline but exposed to the Phase 6 crash.

## Integration, testing and revision
Calibration loop: price paths → portfolio tests → leverage outcomes → wealth ceilings → target thresholds. Data is loaded by [src/game_controller.py](../../src/game_controller.py). `[TODO: link commits]`

## Remaining limitation
Scenario 2 still needs calibration and benchmark re-runs (stated next step); a re-check of the CSVs found a ≈ +30 % jump at second 1,651 in Scenario 1 and text-formatted numbers in Scenario 2 — see [data_and_sources.md](../../docs/data_and_sources.md) §6.

> Short version of [evidence/HONG_NGUYEN_CONTRIBUTIONS.md](../evidence/HONG_NGUYEN_CONTRIBUTIONS.md). **Nguyễn Hồng Nguyên should review, correct and sign off.**
