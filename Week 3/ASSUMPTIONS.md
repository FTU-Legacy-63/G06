# Assumptions

The MVP intentionally simplifies several market mechanisms to maintain technical feasibility and preserve the intended behavioral lesson.

## Assumption 1: Instant Market Liquidity

- **Assumption:** Forced-liquidation orders and user trades are executed immediately at the current tick price without delay, provided that the asset has not reached its session price ceiling or floor.
- **Reason:** Avoids requiring an order-book depth matching engine and complex liquidity-pool modeling.
- **Risk:** Real-world fire sales may cause substantial slippage, executing at prices far lower than displayed.
- **Disclosure:** *"This simulation assumes instant liquidity under normal trading conditions. Real-world liquidations may incur severe price slippage."*

## Assumption 2: Amplified Deterministic Market Paths

- **Assumption:** The simulation strictly follows a 1,800-second scripted price series across all 6 phases rather than real-time stochastic random walks. The MVP is designed to contain two deterministic scenario datasets; `market_scenario.csv` is the currently completed scenario.
- **Reason:** Guarantees that players experience the intended behavioral finance traps (e.g., Phase 1 deceptive green, Phase 4 correction, Phase 5 bull-trap bounce, and Phase 6 systemic plunge) without RNG variance diluting the lesson.
- **Risk:** Replaying the same scenario allows players to memorize asset price peaks and market movements.
- **Disclosure:** *"Market conditions follow intensified deterministic simulation paths. Multiple scenario tracks are used to reduce replay predictability."*

## Assumption 3: Fixed Multiplier Housing Targets

- **Assumption:** Property targets are strictly pegged to fixed initial-capital multipliers (`3.0×`, `20.0×`, and `100.0×`) derived from benchmark feasibility models.
- **Reason:** Establishes clear, indisputable mathematical targets that force players to evaluate the trade-off between safe, modest returns and high-risk leverage.
- **Risk:** Real-world property markets do not scale proportionally to an individual investor's initial capital.
- **Disclosure:** *"Housing targets represent lifestyle aspirations mathematically scaled to initial starting wealth."*

## Assumption 4: Unlimited Order Volume Matching (Balance-Constrained Only)

- **Assumption:** Any Buy or Sell order submitted by the player matches at 100% fill rate without volume caps or order-book supply limits, constrained solely by available cash, margin borrowing capacity, and the session price ceiling/floor.
- **Reason:** Eliminates the need for order-book queues and partial fills, keeping gameplay focused squarely on leverage risk and solvency management.
- **Risk:** Real-world orders may be partially filled or remain unfilled because of insufficient market depth, particularly during extreme market movements.
- **Disclosure:** *"The simulation ignores market-depth volume limits. Orders are bounded by account balance, margin capacity, and predefined market price limits."*

## Assumption 5: Session Price Ceiling and Floor

- **Assumption:** Each AM and PM trading session has a maximum price movement of **±30% from its session opening/reference price**. The price limit resets at the beginning of each new AM/PM session.
- **Reason:** Prevents unrestricted single-session price movements while preserving the amplified volatility required by the simulation. Separate AM/PM limits also allow extreme multi-session market crashes to develop progressively.
- **Risk:** This simplified session-based price-limit mechanism does not reproduce all exchange-specific reference-price, order-priority, or price-limit rules.
- **Disclosure:** *"Asset prices are limited to ±30% per trading session. The reference price resets at the beginning of each AM/PM session."*

Because the price limit resets between sessions, the theoretical maximum cumulative movement across one complete phase is:

| Direction | AM | PM | Maximum Phase Movement |
|---|---:|---:|---:|
| Maximum Increase | +30% | +30% | **+69%** |
| Maximum Decline | −30% | −30% | **−51%** |

The cumulative limits are compounded rather than added:

**Maximum increase:** `1.30 × 1.30 − 1 = +69%`

**Maximum decline:** `0.70 × 0.70 − 1 = −51%`

## Assumption 6: Fixed Maintenance Margin

- **Assumption:** The MVP uses a fixed **20% maintenance margin** across all leveraged positions. A margin call is triggered when the player's margin ratio reaches or falls below 20%.
- **Reason:** Creates one transparent and testable threshold across all leverage tiers while allowing the maximum 4× leverage tier to remain playable.
- **Risk:** Real brokers may apply different maintenance requirements depending on the security, volatility, client, and market conditions.
- **Disclosure:** *"The simulation uses a standardized 20% maintenance-margin threshold. Real-world margin requirements vary by broker and security."*

The margin ratio is calculated as:

`Margin Ratio = Net Equity / Gross Exposure`

The resulting margin-call sensitivity is:

| Margin Tier | Initial Margin Ratio | Asset Decline to 20% Margin Call | Theoretical Equity Wipeout |
|---|---:|---:|---:|
| **Cash (1.0×)** | 100.00% | N/A | −100.00% |
| **2×** | 50.00% | **−37.50%** | −50.00% |
| **3×** | 33.33% | **−16.67%** | −33.33% |
| **4×** | 25.00% | **−6.25%** | −25.00% |

The **20% threshold represents the margin-call point, not the theoretical equity wipeout point**. At 4× leverage, for example, a decline of approximately **6.25% from the position's entry price** is sufficient to trigger a margin call even though the player's equity does not theoretically reach zero until a 25% decline.

## Assumption 7: Margin Tier Specification

| Tier Level | Multiplier / Borrowing Capacity | Max Purchasing Power | Max Margin Debt (per $1 Equity) | Benchmark Wealth Ceiling (Phase 1–5) | Margin Call Trigger (20% Maintenance Margin) | Risk Profile |
|---|---|---|---|---|---|---|
| **Cash (1.0×)** | 1.0× Buying Power | 1.0× Equity | 0.0× Equity | **2.92× – 5.20×** | **N/A** | Zero margin-liquidation risk; no broker margin calls. |
| **2×** | 2.0× Buying Power | 2.0× Equity | 1.0× Equity | **7.02× – 21.27×** | **−37.50%** | Moderate Risk: A 10% asset decline produces approximately a 20% equity loss. Theoretical equity wipeout occurs at a 50% decline. |
| **3×** | 3.0× Buying Power | 3.0× Equity | 2.0× Equity | **14.72× – 72.84×** | **−16.67%** | High Risk: A 10% asset decline produces approximately a 30% equity loss. Theoretical equity wipeout occurs at a 33.3% decline. |
| **4×** | 4.0× Buying Power | 4.0× Equity | 3.0× Equity | **27.99× – 217.45×** | **−6.25%** | Extreme Risk: A 10% asset decline produces approximately a 40% equity loss. Theoretical equity wipeout occurs at a 25% decline. |

The Phase 1–5 benchmark wealth ceilings represent **perfect-foresight upper-bound outcomes** calculated from the current market scenario. They are used for stress testing and target calibration rather than as expected player outcomes.
