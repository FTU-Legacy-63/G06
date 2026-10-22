# Best-Case Optimization and Player Difficulty Calibration

## 1. Overview

Two optimization approaches were applied separately to **both market scenarios** to measure the wealth attainable under deterministic, fully known price paths and the optimizer's trading constraints. The concentrated Dynamic Programming (DP) approach establishes a sequential benchmark; staggered re-leveraging uses Mixed-Integer Linear Programming (MILP) to improve each selected trading cycle by allocating additional whole-share BUY orders as margin capacity develops.

| Feature | Approach 1 — Concentrated Dynamic Programming | Approach 2 — Staggered Re-Leveraging MILP |
|---|---|---|
| Core idea | Search for a high-value sequence of one-position trading cycles | Optimize multiple BUY allocations within the DP-selected cycles |
| Trading structure | BUY → Hold → SELL → Settlement → Reinvest | BUY → Unrealized gain → Additional BUY(s) → Common SELL → Settlement |
| Position structure | One concentrated asset position per cycle | Several integer-share purchase lots, potentially across different assets |
| Use of new margin capacity within a cycle | No | Yes, subject to buying-power and margin constraints |
| Compounding | Between completed cycles | Between cycles and through additional intra-cycle exposure |
| Limitation | Optimality refers to the specified sequential DP model | MILP solves fixed cycles; the complete multi-cycle route is **not** proved globally optimal |


All wealth multiples are calculated as `Final Equity / $10,000`.

| Scenario | Fixed leverage tier | Concentrated DP wealth | Staggered MILP wealth | Staggered final equity | Improvement vs. DP |
|---|---:|---:|---:|---:|---:|
| **Scenario 1** | 2× | 25.007857× | **31.534604×** | **$315,346.04** | 26.10% |
| **Scenario 1** | 3× | 85.517668× | **156.869452×** | **$1,568,694.52** | 83.44% |
| **Scenario 1** | 4× | 257.709480× | **491.696973×** | **$4,916,969.73** | 90.80% |
| **Scenario 2** | 2× | 103.427759× | **137.817680×** | **$1,378,176.80** | 33.25% |
| **Scenario 2** | 3× | 545.345477× | **1,127.322099×** | **$11,273,220.99** | 106.72% |
| **Scenario 2** | 4× | 2,249.165859× | **5,990.443600×** | **$59,904,436.00** | 166.34% |

**Interpretation:** Scenario 2 provides substantially greater exploitable upside to a perfect-foresight optimizer than Scenario 1 at all three leverage tiers. This is evidence of different *model-based opportunity sets*, not proof that ordinary players will find Scenario 2 easier.

## 2. Data and Financial Assumptions

Both inputs passed the script's pre-optimization dataset checks.

| Rule or assumption | Setting in the completed run |
|---|---|
| Datasets | `market_scenario_1.csv` and `market_scenario_2.csv`, corrected versions |
| Market size | 1,800 global ticks, 50 assets, six 300-tick phases per scenario |
| Data continuity | AM closing tick equals PM opening tick; the adjacent phase-boundary prices are continuous |
| Price limits | Each asset remains within 70%–130% of its **starting price for the full 300-tick phase** |
| Starting equity | $10,000 |
| Price conversion | Raw price / 1,400 for optimizer USD valuation |
| Position quantities | Whole shares only; long positions |
| Fixed leverage tiers | 2×, 3×, and 4× (evaluated separately) |
| Maintenance-margin trigger | Margin ratio ≤20% |
| Optimizer survival threshold | Margin ratio ≥20.001% (20% plus 0.001 percentage point buffer) |
| Settlement assumption | 75 ticks for BUY eligibility and 75 ticks after SELL before capital is reused |
| MILP time limit | 60 seconds per cycle |
| MILP relative-gap target | 0.1% |
| Property targets | Small House 3×; Normal House 20×; ToLam Villa 100× |

**Model scope:** The reported optimizer evaluates mark-to-market equity and margin constraints along known market paths. It does **not** demonstrate typical human performance or incorporate uncertainty about future prices. Transaction costs, market impact, order-book liquidity, and the game's separate bank-savings accrual are not explicitly modeled in this optimizer. The 75-tick settlement parameter also needs to be reconciled with the running game engine if it uses a different value.

## 3. Approach 1 — Concentrated Dynamic Programming

The DP model searches for a sequence of profitable cycles while using a single concentrated position at any one time:

`Available equity → BUY whole shares → Hold → SELL → Wait for settlement → Reinvest`

It searches over candidate assets and BUY/SELL ticks, subject to initial buying power, maintenance survival along the holding path, and settlement timing. The account's enlarged equity is available to fund subsequent cycles after the relevant waiting period.

### Corrected-dataset DP results

| Scenario | 2× DP | 3× DP | 4× DP |
|---|---:|---:|---:|
| Scenario 1 | 25.007857× | 85.517668× | **257.709480×** |
| Scenario 2 | 103.427759× | 545.345477× | **2,249.165859×** |

The large terminal values arise from **repeated leveraged compounding across well-timed trading windows**. No individual share needs to appreciate by the reported final wealth multiple.

**Main limitation:** A concentrated position does not add shares when unrealized gains increase buying power during the same trading cycle. The sequential DP optimum is specific to this restricted trading structure; it is not an upper bound on all permissible trading strategies.

## 4. Approach 2 — Whole-Share Staggered Re-Leveraging MILP

Staggered optimization improves the allocation within each BUY-to-SELL window selected by the DP route:

`Initial BUY → Price appreciation → More available margin capacity → Additional whole-share BUYs → Common SELL → Settlement`

Within a fixed cycle, MILP chooses the timing, asset and integer quantity of additional purchases. The program enforces a maximum fixed-tier exposure while additional BUYs are possible and checks the survival margin ratio at every tick through the cycle exit.

### Actual staggered results

| Scenario | 2× staggered | 3× staggered | 4× staggered |
|---|---:|---:|---:|
| Scenario 1 | 31.534604× | 156.869452× | **491.696973×** |
| Scenario 2 | 137.817680× | 1,127.322099× | **5,990.443600×** |

Relative improvement is calculated as:

`Improvement (%) = (Staggered Wealth Multiple / DP Wealth Multiple − 1) × 100`

For example, Scenario 1 at 3× produces `(156.869452 / 85.517668 − 1) × 100 ≈ 83.44%` improvement over its concentrated DP baseline. Scenario 2 at 4× produces approximately **166.34%** improvement.

### Solver status and margin safety

| Scenario | Tier | DP trading cycles | Lowest reported margin ratio | All fixed-cycle MILPs met configured optimality status? | Worst relative gap |
|---|---:|---:|---:|---|---:|
| Scenario 1 | 2× | 9 | 48.467234% | **No** | **0.195264%** |
| Scenario 1 | 3× | 9 | 31.289628% | Yes | ~0.0999% |
| Scenario 1 | 4× | 10 | 22.700828% | Yes | ~0.0804% |
| Scenario 2 | 2× | 10 | 49.383953% | Yes | ~0.1000% |
| Scenario 2 | 3× | 10 | 32.509702% | Yes | ~0.1000% |
| Scenario 2 | 4× | 11 | 24.073384% | Yes | ~0.0901% |

**Important solver qualification:** Scenario 1 at 2× has one time-limited cycle (Cycle 5), with a reported **0.195264%** MIP gap above the 0.1% target. Its computed portfolio is a feasible incumbent, but that cycle was **not certified optimal** at the configured gap. The `MILP_Proven_Optimal=True` flag for other cycles means the solver met its configured termination criteria; it does **not** establish an exact zero-gap solution or global optimality of the full trading sequence.

The lowest reported margin ratios exceed the optimizer's 20.001% survival floor. This validates the reported paths under the model's constraints, not their resilience to an unexpected price path or different execution assumptions.

## 5. Property Targets — 3× / 20× / 100×

The game's three property goals are fixed final-equity thresholds:

| Property target | Required wealth multiple | Required final equity | Gain above starting equity | Intended design label |
|---|---:|---:|---:|---|
| Small House | **3×** | **$30,000** | $20,000 | Basic |
| Normal House | **20×** | **$200,000** | $190,000 | Intermediate |
| ToLam Villa | **100×** | **$1,000,000** | $990,000 | Expert |

The check is:

`Target reached = (Final Equity / Initial Capital) ≥ Target Multiple`

### Target attainment by scenario and leverage tier

| Scenario | Tier | 3× Small House | 20× Normal House | 100× ToLam Villa |
|---|---:|---|---|---|
| Scenario 1 | 2× | PASS | PASS | **BELOW** |
| Scenario 1 | 3× | PASS | PASS | PASS |
| Scenario 1 | 4× | PASS | PASS | PASS |
| Scenario 2 | 2× | PASS | PASS | PASS |
| Scenario 2 | 3× | PASS | PASS | PASS |
| Scenario 2 | 4× | PASS | PASS | PASS |

**Scenario 1, 2× exception:** The staggered portfolio finishes at **31.534604×** ($315,346.04), below the 100× target ($1,000,000). Its shortfall is **$684,653.96**. This is a failure of the **computed strategy to reach 100×**, not proof that no alternative 2× strategy could ever reach it.

### Robustness across the two scenarios

A target is marked as achieved in **both** scenarios for a given leverage tier only when the computed staggered strategy passes that target separately in Scenario 1 and Scenario 2.

| Leverage tier | 3× across both | 20× across both | 100× across both |
|---|---|---|---|
| 2× | PASS | PASS | **BELOW** |
| 3× | PASS | PASS | PASS |
| 4× | PASS | PASS | PASS |

This two-scenario test strengthens the **attainability evidence** for the selected optimizer strategies. It does not measure the probability of success for a player and should not be called a real-world robustness or solvability proof.

## 6. Implications for Player Difficulty

The corrected results suggest the property-target thresholds are attainable by sufficiently well-timed, leveraged strategies in the tested scenarios, with one observed exception for the 2× strategy in Scenario 1 at 100×. However, **best-case optimizer attainability is not equivalent to player difficulty**:

- **3× (Small House):** Attained in all six optimizer runs; provides the lowest property threshold. This does not establish its completion rate without leverage.
- **20× (Normal House):** Also attained in all six runs, but requires considerably more compounding than 3×.
- **100× (ToLam Villa):** Attained in five of six computed staggered runs; only 2× in Scenario 1 remains below it. Reaching 100× demands sustained gains and carefully managed leverage under the evaluated routes.

Scenario 2's materially higher optimizer outcomes may justify further scenario-balancing or player testing, but the direction and size of any difficulty adjustment should be determined using gameplay trials (player choices, available information, liquidations and completion rates), **not by rescaling targets from perfect-foresight multiples alone**.

## 7. Interpretation Boundaries and Outstanding QA

1. **No global-optimality claim.** The DP and within-cycle MILPs solve different restricted optimization problems; the full staggered sequence is conditioned on DP-selected cycle boundaries.
2. **Solver certification is conditional.** The Scenario 1, 2× run has a 0.195264% gap in one cycle. Other per-cycle results terminate within their configured tolerances, not necessarily at mathematical exact optimality.
3. **Full foresight.** The optimization assumes knowledge of the entire future price path, unlike a human trader.
4. **Model–engine alignment.** Confirm that the game engine and optimizer use the same settlement restrictions, share rounding, savings treatment, leverage timing, liquidation trigger and effective prices before treating these as reproducible gameplay bounds.
5. **Dataset QA scope.** Both corrected CSVs passed the script's continuity and full-phase ±30% checks. Those tests do not independently establish plausible market behavior or every gameplay rule.
6. **Trading frictions.** Fees, slippage, position-level liquidity limitations and other real-market frictions are not represented; therefore the simulated results can be substantially above plausible execution outcomes.

## 8. Reproducibility and Evidence Files

The file `analysis/best_case.py` runs the corrected Scenario 1 and Scenario 2 separately and produces per-scenario outputs plus combined cross-scenario comparisons. From this document's location in `analysis/`, the following are the **default output paths created by the script** (check that the generated files have been committed before publishing these links):

| Evidence | Location relative to `analysis/` | Purpose |
|---|---|---|
| Optimizer source | [`best_case.py`](../../analysis/best_case.py) | Dual-scenario runner, DP, MILP, calibration and output merging |
| Scenario 1 detailed results | [`analysis/scenario_1/`](../../analysis/output/scenario_1/) | Summary, trading cycles, BUY allocations, margin audit, workbook, calibration and run log |
| Scenario 2 detailed results | [`analysis/scenario_2/`](../../analysis/output/scenario_2/) | Equivalent results for the second market path |
| Combined summary | [`analysis/whole_share_srlp_summary.csv`](../../analysis/output/whole_share_srlp_summary.csv) | Six scenario-by-tier rows |
| Combined cycles | [`analysis/whole_share_srlp_cycles.csv`](../../analysis/output/whole_share_srlp_cycles.csv) | Trading-cycle evidence for both scenarios |
| Combined BUY allocations | [`analysis/whole_share_srlp_buy_allocations.csv`](../../analysis/output/whole_share_srlp_buy_allocations.csv) | Whole-share purchase decisions |
| Combined margin audit | [`analysis/whole_share_srlp_margin_audit.csv`](../../analysis/output/whole_share_srlp_margin_audit.csv) | Tick-by-tick account and margin verification |
| Combined target calibration | [`analysis/target_calibration_3x_20x_100x.csv`](../../analysis/output/target_calibration_3x_20x_100x.csv) | Six tiers × three targets |
| Cross-scenario tier comparison | [`analysis/scenario_tier_comparison.csv`](../../analysis/output/scenario_tier_comparison.csv) | Side-by-side leverage outcomes and attainment flags |
| Cross-scenario robustness | [`analysis/target_robustness_both_scenarios.csv`](../../analysis/output/target_robustness_both_scenarios.csv) | Whether each target passes in both scenarios |

### Final calibration statement

Under the tested whole-share, fixed-tier, 75-tick settlement, 20% maintenance-margin **perfect-foresight** model, the computed staggered wealth multiples range from **31.534604×** (Scenario 1, 2×) to **5,990.443600×** (Scenario 2, 4×). The 3× and 20× property targets are achieved by all six tested strategies; 100× is achieved by five. These are **optimizer-derived attainable outcomes**, not predicted player success rates or proven global upper bounds.
