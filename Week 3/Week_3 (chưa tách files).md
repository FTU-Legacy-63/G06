# WEEK 3: INPUT, INFORMATION AND EVIDENCE READINESS

---

# 1. Input Dictionary

This file defines the minimum inputs and state variables required by the MVP before implementation.

| Variable | Meaning | Unit / Format | Source | Output Affected |
| :--- | :--- | :--- | :--- | :--- |
| `assigned_scenario_id` | Randomly assigned scenario (`1` or `2`) that determines initial cash balance and the locked six-phase price path (`market_scenario.csv`). | Integer: `1` or `2` | System-generated at launch | Sets `initial_capital` and `fixed_price_path` |
| `initial_capital` | Starting liquid cash balance assigned to the player based on the scenario. | KRW/USD (Numeric: e.g., $10,000 USD / 20,000,000 KRW) | System-generated via `assigned_scenario_id` | Starting Net Worth and initial purchasing power |
| `fixed_price_path` | Predetermined 1,800-second sequence (30 minutes across 6 phases) covering 50 asset tickers, phase states, and news triggers. | CSV time-series (`market_scenario.csv`) | Team-created data structure | Real-time portfolio revaluation, margin alerts, and liquidation checks |
| `target_house_type` | Selected financial goal defining game difficulty, required multiplier, and final narrative ending. | Categorical: `Small House` / `Normal House` / `ToLam Villa` | User input at start screen | Sets `property_target_value` and ending narrative |
| `property_target_value` | Mandatory financial threshold required to purchase the chosen house and win. | Numeric: Multiplier × `initial_capital` | Calculated (`initial_capital` × house multiplier) | Target Progress UI gauge and Win/Loss state |
| `margin_tier` | Selected margin financing tier determining maximum purchasing power and debt capacity. | Categorical / Tier: `2x`, `3x`, `4x` (or Cash-only / 1.0x) | User input | Purchasing power, Margin Debt, Margin Call, and Forced Liquidation triggers |
| `orders` | Player trading actions executed during each phase window. | Categorical (Buy / Sell / Hold) + Asset Ticker + Volume + Margin Toggle | User input | Cash balance, asset share volume, margin debt, and net equity |

## Calibrated House Target Difficulty Matrix

*Empirically calibrated against benchmark backtests (`best_case_portfolio_summary.csv`).*

| House Type (`target_house_type`) | Target Multiplier | Required Strategy / Benchmark Feasibility | Consequence / Ending Narrative |
| :--- | :---: | :--- | :--- |
| **Small House** *(Easy / Safe)* | **$3.0\times$ Capital** | Achievable using **Cash Only (1.0×)**. Benchmark yield is $2.92\times$ (1 trade/phase) to $5.20\times$ (AM/PM rotation). | **Normie Ending:** Survived the crisis safely with zero margin debt, but wealth growth is modest. Life remains plain, mundane, and unexciting. |
| **Normal House** *(Medium / Balanced)* | **$20.0\times$ Capital** | Requires active trading with **2.0× or 3.0× Margin**. Benchmark yield spans $7.02\times$ to $72.84\times$. | **Middle-Class Stability Ending:** Navigated market turbulence with disciplined leverage. Enjoy comfortable suburban living and solid financial security. |
| **ToLam Villa** *(Extreme / Hard)* | **$200.0\times$ Capital** | Mathematically impossible without **4.0× Margin**. Theoretical ceiling reaches **$217.45\times$ (+21,645%)** under perfect 10-trade execution before Phase 6 collapse. | **Extravagant Luxury Ending:** Flawless timing generates supreme multi-generational wealth and endless fun. A single misstep triggers total wipeout. |

## Margin Tier Specification

| Tier Level | Multiplier / Borrowing Capacity | Max Purchasing Power | Max Margin Debt (per $1 Equity) | Benchmark Wealth Ceiling (Phase 1–5) | Risk Profile |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **Cash (1.0x)** | $1.0\times$ Buying Power | $1.0 \times \text{Equity}$ | $0.0 \times \text{Equity}$ | **$2.92\times – 5.20\times$** | Zero liquidation risk; immune to broker margin calls. |
| **2x** | $2.0\times$ Buying Power | $2.0 \times \text{Equity}$ | $1.0 \times \text{Equity}$ | **$7.02\times – 21.27\times$** | Moderate: Standard retail brokerage tier. Requires a $35\%$ crash to trigger liquidation. |
| **3x** | $3.0\times$ Buying Power | $3.0 \times \text{Equity}$ | $2.0 \times \text{Equity}$ | **$14.72\times – 72.84\times$** | High Risk: Breaches 30% maintenance threshold on a $15\% - 20\%$ price decline. |
| **4x** | $4.0\times$ Buying Power | $4.0 \times \text{Equity}$ | $3.0 \times \text{Equity}$ | **$27.99\times – 217.45\times$** | Extreme Risk (CFD-level): Maximum upside potential (~200×); vulnerable to instant liquidation on a $10\% - 15\%$ shock. |

## Core Input Flow

> `assigned_scenario_id` (Random 1 or 2) → Sets `initial_capital` + `fixed_price_path` (`market_scenario.csv`) → User selects `target_house_type` (Difficulty: $3\times$, $20\times$, or $200\times$) → Sets `property_target_value` → User executes `orders` with selected `margin_tier` (`2x`, `3x`, `4x`) → Real-time Margin & Equity Valuation → Financial & Narrative Outcome

---

# 2. Source–Use Map

This file records where external information is used in the MVP, how it was modified, and the limitations of each source.

| Source | Claim / Use in Product | Limitation & Team Modification |
| :--- | :--- | :--- |
| Historical KOSPI, CFD, and tech-stock price action from the April 2023 Korea margin crisis | Used as empirical problem evidence and historical baseline for modeling systemic cascade liquidations across 50 Korean equity and ETF tickers (`market_scenario.csv`). | **Team Modification:** The historical crisis unfolded over multiple weeks. The team **synthetically intensified the price series and compressed it into an 1,800-second (30-minute), 6-phase sequence**. Phase 5 features aggressive bull-trap fakeouts, followed by an extreme Phase 6 systemic collapse where core assets drop over **−57%** within 300 seconds. Circuit breakers are omitted. |
| Empirical Strategy Optimization Dataset (`best_case_portfolio_summary.csv` & `best_case_portfolio_combos.csv`) | Used to verify maximum mathematical wealth ceilings and establish defensible house target multipliers ($3\times$, $20\times$, and $200\times$). | **Benchmark Limitation:** Assumes frictionless instant execution, perfect trade timing (capturing exact AM/PM local peaks across tickers like Vintrumite, POSCO Future M, and Kakao), and full compounding without slippage. |
| Standard Korean brokerage margin regulations (e.g., Kiwoom Securities) | Used as a regulatory baseline for defining initial margin tiers (`2x`, `3x`, `4x`) and the 30% maintenance margin threshold. | The MVP standardizes margin into 3 discrete borrowing multipliers and applies a universal liquidation rule across all 50 assets, omitting tiered interest rate brackets. |

## Source-Use Principle

External crisis data provided the **historical foundation**, which was **modified by the team into an intensified deterministic simulation model**. Benchmark algorithmic runs confirmed that peak margin returns can reach **~200×** under optimal conditions, providing empirical justification for the ToLam Villa difficulty tier.

---

# 3. Assumptions

The MVP intentionally simplifies several market mechanisms to maintain technical feasibility and preserve the intended behavioral lesson.

## Assumption 1: Instant Market Liquidity
* **Assumption:** Forced-liquidation orders and user trades are executed immediately at the current tick price without delay.
* **Reason:** Avoids requiring an order-book depth matching engine and complex liquidity-pool modeling.
* **Risk:** Real-world fire sales cause substantial slippage, executing at prices far lower than displayed.
* **Disclosure:** *"This simulation assumes instant liquidity. Real-world liquidations often incur severe price slippage."*

## Assumption 2: Amplified Deterministic Market Paths
* **Assumption:** The simulation strictly follows the 1,800-second scripted price series in `market_scenario.csv` across all 6 phases rather than real-time stochastic random walks.
* **Reason:** Guarantees that players experience the intended behavioral finance traps (e.g., Phase 1 deceptive green, Phase 4 correction, Phase 5 bull-trap bounce, and Phase 6 systemic plunge) without RNG variance diluting the lesson.
* **Risk:** Replaying the same scenario allows players to memorize asset price peaks.
* **Disclosure:** *"Market conditions follow an intensified historical simulation model. Replay variety is provided across distinct scenario tracks."*

## Assumption 3: Fixed Multiplier Housing Targets
* **Assumption:** Property targets are strictly pegged to fixed initial-capital multipliers ($3.0\times$, $20.0\times$, and $200.0\times$) derived from benchmark feasibility models.
* **Reason:** Establishes clear, indisputable mathematical targets that force players to evaluate the trade-off between safe, modest returns and high-risk leverage.
* **Risk:** Real-world property markets do not scale proportionally to an individual investor's initial capital.
* **Disclosure:** *"Housing targets represent lifestyle aspirations mathematically scaled to initial starting wealth."*

## Assumption 4: Unlimited Order Volume Matching (Balance-Constrained Only)
* **Assumption:** Any Buy or Sell order submitted by the player matches instantly at 100% fill rate without volume caps or order-book supply limits, constrained solely by available cash and margin borrowing capacity.
* **Reason:** Eliminates the need for order-book queues and partial fills, keeping gameplay focused squarely on leverage risk and solvency management.
* **Risk:** In real-world market crashes, bids evaporate completely (limit-down freeze), making it impossible to offload large positions.
* **Disclosure:** *"The simulation assumes infinite market liquidity for player orders. Orders are bounded only by available account balance and margin capacity, ignoring market-depth volume limits."*

---

# 4. Sample Input–Output

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
