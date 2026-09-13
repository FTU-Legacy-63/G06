# PROJECT_PROPOSAL.md

## 1. Problem Direction

Traditional financial education often explains margin trading and liquidation through static formulas, leaving inexperienced investors unprepared for the speed and pressure of real market crashes.

The project addresses **leverage blindness**: the tendency to underestimate downside exposure and make poor decisions when leverage, margin pressure, and forced liquidation interact under extreme volatility.

The simulator converts these concepts into an interactive environment where financial consequences emerge directly from the player's leverage, liquidity, and trading decisions.


## 2. Target User and User Task

| | Definition |
|---|---|
| **Target Users** | Retail investors, inexperienced day traders, and finance and banking students |
| **Primary Task** | Manage a leveraged stock portfolio during a highly volatile simulated market session |
| **Risk Task** | Monitor leverage and margin health, maintain liquidity, and reduce exposure before forced liquidation |
| **Decision Task** | Buy, Sell, Hold, select margin tiers, deleverage positions, or preserve cash under time pressure |


## 3. Desired User Outcome

After completing the simulation, users should be able to:

- understand how leverage amplifies both gains and losses;
- recognize how falling asset prices deteriorate margin health and can trigger forced liquidation;
- manage leverage, liquidity, and cash buffers more proactively;
- make more disciplined decisions under market stress;
- recognize behavioral tendencies such as FOMO, greed, loss aversion, and panic selling.

> **Desired change:** From understanding leverage theoretically to managing leverage under simulated market stress.


## 4. Product Statement

> An interactive, web-based **market crash survival simulator** that simulates a mid-2026 South Korean margin-driven market crisis and transforms abstract leverage and behavioral-finance concepts into a high-pressure trading experience.

The player manages a portfolio through a **30-minute compressed trading session** consisting of six market phases. Market conditions evolve from deceptive bullish signals and sustained market growth to euphoria and a severe negative shock.

Players choose among Cash, 2x, 3x, and 4x exposure while pursuing different property-based financial targets. Higher targets require greater risk-taking, creating a direct trade-off between wealth ambition and financial survival.


## 5. Main Output

| Output | Description |
|---|---|
| **Interactive Trading Simulator** | Trading interface displaying simulated market prices, portfolio value, PnL, leverage, margin health, target progress, and liquidation risk |
| **Post-Simulation Risk & Decision Review** | Reviews financial outcome, leverage exposure, liquidity management, liquidation status, target achievement, and key player decisions |
| **Scenario Playback Engine** | Replays deterministic market events and player decisions to compare alternative risk-management paths |

**Core result:**  
`Player Decisions → Financial Consequences → Risk Feedback`

The simulation produces measurable financial outcomes including final net equity, cash balance, portfolio value, margin debt, effective leverage, margin health, liquidation status, and property-target progress.


## 6. Product Pattern

**Pattern:** `Simulated Environment / Serious Game / Web Application`

| Component | Initial Approach |
|---|---|
| **Market Environment** | Deterministic, event-driven market simulation across six phases |
| **Price Feed** | Predetermined 1,800-second price paths across the simulated asset universe |
| **Financial Logic** | Continuous portfolio valuation, margin debt, net equity, leverage, target-progress, and liquidation calculations |
| **Risk Enforcement** | Margin warning before maintenance breach and automatic forced liquidation when the maintenance threshold is violated |
| **User Interaction** | Real-time Buy/Sell/Hold decisions, margin-tier selection, deleveraging, and cash management |
| **Frontend** | React / Next.js interactive trading interface |
| **Simulation Engine** | Deterministic state engine controlling the 1,800-second market progression, six phases, orders, and financial states |


## 7. MVP Structure and Feasibility

### MVP Structure

The Target MVP consists of:

- **1 (out of 2) deterministic market scenarios**;
- **50 simulated Korean-market assets**;
- **6 market phases** across a 30-minute / 1,800-second session;
- **3 property-target difficulties:** Small House, Normal House, and ToLam Villa;
- **4 exposure choices:** Cash 1.0x, 2x, 3x, and 4x;
- continuous portfolio and leverage revaluation;
- margin-health warnings;
- automatic forced liquidation following a maintenance breach;
- post-simulation financial and decision debrief.

The financial risk engine continuously evaluates:

| Financial Metric | Formula |
|---|---|
| **Gross Exposure** | $\text{Gross Exposure} = \sum_i (\text{Shares}_i \times \text{Current Price}_i)$ |
| **Net Equity** | $\text{Net Equity} = \text{Liquid Cash} + \text{Gross Exposure} - \text{Margin Debt}$ |
| **Effective Leverage** | $\text{Effective Leverage} = \frac{\text{Gross Exposure}}{\text{Net Equity}}$ |
| **Margin Ratio** | $\text{Margin Ratio} = \frac{\text{Net Equity}}{\text{Gross Exposure}}$ |

A maintenance breach occurs when:

| Trigger | Condition | System Action |
|---|---|---|
| **Maintenance Breach** | $\text{Effective Leverage} > 5.0\times$ or $\text{Margin Ratio} < 20\%$ | Automatic forced liquidation of all open equity holdings at the current simulated market price |

At this point, the "broker" automatically executes forced liquidation of the player's open equity holdings at the current simulated market price.

### Feasibility

**Initial assessment: High.**

The MVP does not require live brokerage, exchange, or real-money integration. Market prices and events are supplied by a predetermined simulation dataset, while portfolio valuation, leverage monitoring, margin enforcement, order execution, and phase transitions are handled internally.

The system can therefore be implemented using standard web technologies and a deterministic state engine while preserving consistent and reproducible financial outcomes.

### Remaining Design Questions

| Question | Why It Matters |
|---|---|
| **How simple should the trading interface be?** | Beginners need sufficient market and risk information without excessive interface complexity |
| **How visible should pre-liquidation warnings be?** | Risk deterioration must be understandable without eliminating the pressure created by approaching liquidation |
| **How should performance be presented?** | Results should reflect survival, leverage control, liquidity, drawdown, and target progress rather than final wealth alone |
| **How much behavioral interpretation should appear in the debrief?** | Behavioral feedback should remain explainable and directly connected to observable player decisions |


## Proposal Summary

**Problem:** Leverage blindness under extreme market stress  
**User:** Inexperienced retail investors, day traders, and finance students  
**Solution:** Interactive leveraged-market crash survival simulator  
**Market Structure:** 1,800-second deterministic simulation across six market phases  
**Learning Goal:** Better leverage, liquidity, and behavioral risk management  
**Risk Mechanism:** Dynamic leverage monitoring → Margin warning → Maintenance breach → Forced liquidation  
**Main Outputs:** Trading Simulator · Risk & Decision Review · Scenario Playback
