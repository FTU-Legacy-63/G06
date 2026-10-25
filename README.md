# 📉 Free Fall 2.0

**An interactive, web-based market-crash survival simulator in which players manage a leveraged stock portfolio and experience how margin, liquidity, and forced liquidation interact under extreme volatility.**

*Technology Applications in Finance and Banking – NHA408E · Foreign Trade University (FTU) 2026 · Group 06*

| Resource | Link |
|---|---|
| **Live Product** | [Cloudflare Worker](https://phan-dung.ngqminh6979.workers.dev/) *(Backup mirror: [https://ftu-legacy-63.github.io/G06/](https://ftu-legacy-63.github.io/G06/))* |
| **Comprehensive Final Report** | [FINAL_GROUP_REPORT.md](FINAL_GROUP_REPORT.md) |
| **Final Release** | [GitHub Release v1.0.0](https://github.com/FTU-Legacy-63/G06/releases/tag/v1.0.0) |
| **Repository** | [https://github.com/FTU-Legacy-63/G06](https://github.com/FTU-Legacy-63/G06) |

---

## 1. Finance Problem
Textbooks explain margin trading and liquidation through static balance sheets. Inexperienced investors therefore underestimate downside exposure and panic when leverage, margin pressure, and forced liquidation combine during a crash (**leverage blindness**). Free Fall 2.0 addresses the gap between knowing static margin formulas and managing an account under real-time deterioration.

## 2. Target User
Retail equity traders, day traders, and finance and banking students who need risk-management practice in a safe environment.

## 3. User Task and Decision Loop
Manage a leveraged portfolio across a compressed 30-minute market session (1,800 seconds across 6 market phases):
- **Decisions:** Buy, Sell, Hold, select a Margin Tier (Cash 1×, 2×, 3×, 4×), de-leverage open positions, or allocate uninvested funds into Safe Haven Bank Savings.
- **Objective:** Survive market shocks without triggering a maintenance margin breach while pursuing property wealth targets: Small House (3×), Normal House (20×), or ToLam Villa (100× initial capital).

## 4. Main Product Output
1. **Interactive Trading Terminal:** Real-time asset price boards, portfolio revaluation, net equity, effective leverage gauges, margin health indicators, and liquidation risk warnings.
2. **Post-Simulation Risk Review:** Detailed accounting breakdown of final net equity, margin debt, liquidation audit logs, target attainment status, and one of four narrative endings (*Normie*, *Middle-Class Stability*, *Extravagant Luxury*, or *Wipeout*).

## 5. How the Product Works
```text
Scenario & Capital Selection → House Target & Margin Tier → 1,800-Second Market Session
  → Order Placement & Validation → Portfolio Revaluation → Margin Health Monitoring
  → Forced Liquidation Check (if ratio < 20%) → Debrief & Behavioral Review
```

- **Input:** Deterministic scenario selection (`market_scenario_1.csv` or `market_scenario_2.csv`), initial capital ($10,000 USD or ₩20,000,000 KRW), target house tier, Buy/Sell orders, and Bank Savings transfers.
- **Process:** Each second (tick), the engine pulls price updates from the dataset, recalculates gross stock exposure, updates margin debt and equity, enforces T+0.5 settlement holding pens, credits compounded bank savings (+4.75% per completed session), and triggers immediate forced liquidation if margin ratio drops below 20.00% or leverage reaches 5.0×.
- **Output:** Live HUD updates, audio-visual margin alerts, and an end-of-game performance review.

Detailed specifications: [Financial Logic](docs/financial_logic.md) · [User Flow](docs/user_flow.md)

## 6. How to Run and Access

### Web Application
Access the deployed terminal directly in any modern desktop browser:
- Primary: [https://ftu-legacy-63.github.io/G06/](https://ftu-legacy-63.github.io/G06/)
- Mirror: [https://phan-dung.ngqminh6979.workers.dev/](https://phan-dung.ngqminh6979.workers.dev/)

### Local HTTP Simulation Server & API Bridge
Run the zero-dependency REST server to serve the frontend locally:
```bash
python api_server.py
```
Open `http://localhost:8000` in your web browser.

### Interactive CLI Prototype
Run the terminal-based decision engine:
```bash
python src/interactive_demo.py
```

### Automated Unit Test Suite
Run the test runner from the repository root:
```bash
python -m unittest discover tests
```
*Current test run: 66 tests passing (100% pass rate).*

### Environment & Dependencies
- **Core Engine, API, & Tests:** Zero external dependencies. Built entirely on the Python Standard Library (`unittest`, `http.server`, `json`, `csv`, `dataclasses`, `enum`, `math`, `threading`). Tested on Python 3.10, 3.11, 3.12, and 3.14.
- **Quantitative Benchmark Optimizer (`analysis/best_case.py`):** Requires `pandas>=2.0.0`, `numpy>=1.24.0`, and `scipy>=1.10.0`. Install via:
  ```bash
  pip install -r requirements.txt
  ```

## 7. Sample Input and Example Use Cases
Formal specifications and test logs are detailed in [`docs/testing.md`](docs/testing.md).

- **Boundary Maintenance Case (Tests T03–T04):** Initial capital $10,000 at 4× margin. Buy 400 shares @ $100 (Position = $40,000, Debt = $30,000, Margin Ratio = 25.00%). A −6.25% price drop to $93.75 reduces equity to $7,500 on $37,500 position, hitting exactly **20.00%** (`WARNING` status, no liquidation). A single cent further drop to $93.74 yields **19.9914%** (`MARGIN_CALL`), immediately triggering forced liquidation.
- **High-Leverage Wipeout with Liquidation Penalty (Test T09):** Capital ₩10,000,000 at 4× margin (Position = ₩40,000,000, Debt = ₩30,000,000). A −20% shock drops position value to ₩32,000,000 (Margin Ratio = 6.25%). The broker liquidates all shares, takes a 5% penalty fee (₩1,600,000), collects net proceeds of ₩30,400,000, and fully repays the ₩30,000,000 debt. Remaining cash is **₩400,000** (a 96% loss).
- **Safe Haven Bank Protection (Test T10):** A user deposits $4,000 into Bank Savings. Even during a −50% market collapse in Phase 6, the bank principal remains intact and compounds at +4.75% per completed session.

## 8. Financial Logic Summary
- **Gross Exposure:** $\sum \text{Shares}_i \times \text{Current Price}_i$
- **Trading Equity:** $\text{Liquid Cash} + \text{Gross Exposure} - \text{Margin Debt}$
- **Total Net Worth:** $\text{Trading Equity} + \text{Bank Savings}$
- **Effective Leverage:** $\text{Gross Exposure} \div \text{Trading Equity}$
- **Margin Ratio:** $\text{Trading Equity} \div \text{Gross Exposure}$
- **Liquidation Rules:** Triggered if Effective Leverage $\ge 5.0\times$ or Margin Ratio $< 20.00\%$. The broker executes a fire-sale of all holdings at the current tick, subtracts a 5% penalty from gross proceeds, repays margin debt, and locks trading if remaining equity $\le 0$.
- **Settlement Delay (T+0.5):** Orders before tick 150 of any phase settle in 30 seconds (tick + 30). Orders placed at or after tick 150 remain in the holding pen until the start of the next phase.

Full formula specifications: [`docs/financial_logic.md`](docs/financial_logic.md).

## 9. Data and Source Summary
The simulation runs on two deterministic market datasets (`data/market_scenario_1.csv` and `data/market_scenario_2.csv`), each tracking 50 Korean stocks and leveraged ETFs over 1,800 ticks (6 phases × 300 ticks).
- Datasets are modeled on the mid-2026 South Korea margin crisis and audited for AM/PM price continuity, phase-boundary continuity, and ±30% phase price limits (`data/audit/`).
- Wealth targets are calibrated via whole-share Dynamic Programming and staggered MILP optimization (`analysis/best_case.py`), establishing empirical upper-bound milestones of ~109× (concentrated) and ~156× (staggered re-leveraging).

Full data dictionary and audit logs: [`docs/data_and_sources.md`](docs/data_and_sources.md).

## 10. Testing Summary
The automated test suite in `tests/` contains **66 unit tests** covering:
- **12 Formal Test Specifications (T01–T12):** Normal execution, boundary maintenance, invalid input handling, and financial consistency.
- **Bug Resolution Regressions:** Verification of fixes for BUG-01 through BUG-06 (settlement queues, margin multiplier initialization, state locks, zero-cash validations).
- **HTML/UI Parity:** Complete visual and functional parity between `index.html` and `web/index.html`.

Complete verification table and bug triage logs: [`docs/testing.md`](docs/testing.md).

## 11. Known Limitations
- Orders execute with instant tick liquidity and zero slippage (order-book depth modeling was placed out of MVP scope).
- Prices are deterministic and synthetic to ensure reproducible classroom evaluation.
- Broker maintenance margin is standardized at 20.00% across all securities.

Full limitations: [`docs/limitations.md`](docs/limitations.md) · Post-midterm revision history: [`docs/revision_summary.md`](docs/revision_summary.md).

## 12. Team and Individual Responsibilities

| Member | Student ID | Primary Role | Core Responsibility |
|---|---|---|---|
| **Trần Hữu Dụ** | 2412380013 | Coordinator · Mechanism Designer | Financial logic rules, formulas, target matrix, Phase 1 system workflow diagram |
| **Nguyễn Hồng Nguyên** | 2412380038 | Data Gatherer · Quantitative Calibration | Dual-scenario price datasets, audit workbooks, MILP benchmark optimization |
| **Cáp Phan Quang Khánh** | 2412380020 | Scenario Designer | Scenario narrative trees, six-phase event scripts, player decision mapping |
| **Nguyễn Quang Minh** | 2412380031 | Technical Developer · Engine Architect | Python simulation engine, state controller, REST API server, automated test suite |
| **Triệu Đức Lương** | 2412380029 | UI/UX & Frontend Designer | Trading terminal UI, dark-mode design system, live gauges, GitHub Pages deployment |

- [Group Contribution Map](contribution/contribution_map.md)
- Individual Footprints: [Trần Hữu Dụ](contribution/individual/tran-huu-du.md) · [Nguyễn Hồng Nguyên](contribution/individual/nguyen-hong-nguyen.md) · [Cáp Phan Quang Khánh](contribution/individual/cap-phan-quang-khanh.md) · [Nguyễn Quang Minh](contribution/individual/nguyen-quang-minh.md) · [Triệu Đức Lương](contribution/individual/trieu-duc-luong.md)

## Repository Layout
```text
/
├── README.md                 # Primary project overview and quickstart guide
├── requirements.txt          # Python dependency specifications
├── index.html                # Standalone trading terminal interface (root deployment)
├── api_server.py             # HTTP REST API server bridging engine with frontend
├── docs/                     # Detailed project documentation
│   ├── financial_logic.md    # Accounting identities, margin formulas, risk enforcement
│   ├── data_and_sources.md   # Dataset schema, audit workbooks, benchmark notes
│   ├── user_flow.md          # System workflow, player paths, phase scripts
│   ├── testing.md            # 4-tier testing framework, master test table, bug triage
│   ├── limitations.md        # Technical and financial constraints
│   ├── revision_summary.md   # Chronological log of post-midterm refinements
│   └── img/                  # Architecture diagrams and system flowcharts
├── contribution/             # Individual and team accountability files
│   ├── contribution_map.md   # Consolidated group contribution matrix
│   ├── individual/           # Individual footprint markdown files (all 5 members)
│   └── evidence/             # Original individual contribution records
├── src/                      # Backend Python simulation modules
│   ├── simulation_engine.py  # Portfolio valuation, margin ratios, liquidation penalty
│   ├── game_controller.py    # 1,800-tick phase management, order validation
│   ├── interactive_demo.py   # Standalone CLI prototype
│   └── api_server.py         # Module copy of the HTTP REST API server
├── tests/                    # Automated unit test suite (66 tests, 100% pass)
│   ├── test_simulation_engine.py
│   ├── test_week6_integration.py
│   ├── test_bug_fixes_5_to_11.py
│   ├── test_critical_bugs_c1_to_c5.py
│   ├── test_moderate_and_visual_fixes.py
│   └── test_complete_bug_report_45.py
├── data/                     # Deterministic market price datasets and audit files
│   ├── market_scenario_1.csv
│   ├── market_scenario_2.csv
│   └── audit/                # Excel audit workbooks for scenario continuity
├── analysis/                 # Quantitative optimization and benchmark models
│   ├── best_case.py          # Whole-share DP and staggered MILP optimizer
│   └── output/               # Calibration tables and buy-allocation summaries
├── web/                      # Web frontend assets and mirrored client files
│   ├── index.html            # Mirrored trading terminal interface
│   └── data/                 # Client-side market tick data arrays
├── assets/                   # Background illustrations and UI images
└── archive/                  # Historical weekly deliverables (Weeks 2–6)
```
