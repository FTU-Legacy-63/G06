# Input Dictionary

This file defines the minimum inputs and state variables required by the MVP before implementation.

| Variable | Meaning | Unit / Format | Source | Output Affected |
| :--- | :--- | :--- | :--- | :--- |
| `assigned_scenario_capital` | Randomly assigned scenario (1, 2, or 3) that determines both starting capital and the fixed market path. | Integer: `1`, `2`, or `3` | System-generated at launch | Initial wealth and market conditions |
| `fixed_price_path` | Predetermined sequence of stock-price changes across Phases 1–6 for the assigned scenario. | Array of percentage changes | Team-created | Portfolio valuation across all phases |
| `target_house_type` | Player's selected financial goal. Mini Apartment requires 2× initial capital; Gangnam Villa requires 8× initial capital. | Categorical: `Mini Apartment` / `Gangnam Villa` | User input | Financial target and ending |
| `initial_capital` | Starting cash balance assigned to the player. | KRW, numeric | System-generated based on scenario | Starting Net Worth and purchasing power |
| `initial_margin_ratio` | Margin ratio selected by the player. | Percentage: 25%–50% | User input | Leverage, Margin Call and Forced Liquidation risk |
| `orders` | Trading decisions submitted by the player during each phase. | Buy / Sell / Hold + Volume + Cash/Margin | User input | Portfolio holdings, cash, debt and investment return |

## Core Input Flow

> `assigned_scenario_capital` → `initial_capital` + `fixed_price_path` → `target_house_type` → `orders` + `initial_margin_ratio` → Financial Outcome

# Source–Use Map

This file records where external information is used in the MVP and the limitations of each source.

| Source | Claim / Use in Product | Limitation |
| :--- | :--- | :--- |
| Historical KOSPI and CFD market reports from the April 2023 Korea margin crisis | Used as problem evidence and as a reference for designing realistic market declines in Phases 4–6. | The real event occurred over multiple days, while the simulation compresses the market sequence into approximately 30 minutes. Real-world circuit breakers are excluded from the MVP. |
| Standard Korean brokerage margin requirements (e.g., Kiwoom Securities) | Used as a reference for defining leverage limits and margin mechanics. | The MVP applies standardized margin rules and does not model differences across brokers, securities, or client tiers. |

## Source-Use Principle

External data is used to establish **realistic boundaries and assumptions**, while the actual six-phase price paths remain deterministic and are created specifically for the simulation.

# Assumptions

The MVP intentionally simplifies several real-world market mechanisms to maintain technical feasibility and preserve the intended learning experience.

## Assumption 1: Instant Market Liquidity

**Assumption:** Forced-liquidation orders are executed immediately at the current simulated market price.

**Reason:** Avoids requiring a complex order-book and market-impact model.

**Risk:** Real forced liquidations may experience slippage, meaning the actual execution price can be worse than the displayed market price.

**Disclosure:**  
> "This simulation assumes instant liquidity. Real-world liquidations may incur significant slippage."

---

## Assumption 2: Deterministic Market Paths

**Assumption:** Each scenario follows a predetermined six-phase price path rather than randomly generated market movements.

**Reason:** Ensures that players experience the intended behavioral events, including the bull market, correction, bull trap, and final crash.

**Risk:** Players may learn the price sequence when replaying the same scenario.

**Disclosure:** The simulation is primarily designed as a controlled educational experience. Replay variation is provided through different scenario IDs.

# Sample Input–Output

This file demonstrates how fixed scenarios combined with different player decisions produce predictable financial consequences.

## Sample Case 1: Scenario 1 + Gangnam Villa — The Wipeout

### Sample Input

| Input | Value |
| :--- | :--- |
| Scenario | Scenario 1 |
| Initial Capital | 10,000,000 KRW |
| Financial Target | Gangnam Villa |
| Target Value | 80,000,000 KRW |
| Market Path | Aggressive bull run followed by a sudden crash |
| Phase 5 Shock | −20% |
| Player Strategy | Maximum margin exposure |
| Maximum Leverage | 1:5 |

### Intended Consequence

The player uses maximum leverage during the bull market to pursue the 8× financial target.

When the predetermined **−20% market shock** occurs, the leveraged position suffers a disproportionately large equity loss. Equity falls below the required maintenance level, triggering:

> **Market Crash → Maintenance Margin Breach → Margin Call → Forced Liquidation**

**Final Outcome:** Forced Liquidation / Wipeout  
**Financial Target:** Failed

---

## Sample Case 2: Scenario 3 + Mini Apartment — The Normie

### Sample Input

| Input | Value |
| :--- | :--- |
| Scenario | Scenario 3 |
| Initial Capital | 50,000,000 KRW |
| Financial Target | Mini Apartment |
| Target Value | 100,000,000 KRW |
| Market Path | Moderate growth followed by a correction |
| Market Shock | −10% |
| Player Strategy | Cash-only investment |
| Margin Used | 0% |

### Intended Consequence

The player's portfolio declines during the predetermined correction. However, because the player has no Margin Debt, the decline does not trigger a Margin Call or Forced Liquidation.

> **Market Correction → Portfolio Loss → No Margin Call → Player Remains Solvent**

**Final Outcome:** Neutral / Normie Ending  
**Liquidation:** No  
**Financial Status:** Solvent but financial target not achieved
