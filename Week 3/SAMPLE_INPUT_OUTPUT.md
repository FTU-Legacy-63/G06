# Sample Input–Output

This file demonstrates how the scenario data, margin tiers, and house targets produce predictable financial consequences.

## Sample Case 1: Scenario 1 + ToLam Villa (Extreme Difficulty — The Wipeout)

### Sample Input
| Variable | Value |
| :--- | :--- |
| `assigned_scenario_id` | Scenario 1 (`market_scenario.csv`) |
| `initial_capital` | $10,000 USD (or 20,000,000 KRW) |
| `target_house_type` | ToLam Villa (Extreme Difficulty) |
| `property_target_value` | **$2,000,000 USD** ($200.0\times$ Initial Capital) |
| `margin_tier` Selected | **4x Tier** (Maximum Leverage) |
| Strategy Pursued | Attempting the empirical AM/PM rotation strategy to hit the ~200× ceiling |
| Execution Failure | Player holds a full leveraged position into Phase 6 rather than rotating out |
| Phase 6 Market Shock | Systemic crash across holdings: Vintrumite drops −57.8%, Samsung drops −56.9% |

### Expected Consequence
1. In Phase 5, the player rides the euphoric wave with 4× leverage, temporarily growing equity toward seven figures.
2. In Phase 6 (Second 1501–1800), the systemic collapse hits: asset values plummet by over **−56%** within 300 seconds.
3. Because the position is leveraged 4× ($3.0\text{ debt} : 1.0\text{ equity}$), a price drop greater than **10%** severely damages equity, and a drop exceeding **25%** completely erases net worth.
4. Net Equity falls below the 30% maintenance threshold within seconds of Phase 6 opening:
   $$\text{Margin Ratio} = \frac{\text{Net Equity}}{\text{Gross Exposure}} < 30\%$$
5. **Trigger:** Forced Liquidation. The broker sells all shares at collapsed market prices.
6. Gross proceeds fail to cover margin debt after severe intra-tick drops, driving Net Equity to **$0 (or negative)**.

* **Final Result:** Forced Liquidation / Total Account Wipeout.
* **Ending:** Failed Target. Complete financial insolvency.

---

## Sample Case 2: Scenario 1 + Small House (Easy Difficulty — The Normie)

### Sample Input
| Variable | Value |
| :--- | :--- |
| `assigned_scenario_id` | Scenario 1 (`market_scenario.csv`) |
| `initial_capital` | $10,000 USD (or 20,000,000 KRW) |
| `target_house_type` | Small House (Easy Difficulty) |
| `property_target_value` | **$30,000 USD** ($3.0\times$ Initial Capital) |
| `margin_tier` Selected | **Cash Only (1.0x / 0% Margin Debt)** |
| Position Allocation | Conservative 1-trade-per-phase strategy across Phases 1–4, shifting to cash prior to Phase 6 |
| Phase 6 Market Shock | −57% systemic crash occurs while player holds safe cash reserve |

### Expected Consequence
1. Across Phases 1–4, the player selects solid fundamental uptrends using pure cash, achieving benchmark equity of approximately **$29,247 USD** ($2.92\times$ capital preservation baseline).
2. Recognizing market euphoria in Phase 5, the player liquidates positions to hold pure cash heading into Phase 6.
3. During Phase 6, stock prices collapse by −57%. Because the player holds zero margin debt and has de-risked into cash, portfolio value remains stable at ~$29,000 – $30,000 USD.
4. Margin Ratio remains at **100% (No Debt)** throughout the entire crisis. No margin call or liquidation can physically trigger.

* **Final Result:** Solvent; capital fully preserved, achieving the baseline target (~$3.0\times$).
* **Ending:** Normie Ending — Survived the crisis safely with zero liquidation stress, but lived a modest, unexciting, and strictly ordinary life.
