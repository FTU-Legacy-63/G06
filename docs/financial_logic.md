# Financial Logic and Mechanics

This document specifies the accounting formulas, margin rules, risk thresholds, settlement mechanics, and benchmark targets implemented in `src/simulation_engine.py`.

---

## 1. Core Accounting Identities

The engine separates liquid trading capital from safe haven bank deposits to ensure risk isolation:

| Variable | Mathematical Definition | Purpose |
|---|---|---|
| **Liquid Cash** | $C_t$ | Free cash available for order margin or withdrawal. |
| **Gross Exposure** | $E_t = \sum (S_{i,t} \times P_{i,t})$ | Current market value of all held stock positions. |
| **Margin Debt** | $D_t$ | Principal borrowed from the broker to fund leveraged purchases. |
| **Trading Equity** | $TE_t = C_t + E_t - D_t$ | Broker-custodied equity available as margin collateral. |
| **Bank Savings** | $B_t$ | Risk-free deposits held outside the brokerage custody. |
| **Total Net Worth** | $NW_t = TE_t + B_t$ | Comprehensive player wealth. |
| **Effective Leverage** | $L_t = \frac{E_t}{TE_t}$ | Current ratio of stock exposure to trading equity. |
| **Margin Ratio** | $MR_t = \frac{TE_t}{E_t} = \frac{1}{L_t}$ | Primary solvency metric monitored by the broker. |

*Note on Bank Savings Isolation:* To reflect prudent risk management and prevent artificial inflation of collateral (verified in Test `test_bank_savings_isolated_from_margin_collateral`), Bank Savings are excluded from $TE_t$ during margin ratio calculations. Bank savings remain 100% immune to forced liquidation sales.

---

## 2. Order Mechanics and Leverage Tiers

When a player places a BUY order with margin enabled:
$$\text{Order Cost} = \text{Shares} \times \text{Current Price}$$
$$\text{Required Cash} = \frac{\text{Order Cost}}{\text{Margin Multiplier}}$$
$$\text{New Margin Debt} = \text{Order Cost} - \text{Required Cash}$$

Orders are validated against three criteria:
1. Available cash must cover Required Cash ($\text{Required Cash} \le C_t$).
2. For SELL orders, the player must hold sufficient available shares ($S_{i,t} \ge \text{Shares to Sell}$). Short selling is disabled.
3. Order quantity must be positive ($\text{Shares} > 0$).

### Margin Tier Specifications
| Margin Tier | Purchasing Power | Max Borrowing Ratio | Initial Margin Ratio | Price Drop to 20% Margin Call | Theoretical Wipeout Move |
|---|---|---|---|---|---|
| **Cash 1.0×** | 1.0× | 0.0× | 100.0% | N/A (Immune) | −100.0% |
| **Margin 2.0×** | 2.0× | 1.0× | 50.0% | **−37.50%** | −50.00% |
| **Margin 3.0×** | 3.0× | 2.0× | 33.33% | **−16.67%** | −33.33% |
| **Margin 4.0×** | 4.0× | 3.0× | 25.00% | **−6.25%** | −25.00% |

The single-stock price triggering a margin call ($P_{call}$) is derived directly from the maintenance margin requirement ($MMR = 0.20$):
$$P_{call} = \frac{D_t}{\text{Shares} \times (1 - MMR)} = \frac{D_t}{0.80 \times \text{Shares}}$$

---

## 3. Risk States and Forced Liquidation Rules

| Risk State | Trigger Condition | System Action |
|---|---|---|
| **HEALTHY** | Margin Debt = 0, or Margin Ratio $\ge 25.00\%$ | Normal trading; status indicator green. |
| **WARNING** | $20.00\% \le \text{Margin Ratio} < 25.00\%$ | Amber warning alert; prompts voluntary de-risking or asset sales. |
| **MARGIN CALL** | $\text{Margin Ratio} < 20.00\%$ or Leverage $\ge 5.0\times$ | Red alert; automated forced liquidation triggered immediately. |
| **LIQUIDATED** | Post-liquidation status | Positions cleared, debt settled, trading disabled. |

### Forced Liquidation Execution & Penalty
When a margin call triggers:
1. **Fire-Sale:** 100% of open equity holdings are sold immediately at the current tick price:
   $$\text{Gross Proceeds} = \sum (\text{Shares}_i \times \text{Current Price}_i)$$
2. **Liquidation Penalty Fee:** A **5.0% penalty fee** is assessed on gross sales to simulate real-world auction slippage and exchange penalty fees:
   $$\text{Penalty} = 0.05 \times \text{Gross Proceeds}$$
   $$\text{Net Proceeds} = \text{Gross Proceeds} - \text{Penalty}$$
3. **Debt Repayment:** Net proceeds repay outstanding margin debt:
   $$\text{Final Cash} = C_t + \max(0, \text{Net Proceeds} - D_t)$$
   $$\text{Uncovered Debt} = \max(0, D_t - \text{Net Proceeds})$$
4. **Lockout:** If final net worth $\le 0$, the session terminates in a *Wipeout*. Trading is locked to prevent state corruption.

---

## 4. Settlement Mechanics and Bank Yield

### T+0.5 Settlement Delay (Holding Pen)
To model clearing friction and prevent intraday churn:
- **First Half of Phase (Ticks 1–149):** Purchased shares enter a `pending_queue` exposed to market volatility but locked from selling. Deliveries convert to active holdings exactly 30 ticks later (Tick + 30).
- **Second Half of Phase (Ticks 150–300):** Orders placed at or after tick 150 remain locked across the session break and deliver at Tick 1 of the subsequent phase.

### Bank Savings Yield
- Liquid funds transferred to Safe Haven Bank earn a fixed **+4.75% compound return** credited at each completed session transition (Ticks 150 and 300).
- Bank Savings can be withdrawn to liquid cash at any time during open trading, provided the amount withdrawn does not breach the emergency reserve setting.

---

## 5. Property Wealth Targets and Benchmarks

Targets are calibrated against empirical upper-bound frontiers calculated by the whole-share MILP optimizer (`analysis/best_case.py`):

| Property Target | Multiplier Target | Required Capital (from \$10k) | Optimization Ceiling Share | Feasible Strategy |
|---|---|---|---|---|
| **Small House** | **3.0×** | \$30,000 | 1.9% of benchmark | Achievable with conservative cash trading and timely bank rotations. |
| **Normal House** | **20.0×** | \$200,000 | 12.8% of benchmark | Requires disciplined 2×–3× margin management during bull phases. |
| **Glorious Forest Villa** | **100.0×** | \$1,000,000 | 64.1% of benchmark | Demands 4× maximum leverage with near-perfect exit timing before Phase 6. |

---

## 6. Formal Reconciliations

Earlier working drafts contained minor discrepancies across working notes. The authoritative specifications implemented in the codebase are reconciled below:

1. **Trading Equity vs Total Net Worth:** Total Net Worth includes Bank Savings. However, the Margin Ratio evaluated for liquidation risk considers Trading Equity ($C_t + E_t - D_t$) only, preventing non-custodied bank balances from serving as unpledged collateral.
2. **Maintenance Margin Threshold:** Standardized globally at **20.00%**. Exactly 20.00% triggers a `WARNING`; strictly less than 20.00% triggers forced liquidation.
3. **Settlement Boundary:** Standardized at `tick < 150` for intra-phase delivery (T+30) and `tick >= 150` for next-phase delivery.
4. **Phase Price Volatility Limits:** Standardized at ±30% per session (compounded phase limit of +69%/−51%).
5. **Benchmark Ceiling:** Standardized on the whole-share MILP optimizer ceiling (~109× concentrated DP, ~156× staggered re-leveraging), superseding early unconstrained continuous models.
