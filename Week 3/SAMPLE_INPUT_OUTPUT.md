# Sample Input–Output

This file demonstrates how the scenario data, margin tiers, and house targets produce predictable financial consequences.

## Sample Case 1: Scenario 1 + ToLam Villa (Extreme Difficulty — The Wipeout)

### Sample Input

| Variable | Value |
| :--- | :--- |
| `assigned_scenario_id` | Scenario 1 (`market_scenario.csv`) |
| `initial_capital` | $10,000 USD |
| `target_house_type` | ToLam Villa (Extreme Difficulty) |
| `property_target_value` | **$1,000,000 USD** ($100.0\times$ Initial Capital) |
| `leverage_per_order` | **4x Tier** (Maximum Leverage) applied to each selected leveraged order |
| Strategy Pursued | Attempting the empirical AM/PM rotation strategy to hit the ~200× ceiling |
| Execution Failure | Player opens and holds a full 4× leveraged position into Phase 6 rather than rotating out |
| Phase 6 Market Shock | Systemic crash across holdings after applying the ±30% AM/PM session price limits: Vintrumite drops approximately −48.7%, Samsung drops approximately −51.0% across Phase 6 |

### Expected Consequence

1. Through Phases 1–5, the player repeatedly applies 4× leverage to selected winning orders, allowing realized equity gains to be reused for subsequent positions.
2. In Phase 6 (Second 1501–1800), the systemic collapse hits: major driver assets fall by approximately **−49% to −51%** across the phase after applying the ±30% AM/PM session price limits.
3. Because the active position is leveraged 4× ($3.0\text{ debt} : 1.0\text{ equity}$), a price drop of approximately **6.25%** from the position's entry price reduces the Margin Ratio to the fixed **20% maintenance threshold**.
4. The Margin Ratio reaches or falls below the 20% maintenance threshold within Phase 6:

$$
\text{Margin Ratio} = \frac{\text{Net Equity}}{\text{Gross Exposure}} \leq 20\%
$$

5. **Trigger:** Margin Call = Instant Forced Liquidation. The broker immediately sells the active leveraged position at the current executable market price.
6. If the market has already fallen sufficiently before liquidation execution, gross proceeds may fail to cover outstanding margin debt, driving Net Equity to **$0 (or negative)**.

* **Final Result:** Forced Liquidation / Potential Total Account Wipeout.
* **Ending:** Failed Target. Severe financial loss or complete insolvency.

---

## Sample Case 2: Scenario 1 + Small House (Easy Difficulty — The Normie)

### Sample Input

| Variable | Value |
| :--- | :--- |
| `assigned_scenario_id` | Scenario 1 (`market_scenario.csv`) |
| `initial_capital` | $10,000 USD |
| `target_house_type` | Small House (Easy Difficulty) |
| `property_target_value` | **$30,000 USD** ($3.0\times$ Initial Capital) |
| `leverage_per_order` | **Cash Only (1.0x / 0% Margin Debt)** for each selected order |
| Position Allocation | Conservative 1-trade-per-phase strategy across Phases 1–5, shifting to cash prior to Phase 6 |
| Phase 6 Market Shock | Approximately −49% to −51% systemic driver crash occurs while player holds safe cash reserve |

### Expected Consequence

1. Across Phases 1–5, the player selects the best cash-only trade in each phase, achieving benchmark equity of approximately **$29,247 USD** ($2.92\times$ initial capital).
2. At the end of Phase 5, the player liquidates all positions and holds pure cash heading into Phase 6.
3. During Phase 6, major driver stock prices collapse by approximately −49% to −51%. Because the player holds zero margin debt and has de-risked into cash, account equity remains approximately **$29,247 USD**.
4. Margin Ratio is **N/A (no leveraged exposure / no margin debt)** throughout the crisis. No margin call or forced liquidation can trigger.

* **Final Result:** Solvent; capital preserved at approximately **2.92×** initial capital, just below the **3.0×** target.
* **Ending:** Normie Ending — Survived the crisis safely with zero liquidation stress, but narrowly missed the target.
