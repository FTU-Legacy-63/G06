# OBJECTIVE INDIVIDUAL CONTRIBUTION EVIDENCE

**Course:** Technology Applications in Banking and Finance (NHA408E) - FTU 2026  
**Project:** Free Fall 2.0 (Group 6)  
**Member:** Trần Hữu Dụ  
**Student ID:** 2412380013  
**Assigned Role:** Coordinator - Mechanism Designer  

---

## 1. Executive Summary of Responsibilities

As the **Coordinator and Mechanism Designer**, my core responsibility is authoring the rulebook and game mechanics document, which includes establishing the formulas for leverage, margin maintenance, liquidation cascades, and win/loss states. I ensure that the financial logic correctly reflects "leverage blindness" and provides a mathematically verifiable framework and interaction flow for the backend engine.

| Area | Responsibility | Concrete Repository Deliverable |
|---|---|---|
| **Financial Risk Engine** | Designed the formulas for equity revaluation, bank savings accrual, margin debt tracking, and liquidation triggers. | `SOLUTION_STRUCTURE.md` |
| **Core User-Facing Flow** | Designed the Phase 1 interaction loop, defining the 1-second price triggers, financial recalculation sequence, and T+0.5 settlement rules. | `FEATURE_MAP.md` |
| **Margin & Liquidation Mechanics** | Established the 20% maintenance margin threshold, the $\ge 5.0\times$ forced liquidation trigger, and margin warning rules. | `ASSUMPTIONS.md` |
| **Difficulty & Target Calibration** | Calibrated the three house targets (Small House, Normal House, ToLam Villa) based on empirical backtesting to balance risk/reward. | `INPUT_DICTIONARY.md` |
| **Logic Verification & Edge Cases** | Created verifiable manual calculation cases (e.g., High Leverage Wipeout vs. Cash-Only Normie) to test the engine's financial logic. | `SAMPLE_INPUT_OUTPUT.md`, `MIDTERM_REVIEW.md` |

---

## 2. Technical Evidence & Implementation Details

### 2.1 Core Financial & Risk Logic (`SOLUTION_STRUCTURE.md` & `ASSUMPTIONS.md`)
Designed the deterministic financial formulas that run on every price tick:
- **Gross Exposure:**
  $$\text{Gross Exposure} = \sum (\text{Shares}_i \times \text{Current Price}_i)$$
- **Net Equity:**
  $$\text{Net Equity} = \text{Liquid Cash} + \text{Bank Savings} + \text{Gross Exposure} - \text{Margin Debt}$$
- **Effective Leverage & Margin Ratio:**
  $$\text{Effective Leverage} = \frac{\text{Gross Exposure}}{\text{Net Equity}}$$
  $$\text{Margin Ratio} = \frac{\text{Net Equity}}{\text{Gross Exposure}}$$
- **Forced Liquidation Rules:**
  - Defined the Fixed Maintenance Margin at **20%**.
  - Set the system to automatically execute a fire-sale of 100% open equity holdings if $\text{Effective Leverage} \ge 5.0\times$ (equivalent to $\text{Margin Ratio} \le 20\%$).

### 2.2 Core User-Facing Feature Flow (`FEATURE_MAP.md`)
Mapped the comprehensive Phase 1 system architecture and sequence of events to connect user actions with financial logic:
- **Interaction Loop:** Designed the step-by-step logic from account initialization through the 5-minute countdown, applying a 1-second background trigger to advance prices, validate orders, and trigger forced liquidations if the margin call price is breached.
- **T+0.5 Settlement Delay Mechanism:**
  - Formulated the rule where orders executed at `Tick ≤ 150` are delivered to active holdings during the current phase.
  - Orders executed at `Tick > 150` are logged as pending and delivered in Phase 2, exposing shares to live price action without allowing the player to sell.

### 2.3 Empirical Calibration & Target Matrix (`INPUT_DICTIONARY.md`)
Utilized the empirical backtest dataset (`best_case_portfolio_summary.csv`) to set realistic yet challenging financial goals:
- **Small House (Easy):** Set at **$3.0\times$ Capital**. Achievable using Cash Only (1.0x) since peak benchmark yield is $5.20\times$.
- **Normal House (Medium):** Set at **$20.0\times$ Capital**. Requires 2.0x–3.0x margin trading.
- **ToLam Villa (Extreme):** Set at **$100.0\times$ Capital**. Mathematically viable only by leveraging up to 4.0x (theoretical ceiling of $217.45\times$) prior to the Phase 6 collapse.

### 2.4 Market Constraints & Savings Design
- **Session Price Limits:** Defined the $\pm 30\%$ AM/PM session price ceiling and floor, which allows for a maximum cumulative phase movement of $+69\%$ or $-51\%$.
- **Bank Savings Mechanism:** Established a fixed **4.75% return per completed AM/PM session** to provide a risk-free alternative to equity exposure.

---

## 3. Individual Footprint Self-Check (Midterm Checklist Section 7)

1. **My Main Responsibility:**  
   Designing the simulation's mathematical rulebook, including formulas for continuous portfolio valuation, margin maintenance thresholds, and the overarching Core User-Facing Feature Flow (Phase 1 interaction loop).
2. **My Most Important Output So Far:**  
   The defined Financial Logic chain (`MIDTERM_REVIEW.md`), the formal Risk Engine parameters (`SOLUTION_STRUCTURE.md`), the empirically calibrated Target Matrix (`INPUT_DICTIONARY.md`), and the comprehensive system flow architecture (`FEATURE_MAP.md`).
3. **Where the Evidence is Located:**  
   In the repository files `SOLUTION_STRUCTURE.md`, `ASSUMPTIONS.md`, `INPUT_DICTIONARY.md`, `FEATURE_MAP.md`, `SAMPLE_INPUT_OUTPUT.md`, and `MIDTERM_REVIEW.md`.
4. **How My Output Supports the Group Product:**  
   My financial models and logic flowcharts provide the foundational framework that supports all four of my team members:
   - It provides the exact mathematical blueprint and state-transition logic that the **Technical Developer (Nguyễn Quang Minh)** programs into the backend engine.
   - It defines the financial thresholds, margin tiers, and house targets that the **Scenario Designer (Cáp Phan Quang Khánh)** uses to script player decisions and narrative consequences.
   - It establishes the mathematical and timeline constraints (such as 1-second intervals and ±30% volatility limits) that guide the **Data Gatherer (Nguyễn Hồng Nguyên)** in structuring the dataset.
   - It determines the specific metrics (Net Equity, Target Progress, Leverage) and risk states (Margin Warnings) that the **UI/UX Designer (Triệu Đức Lương)** must visualize on the dashboard.
5. **What I Will Improve or Complete Next (Post-Midterm):**  
   - Refine the execution penalty logic during the Phase 6 cascade plunge.
   - Map out the precise Target Progress % calculations for the UI dashboard.
   - Standardize the formulas for the post-game narrative debrief evaluation.
