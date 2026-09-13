# Assumptions

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
