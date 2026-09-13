# WEEK 3: INPUT, INFORMATION AND EVIDENCE READINESS

---

# 1. Input Dictionary

This file defines the minimum inputs and state variables required by the MVP before implementation[cite: 5].

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
| **Small House** *(Easy / Safe)* | **3.0× Capital** | Achievable using **Cash Only (1.0×)**. Benchmark yield is 2.92× (1 trade/phase) to 5.20× (AM/PM rotation). | **Normie Ending:** Survived the crisis safely with zero margin debt, but wealth growth is modest. Life remains plain, mundane, and unexciting. |
| **Normal House** *(Medium / Balanced)* | **20.0× Capital** | Requires active trading with **2.0× or 3.0× Margin**. Benchmark yield spans 7.02× to 72.84×. | **Middle-Class Stability Ending:** Navigated market turbulence with disciplined leverage. Enjoy comfortable suburban living and solid financial security. |
| **ToLam Villa** *(Extreme / Hard)* | **100.0× Capital** | Mathematically impossible without **4.0× Margin** (3.0× peaks at 72.84×). Requires near-flawless multi-phase compounding before the Phase 6 collapse. | **Extravagant Luxury Ending:** Flawless timing generates supreme multi-generational wealth and elite status. A single misstep triggers total wipeout. |

## Margin Tier Specification

| Tier Level | Multiplier / Borrowing Capacity | Max Purchasing Power | Max Margin Debt (per $1 Equity) | Drop to Breach 20% Maintenance Margin | Risk Profile |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **Cash (1.0x)** | 1.0× Buying Power | 1.0 × Equity | 0.0 × Equity | N/A (Cannot Liquidate) | Zero liquidation risk; immune to broker margin calls. |
| **2x** | 2.0× Buying Power | 2.0 × Equity | 1.0 × Equity | **-37.50%** | Moderate: High cushion against normal intraday volatility; liquidates in catastrophic systemic shocks. |
| **3x** | 3.0× Buying Power | 3.0 × Equity | 2.0 × Equity | **-16.67%** | High Risk: Vulnerable to sharp corrections and Phase 5 bull traps (max yield: 72.84×). |
| **4x** | 4.0× Buying Power | 4.0 × Equity | 3.0 × Equity | **-6.25%** | Extreme Risk (CFD-level): Unlocks the 100.0× ceiling; highly fragile to even minor price dips. |

## Core Input Flow

> `assigned_scenario_id` (Random 1 or 2) → Sets `initial_capital` + `fixed_price_path` (`market_scenario.csv`) → User selects `target_house_type` (Difficulty: 3×, 20×, or 100×) → Sets `property_target_value` → User executes `orders` with selected `margin_tier` (`2x`, `3x`, `4x`) → Real-time Margin & Equity Valuation → Financial & Narrative Outcome

---

# 2. Source–Use Map

This file records where external information is used in the MVP, how it was modified, and the limitations of each source[cite: 5].

| Source | Claim / Use in Product | Limitation & Team Modification |
| :--- | :--- | :--- |
| Historical KOSPI, CFD, and tech-stock price action from the April 2023 Korea margin crisis | Used as empirical problem evidence and historical baseline for modeling systemic cascade liquidations across 50 Korean equity and ETF tickers (`market_scenario.csv`). | **Team Modification:** The historical crisis unfolded over multiple weeks. The team **synthetically intensified the price series and compressed it into an 1,800-second (30-minute), 6-phase sequence**. Phase 5 features aggressive bull-trap fakeouts, followed by an extreme Phase 6 systemic collapse where core assets drop over **-57%** within 300 seconds. Circuit breakers are omitted. |
| Empirical Strategy Optimization Dataset (`best_case_portfolio_summary.csv` & `best_case_portfolio_combos.csv`) | Used to verify maximum mathematical wealth ceilings and establish defensible house target multipliers (3×, 20×, and 100×). | **Benchmark Limitation:** Assumes frictionless instant execution, perfect trade timing (capturing exact AM/PM local peaks across tickers like Vintrumite, POSCO Future M, and Kakao), and full compounding without slippage. Benchmark confirms 3.0× leverage caps at 72.84×, making 100× achievable exclusively via the 4.0× margin tier. |
| Standard Korean brokerage margin regulations (e.g., Kiwoom Securities) | Used as a regulatory baseline for defining initial margin tiers (`2x`, `3x`, `4x`) and risk enforcement mechanics. | **Team Modification:** Standard regulatory accounts use a 30% or 130%-140% threshold. The MVP calibrates the maintenance margin level to **20% (maximum effective leverage of 5.0×)** so that the 4.0× tier (which starts at 25% margin ratio) has a playable operational buffer rather than liquidating instantly upon trade entry. |

## Source-Use Principle

External crisis data provided the **historical foundation**, which was **modified by the team into an intensified deterministic simulation model**. The maintenance margin floor is calibrated to **20%** to ensure mathematical consistency across all margin tiers while preserving high-pressure liquidation dynamics.

---

# 3. Assumptions

The MVP intentionally simplifies several market mechanisms to maintain technical feasibility and preserve the intended behavioral lesson[cite: 5].

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
* **Assumption:** Property targets are strictly pegged to fixed initial-capital multipliers (3.0×, 20.0×, and 100.0×) derived from benchmark feasibility models.
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

This file demonstrates how the scenario data, margin tiers, and house targets produce predictable financial consequences[cite: 5].

## Sample Case 1: Scenario 1 + ToLam Villa (Extreme Difficulty — The Wipeout)

### Sample Input
| Variable | Value |
| :--- | :--- |
| `assigned_scenario_id` | Scenario 1 (`market_scenario.csv`) |
| `initial_capital` | $10,000 USD (or 20,000,000 KRW) |
| `target_house_type` | ToLam Villa (Extreme Difficulty) |
| `property_target_value` | **$1,000,000 USD** (100.0× Initial Capital) |
| `margin_tier` Selected | **4x Tier** (Maximum Leverage) |
| Position Allocation | Full 4.0× gross exposure: $40,000 USD position ($10,000 equity, $30,000 margin debt; starting margin ratio = 25%) |
| Strategy Pursued | Attempting aggressive multi-phase compounding to reach the $1,000,000 USD (100×) goal |
| Execution Failure | Player holds a full leveraged position into Phase 6 rather than rotating to cash |
| Phase 6 Market Shock | Systemic crash across holdings: Vintrumite drops -57.8%, Samsung drops -56.9% |

### Expected Consequence
1. In Phase 5, the player rides the euphoric wave with 4× leverage, temporarily growing equity near the seven-figure threshold.
2. In Phase 6 (Second 1501–1800), the systemic collapse hits. A price drop of just **-6.25%** pushes position value to $37,500 USD, reducing net equity to $7,500 USD ($37,500 - $30,000 debt).
3. At that point, the Margin Ratio hits **20.0%** (effective leverage reaches **5.0×**). Any further tick decline breaches the 20% maintenance margin floor.
4. **Trigger:** Forced Liquidation. The broker automatically fires a market-sell order for all holdings to recover the $30,000 debt.
5. Because asset prices plummet by more than -56% during Phase 6, liquidation execution at crash prices fails to cover the borrowed debt, driving Net Equity to **$0 (or negative)**.

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
| `property_target_value` | **$30,000 USD** (3.0× Initial Capital) |
| `margin_tier` Selected | **Cash Only (1.0x / 0% Margin Debt)** |
| Position Allocation | Conservative 1-trade-per-phase strategy across Phases 1–4, shifting to cash prior to Phase 6 |
| Phase 6 Market Shock | -57% systemic crash occurs while player holds safe cash reserve |

### Expected Consequence
1. Across Phases 1–4, the player selects solid fundamental uptrends using pure cash, achieving benchmark equity of approximately **$29,247 USD** (2.92× capital preservation baseline).
2. Recognizing market euphoria in Phase 5, the player liquidates positions to hold pure cash heading into Phase 6.
3. During Phase 6, stock prices collapse by -57%. Because the player holds zero margin debt and has de-risked into cash, portfolio value remains stable at ~$29,000 – $30,000 USD.
4. Margin Ratio remains at **100% (No Debt)** throughout the entire crisis. No margin call or liquidation can physically trigger.

* **Final Result:** Solvent; capital fully preserved, achieving the baseline target (~3.0×).
* **Ending:** Normie Ending — Survived the crisis safely with zero liquidation stress, but lived a modest, unexciting, and strictly ordinary life.
