# 📉 Free Fall 2.0

**An interactive, web-based market-crash survival simulator in which players manage a leveraged stock portfolio and experience how margin, liquidity and forced liquidation interact under extreme volatility.**

*Technology Applications in Finance and Banking – NHA408E · FTU 2026 · Group 06*

| | |
|---|---|
| **Live product** | GitHub Pages: https://ftu-legacy-63.github.io/G06/ · Cloudflare build: https://phan-dung.ngqminh6979.workers.dev/ — `[TODO: state which one is the official final build]` |
| **Final release** | `[TODO: create tag/Release, e.g. v1.0-final, and paste link]` |
| **Repository** | https://github.com/FTU-Legacy-63/G06 |

---

## 1. Finance problem
Traditional financial education explains margin trading and liquidation through static formulas. Inexperienced investors therefore underestimate downside exposure and decide poorly when leverage, margin pressure and forced liquidation combine during a crash (**leverage blindness**). Free Fall 2.0 targets the gap between *knowing how leverage works* and *managing it while the account is deteriorating*.

## 2. Target user
Retail investors, inexperienced day traders, and finance and banking students.

## 3. User task / decision
Manage a leveraged portfolio through a compressed 30-minute market session: **Buy / Sell / Hold, choose a margin tier (Cash 1×, 2×, 3×, 4×), de-leverage, or move cash into Bank Savings** before margin health forces a liquidation, while pursuing a property-based wealth target (Small House 3×, Normal House 20×, ToLam Villa 100× of initial capital).

## 4. Main product output
1. **Interactive trading simulator**: prices, portfolio value, net equity, effective leverage, margin health, target progress, liquidation risk.
2. **Post-simulation risk & decision review**: final net equity, margin debt, liquidation status, target result and one of the narrative endings (Normie / Middle-Class Stability / Extravagant Luxury / Wipeout).

*(Scenario Playback, detailed behavioural classification, advanced charts and export were postponed — see [limitations](docs/limitations.md).)*

## 5. How the product works
`Scenario & capital → House target → Margin tier → 1,800-second market (6 phases × 300 s) → Orders → Revaluation → Margin check → Consequence → Debrief`

- **Input:** assigned scenario (`market_scenario_1.csv` or `market_scenario_2.csv`) and initial capital ($10,000 / ₩20,000,000 baseline), target house, margin tier, Buy/Sell orders, Bank Savings deposits/withdrawals.
- **Process:** every tick the engine reads prices from the deterministic dataset, revalues holdings, updates margin debt, net equity, effective leverage and margin ratio, delivers pending (T+0.5) orders, accrues Bank Savings, and triggers forced liquidation when the maintenance rule is breached.
- **Output:** live account metrics and warnings, then the final review.

Details: [financial logic](docs/financial_logic.md) · [user flow](docs/user_flow.md)

## 6. How to run / access
- **Web build:** https://ftu-legacy-63.github.io/G06/ and https://phan-dung.ngqminh6979.workers.dev/ `[TODO: keep only the official one]`
- **CLI prototype:** `python src/interactive_demo.py`
- **REST API for the web UI:** `python src/api_server.py`
- **Automated tests (from repo root):** `python -m unittest discover tests` — see [testing.md](docs/testing.md) for what the current test file covers
- **Dependencies:** `[TODO: Python version / requirements.txt]`

## 7. Sample input and example use case
Full cases: [`docs/testing.md`](docs/testing.md) (T01–T12) and the sample scenarios below.

**Boundary example (tests T02–T04):** capital $10,000, 4× tier, buy 400 shares @ $100 → cost $40,000, margin debt $30,000, margin ratio **25.00 %**. A −6.25 % price move ($93.75) gives ratio **20.00 %** (warning, no liquidation); one cent lower ($93.74) gives **19.99 %** → margin call and immediate forced liquidation.

**Wipeout example (test T09):** capital ₩10m, 4× → position ₩40m, debt ₩30m. After a −20 % shock the position is worth ₩32m (ratio 6.25 %); liquidation applies a 5 % penalty (₩1.6m), net proceeds ₩30.4m repay the ₩30m debt, leaving **₩0.4m** of the original ₩10m.

**Scenario examples:** *ToLam Villa + 4× held into Phase 6 → forced liquidation / possible wipeout*; *Small House + cash only, rotated into Bank Savings before Phase 6 → solvent at ≈ 2.92× capital*.

## 8. Financial logic summary
Net equity = cash + Bank Savings + stock value − margin debt · Effective leverage = stock value ÷ net equity · Margin ratio = net equity ÷ stock value. Forced liquidation when leverage ≥ 5.0× or margin ratio < 20 % (fire-sale of all open holdings + 5 % penalty). Bank Savings: +4.75 % per completed AM/PM session. Orders under tick 150 settle in-phase (T+0.5); later orders deliver at Phase 2 entry. Full rules: [financial_logic.md](docs/financial_logic.md).

## 9. Data and source summary
Two deterministic scenarios (`market_scenario_1.csv`, `market_scenario_2.csv`): each 50 Korean stocks/ETFs × 1,800 one-second prices (90,000 price cells), six phases, five market drivers plus decoy assets; synthetic and inspired by a Korean margin-crisis episode. Scenario 1 is audited (`market_scenario_audit_1.xlsm`) and benchmarked with `best_case.py` (whole-share optimiser: ≈ 109× concentrated, ≈ 156× staggered re-leveraging from $10,000); Scenario 2 has an audit workbook but no benchmark yet. See [data_and_sources.md](docs/data_and_sources.md).

## 10. Testing summary
`tests/test_simulation_engine.py` contains 4 engine tests (high-leverage wipeout with penalty, cash-only solvency, Bank Savings, T+0.5 settlement). The Week 6 specification `test_case.md` records 12 formal cases (T01–T12) and a 14-test run; 6 defects (BUG-01…06) were logged and verified fixed. The 12-case suite must be matched to the committed test file — see [testing.md](docs/testing.md).

## 11. Known limitations
[docs/limitations.md](docs/limitations.md) · Post-midterm changes: [docs/revision_summary.md](docs/revision_summary.md)

## 12. Team and contribution
| Member | Role |
|---|---|
| Trần Hữu Dụ | Coordinator · Mechanism designer |
| Nguyễn Hồng Nguyên | Data gatherer · Quantitative calibration |
| Cáp Phan Quang Khánh | Scenario designer · Content lead |
| Nguyễn Quang Minh | Technical developer · Engine architect |
| Triệu Đức Lương | UI/UX & frontend designer |

- [Group contribution map](contribution/contribution_map.md)
- Individual footprints: [Dụ](contribution/individual/tran-huu-du.md) · [Nguyên](contribution/individual/nguyen-hong-nguyen.md) · [Khánh](contribution/individual/cap-phan-quang-khanh.md) · [Minh](contribution/individual/nguyen-quang-minh.md) · [Lương](contribution/individual/trieu-duc-luong.md)

## Repository layout
```text
README.md
docs/            financial_logic · data_and_sources · user_flow · testing · limitations · revision_summary · img/
contribution/    contribution_map.md · individual/ · evidence/ (original *_CONTRIBUTIONS.md files)
src/             __init__.py · simulation_engine.py · game_controller.py · api_server.py · interactive_demo.py
analysis/        best_case.py (benchmark optimiser)
data/            market_scenario_1.csv · market_scenario_2.csv · audit/ (audit workbooks) · market_scenario_1_plot.png · best_case_* outputs
tests/           test_simulation_engine.py
web/ + index.html  trading-terminal interface
assets/          background images
archive/         original weekly submissions (Week 2–6, proposal, midterm files)
```
