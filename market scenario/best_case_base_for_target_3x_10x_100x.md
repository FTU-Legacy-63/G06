# Free Fall 2.0 — Whole-Share Best-Case Base for 3× / 10× / 100× Targets

## 1. Purpose

This document records the latest best-case optimization benchmark for **Scenario 1** after rerunning `best_case.py` on the updated `market_scenario_1.csv`.

The current version changes the execution model in one important way:

```text
ALL BUY and SELL quantities must be whole shares.
Fractional shares are not allowed.
```

The optimizer therefore uses:

1. an **exact whole-share concentrated dynamic program** to establish sequential cycle boundaries; and
2. a **whole-share staggered re-leveraging MILP** inside each cycle.

The main purpose of this benchmark is to establish whether the game can support wealth targets of:

\[
3\times,\qquad 10\times,\qquad 100\times
\]

under the fixed 2×, 3×, and 4× margin products.

## 2. Executive Summary

The latest whole-share results are:

| Fixed Margin Tier | Whole-Share Concentrated DP | Whole-Share Staggered MILP | Final Equity | Improvement vs DP | Minimum Margin Ratio |
|---:|---:|---:|---:|---:|---:|
| 2× | 14.491090× | **15.532505×** | **$155,325.05** | +7.19% | 49.007278% |
| 3× | 42.454466× | **52.186422×** | **$521,864.22** | +22.92% | 31.968961% |
| 4× | 112.778919× | **156.632261×** | **$1,566,322.61** | +38.88% | 23.458050% |

The strongest feasible result in this run is the **4× fixed tier**:

\[
\boxed{\$10,000\rightarrow\$1,566,322.61}
\]

\[
\boxed{156.632261\times}
\]

Therefore the current validated whole-share lower bound is:

\[
\boxed{BestCase_{Scenario1,WholeShare}\ge 156.632261\times}
\]

This is a **feasible lower bound**, not a proof of the unrestricted global optimum.

## 3. Target Feasibility — 3× / 10× / 100×

The table below reports the **first completed optimization cycle** whose ending cumulative wealth is at or above each target. It does not claim that the target was first crossed exactly at that second inside the holding path.

| Tier | 3× Target | Completed at | Wealth | 10× Target | Completed at | Wealth | 100× Target | Completed at | Wealth |
|---:|:---|---:|---:|:---|---:|---:|:---|---:|---:|
| 2× | Cycle 4 | 628 | 3.025541× | Cycle 8 | 1500 | 12.715045× | Not reached | — | — |
| 3× | Cycle 4 | 628 | 4.833461× | Cycle 6 | 1067 | 12.812264× | Not reached | — | — |
| 4× | Cycle 3 | 452 | 3.962408× | Cycle 5 | 822 | 14.620668× | Cycle 9 | 1500 | 108.531636× |

Key calibration implication:

```text
2×  → reaches 3× and 10×, but not 100×
3×  → reaches 3× and 10×, but not 100×
4×  → reaches 3×, 10×, and 100×
```

For the current Scenario 1 path, the **100× target is achievable only in the 4× benchmark** among the three fixed tiers tested.

## 4. Scenario and Solver Assumptions

| Parameter | Value |
|---|---:|
| Input file | `market_scenario_1.csv` |
| Initial Capital | $10,000 |
| Securities | 50 |
| Total Ticks | 1,800 |
| Large Phases | 6 |
| Phase Duration | 300 seconds |
| Price Conversion | Raw Price / 1400 |
| T+0.5 Settlement Delay | 75 seconds |
| Fixed Margin Products | 2×, 3×, 4× |
| Maintenance Trigger | ≤20.000% |
| Numerical Survival Floor | ≥20.001% |
| Share Rule | **Whole shares only** |
| Short Selling | Not allowed |
| Transaction Costs | 0 |
| Slippage | 0 |
| Execution Liquidity | Unlimited at displayed price |
| Forecasting | Perfect foresight |
| MILP Time Limit | 60 seconds per cycle |
| MILP Target Relative Gap | 0.100% |

Displayed game price is:

\[
P_{game}=\frac{P_{raw}}{1400}
\]

## 5. Whole-Share Rule

The key execution constraint is now:

\[
q_{\tau,i}\in\mathbb{Z}_{\ge 0}
\]

where `q` is the number of shares purchased at BUY second `τ` for ticker `i`.

For every allocation:

\[
BUY\ Notional=q_{\tau,i}\times P_{\tau,i}
\]

\[
SELL\ Value=q_{\tau,i}\times P_{sell,i}
\]

The generated allocation output was checked directly:

- Integer BUY quantities: **PASS**
- Integer SELL quantities: **PASS**
- Whole-share rule overall: **PASS**

This removes the earlier inconsistency in which a BUY notional could be smaller than the price of one share while still representing a positive position.

## 6. Fixed Margin Products

The player does not choose arbitrary leverage. The only available margin tiers are:

\[
2\times,\qquad3\times,\qquad4\times
\]

| Margin Tier | Initial Margin |
|---:|---:|
| 2× | 50.000% |
| 3× | 33.333% |
| 4× | 25.000% |

For fixed tier `L`:

\[
Initial\ Margin=\frac{1}{L}
\]

The fixed tier constrains new buying power. Effective leverage can drift after prices move, provided the account remains above the maintenance threshold.

## 7. Optimization Architecture

### Stage 1 — Exact Whole-Share Concentrated DP

The first stage searches sequential concentrated trades using integer share quantities:

```text
settled cash
→ BUY one ticker in whole shares
→ hold
→ SELL the full position
→ wait 75 seconds for settlement before reusing the cash
→ next cycle
```

The DP determines the baseline route and cycle boundaries for each fixed tier.

### Stage 2 — Whole-Share Staggered Re-Leveraging MILP

Within each inherited cycle, the MILP may:

- BUY at multiple seconds;
- BUY repeatedly as equity increases;
- allocate to more than one ticker;
- use only integer share quantities;
- check fixed-tier buying power while additional BUYs are still permitted;
- check maintenance margin every second;
- hold every purchased lot until the common cycle SELL second.

The final eligible BUY second is:

\[
LastBuy=Sell-75
\]

so every new lot satisfies the encoded 75-second holding/settlement timing requirement before the common cycle exit.

## 8. Whole-Share MILP Formulation

For cycle-start equity `E₀`, integer quantity `q_{τ,i}`, BUY price `P_{τ,i}`, and current price `P_{u,i}`:

### Gross Portfolio Value

\[
G_u=\sum_{\tau\le u}\sum_i q_{\tau,i}P_{u,i}
\]

### Equity

\[
E_u=E_0+\sum_{\tau\le u}\sum_i q_{\tau,i}(P_{u,i}-P_{\tau,i})
\]

### Fixed-Tier Buying Power

While more BUYs are allowed:

\[
G_u\le L E_u
\]

### Maintenance Margin

Using the numerical survival floor `m = 20.001%`:

\[
E_u\ge mG_u
\]

### Objective

All lots are sold at the common SELL second, so the MILP maximizes:

\[
E_{sell}=E_0+\sum_{\tau,i}q_{\tau,i}(P_{sell,i}-P_{\tau,i})
\]

Because `q` is integer, this is now a **mixed-integer linear optimization problem**, not the continuous LP used by the earlier fractional-share version.

## 9. Concentrated Whole-Share DP Baselines

| Tier | DP Final Equity | DP Wealth | DP Cycles |
|---:|---:|---:|---:|
| 2× | $144,910.90 | 14.491090× | 9 |
| 3× | $424,544.66 | 42.454466× | 9 |
| 4× | $1,127,789.19 | 112.778919× | 10 |

These baselines are already whole-share benchmarks. The staggered MILP must reproduce or improve on the corresponding DP path.

## 10. Final Whole-Share Tier Comparison

| Tier | DP Wealth | Staggered Wealth | Final Equity | Improvement | Total BUY Orders | Cycles | Minimum MR | All Cycles Proven Optimal? | Worst Cycle Gap |
|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---:|
| 2× | 14.491090× | **15.532505×** | $155,325.05 | +7.19% | 82 | 9 | 49.007278% | No | 1.741362% |
| 3× | 42.454466× | **52.186422×** | $521,864.22 | +22.92% | 113 | 9 | 31.968961% | No | 0.430482% |
| 4× | 112.778919× | **156.632261×** | $1,566,322.61 | +38.88% | 102 | 10 | 23.458050% | No | 0.117075% |

## 11. Detailed 2× Results

Whole-share concentrated benchmark: **14.491090×** = **$144,910.90**.

Whole-share staggered result: **15.532505×** = **$155,325.05**.

Improvement: **+7.19%**.

| Cycle | Start | Sell | BUY Orders | Assets | Cycle Growth | Ending Equity | Cumulative Wealth | Min MR | Max Effective Lev. | Proven Optimal? | MIP Gap |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---:|
| 1 | 27 | 112 | 5 | 1 | 1.301134× | $13,011.34 | 1.301134× | 49.0073% | 2.0405× | Yes | 0.096634% |
| 2 | 193 | 268 | 3 | 3 | 1.269738× | $16,520.99 | 1.652099× | 49.9206% | 2.0032× | Yes | 0.009985% |
| 3 | 345 | 452 | 10 | 4 | 1.280442× | $21,154.17 | 2.115417× | 49.9467% | 2.0021× | Yes | 0.036445% |
| 4 | 551 | 628 | 4 | 2 | 1.430234× | $30,255.41 | 3.025541× | 50.0141% | 1.9994× | Yes | 0.004027% |
| 5 | 703 | 860 | 20 | 4 | 1.404892× | $42,505.58 | 4.250558× | 49.8318% | 2.0068× | Yes | 0.099897% |
| 6 | 992 | 1067 | 1 | 1 | 1.381395× | $58,717.01 | 5.871701× | 50.0417% | 1.9983× | Yes | 0.051436% |
| 7 | 1142 | 1220 | 4 | 2 | 1.273683× | $74,786.88 | 7.478688× | 50.0104% | 1.9996× | Yes | 0.026213% |
| 8 | 1304 | 1500 | 34 | 2 | 1.700171× | $127,150.45 | 12.715045× | 50.0021% | 1.9999× | **No** | 1.741362% |
| 9 | 1650 | 1725 | 1 | 1 | 1.221585× | $155,325.05 | 15.532505× | 50.0029% | 1.9999× | Yes | 0.001177% |

## 12. Detailed 3× Results

Whole-share concentrated benchmark: **42.454466×** = **$424,544.66**.

Whole-share staggered result: **52.186422×** = **$521,864.22**.

Improvement: **+22.92%**.

| Cycle | Start | Sell | BUY Orders | Assets | Cycle Growth | Ending Equity | Cumulative Wealth | Min MR | Max Effective Lev. | Proven Optimal? | MIP Gap |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---:|
| 1 | 27 | 112 | 6 | 1 | 1.454601× | $14,546.01 | 1.454601× | 31.9690% | 3.1280× | Yes | 0.072271% |
| 2 | 193 | 268 | 2 | 2 | 1.405290× | $20,441.36 | 2.044136× | 33.2306% | 3.0093× | Yes | 0.056421% |
| 3 | 345 | 452 | 19 | 3 | 1.434198× | $29,316.96 | 2.931696× | 33.2623% | 3.0064× | **No** | 0.156036% |
| 4 | 551 | 628 | 4 | 2 | 1.648691× | $48,334.61 | 4.833461× | 33.3367% | 2.9997× | Yes | 0.019262% |
| 5 | 703 | 860 | 27 | 3 | 1.686097× | $81,496.84 | 8.149684× | 33.1768% | 3.0142× | Yes | 0.067343% |
| 6 | 992 | 1067 | 1 | 1 | 1.572118× | $128,122.64 | 12.812264× | 33.3597% | 2.9976× | Yes | 0.048760% |
| 7 | 1142 | 1220 | 5 | 2 | 1.414857× | $181,275.20 | 18.127520× | 33.3345% | 2.9999× | Yes | 0.004075% |
| 8 | 1304 | 1500 | 48 | 2 | 2.160663× | $391,674.67 | 39.167467× | 33.3338% | 3.0000× | **No** | 0.430482% |
| 9 | 1650 | 1725 | 1 | 1 | 1.332392× | $521,864.22 | 52.186422× | 33.3337% | 3.0000× | Yes | 0.000252% |

## 13. Detailed 4× Results

Whole-share concentrated benchmark: **112.778919×** = **$1,127,789.19**.

Whole-share staggered result: **156.632261×** = **$1,566,322.61**.

Improvement: **+38.88%**.

| Cycle | Start | Sell | BUY Orders | Assets | Cycle Growth | Ending Equity | Cumulative Wealth | Min MR | Max Effective Lev. | Proven Optimal? | MIP Gap |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---:|
| 1 | 27 | 112 | 6 | 1 | 1.609820× | $16,098.20 | 1.609820× | 23.4581% | 4.2629× | Yes | 0.080432% |
| 2 | 193 | 268 | 2 | 2 | 1.540643× | $24,801.59 | 2.480159× | 24.8529% | 4.0237× | Yes | 0.006521% |
| 3 | 345 | 452 | 21 | 2 | 1.597643× | $39,624.08 | 3.962408× | 24.9216% | 4.0126× | **No** | 0.117075% |
| 4 | 551 | 667 | 32 | 2 | 2.197136× | $87,059.48 | 8.705948× | 24.8683% | 4.0212× | Yes | 0.032885% |
| 5 | 747 | 822 | 1 | 1 | 1.679388× | $146,206.68 | 14.620668× | 25.0004% | 3.9999× | Yes | 0.000734% |
| 6 | 914 | 989 | 2 | 2 | 1.479895× | $216,370.51 | 21.637051× | 24.1945% | 4.1332× | Yes | 0.001135% |
| 7 | 1067 | 1156 | 4 | 2 | 1.438768× | $311,307.01 | 31.130701× | 25.0026% | 3.9996× | Yes | 0.012317% |
| 8 | 1231 | 1306 | 1 | 1 | 1.443471× | $449,362.65 | 44.936265× | 23.5214% | 4.2515× | Yes | 0.000001% |
| 9 | 1381 | 1500 | 32 | 2 | 2.415235× | $1,085,316.36 | 108.531636× | 25.0027% | 3.9996× | Yes | 0.086982% |
| 10 | 1650 | 1725 | 1 | 1 | 1.443195× | $1,566,322.61 | 156.632261× | 25.0000% | 4.0000× | Yes | 0.000014% |

## 14. Solver Optimality and Interpretation

The result is always usable as a feasible benchmark when the MILP returns a feasible incumbent, even if the solver reaches its 60-second cycle limit.

The following cycles were **not proven optimal**:

| Tier | Cycle | Returned Wealth at Cycle End | Relative MIP Gap | Status |
|---:|---:|---:|---:|:---|
| 2× | 8 | 12.715045× | 1.741362% | Time limit reached |
| 3× | 3 | 2.931696× | 0.156036% | Time limit reached |
| 3× | 8 | 39.167467× | 0.430482% | Time limit reached |
| 4× | 3 | 3.962408× | 0.117075% | Time limit reached |

For the **best 4× tier**, only Cycle 3 was not proven optimal, with a remaining MIP gap of:

\[
0.117075\%
\]

Therefore `156.632261×` is a validated feasible 4× result; the true optimum within the same whole-share cycle formulation may be slightly higher.

## 15. Margin Safety

| Tier | Minimum Observed Margin Ratio | Maintenance Trigger | Result |
|---:|---:|---:|:---:|
| 2× | 49.007278% | 20.000% | **PASS** |
| 3× | 31.968961% | 20.000% | **PASS** |
| 4× | 23.458050% | 20.000% | **PASS** |

All three benchmark paths remain above the encoded maintenance trigger throughout their audited cycle paths.

Thus, under the model assumptions:

```text
Margin Calls:        0
Forced Liquidations: 0
```

## 16. Why Effective Leverage Can Exceed the Fixed Tier

The audit can show effective leverage temporarily above the nominal 2× / 3× / 4× product after prices move.

This does not mean the player selected a new leverage product.

The code enforces:

```text
Gross Portfolio <= Tier × Equity
```

while additional BUYs are still allowed, and independently enforces the maintenance-margin floor at every second.

After a price decline, effective leverage can rise above the original tier even though no additional BUY has been made. Survival is then determined by maintenance margin.

## 17. What Changed From the Earlier Fractional-Share Benchmark

The earlier benchmark used continuous/fractional positions. The current run instead requires integer quantities throughout both the concentrated DP and staggered optimizer.

The current best result is:

\[
\boxed{156.632261\times}
\]

rather than the earlier fractional-share benchmark of:

\[
180.163526\times
\]

The newer value should be used for the current game implementation because:

1. the game permits **whole shares only**; and
2. this run uses the updated `market_scenario_1.csv`.

The old 180.163526× value remains useful only as a historical fractional-share benchmark under the earlier scenario/model configuration.

## 18. Where the 4× Benchmark Builds Wealth

The 4× route compounds through 10 sequential cycles.

Important milestones are:

- **Cycle 3**, sell second 452: 3.962408× = $39,624.08.
- **Cycle 5**, sell second 822: 14.620668× = $146,206.68.
- **Cycle 9**, sell second 1500: 108.531636× = $1,085,316.36.
- **Cycle 10**, sell second 1725: 156.632261× = $1,566,322.61.

The 100× threshold is first exceeded at the end of **Cycle 9**:

\[
108.531636\times
\]

and the final Cycle 10 raises the account to:

\[
\boxed{156.632261\times}
\]

## 19. Current Model Capabilities

The current engine supports:

- fixed 2× / 3× / 4× margin products;
- whole-share quantities only;
- repeated staggered BUYs inside a cycle;
- multiple tickers inside one cycle;
- re-leveraging as equity increases;
- all 50 securities;
- per-second maintenance-margin checks;
- 75-second timing constraint;
- common cycle exit;
- long-only allocation;
- perfect foresight.

## 20. Current Model Limitations

The current whole-share MILP still does **not** model the completely unrestricted trading problem.

### Common SELL Time

Every lot inside a cycle is held until the same cycle SELL second.

### No Partial SELLs Inside a Cycle

The engine cannot yet perform:

```text
BUY A
BUY B
SELL part of A
reuse the settled proceeds
BUY C
keep the remainder of A
```

### Cycle Boundaries Come From the Concentrated DP

The staggered MILP improves allocation inside those boundaries but does not globally redesign all cycle start/end times after staggered re-leveraging is introduced.

### No Overlapping Sequential Cycles

One cycle is completed and settlement logic is respected before the next DP cycle becomes available.

Therefore:

\[
GlobalBest\ge 156.632261\times
\]

but the unrestricted global optimum has not been proven.

## 21. Regression Benchmarks for Future Code

Any future optimizer using the **same updated Scenario 1 data and the same whole-share assumptions** should reproduce or exceed:

| Tier | Current Feasible Benchmark |
|---:|---:|
| 2× | **15.532505×** |
| 3× | **52.186422×** |
| 4× | **156.632261×** |

A lower result does not automatically prove a bug if the assumptions or solver time budget have changed, but under identical settings these values should be treated as the current regression incumbents.

## 22. Generated Output Files

The run generated:

```text
whole_share_srlp_output.xlsx
whole_share_srlp_summary.csv
whole_share_srlp_cycles.csv
whole_share_srlp_buy_allocations.csv
whole_share_srlp_margin_audit.csv
```

### `whole_share_srlp_output.xlsx`

Combined workbook containing Market Scenario, Summary, Cycles, BUY Allocations, and Margin Audit.

### `whole_share_srlp_summary.csv`

Final comparison across the 2×, 3×, and 4× fixed tiers.

### `whole_share_srlp_cycles.csv`

Cycle-level outputs including start/sell seconds, integer baseline quantity, order count, asset count, cycle growth, ending equity, margin ratio, effective leverage, MIP gap, and solver status.

### `whole_share_srlp_buy_allocations.csv`

Every non-zero whole-share BUY and corresponding common-cycle SELL quantity.

### `whole_share_srlp_margin_audit.csv`

Second-by-second Equity, Gross Portfolio, Effective Leverage, Margin Ratio, and whether additional BUYs remain allowed.

## 23. Final Conclusion

The latest run establishes the following feasible whole-share best-case benchmarks:

\[
2\times:\quad \$10,000\rightarrow\$155,325.05
\]

\[
15.532505\times
\]

\[
3\times:\quad \$10,000\rightarrow\$521,864.22
\]

\[
52.186422\times
\]

\[
4\times:\quad \$10,000\rightarrow\$1,566,322.61
\]

\[
156.632261\times
\]

The strongest current route is the **4× fixed-margin whole-share strategy**:

\[
\boxed{\$10,000\rightarrow\$1,566,322.61}
\]

\[
\boxed{156.632261\times}
\]

This result:

```text
uses whole shares only
uses fixed 4× margin
uses staggered BUYs and re-leveraging
respects the encoded 20.001% survival floor
reaches the 100× target by the end of Cycle 9
finishes at 156.632261×
contains one 4× cycle that was feasible but not proven optimal within the 60-second time limit
```

Accordingly, the current benchmark should be stated as:

\[
\boxed{BestCase_{Scenario1,WholeShare}\ge 156.632261\times}
\]

not as a proof that the unrestricted global optimum equals that value.
