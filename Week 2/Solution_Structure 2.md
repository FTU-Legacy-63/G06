# SOLUTION_STRUCTURE.md

## Korean Stock Market Simulation Game (Seoul 2026 Crisis Simulator)
> **Core Structure:** User → Input → Process → Output → User Action[cite: 4]

---

## 1. User → Input → Process → Output → User Action

| Stage | Definition |
| :--- | :--- |
| **User** | Retail investors, day traders, and finance students practicing leverage risk management[cite: 4]. |
| **Input** | Randomly assigned scenario (`1` or `2`), chosen house target difficulty (`Small House`, `Normal House`, `ToLam Villa`), selected margin tier (`2x`, `3x`, `4x` or Cash 1.0x), and active Buy/Sell/Hold trading orders[cite: 4]. |
| **Process** | Real-time tick engine (1,800s time-series) → Continuous asset revaluation across 50 tickers → Dynamic leverage monitoring → Margin warning alert / Forced Liquidation execution → Phase transition[cite: 4]. |
| **Output** | Cash balance, portfolio valuation, margin debt, net equity, effective leverage ratio, property target progress %, and narrative debrief[cite: 4]. |
| **User Action** | Submit Buy/Sell market orders, toggle margin tiers, deleverage open positions, hold cash reserves, or respond to margin stress before forced liquidation executes[cite: 4]. |

**Core learning loop:**  
`Scenario & Capital Assignment → House Target Selection → Market Stress & Traps → Leverage Decisions → Financial Consequence → Behavioral Feedback`[cite: 4]

---

## 2. Initial Required Information

| Input Variable | Meaning | Source |
| :--- | :--- | :--- |
| `assigned_scenario_id` | Determines starting cash and locks the deterministic market path (`1` or `2`)[cite: 4]. | System-generated (Random at launch)[cite: 4] |
| `initial_capital` | Starting liquid balance ($10,000 USD / 20,000,000 KRW equivalent baseline)[cite: 4]. | System-defined by scenario[cite: 4] |
| `target_house_type` | Lifestyle target defining game difficulty and required multiplier ($3.0\times$, $20.0\times$, or $200.0\times$)[cite: 4]. | User Selection[cite: 4] |
| `property_target_value` | Exact equity required to win the selected ending (`initial_capital` × Multiplier). | Calculated Parameter |
| `margin_tier` | Discrete leverage multiplier tier chosen by player: `2x`, `3x`, `4x` (or Cash 1.0x)[cite: 4]. | User Selection |
| `orders` | Buy / Sell / Hold orders with designated volume and asset ticker[cite: 4]. Unlimited volume execution bounded by available account balance. | User Input[cite: 4] |
| `fixed_price_path` | 1,800-second deterministic tick series spanning 50 assets and 6 market phases (`market_scenario.csv`)[cite: 4]. | System Dataset (`market_scenario.csv`)[cite: 4] |

---

## 3. Core Process & Financial Risk Engine

> **Deterministic, event-driven financial market simulation with real-time user decisions.**[cite: 4]

One trading day is compressed into **30 minutes (1,800 seconds)** across **6 distinct phases** (300 seconds per phase)[cite: 4].

### Valuation Pipeline (Executed on every price tick and user action)
1. **Gross Stock Exposure:**
   $$\text{Gross Exposure} = \sum (\text{Shares}_i \times \text{Current Price}_i)$$
2. **Net Equity & Debt Accounting:**
   $$\text{Total Assets} = \text{Liquid Cash} + \text{Gross Exposure}$$
   $$\text{Net Equity} = \text{Total Assets} - \text{Margin Debt}$$
3. **Dynamic Leverage Calculation:**
   $$\text{Effective Leverage} = \frac{\text{Gross Exposure}}{\text{Net Equity}}$$
4. **Target Progress Tracking:**
   $$\text{Target Progress \%} = \left(\frac{\text{Net Equity}}{\text{Property Target Value}}\right) \times 100$$

### Financial Logic & Risk Enforcement Rules

The system tracks dynamic borrowing risk in terms of leverage multiples ($x$):

| Financial State | Condition / Formula | System Output & Immediate Action |
| :--- | :--- | :--- |
| **Safe Zone** | $\text{Effective Leverage} \le \mathbf{2.0\times}$ | Collateral buffer is healthy; normal gameplay proceeds without intervention[cite: 4]. |
| **Margin Warning (Amber Alert)** | $\mathbf{2.0\times} < \text{Effective Leverage} \le \mathbf{3.33\times}$ | Visual warning banner flashes on dashboard; prompts voluntary de-risking or position cuts[cite: 4]. |
| **Maintenance Breach (Forced Liquidation)** | $\text{Effective Leverage} > \mathbf{3.33\times}$ *(equivalent to Margin Ratio < 30%)* | Broker automatically executes a market fire-sale of 100% of open equity holdings at current tick price to settle `Margin Debt`[cite: 4]. Losses deduct from remaining equity. |
| **Solvency Check (Bankruptcy)** | $\text{Net Equity} \le 0$ | Terminal state: **Total Account Wipeout / Game Over**[cite: 4]. |

---

## 4. MVP Flow & 6-Phase Narrative Structure

Based on empirical data from `market_scenario.csv`:

| Phase | Phase Name | Duration | Market Dynamics | Primary Behavioral Mechanism |
| :---: | :--- | :---: | :--- | :--- |
| **1** | **Fake Positive News** | Sec 1–300 | Deceptive bullish rumors; initial asset uptick. | Baiting players into opening margin accounts and taking early leveraged exposure[cite: 4]. |
| **2** | **True Positive News** | Sec 301–600 | Broad rally validated by corporate fundamentals. | Reinforcing confidence; rewarding early risk-takers[cite: 4]. |
| **3** | **Bull Market** | Sec 601–900 | Momentum acceleration across tech/semiconductors. | Tempting players chasing high targets (ToLam Villa) to switch to 3x/4x margin tiers[cite: 4]. |
| **4** | **Strong Growth (FOMO)** | Sec 901–1200 | Rapid valuation surge; high volatility. | Fear Of Missing Out (FOMO); peak borrowing occurs[cite: 4]. |
| **5** | **Market Euphoria** | Sec 1201–1500 | Peak valuations followed by sharp intraday fakeouts and bull traps. | Greed trap; optimal strategies take profits here, while greedy players hold max margin into the close[cite: 4]. |
| **6** | **Negative Shock** | Sec 1501–1800 | Severe systemic crash (Samsung, Vintrumite drop **−57%**). | High leverage accounts exceed $3.33\times$ leverage, triggering broker forced liquidations[cite: 4]. |

---

## 5. Calibrated Difficulty Levels & Narrative Endings

Empirical backtesting (`best_case_portfolio_summary.csv`) confirms that un-leveraged investing yields up to $5.20\times$, while optimal 4x margin compounding achieves up to **$217.45\times$ (~200×)**:

| Target House | Multiplier | Feasible Leverage | Narrative Ending Consequence |
| :--- | :---: | :---: | :--- |
| **Small House** *(Easy)* | **$3.0\times$ Capital** | Cash Only (1.0x) | **Normie Ending:** Survived the crash safely with zero debt, but wealth growth barely beats inflation. A secure but completely mundane, uninspiring life. |
| **Normal House** *(Medium)* | **$20.0\times$ Capital** | 2.0x – 3.0x Margin | **Middle-Class Stability Ending:** Successfully balanced risk and return. Achieved comfortable home ownership and solid financial security. |
| **ToLam Villa** *(Hard)* | **$200.0\times$ Capital** | 4.0x Margin (Extreme) | **Extravagant Luxury Ending:** Flawless market execution unlocks supreme multi-generational wealth and endless fun. <br>**Failure Consequence:** Total liquidation wipeout and bankruptcy. |

---

## 6. Technical Route & System Architecture

### Technical Route
`Scenario Dataset (CSV) → Core State Engine (React/Next.js) → Valuation & Risk Model → Trading Interface → Post-Game Consequence Debrief`[cite: 4]

| Component | Function | Implementation Responsibility |
| :--- | :--- | :--- |
| **Market Data Architecture** | Stores the 1,800-second price matrix across 50 assets and news queue (`market_scenario.csv`). | **Nguyễn Hồng Nguyên** *(Data Gatherer)* |
| **Financial Risk Engine** | Implements equity revaluation, margin debt tracking, $3.33\times$ maintenance trigger, and liquidation calculations. | **Trần Hữu Dụ** *(Mechanism Designer)* |
| **Scenario & Narrative Controller** | Scripts phase transitions, deceptive/true headlines, decision matrices, and 3 ending consequences. | **Cáp Phan Quang Khánh** *(Scenario Designer)* |
| **Dashboard UI/UX** | Renders live price ticker, dynamic leverage gauge, visual liquidation alerts, and order entry interface. | **Triệu Đức Lương** *(UI/UX Designer)* |
| **Core Simulation Engine** | Controls the 1,800s timer loop, order execution (unlimited volume matching), and state synchronization. | **Nguyễn Quang Minh** *(Technical Developer)* |

---

## 7. Scope Boundaries (Target vs. Fallback vs. Out of Scope)

| Scope Tier | Boundaries |
| :--- | :--- |
| **Target MVP** | Single-player web simulator with 2 scenarios, 50 Korean assets, 3 house difficulties ($3.0\times$, $20.0\times$, $200.0\times$), 3 margin tiers (`2x`, `3x`, `4x`), real-time 1,800s tick progression, automatic liquidation at $> 3.33\times$ leverage, and educational debrief[cite: 4]. |
| **Fallback** | Turn-based phase evaluation (6 discrete phase decisions rather than second-by-second ticks), simplified asset basket (top 5 core assets instead of 50), and manual margin call check[cite: 4]. |
| **Out of Scope** | Real-money brokerage integration, order-book depth/slippage modeling, multiplayer lobbies, derivative options contracts, and institutional/regulator playable roles[cite: 4]. |

---

## 8. Solution Summary

`Retail Investor → Assigned Capital ($10k/20m KRW) → Select House Target (3x / 20x / 200x) → Select Margin Tier (Cash / 2x / 3x / 4x) → 1,800s Compressed Simulation → Continuous Leverage Health Valuation → Phase 6 Shock & Cascade → Consequence Debrief (Normie / Stability / Luxury / Wipeout)`[cite: 4]
