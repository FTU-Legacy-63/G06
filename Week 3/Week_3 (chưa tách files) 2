# Input Dictionary

This file defines the minimum inputs and state variables required by the MVP before implementation.

| Variable | Meaning | Unit / Format | Source | Output Affected |
| :--- | :--- | :--- | :--- | :--- |
| `assigned_scenario_id` | Randomly assigned scenario (`1` or `2`) that determines initial cash balance and the locked six-phase price path. | Integer: `1` or `2` | System-generated at launch | Sets `initial_capital` and `fixed_price_path` |
| `initial_capital` | Starting liquid cash balance assigned to the player based on the scenario. | KRW (Numeric: e.g., 20m or 50m KRW) | System-generated via `assigned_scenario_id` | Starting Net Worth and initial purchasing power |
| `fixed_price_path` | Predetermined sequence of stock-price changes and news across Phases 1–6 tied to the assigned scenario. | Array of percentage changes | Team-created data structure | Portfolio revaluation and margin triggers |
| `target_house_type` | Selected financial goal defining game difficulty, required multiplier, and final narrative ending. | Categorical: `Small House` / `Normal House` / `Big-Ass Villa` | User input at start screen | Sets `property_target_value` and ending narrative |
| `property_target_value` | Mandatory financial threshold required to purchase the chosen house and win. | KRW (Numeric: Multiplier × `initial_capital`) | Calculated (`initial_capital` × house multiplier) | Target Progress UI gauge and Win/Loss state |
| `initial_margin_ratio` | Maximum margin leverage ratio selected/unlocked for trading. | Percentage: 20%–50% (Max 1:5 leverage) | User input | Purchasing power, Margin Call, and Forced Liquidation triggers |
| `orders` | Player trading actions executed during a phase. | Categorical (Buy / Sell / Hold) + Volume + Cash/Margin toggle | User input | Cash, share holdings, margin debt, and net equity |

## House Target Difficulty Matrix

| House Type (`target_house_type`) | Target Multiplier | Required Strategy / Constraint | Consequence / Ending Narrative |
| :--- | :---: | :--- | :--- |
| **Small House** *(Easy / Safe)* | $1.5\times \text{Capital}$ | Achievable with cash or very conservative leverage. | **Normie Ending:** Survived safely, but life remains plain, restrictive, and completely boring. |
| **Normal House** *(Medium / Balanced)* | $3.5\times \text{Capital}$ | Requires moderate margin use; vulnerable to major market corrections. | **Middle-Class Stability Ending:** Comfortable suburban life with balanced security. |
| **Big-Ass Villa** *(Hard / Degenerate)* | $8.0\times \text{Capital}$ | Mathematically forces maximum leverage (1:4 or 1:5); extreme liquidation vulnerability. | **Extravagant Luxury Ending:** Endless fun and elite status if won; total wipeout if margin-called. |

## Core Input Flow

> `assigned_scenario_id` (Random 1 or 2) → Sets `initial_capital` + `fixed_price_path` → User selects `target_house_type` (Difficulty: $1.5\times$, $3.5\times$, or $8\times$) → Sets `property_target_value` → `orders` + `initial_margin_ratio` → Financial & Behavioral Consequence

---

# Source–Use Map

This file records where external information is used in the MVP and the limitations of each source.

| Source | Claim / Use in Product | Limitation |
| :--- | :--- | :--- |
| Historical KOSPI and CFD market reports from the April 2023 Korea margin crisis | Used as problem evidence and empirical basis for the two 6-phase price crash and bull-trap scripts. | The historical crash unfolded over several days, whereas the game compresses the timeline into ~30 minutes. Real-world regulatory exchange halts (circuit breakers) are excluded for simplicity. |
| Standard Korean brokerage margin rules (e.g., Kiwoom Securities) | Used to parameterize authentic initial margin rates (e.g., 40%–50%) and maintenance margin thresholds (30%). | Applies a single universal regulatory threshold across all assets, ignoring VIP client fee/rate tiers. |

---

# Assumptions

The MVP intentionally simplifies several market mechanisms to maintain technical feasibility and preserve the intended behavioral lesson.

## Assumption 1: Instant Market Liquidity
* **Assumption:** Forced-liquidation orders are executed immediately at the current simulated market price.
* **Reason:** Avoids requiring an order-book matching engine and complex liquidity-depth calculations.
* **Risk:** Real-world fire sales cause substantial slippage, executing at far worse prices than displayed.
* **Disclosure:** *"This simulation assumes instant liquidity. Real-world liquidations often incur severe price slippage."*

## Assumption 2: Deterministic Market Paths
* **Assumption:** Each of the 2 scenarios follows a predetermined, hardcoded six-phase price path rather than real-time stochastic/random price movements.
* **Reason:** Guarantees that players experience the intended behavioral finance traps (e.g., Phase 1 deceptive green, Phase 4 correction, Phase 5 bull-trap bounce).
* **Risk:** Players replaying the same scenario ID can anticipate future price moves.
* **Disclosure:** *"Market conditions follow a controlled historical simulation model. Replay variety is provided across the 2 distinct scenario tracks."*

## Assumption 3: Fixed Difficulty Multipliers
* **Assumption:** Property targets are strictly tied to fixed initial-capital multipliers ($1.5\times$, $3.5\times$, $8.0\times$) rather than dynamic real-estate market fluctuations.
* **Reason:** Creates a clear mathematical constraint that forces the user to choose between safe, modest returns and high-risk leverage.
* **Risk:** Real-world housing prices fluctuate independently of stock portfolio values.
* **Disclosure:** *"Housing targets represent fixed lifestyle aspirations relative to starting wealth."*

---

# Sample Input–Output

This file demonstrates how the 2 scenarios combined with the 3 difficulty choices produce predictable financial consequences.

## Sample Case 1: Scenario 1 + Big-Ass Villa (High Difficulty — The Wipeout)

### Sample Input
| Variable | Value |
| :--- | :--- |
| `assigned_scenario_id` | Scenario 1 |
| `initial_capital` | 20,000,000 KRW |
| `target_house_type` | Big-Ass Villa (Hard Difficulty) |
| `property_target_value` | 160,000,000 KRW ($8.0\times$) |
| Strategy | Max leverage (1:5) in Phase 3 to hit the 160m target |
| Phase 5 Market Event | Severe shock (−20%) masked by deceptive bounce headline |

### Expected Consequence
1. In Phase 3, player borrows 80,000,000 KRW in margin to hold a 100,000,000 KRW position.
2. In Phase 5, the stock drops 20%. Position value falls to 80,000,000 KRW while margin debt remains 80,000,000 KRW.
3. Net Equity reaches 0 KRW ($\text{Margin Ratio} = 0\% < 30\%$ maintenance threshold).
4. **Trigger:** Forced Liquidation. The broker liquidates all shares at market price.

* **Final Result:** Total Wipeout / Bankruptcy.
* **Ending:** Failed Target. Complete financial insolvency.

---

## Sample Case 2: Scenario 2 + Small House (Easy Difficulty — The Normie)

### Sample Input
| Variable | Value |
| :--- | :--- |
| `assigned_scenario_id` | Scenario 2 |
| `initial_capital` | 50,000,000 KRW |
| `target_house_type` | Small House (Easy Difficulty) |
| `property_target_value` | 75,000,000 KRW ($1.5\times$) |
| Strategy | Cash-only investing (0% margin debt), selective rebalancing |
| Phase 5 Market Event | Moderate drop (−15%) with high volatility |

### Expected Consequence
1. Player allocates 40,000,000 KRW in cash shares and holds 10,000,000 KRW cash reserve.
2. In Phase 5, market drops 15%. Stock value falls to 34,000,000 KRW.
3. Total equity equals 44,000,000 KRW. Because margin debt is 0, margin health remains $100\%$.
4. No liquidation is triggered. Player recovers modestly in Phase 6 to end at 52,000,000 KRW.

* **Final Result:** Solvent; capital preserved, but fails the $1.5\times$ target.
* **Ending:** Normie Ending — Survived the crash safely, but locked into a completely mundane, uninspiring lifestyle.
