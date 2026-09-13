# SOLUTION_STRUCTURE.md

## Korean Stock Market Simulation Game
> **Core Structure:** User → Input → Process → Output → User Action

---

## 1. User → Input → Process → Output → User Action

| Stage | Definition |
| :--- | :--- |
| **User** | Retail investors, inexperienced day traders, and finance/banking students. |
| **Input** | Randomly assigned scenario (`1` or `2`), selected house difficulty target (`Small House`, `Normal House`, `Big-Ass Villa`), trading orders (Buy/Sell/Hold), and leverage selection. |
| **Process** | Deterministic price advance → Portfolio revaluation → Margin health check → Margin Call / Forced Liquidation assessment → Phase countdown check. |
| **Output** | Liquid cash, share volume, margin debt, net equity, margin ratio gauge, property target progress %, and narrative ending result. |
| **User Action** | Submit Buy/Sell orders, toggle cash vs. margin borrowing, deleverage, or cut positions before margin calls execute. |

**Core learning loop:**  
`Scenario Assignment → House Target Selection → Market Stress → Leverage Decision → Financial Consequence → Behavioral Feedback`

---

## 2. Initial Required Information

| Input Variable | Meaning | Source |
| :--- | :--- | :--- |
| `assigned_scenario_id` | Selects Scenario 1 or 2, determining starting cash and fixed market path. | System-generated (Random at launch) |
| `initial_capital` | Starting liquid balance (e.g., 20m KRW in Scenario 1; 50m KRW in Scenario 2). | System-defined by Scenario |
| `target_house_type` | Selected lifestyle goal acting as game difficulty ($1.5\times$, $3.5\times$, or $8\times$ capital). | User Selection |
| `property_target_value` | Exact KRW wealth needed to win the selected house ending. | Calculated (`initial_capital` × Multiplier) |
| `orders` | Buy / Sell / Hold + Volume + Cash / Margin financing. | User Input |
| `fixed_price_path` | Predetermined 6-phase market sequence with embedded news and traps. | System-defined by Scenario |

---

## 3. Core Process & Game Architecture

> **Deterministic, event-driven financial market simulation with real-time user decisions.**

One trading day is compressed into **30 minutes** across **6 distinct phases** (approx. 5 minutes per phase).

### Financial Logic Pipeline
1. **Trading Execution:** Validates order volume against cash and available margin borrowing limit.
2. **Valuation Engine:** Recalculates Net Equity on every tick and user trade:
   $$\text{Total Assets} = \text{Liquid Cash} + (\text{Shares} \times \text{Current Price})$$
   $$\text{Net Equity} = \text{Total Assets} - \text{Margin Debt}$$
   $$\text{Margin Ratio} = \frac{\text{Net Equity}}{\text{Shares} \times \text{Current Price}}$$
   $$\text{Target Progress \%} = \left(\frac{\text{Net Equity}}{\text{Property Target Value}}\right) \times 100$$
3. **Risk Enforcement:**
   * **Healthy:** Margin Ratio $\ge 30\%$ maintenance threshold.
   * **Liquidation Triggered:** If Margin Ratio $< 30\%$, the system automatically sells shares at market price, repays margin debt, and records remaining equity.
   * **Solvency Check:** If Equity $\le 0$, session terminates immediately (**Total Wipeout**).

---

## 4. MVP Flow & 6-Phase Narrative Structure

| Phase | Market Tone | News Authenticity | Core Educational Mechanism |
| :---: | :--- | :--- | :--- |
| **1** | Slightly Green | **Fake / Rumors** | Overhyped leaks bait players into opening margin accounts and early leveraged buys. |
| **2** | Steady Green | **True / Fundamental** | Solid corporate earnings build genuine confidence in the uptrend. |
| **3** | Euphoric Bull | **True / Bullish** | Market hits peak; players with high targets (Big-Ass Villa) are heavily tempted to max out leverage. |
| **4** | Slightly Red | **True / Mild Bear** | A mild dip tempts players into complacency or "buying the dip" on margin rather than de-risking. |
| **5** | Crisis Outbreak | **Fakeouts / Bull Traps** | Sharp crash with deceptive recovery headlines; liquidity freezes and Margin Calls begin. |
| **6** | The Cascade | **Panic / Systemic Shock** | Unchecked leverage breaches maintenance margins, triggering broker forced liquidations and final endings. |

---

## 5. Difficulty Levels & Narrative Endings

The player's initial choice of house sets the difficulty and determines the final ending screen:
