# Post-Midterm Revision Summary

This document traces the evolution of Free Fall 2.0 following the Week 4 midterm checkpoint, detailing key decisions, architectural adjustments, and defect remediations.

---

## 1. Post-Midterm Revision Log

| # | Domain | Original Midterm State | Final State | Rationale & Impact | Primary Owner | Verification Evidence |
|:---:|---|---|---|---|---|---|
| **1** | **Core Identity** | Early proposal conceptualized debt-free portfolio puzzles. | Dedicated margin trading simulator with cross-margin liquidation cascades. | Establishes pedagogical focus on "leverage blindness" during crashes. | Trần Hữu Dụ | Midterm Review, `financial_logic.md` |
| **2** | **Wealth Targets** | Initial targets set at 2× and 8× capital (Mini Apartment, Gangnam Villa). | Calibrated to 3× (Small House), 20× (Normal House), and 100× (ToLam Villa). | Grounded targets against whole-share optimization ceilings (~156× benchmark). | Nguyễn Hồng Nguyên | `best_case.py`, `analysis/` |
| **3** | **Leverage Interface** | Input requested continuous `initial_margin_ratio` percentages (50%, 40%, 33%, 25%). | Fixed tier selection: Cash 1.0×, 2.0×, 3.0×, and 4.0×. | Eliminates input friction for players under compressed time limits. | Trần Hữu Dụ | `game_controller.py`, `index.html` |
| **4** | **Market Scenarios** | Single market scenario path. | Dual deterministic scenarios (`market_scenario_1.csv` & `market_scenario_2.csv`). | Prevents players from memorizing turning points across runs. | Nguyễn Hồng Nguyên | `data/`, `data_and_sources.md` |
| **5** | **Hedging Mechanics** | All player cash remained exposed to stock market accounts. | Added Safe Haven Bank Savings earning +4.75% compounded per session. | Provides an explainable capital-preservation tool during crash phases. | Trần Hữu Dụ | `simulation_engine.py`, Test T10 |
| **6** | **Settlement Timing** | Instant intra-tick share settlements. | T+0.5 holding pen (orders before tick 150 settle in 30 ticks; orders $\ge$ 150 deliver in Phase 2). | Models real-world clearing delays and prevents high-frequency churn. | Trần Hữu Dụ, Nguyễn Quang Minh | `simulation_engine.py`, Test T11 |
| **7** | **Feature Scope Freeze** | Considered complex social leaderboards, user login, and order-book depth. | Frozen to single-player desktop trading terminal. | Protects MVP operational stability and prevents external server failure risks. | Full Group | `user_flow.md` §3, Checkpoint 5 |
| **8** | **Data Scope Trimming** | Considered macro FX (USD/KRW) feeds, foreign fund flows, and central bank rates. | Excluded macroeconomic feeds; focused on 50 stock price series. | Eliminates unnecessary cognitive noise for the player. | Nguyễn Hồng Nguyên | `data_and_sources.md` §8 |
| **9** | **Dataset Normalization** | Raw CSVs had price formatting issues, text commas, and boundary discontinuities. | Audited and normalized all 1,800 ticks across both scenarios; verified ±30% phase caps. | Ensures reliable runtime price lookup without NaN crashes. | Nguyễn Hồng Nguyên | `data/audit/` |
| **10** | **Benchmark Optimization** | Early continuous relaxation estimate (~217×). | Whole-share Dynamic Programming and staggered MILP optimizer (~156× ceiling). | Produces a mathematically defensible empirical benchmark. | Nguyễn Hồng Nguyên | `analysis/best_case.py` |
| **11** | **Automated Test Suite** | 4 initial midterm unit tests. | Expanded to 66 automated tests covering formal cases T01–T12 and defect regressions. | Provides 100% automated test coverage across boundary and failure states. | Nguyễn Quang Minh | `tests/` (100% passing) |
| **12** | **Defect Remediation** | Six defects logged during Week 6 testing (BUG-01 through BUG-06). | All 6 defects resolved, regression-tested, and verified. | Eliminates delivery freezes, attribute errors, and state corruption. | Nguyễn Quang Minh, Triệu Đức Lương | `docs/testing.md` §5 |
| **13** | **Technical Stack Route** | Early draft explored heavy multi-container Next.js/React stacks with Streamlit fallback. | Lightweight zero-dependency Python engine + REST API server + vanilla web terminal. | Guarantees instant local startup and zero-dependency reproducibility. | Nguyễn Quang Minh | `api_server.py`, `src/` |
| **14** | **Deployment Strategy** | Local testing only. | GitHub Pages client deployment paired with a Cloudflare Worker mirror. | Delivers immediate, zero-installation browser accessibility for reviewers. | Triệu Đức Lương | README, GitHub Pages |
| **15** | **Repository Structure** | Fragmented weekly submissions (`week 2/`, `week 3/`, etc.). | Reorganized into the standard `docs/`, `src/`, `tests/`, `data/`, `contribution/` layout. | Satisfies course repository readiness criteria and simplifies audit navigation. | Full Group | `final-repo-readiness.md` |

---

## 2. Scope Freeze Confirmation
In accordance with Week 6 checkpoint guidelines, feature development was formally frozen. Post-midterm efforts focused exclusively on algorithmic verification, dataset auditing, defect resolution, and documentation consolidation.
