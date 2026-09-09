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
