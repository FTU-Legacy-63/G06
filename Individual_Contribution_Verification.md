# NHA408E: Final Individual Contribution Verification (Group 06: Free Fall 2.0)

**Course:** Technology Applications in Finance and Banking (NHA408E)  
**Group:** Group 06 (Free Fall 2.0)  
**Repository:** https://github.com/FTU-Legacy-63/G06  
**Live Deployment:** https://phan-dung.ngqminh6979.workers.dev/ (Mirror: https://ftu-legacy-63.github.io/G06/)

---

## Question 1: Most Important Individual Contributions and Practical Significance

| Member (Student ID) | Area | Most Important Contribution & Repository Files | How It Is Used in the Final Product & Practical Significance |
|---|---|---|---|
| **Trần Hữu Dụ** (2412380013) | Financial Mechanism & System Workflow | **Margin Rulebook and Phase 1 System Flowchart**<br>- [`docs/financial_logic.md`](../docs/financial_logic.md)<br>- [`docs/img/phase_1_workflow.jpg`](../docs/img/phase_1_workflow.jpg)<br>- [`docs/user_flow.md`](../docs/user_flow.md) (§1–2)<br>- [`contribution/individual/tran-huu-du.md`](individual/tran-huu-du.md) | **Usage:** Defines the accounting identities (`Trading Equity = Cash + Stock Value - Margin Debt`, `Margin Ratio = Trading Equity / Stock Value`), the four leverage tiers (1.0x, 2.0x, 3.0x, 4.0x), the 20.00% maintenance margin floor, the 5% forced liquidation fee, the +4.75% per-session Safe Haven Bank rate, and the T+0.5 settlement rule.<br>**Practical Significance:** Gives the Python and JavaScript engines an exact mathematical specification. For example, at 4.0x leverage (25% initial margin), a 6.26% price drop breaches the 20% maintenance floor and triggers forced liquidation, teaching players non-linear margin path dependency rather than static textbook formulas. |
| **Nguyễn Hồng Nguyên** (2412380038) | Market Data & Quantitative Calibration | **Dual 50-Asset × 1,800-Tick Datasets and Whole-Share DP/MILP Calibration**<br>- [`data/market_scenario_1.csv`](../data/market_scenario_1.csv)<br>- [`data/market_scenario_2.csv`](../data/market_scenario_2.csv)<br>- [`data/audit/market_scenario_audit_1.xlsm`](../data/audit/market_scenario_audit_1.xlsm)<br>- [`data/audit/market_scenario_audit_2.xlsx`](../data/audit/market_scenario_audit_2.xlsx)<br>- [`analysis/best_case.py`](../analysis/best_case.py)<br>- [`docs/data_and_sources.md`](../docs/data_and_sources.md) | **Usage:** Supplies the tick-by-tick price feeds loaded by [`src/game_controller.py`](../src/game_controller.py) and [`index.html`](../index.html) across six 300-tick phases, while [`analysis/best_case.py`](../analysis/best_case.py) computes theoretical whole-share wealth ceilings under concentrated Dynamic Programming and staggered MILP models.<br>**Practical Significance:** Auditing AM/PM session continuity and ±30% phase price caps prevents NaN lookup errors and artificial price jumps during gameplay. The MILP ceilings (31.53x at 2x leverage, 156.87x at 3x, and 491.70x at 4x in Scenario 1) empirically ground the 3x (Small House), 20x (Normal House), and 100x (ToLam Villa) property targets so that reaching 100x requires taking real 3x–4x margin risk. |
| **Cáp Phan Quang Khánh** (2412380020) | Scenario Architecture & News Scripts | **Six-Phase Behavioral Narrative, Decision Tree, and Dual-Scenario News Feeds**<br>- [`docs/user_flow.md`](../docs/user_flow.md) (§5–7)<br>- [`data/Scenario1 news.md`](../data/Scenario1%20news.md)<br>- [`data/Scenario2 news.md`](../data/Scenario2%20news.md)<br>- [`contribution/individual/cap-phan-quang-khanh.md`](individual/cap-phan-quang-khanh.md) | **Usage:** Maps the six-phase narrative arc (Phase 1 Fake Positive News, Phase 2 True Positive News, Phase 3 Bull Market, Phase 4 FOMO Growth, Phase 5 Euphoria & Bull Traps, Phase 6 Negative Shock) and feeds timestamped macro and company news alerts (for Vintrumite, Samsung Electronics, KODEX Semiconductor, KODEX Leverage, and TIGER Semiconductor TOP10) into the in-game news dossier modal.<br>**Practical Significance:** Turns raw CSV price series into an information-filtering challenge. Players must distinguish noise and bull traps from fundamental catalysts before placing leveraged orders or moving cash into the Safe Haven Bank. |
| **Nguyễn Quang Minh** (2412380031) | Financial Engine, Full-Stack Integration & Automated Testing | **Core Python Simulation Engine, REST API, SPA ClientEngine, Web Audio Engine, and 66-Test Verification Suite**<br>- [`src/simulation_engine.py`](../src/simulation_engine.py)<br>- [`src/game_controller.py`](../src/game_controller.py)<br>- [`src/api_server.py`](../src/api_server.py)<br>- [`index.html`](../index.html) & [`web/index.html`](../web/index.html)<br>- [`tests/`](../tests/) (6 test modules, 66 tests)<br>- [`docs/testing.md`](../docs/testing.md) | **Usage:** Implements `MarginEngine` and `AccountState` in [`src/simulation_engine.py`](../src/simulation_engine.py), the 1,800-tick phase controller in [`src/game_controller.py`](../src/game_controller.py), the standard-library HTTP bridge in [`src/api_server.py`](../src/api_server.py), and the browser-side `ClientEngine`, Chart.js telemetry, and 17-track Web Audio state machine in [`index.html`](../index.html).<br>**Practical Significance:** Delivers a working, dual-runtime simulator that executes identical financial arithmetic in local Python grading scripts and in the browser on Cloudflare Workers and GitHub Pages. The 66 automated unit tests guard against regression bugs, price spoofing, and floating-point drift. |
| **Triệu Đức Lương** (2412380029) | UI/UX Design & Frontend Telemetry | **Dark-Mode Trading Terminal UI System, Risk Gauges, and 3-Card Briefing Flow**<br>- [`index.html`](../index.html) & [`web/index.html`](../web/index.html)<br>- [`docs/user_flow.md`](../docs/user_flow.md) (§8)<br>- [`contribution/individual/trieu-duc-luong.md`](individual/trieu-duc-luong.md) | **Usage:** Structures the visual layout of the 3-card onboarding screen (Crisis, Mission, Takeaway), the multi-panel trading dashboard, the Margin Health bar (marking the 20.00% maintenance threshold in red), the Leverage gauge (0.0x–4.0x), and the Property Target progress bar.<br>**Practical Significance:** Translates engine state variables (`equity`, `margin_ratio`, `leverage`, `target_progress`) into immediate visual feedback under a 1-second tick clock, and enforces `.toFixed(2)` formatting (resolving BUG-03) so players can read margin buffers accurately during market crashes. |

---

## Question 2: Collaborative Feature, Financial Calculation, and Bug Fix Verification

To show how specification, quantitative validation, implementation, debugging, and testing connected across the group, we detail one primary end-to-end collaboration (**T+0.5 Settlement Holding Pen and Cross-Margin Forced Liquidation with BUG-01 Fix**) followed by two supporting collaborative examples.

### Primary Example: T+0.5 Settlement Holding Pen, Forced Liquidation Calculation, and BUG-01 Fix

#### 1. What the Feature and Calculation Do
In [`src/simulation_engine.py`](../src/simulation_engine.py), purchased shares do not become immediately sellable if a timestamp is supplied (`current_tick is not None`). Instead, they enter `state.pending_shares` and `state.pending_queue` under the **T+0.5 settlement rule**:
- **Morning session orders (`phase_tick < 150`):** Settle into active `state.holdings` after 30 ticks (`delivery_tick = phase_tick + 30`, `deliver_in_phase = current_phase`).
- **Afternoon session orders (`phase_tick >= 150` in Phases 1–5):** Lock in the holding pen until the start of the next phase (`delivery_tick = 1`, `deliver_in_phase = current_phase + 1`).
- **Cross-margin exposure and forced liquidation calculation:** While locked in `pending_shares`, unsettled shares are still marked to market every tick in `calculate_stock_portfolio_value()` (lines 227–243) and count toward `trading_equity` and `margin_ratio` in `evaluate()` (lines 275–283):
  - **Trading Equity Formula:** `Trading Equity = Cash + Stock Value (active + pending) - Margin Debt`
  - **Margin Ratio Formula:** `Margin Ratio = Trading Equity / Stock Value (active + pending)`

  If Margin Ratio < 0.20 (for example, on a 4.0x leveraged position of $40,000 with $30,000 debt when the stock price drops 6.26% from $100.00 to $93.74, yielding `Margin Ratio = $7,496 / $37,496 = 19.9914%`), `trigger_forced_liquidation()` (lines 455–519) liquidates both `holdings` and `pending_shares`, deducts the 5% penalty (`Penalty = 0.05 * Gross Proceeds`), repays `margin_debt`, and leaves `bank_savings` untouched.

#### 2. Division of Responsibilities (Who Developed, Fixed, and Tested It)
1. **Financial Specification (Trần Hữu Dụ):** Designed the T+0.5 settlement rule, the `phase_tick < 150` session cutoff, the 20.00% maintenance margin trigger, the 5% liquidation penalty formula, and the Safe Haven Bank isolation rule in [`docs/financial_logic.md`](../docs/financial_logic.md) and [`docs/img/phase_1_workflow.jpg`](../docs/img/phase_1_workflow.jpg).
2. **Engine Implementation & BUG-01 Fix (Nguyễn Quang Minh):**
   - Programmed `PendingDelivery`, `execute_order()` (lines 323–435), `process_deliveries()` (lines 436–454), `evaluate()` (lines 250–321), and `trigger_forced_liquidation()` (lines 455–519) in [`src/simulation_engine.py`](../src/simulation_engine.py), and mirrored the logic in `ClientEngine` inside [`index.html`](../index.html).
   - Fixed **BUG-01 (Critical)**: Initially, orders placed at or after tick 150 (`phase_tick >= 150`) remained stuck in `pending_queue` when the game advanced to Phase 2 because delivery checked tick thresholds without first checking whether `current_phase` had advanced past `deliver_in_phase`. Nguyễn Quang Minh updated `process_deliveries()` at line 443 of [`src/simulation_engine.py`](../src/simulation_engine.py) to decouple phase advancement from intra-phase tick comparison:
     ```python
     should_deliver = (current_phase > item.deliver_in_phase) or (
         current_phase == item.deliver_in_phase and phase_tick >= item.delivery_tick
     )
     ```
3. **UI Lockout & Decimal Formatting Integration (Triệu Đức Lương & Nguyễn Quang Minh):** Triệu Đức Lương designed the pending-share HUD indicators and fixed floating-point display artifacts (**BUG-03**) using `.toFixed(2)` in [`index.html`](../index.html), while Nguyễn Quang Minh wired the post-liquidation order lockout (**BUG-04**, line 337 of [`src/simulation_engine.py`](../src/simulation_engine.py)).
4. **Testing & Financial Verification (Nguyễn Quang Minh & Trần Hữu Dụ):**
   - **Trần Hữu Dụ** verified the engine's outputs against hand-calculated financial tables (confirming that a ₩10,000,000 capital / ₩30,000,000 debt position subjected to a −20% shock yields ₩32,000,000 gross proceeds, a ₩1,600,000 penalty at 5%, ₩30,400,000 net proceeds, full repayment of ₩30,000,000 debt, and exactly **₩400,000** final cash, plus verifying that phase-boundary deliveries unfreeze at tick 1 of Phase 2).
   - **Nguyễn Quang Minh** wrote automated unit and regression tests in [`tests/test_simulation_engine.py`](../tests/test_simulation_engine.py) and [`tests/test_week6_integration.py`](../tests/test_week6_integration.py) (`test_t03_boundary_exactly_at_maintenance_margin`, `test_t04_boundary_breach_triggers_liquidation`, `test_t08_financial_consistency_week4_spec`, `test_t09_bank_savings_safe_haven`, and `test_t10_settlement_workflow_holding_pen`).

#### 3. How to Verify the Final Implementation
Reviewers can verify the implementation in three ways:
1. **Run the automated test suite from the repository root:**
   ```bash
   python -m unittest discover tests -v
   ```
   This executes all **66 automated tests** across 6 test modules in [`tests/`](../tests/), including `test_t03_boundary_exactly_at_maintenance_margin`, `test_t04_boundary_breach_triggers_liquidation`, `test_t08_financial_consistency_week4_spec`, and `test_t10_settlement_workflow_holding_pen` in [`tests/test_week6_integration.py`](../tests/test_week6_integration.py) (lines 56–87 and 108–155).
2. **Inspect the source code directly:**
   - T+0.5 queue assignment: [`src/simulation_engine.py`](../src/simulation_engine.py) lines 379–400.
   - BUG-01 fix in `process_deliveries()`: [`src/simulation_engine.py`](../src/simulation_engine.py) lines 436–454.
   - 20.00% maintenance margin check and 5% penalty liquidation math: [`src/simulation_engine.py`](../src/simulation_engine.py) lines 275–295 and 455–519.
3. **Check the defect and test documentation:**
   - Formal test table (T01–T12) and defect log (BUG-01 to BUG-06) in [`docs/testing.md`](../docs/testing.md) (§3–5).

---

### Summary of Additional Collaborative Verification Examples

| Collaborative Item | Developed / Specified By | Integrated / Coded By | Tested / Verified By | Verification Evidence in Repository |
|---|---|---|---|---|
| **3x / 20x / 100x Property Target Calibration** (revised from 2x / 8x after midterm) | **Nguyễn Hồng Nguyên** (built whole-share DP & staggered MILP optimizer in [`analysis/best_case.py`](../analysis/best_case.py)) & **Trần Hữu Dụ** (defined target tier rules) | **Nguyễn Quang Minh** (updated `HOUSE_MULTIPLIERS` in [`src/simulation_engine.py`](../src/simulation_engine.py) lines 28–38 and target gauges in [`index.html`](../index.html)) | **Trần Hữu Dụ** & **Nguyễn Hồng Nguyên** (verified MILP feasibility across Scenarios 1 & 2 for 2x/3x/4x tiers) | [`analysis/best_case.py`](../analysis/best_case.py), [`analysis/best_case_calibration_targets_3x_20x_100x.md`](../analysis/best_case_calibration_targets_3x_20x_100x.md), [`docs/revision_summary.md`](../docs/revision_summary.md) (Item #2 & #10) |
| **Dual-Scenario Price Normalization & Alias Mapping** (50 assets × 1,800 ticks, ±30% phase caps) | **Nguyễn Hồng Nguyên** (cleaned CSVs, audited ±30% caps in [`data/audit/`](../data/audit/)) & **Cáp Phan Quang Khánh** (aligned Phase 1 news tickers) | **Nguyễn Quang Minh** (coded `ALIAS_MAP` in [`src/simulation_engine.py`](../src/simulation_engine.py) lines 88–99 and CSV loader in [`src/game_controller.py`](../src/game_controller.py)) | **Nguyễn Quang Minh** (tested alias resolution during liquidation, CRIT-02) & **Nguyễn Hồng Nguyên** (600 phase continuity checks) | [`data/market_scenario_1.csv`](../data/market_scenario_1.csv), [`data/market_scenario_2.csv`](../data/market_scenario_2.csv), [`src/simulation_engine.py`](../src/simulation_engine.py) (lines 480–486), [`tests/test_complete_bug_report_45.py`](../tests/test_complete_bug_report_45.py) |
