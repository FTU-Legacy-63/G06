
# Korea Margin Crisis Simulation

An interactive, consequence-based stock market simulation designed to teach retail investors and students the real-world mechanics and psychological risks of leverage, margin calls, and forced liquidation.

---

## 📌 Project Overview

**Korea Margin Crisis Simulation** compresses a single volatile Korean trading day into a **30-minute interactive session**. Players allocate capital between cash deposits and equities, decide when and how much leverage to use, and navigate dynamic market shocks to achieve a long-term property wealth target while maintaining solvency.

[User Decision] ──► [Market Info & News] ──► [Trade Execution (Cash/Margin)]
▲                                                 │
│                                                 ▼
[Next Decision] ◄── [Consequence / Result] ◄── [Portfolio & Margin Update]


---

## 🎯 Target Users & Core Objectives

* **Target Audience:** Retail investors, finance/banking students, and risk-management learners.
* **Core Task:** Balance returns, market volatility, debt maintenance, and solvency under rapidly shifting market conditions.
* **Problem Addressed:** Static mathematical models fail to convey the emotional pressure and rapid capital erosion of leverage during systemic market shocks.

---

## 🚀 MVP Scope (Week 2)

### Playable Roles
* **Individual Investor** *(Active in MVP)*
* *Planned for Future Releases:* Institutional Investor, Brokerage Firm, Government / Regulator

### Investment Universe
* **Samsung Electronics**
* **SK Hynix**
* **KOSPI-Tracking ETF**

### Core Mechanics
* **Trading:** Buy, Sell, and Hold actions with dynamic position sizing
* **Financing:** Cash vs. Margin allocation with real-time borrowing capacity tracking
* **Risk Engine:** Margin health monitoring, automated Margin Calls, and Forced Liquidation
* **Objectives:** Real-time tracking toward a defined Property Target

---

## 📈 Simulation Progression (6 Phases)

Phase 1: Bullish Momentum       (Rising confidence, early gains) <br>
Phase 2: Leverage Expansion     (Incentive to borrow and scale positions) <br>
Phase 3: Market Overheating     (Peak valuations, volatility spikes) <br>
Phase 4: Severe Market Shock    (Sudden downturn, asset devaluation) <br>
Phase 5: Margin Crisis          (Margin calls triggered, liquidity crunch) <br>
Phase 6: Resolution & Reckoning (Forced liquidation or survival) <br>


---

## 🖥️ Product Architecture & UI Flow

| Screen | Core Purpose & Display Metrics |
| :--- | :--- |
| **🏠 Home** | Overview of net worth, active portfolio, debt load, and property goal progress. |
| **📊 Market** | Live price tickers, breaking news feed, sentiment indicators, and order entry. |
| **💳 Margin** | Borrowing power, collateral coverage ratio, margin debt, and health alerts. |
| **🏁 Results** | Final net worth, ROI, peak leverage ratio, and post-session diagnostic breakdown. |

---

## 👥 Team Responsibilities

* **Trần Hữu Dụ:** Game mechanics, leverage formulas, maintenance margin ratios, liquidation triggers, win/loss conditions.
* **Cáp Phan Quang Khánh:** Scenario decision trees, dynamic market events, narrative branching, consequence logic.
* **Nguyễn Hồng Nguyên:** Asset parameters, historical price series, volatility inputs, leverage limits.
* **Triệu Đức Lương:** UI/UX wireframes, dashboard layout, alert states, user flow, result visualizations.
* **Nguyễn Quang Minh:** Core simulation engine, state management, event controller, settlement logic.

---

## 📂 Project Documentation & Artifacts

* `PROJECT_PROPOSAL.md`: Problem statement, target personas, and value proposition.
* `SOLUTION_STRUCTURE.md`: Technical architecture, state flow diagrams, and MVP specifications.
* **Task Board:** Workstream allocation, milestone tracking, and deliverables by output.
* **Revision Notes:** Log of architectural and design iterations based on feedback.

---

## 📍 Project Status & Roadmap

- [x] **Week 1:** Problem discovery & concept definition.
- [x] **Week 2:** Solution design, core loop validation, MVP scope, and role allocation.
- [ ] **Next Up:** Finalizing data schemas, price series models, volatility distributions, and simulation input assumptions.
combine into 1 file

