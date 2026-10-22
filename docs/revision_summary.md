# Revision Summary (after midterm)

> `Revision_log.md` is empty. This table is derived by comparing Week 4 (`MIDTERM_REVIEW`), Week 5 (`Feature_map`, `Solution_Structure`, `Input_Dictionary`), the midterm verification, the individual contribution files and Week 6 (`bug_log`, `test_case`, benchmark note, scenario files). `[TODO: confirm and add dates/authors.]`

| # | Revision | From → To | Reason | Evidence |
|---|---|---|---|---|
| 1 | Differentiate from Free Fall 1 (K62) | Debt-free puzzle → margin trading, forced liquidation | Core identity | Midterm verification |
| 2 | Property targets | 2× / 8× (Mini Apartment, Gangnam Villa) → 3× / 20× / 100× | Calibrated on benchmarks | [financial_logic.md](financial_logic.md) §6 |
| 3 | Leverage input | `initial_margin_ratio` 50/40/33/25 % → tiers Cash/2×/3×/4× | Simpler, matches tests | Input Dictionary |
| 4 | Scenarios | One scenario → random Scenario 1 or 2 (both CSVs now exist) | Reduce memorisation | [data_and_sources.md](data_and_sources.md) |
| 5 | Rules added | Bank Savings 4.75 %/session, T+0.5 settlement, 5 % penalty, ±30 % session limits | De-risking, realism | Assumptions 5, 7 |
| 6 | Feature scope | Week 5 keep / postpone / remove | Protect margin-cycle focus | [user_flow.md](user_flow.md) §3 |
| 7 | Data scope | Dropped USD/KRW, institutional, fund-flow, central-bank data | Not needed | [data_and_sources.md](data_and_sources.md) §8 |
| 8 | Asset naming | SK Hynix → Vintrumite | Game naming | Data Gatherer file |
| 9 | Dataset audit | Structural audit; audit workbooks with AM/PM reference/floor sheet | Integration readiness | `data/audit/` |
| 10 | Benchmark method | Earlier summary (ceiling 217.45×) → whole-share MILP optimiser: ≈ 109× → ≈ 156× | Richer, more defensible best case | `analysis/best_case.py` |
| 11 | Tests | 4 unit tests (midterm) → 12 formal cases / 14-test run documented; committed file still shows 4 | Week 6 clinic | [testing.md](testing.md) |
| 12 | Defects | BUG-01…06 fixed and verified | Stability before freeze | [testing.md](testing.md) §5 |
| 13 | Technical route | Planned React/Next.js (Streamlit fallback) → Python engine + API + HTML interface | Feasibility `[TODO: confirm]` | `src/`, `index.html` |
| 14 | Hosting | GitHub Pages demo plus a Cloudflare build | Delivery | README |
| 15 | Repository | Weekly folders → final-readiness structure | Evidence easy to find | This repo |

**Stated next steps still open:** Scenario 2 calibration and benchmark re-run; Phase 2–6 news; debrief screen and formulas; Phase 6 execution-penalty refinement; target-progress calculations for the dashboard; mobile layout.
