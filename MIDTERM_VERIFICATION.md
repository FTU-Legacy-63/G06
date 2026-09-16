# MIDTERM VERIFICATION

**Course:** Technology Applications in Finance and Banking (NHA408E) — FTU 2026  
**Exam:** Midterm Exam • Week 5 Readiness & Contribution Verification  
**Group:** 06  
**Product:** Free Fall 2.0  
**Date:** 16/09/2026  
**Team Representative:** Trần Hữu Dụ (Student ID: 2412380013)  
**Repository:** https://github.com/FTU-Legacy-63/G06  
**Instructor / Faculty:** Department of Banking and Finance, Foreign Trade University  

---

## Purpose
This exam is a short verification of the project evidence already available in your repository. Do not rewrite Week 1–Week 5 submissions. Focus only on what still needs to be clarified before moving into Week 6.  
**Submission:** Submit one file to your team repository: `MIDTERM_VERIFICATION.md`

---

# A. GROUP VERIFICATION

### 1. What is the biggest issue your team still needs to solve before Week 6?
*(Choose one issue only. It may be about financial logic, data, assumptions, scoring, MVP scope, user flow, interface, or technical feasibility.)*

**Answer:**  
Our team's single biggest issue to solve before Week 6 is **calibrating the real-time dynamic margin squeeze and forced-liquidation feedback loop within our MVP scope**, ensuring that player attention remains laser-focused on **"leverage blindness"** rather than treating the product as a generic stock trading simulator.

While our predecessor project (Free Fall 1 / K62) focused broadly on general macroeconomic crisis decisions and discretionary asset allocation, Free Fall 2.0 (K63) centers specifically on the fatal mechanics of leveraged trading: **Initial Margin, Effective Leverage, Margin Debt, Maintenance Margin (20% threshold), Margin Calls, and Fire-Sale Liquidation Cascades**. The core unresolved challenge is preventing the game from overwhelming the user with raw trading actions, and instead ensuring that the UI and engine tightly communicate the rapid deterioration of Equity relative to Borrowed Debt during Phase 5 and Phase 6 market shocks.

---

### 2. Why is this issue important?
*(Explain what part of your core product depends on it and what may go wrong if the issue is not solved.)*

**Answer:**  
This issue directly governs the **core learning objective and value proposition** of Free Fall 2.0. The entire simulation revolves around exposing the cognitive vulnerability where investors mistake paper wealth from leveraged gains for actual solvency until a sudden price drop wipes them out.

If this feedback loop is not properly calibrated:
1. **Pedagogical Failure:** Players will treat the game as a standard stock-picking simulator (buy low, sell high) and fail to internalize why a modest -20% market decline causes a catastrophic -100% equity wipeout under 4× leverage.
2. **Product UX Breakdown:** If the transition from **Healthy ($\ge 25\%$)** $\rightarrow$ **Warning ($20\% - 25\%$)** $\rightarrow$ **Margin Call ($< 20\%$)** $\rightarrow$ **Forced Liquidation** happens too abruptly without clear visual indicators and actionable de-risking windows (e.g., depositing into Bank Savings or voluntarily cutting positions), players will perceive liquidation as an arbitrary system penalty rather than an inevitable mathematical consequence of excessive leverage.

---

### 3. What has your team done about this issue so far?
*(Briefly describe what you have already done to understand or solve it—for example: checked a source, tested a calculation, compared options, built a sample case, tried a prototype, changed the design, or simplified the scope.)*

**Answer:**  
To isolate and solve this issue, our team has implemented and verified the following concrete milestones:
1. **Mathematical Formalization & Rulebook:** Established the exact margin formulas in `week 4/MIDTERM_REVIEW.md`, `ASSUMPTIONS.md`, and `SOLUTION_STRUCTURE.md`, explicitly defining:
   $$\text{Margin Ratio} = \frac{\text{Equity}}{\text{Stock Portfolio Value}} = \frac{\text{Cash} + \text{Total Portfolio Value} - \text{Margin Debt}}{\sum \text{Shares}_i \times P_i}$$
   with a strict maintenance floor at $20.0\%$ and a $5.0\%$ forced liquidation penalty fee.
2. **Empirical Return & Target Calibration:** Ran quantitative backtests recorded in `market scenario/best_case_portfolio_summary.csv`, benchmarking achievable return multipliers across leverage tiers (Cash 1× $\rightarrow$ 3× Small House; Margin 2×–3× $\rightarrow$ 20× Normal House; Margin 4× $\rightarrow$ 100× ToLam Villa) across 1,800 price ticks in `market_scenario.csv`.
3. **Core Engine Implementation:** Programmed the calculation core in `src/simulation_engine.py` and `src/game_controller.py`, complete with a T+0.5 settlement delay holding pen (tick 150 cutoff) and a safe-haven Bank Savings module.
4. **Automated Logic Verification:** Authored automated unit tests in `tests/test_simulation_engine.py` verifying high-leverage wipeout (Case 1: 4× leverage, 20% shock triggering liquidation at 6.25% ratio) and cash-only solvency with a 100% pass rate.
5. **Interactive Prototype & Wireframes:** Built a playable terminal prototype (`interactive_demo.py`), FastAPI endpoints (`api_server.py`), and designed dynamic visual wireframes featuring live Margin Health gauges and target progress bars.

---

### 4. What will your team do next about this issue?
*(State the next concrete action before or during Week 6—for example: test more cases, replace a data source, change a rule, simplify the MVP, remove a feature, build a small prototype, or validate a calculation.)*

**Answer:**  
Before and during Week 6, our team will execute three concrete actions to finalize this feedback loop:
1. **Connect Simulation Engine to UI via WebSockets/REST (`Week 6 MVP Integration`):** Wire the Python backend (`api_server.py`) directly to the web dashboard (`web/index.html`), replacing static step transitions with real-time visual updates of the **Margin Health Gauge** (pulsing red when Margin Ratio falls below $25\%$).
2. **Refine Pre-Liquidation Grace Windows & De-risking UX:** Implement an explicit 15-second warning prompt when entering Phase 5/6, allowing users to make an emergency risk-management decision: transfer funds into **Bank Savings**, repay margin debt, or sell partial shares before the clearinghouse executes auto-liquidation.
3. **Remove Secondary Distractions from Scope:** In accordance with our Week 5 Feature Audit (`WEEK_5_REFINEMENT.md`), completely eliminate complex order-book depth queues and cryptocurrency pairs, keeping the MVP strictly focused on the Korean market crisis and the core leverage survival loop.

---

# B. MEMBER CONTRIBUTION VERIFICATION

*Complete one row for each member. Do not list only roles such as "Developer", "Researcher", or "Designer".*

| Member | What did this member actually produce? | How is it used in the project? | What can this member personally explain, calculate, demonstrate, or reproduce? |
|---|---|---|---|
| **Trần Hữu Dụ**<br>*(ID: 2412380013)*<br>**Role:** Coordinator & Mechanism Designer | • Authored the project's **financial-mechanic framework and rulebook**, formalizing Gross Exposure, Net Equity, Effective Leverage, and Margin Ratio formulas.<br>• Formulated the **20% maintenance margin floor**, 5% liquidation penalty fee, T+0.5 settlement rules, and Bank Savings mechanism.<br>• Defined property target tiers (3× Small House, 20× Normal House, 100× ToLam Villa).<br>• Authored: [`SOLUTION_STRUCTURE.md`](../week%202/Solution_Structure%20(1).md), [`ASSUMPTIONS.md`](../week%204/MIDTERM_REVIEW.md), and [`MIDTERM_REVIEW.md`](../week%204/MIDTERM_REVIEW.md). | • Provides the mathematical foundation and rule specification for the entire simulation.<br>• Directly dictates account balance state changes, risk triggers, and target evaluations implemented by the backend engine, scenario scripts, and UI gauges. | • **Calculate and derive** Gross Exposure, Net Equity, Effective Leverage, and Margin Ratio step-by-step from raw trade inputs.<br>• **Explain** the economic justification of the 20% maintenance threshold and how leverage amplifies drawdowns.<br>• **Reproduce** the manual calculation of Margin Call and Forced Liquidation benchmark test cases.<br>• Justify the rules for Bank Savings safe haven and T+0.5 settlement delay. |
| **Nguyễn Hồng Nguyên**<br>*(ID: 2412380038)*<br>**Role:** Data Gatherer & Quantitative Calibration | • Constructed [`market_scenario.csv`](../market%20scenario/market_scenario.csv): a **1,800-second (ticks) × 50-asset** deterministic market dataset covering 6 distinct crisis phases.<br>• Calibrated realistic price paths for driver tickers (Vintrumite, Samsung Electronics, KOSPI ETFs) and market indices.<br>• Built quantitative benchmark models: [`best_case_portfolio_combos.csv`](../market%20scenario/best_case_portfolio_combos.csv) and [`best_case_portfolio_summary.csv`](../market%20scenario/best_case_portfolio_summary.csv) across Cash (1×), 2×, 3×, and 4× strategies. | • Serves as the quantitative market-data backbone ingested directly by the simulation controller to drive tick-by-tick portfolio revaluation.<br>• Benchmark models mathematically prove that target goals (3×, 20×, 100×) are achievable yet appropriately vulnerable to ruin during the Phase 6 crash (-57.8%). | • **Reproduce** the data generation and calibration methodology for all 50 tickers across the 6 market phases.<br>• **Calculate** achievable wealth ceilings and drawdowns under 1×, 2×, 3×, and 4× leverage.<br>• **Explain** driver vs. non-driver price movements, AM/PM price constraints, and the statistical structure of the Phase 6 cascade crash.<br>• Demonstrate how empirical backtest data prevents game targets from being impossible or trivial. |
| **Cáp Phan Quang Khánh**<br>*(ID: 2412380020)*<br>**Role:** Scenario Designer & Content Lead | • Designed the comprehensive **Scenario Tree** and multi-branching user flow across all 6 phases.<br>• Authored event and news scripts (fake hype, corporate earnings, rumors, bull traps, and crisis alerts) tied to specific tick intervals.<br>• Built the Player Decision Matrix mapping actions (Buy, Sell, Hold, Margin Borrow, Savings) to scenario paths.<br>• Authored: [`USER_FLOW.md`](../WEEK_5_REFINEMENT.md), [`MARKET_DATASET.md`](../market%20scenario/), and Phase 1 scenario documentation. | • Converts raw mathematical rules and price ticks into an engaging behavioral learning loop: *Scenario $\rightarrow$ Information $\rightarrow$ Decision $\rightarrow$ Financial State Update $\rightarrow$ Consequence $\rightarrow$ Feedback*.<br>• Controls the timing of news delivery that triggers player psychological traps (FOMO, overconfidence, panic). | • **Walk through and reproduce** the entire Scenario Tree and narrative progression across the 6 phases.<br>• **Demonstrate** the three audited paths from Week 5: Happy Path (de-risking into Bank Savings), Extreme Risk Path (wipeout), and Error Path (rejected trades).<br>• **Explain** how narrative events directly influence player decision-making and lead to leverage blindness. |
| **Nguyễn Quang Minh**<br>*(ID: 2412380031)*<br>**Role:** Technical Developer & Engine Lead | • Developed the core simulation software: [`src/simulation_engine.py`](../src/simulation_engine.py) (portfolio valuation, equity, leverage, Bank Savings, T+0.5 holding pen, forced liquidation).<br>• Implemented phase control and CSV pipeline: [`src/game_controller.py`](../src/game_controller.py).<br>• Built automated unittest suite: [`tests/test_simulation_engine.py`](../tests/test_simulation_engine.py) (4/4 passed).<br>• Created playable CLI prototype [`interactive_demo.py`](../interactive_demo.py) and REST API bridge [`api_server.py`](../api_server.py).<br>• Authored [`CONTRIBUTIONS.md`](../CONTRIBUTIONS.md) and [`WEEK_5_REFINEMENT.md`](../WEEK_5_REFINEMENT.md). | • Acts as the functional execution engine connecting financial rules, market data, and user interface.<br>• Guarantees deterministic, verifiable, and bug-free execution of player orders, settlement delays, and solvency checks for both defense demos and frontend consumption. | • **Run and live-demonstrate** the simulation engine via terminal demo and API dashboard.<br>• **Trace and explain** code-level state mutations during trade execution, price ticks, and margin calls.<br>• **Demonstrate and reproduce** the 4 automated unit tests verifying high-leverage liquidation, cash solvency, bank savings, and T+0.5 settlement.<br>• Explain the programmatic architecture of the T+0.5 delivery queue and liquidation routines. |
| **Triệu Đức Lương**<br>*(ID: 2412380029)*<br>**Role:** UI/UX Designer & Frontend Lead | • Designed the complete trading terminal design system, layout architecture, dark-mode visual hierarchy, and component wireframes.<br>• Architected user-facing layouts: Account Overview, Live Market Ticker, Order Entry Form, News Stream, and Solvency Debrief.<br>• Designed specialized visual risk components: Dynamic **Margin Health Gauge** (Safe/Warning/Margin Call), Effective Leverage meter, and Property Target Progress bar.<br>• Authored UI asset pack and frontend prototypes ([`web/index.html`](../index.html) / [`web/`](../web/)). | • Translates complex backend financial metrics into clear, non-intimidating visual interfaces.<br>• Ensures that critical risk states (approaching margin call) are instantly recognizable to the user, bridging system logic and user experience as required by Week 5. | • **Explain and justify** the UI layout hierarchy, typography, and visual alert states.<br>• **Demonstrate** how backend state variables (Margin Ratio, Leverage, Equity) map to visual components and trigger dynamic warning colors.<br>• **Walk through** the user experience flow from onboarding to game debrief, showing how the interface prevents cognitive overload while reinforcing risk awareness. |

---

> **Verification Note:** Because one person may upload files on behalf of the team, Git commit authorship is not used as proof of individual contribution. The table records each member’s stated output, its use in the project, and what the member should be able to explain or reproduce if clarification is required during the midterm assessment.
