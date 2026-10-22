# Best-Case Optimization and Player Difficulty Calibration

## 1. Overview

Two optimization approaches were used to estimate the best-case performance of Scenario 1. The first establishes a strong sequential benchmark, while the second improves that benchmark by allowing the player to reuse newly created margin capacity during profitable market movements.

|  | **Approach 1 — Concentrated Dynamic Programming** | **Approach 2 — Staggered Re-Leveraging** |
|---|---|---|
| **Core idea** | Find the best sequence of individual leveraged trades | Improve the sequential strategy by adding exposure during profitable cycles |
| **Trading structure** | BUY once → Hold → SELL all → Settlement → Next trade | BUY → Gain → Equity rises → New margin capacity → BUY again → Exit |
| **Positions** | One concentrated position at a time | Multiple staggered BUYs can occur within the same cycle |
| **Use of newly created margin capacity** | No | Yes |
| **Compounding** | Mainly between completed cycles | Between cycles and within profitable cycles |
| **Approximate best-case result** | **109×** | **156×** |
| **Starting capital** | $10,000 | $10,000 |
| **Approximate final wealth** | $1.09 million | $1.56 million |
| **Purpose** | Strong baseline benchmark | Richer best-case benchmark |

The benchmark progression is therefore:

`109× Concentrated Strategy → Staggered Re-Leveraging → 156× Best-Case Strategy`

The second approach improves the wealth multiple by approximately **47×**, equivalent to an improvement of about **43.1%** over the first approach.

## 2. Approach 1 — Concentrated Dynamic Programming (~109×)

The first optimization approach uses a relatively simple sequential strategy. At any point, the optimizer holds one concentrated position, exits the entire position, waits for settlement, and then reinvests the available capital into the next optimal opportunity.

`Capital → BUY → Hold → SELL → T+0.5 Settlement → Reinvest → Repeat`

For each trading cycle, the optimizer searches across the available securities and identifies the combination of BUY timing, SELL timing, and safe leveraged exposure that produces the highest final wealth while remaining above the maintenance-margin threshold.

Under the 4× margin tier, this process increases approximately **$10,000 to $1.09 million**, or about **109× initial wealth**.

### Why the result becomes so large

The result is driven by repeated leveraged compounding. The optimizer does not need a single asset to rise by 100×. Instead, it repeatedly captures strong market windows and reinvests the enlarged Equity into the next opportunity.

`Leverage → Profit → Higher Equity → Larger next position → More profit → Reinvestment`

The result compounds across multiple cycles until the account reaches approximately **109× initial wealth**.

### Main limitation

Once a position has been opened, the concentrated approach does not increase the position until the cycle is finished.

Suppose a profitable 4× position causes Equity to rise. The higher Equity creates additional borrowing capacity, but this extra capacity remains unused until the existing position is sold.

Therefore, the 109× strategy is strong but does not fully exploit the player's ability to re-leverage during a continuing upward trend.

## 3. Approach 2 — Staggered Re-Leveraging (~156×)

The second approach improves the strategy by allowing repeated BUYs during a profitable market window.

`BUY → Price rises → Equity rises → New margin capacity appears → BUY again → Price rises → Re-leverage again → Exit`

Instead of waiting until the position is fully closed, the optimizer can use the additional margin capacity created by unrealized profits.

For example:

| **Stage** | **Effect** |
|---|---|
| Initial BUY | Player uses available margin capacity |
| Asset price rises | Portfolio value and Equity increase |
| Equity increases | Margin capacity increases |
| Additional capacity becomes available | Optimizer can BUY more shares |
| Market continues rising | Larger position generates additional profit |
| Cycle exit | All accumulated gains are carried into the next cycle |

This creates a second layer of compounding: profits increase both **wealth** and the **ability to take additional exposure before the current trade ends**.

The richer strategy increases the best-case benchmark from approximately **109× to 156×**.

| **Metric** | **Result** |
|---|---:|
| Concentrated benchmark | 109× |
| Staggered re-leveraging benchmark | 156× |
| Additional wealth multiple | 47× |
| Relative improvement | **≈43.1%** |

The improvement is approximately:

`(156 / 109 − 1) × 100 ≈ 43.1%`

The key difference can therefore be summarized as:

| **109× Strategy** | **156× Strategy** |
|---|---|
| Profit is mainly reinvested after each completed cycle | Profit can create new buying capacity before the current cycle ends |
| One major entry per cycle | Multiple staggered entries |
| New margin capacity remains unused until exit | New margin capacity can be redeployed immediately |
| Sequential compounding | Sequential + intra-cycle compounding |

## 4. Why the Optimizer Results Matter for Game Difficulty

The optimization results are not intended to represent normal player performance. They provide an estimate of the upper performance range of Scenario 1 under highly effective trading.

This allows the player targets to be positioned below the best-case ceiling. These targets are **thresholds for final wealth**, not promises that a typical player will reach them. The same original trading rules and optimizer approaches are retained; only the Basic target has been updated from 2× to 3×.

The game uses three major performance targets (Small House / Normal House / ToLam Villa):

**3× → 20× → 100×**

Using the stronger **156× benchmark**, the relative difficulty levels are:

| **Player Target** | **Final Wealth from $10,000** | **Share of 156× Benchmark** | **Difficulty** |
|---:|---:|---:|---|
| **3× — Small House** | $30,000 | ≈1.92% | Basic |
| **20× — Normal House** | $200,000 | ≈12.82% | Intermediate |
| **100× — ToLam Villa** | $1,000,000 | ≈64.10% | Expert |
| **109×** | ≈$1.09 million | ≈69.9% | Concentrated optimizer benchmark |
| **156×** | ≈$1.56 million | 100% | Advanced optimization benchmark |

This creates the following performance ladder:

```text
$10,000 STARTING CAPITAL
        │
        ├── 3×   = $30,000       → Basic Target
        │
        ├── 20×  = $200,000      → Intermediate Target
        │
        ├── 100× = $1,000,000    → Expert Target
        │
        ├── 109× ≈ $1.09 million → Concentrated DP Benchmark
        │
        └── 156× ≈ $1.56 million → Staggered Re-Leveraging Benchmark

```

### How the 3× / 20× / 100× targets are calibrated

- **3× (Small House):** Requires final equity of at least $30,000, or a $20,000 gain above initial capital. At approximately 1.92% of the 156× benchmark wealth multiple, it is an introductory success threshold, but it is **not guaranteed** to be achievable without leverage under every market path or trading style.
- **20× (Normal House):** Requires at least $200,000 in final equity, or a $190,000 gain. At approximately 12.82% of the 156× benchmark wealth multiple, it represents a substantially more demanding goal requiring effective timing, compounding, and margin-risk management.
- **100× (ToLam Villa):** Requires at least $1,000,000 in final equity, or a $990,000 gain. At approximately 64.10% of the 156× benchmark wealth multiple, it is an aspirational challenge reserved for unusually effective, high-exposure strategies. The 109× concentrated benchmark is only approximately 9× above this target, illustrating the narrow buffer relative to that benchmark.

Target achievement can be checked with the same formula at each performance level:

`Target reached = (Final Equity / Initial Capital) >= Target Multiple`

With $10,000 starting equity, the corresponding final-equity thresholds are $30,000, $200,000 and $1,000,000. A target is considered reached only if the trading strategy also complies with the margin, settlement, and liquidation rules.

### Consistency and benchmark limitations

The quoted **109× and 156×** figures are retained from the supplied pre-existing optimization write-up; changing a target threshold does **not** change a strategy's realized final wealth. The current `best_case.py` uses **whole-share positions**, fixed **2×/3×/4×** margin tiers, **75-tick BUY and SELL settlement restrictions**, and a **20% maintenance-margin threshold** with a small survival buffer. Its actual tier-by-tier feasible results must be obtained by running the script on the same version of Scenario 1 before claiming the historical 109× or 156× figures are reproduced under those exact implementation settings.

In particular, the 156× reference is **not** a demonstrated guarantee of global optimality for the attached whole-share optimizer. It is a prior best-case calibration reference, not an expected player outcome or a probability of success. Scenario 2 should be calibrated separately if it is included in the final game.
