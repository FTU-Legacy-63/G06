# FEATURE_MAP.md

# Free Fall 2.0 — Feature Map

## 1. Purpose

This document defines the Week 5 feature structure of **Free Fall 2.0**.

It maps the existing Weeks 1–4 financial logic into product features that users can directly interact with and understand.

Each feature is classified along three separate dimensions:

1. **Feature Role**
   - Main Feature
   - Supporting Feature

2. **MVP Priority**
   - Core
   - Optional
   - Out of Scope

3. **Implementation Decision**
   - Keep
   - Postpone
   - Remove

This separation avoids treating "supporting" as "optional."  
A supporting feature may still be essential to the core user flow.


## 2. Core User Goal

> Manage a leveraged stock portfolio through a 30-minute simulated market session, pursue a selected property target, and avoid forced liquidation by controlling leverage, liquidity, and exposure under market stress.

The product should allow the user to:

1. understand the assigned starting condition;
2. choose a financial target;
3. select a leverage level;
4. trade simulated assets;
5. monitor portfolio and margin health;
6. react to deteriorating risk before a maintenance breach;
7. experience the financial consequence of the chosen strategy;
8. understand the final result and why it occurred.


## 3. Main Feature

### Real-Time Leveraged Market Survival Simulation

The **main feature** is the interactive market simulation itself.

The user manages a portfolio across a deterministic **1,800-second trading session** consisting of **6 market phases**.

The core interaction loop is:

`Market Event → User Decision → Portfolio Revaluation → Risk State → Financial Consequence → User Feedback → Next Decision`

If this feature is removed, the product can no longer fulfill its core user task.


## 4. Feature Decision Map

| Feature | Feature Role | MVP Priority | User Purpose | System Function | Decision |
|---|---|---:|---|---|---:|
| **Scenario & Capital Assignment** | Supporting | Core | Understand the starting condition | Randomly assigns Scenario 1 or 2, sets starting capital, and locks the deterministic price path | **Keep** |
| **House Target Selection** | Supporting | Core | Choose financial objective and difficulty | Sets the property target and required wealth multiplier | **Keep** |
| **Margin Tier Selection** | Supporting | Core | Choose desired leverage capacity | Allows Cash 1.0x, 2x, 3x, or 4x margin tier | **Keep** |
| **1,800s Market Simulation** | Main | Core | Experience changing market conditions | Runs deterministic prices across 6 phases | **Keep** |
| **Market Phase & News Feed** | Supporting | Core | Understand why market conditions are changing | Displays phase-specific fake/real news and market events | **Keep** |
| **Asset Selection** | Supporting | Core | Choose an asset to trade | Displays available tradable assets and current prices | **Keep** |
| **Order Entry** | Main | Core | Execute trading decisions | Accepts Buy / Sell / Hold actions and trade quantity | **Keep** |
| **Order Validation** | Supporting | Core | Prevent invalid actions | Checks quantity, holdings, and available purchasing power before execution | **Keep** |
| **Order Execution** | Main | Core | Convert decisions into portfolio changes | Updates holdings, cash, exposure, and margin debt | **Keep** |
| **Portfolio Valuation** | Supporting | Core | Understand current portfolio position | Calculates current portfolio value and Gross Exposure | **Keep** |
| **Net Equity Tracking** | Supporting | Core | Measure actual remaining wealth | Calculates Net Equity after cash, exposure, and debt | **Keep** |
| **Effective Leverage Monitoring** | Supporting | Core | Understand current borrowing risk | Continuously calculates Effective Leverage | **Keep** |
| **Margin Health Indicator** | Supporting | Core | Understand account safety | Converts leverage / margin ratio into Safe, Warning, or Breach state | **Keep** |
| **Pre-Liquidation Warning** | Supporting | Core | Allow voluntary risk reduction before breach | Displays an active warning when leverage enters the danger zone | **Keep** |
| **Forced Liquidation Engine** | Main | Core | Enforce excessive leverage consequence | Automatically liquidates open equity positions when the maintenance threshold is breached | **Keep** |
| **Solvency Check** | Supporting | Core | Determine whether the player remains financially viable | Checks remaining Net Equity after liquidation | **Keep** |
| **Cash / Liquidity Display** | Supporting | Core | Monitor available financial flexibility | Shows current liquid cash balance | **Keep** |
| **Property Target Progress** | Supporting | Core | Track progress toward the selected goal | Calculates Net Equity relative to Property Target Value | **Keep** |
| **Recent Order Log** | Supporting | Core | Understand recent actions and execution | Displays recent trades, prices, and quantities | **Keep** |
| **Post-Simulation Risk & Decision Review** | Supporting | Core | Understand final financial outcome | Summarizes wealth, leverage, liquidation status, target result, and key decisions | **Keep** |
| **Scenario Playback** | Supporting | Optional | Review the sequence of previous decisions | Replays historical market events and player actions | **Postpone** |
| **Detailed Behavioral Classification** | Supporting | Optional | Identify possible behavioral patterns | Classifies observable behaviors such as FOMO or panic selling | **Postpone** |
| **Advanced Performance Charts** | Supporting | Optional | Analyze performance over time | Displays equity, leverage, drawdown, or portfolio-history charts | **Postpone** |
| **Leaderboard** | Supporting | Optional | Compare players | Ranks player results across sessions | **Remove from MVP** |
| **User Account / Login** | Supporting | Optional | Save player history | Stores profile and previous game results | **Remove from MVP** |
| **Export Result** | Supporting | Optional | Share or save results | Exports a simulation summary | **Postpone** |
| **Order-Book Depth** | Supporting | Out of Scope | Model exchange microstructure | Simulates order queues and market depth | **Remove** |
| **Execution Slippage Model** | Supporting | Out of Scope | Model liquidity-dependent execution cost | Adjusts trade prices based on simulated liquidity | **Remove** |
| **Derivative / Option Trading** | Supporting | Out of Scope | Hedge downside risk | Adds options, futures, or other derivatives | **Remove** |
| **Multiplayer Mode** | Supporting | Out of Scope | Compete with other players | Adds real-time multiplayer sessions | **Remove** |
| **Live Brokerage Integration** | Supporting | Out of Scope | Connect to real financial markets | Links the simulator to real-money brokerage infrastructure | **Remove** |


## 5. Core User-Facing Feature Flow

```text
Start
  ↓
Scenario & Initial Capital Assigned
  ↓
Select Property Target
  ↓
Select Margin Tier
  ↓
Start 1,800s Simulation
  ↓
Observe Market Price + Phase News
  ↓
Select Asset
  ↓
Buy / Sell / Hold
  ↓
Order Validation
  │
  ├── Invalid → Show Error → Return to Order Entry
  │
  └── Valid
        ↓
    Execute Order
        ↓
    Update Portfolio State
        ↓
    Recalculate:
    - Cash
    - Gross Exposure
    - Margin Debt
    - Net Equity
    - Effective Leverage
    - Target Progress
        ↓
    Evaluate Margin Health
        │
        ├── Safe
        │     ↓
        │   Continue Trading
        │
        ├── Warning
        │     ↓
        │   Show Risk Alert
        │     ↓
        │   User may Deleverage / Hold Cash / Continue Risk
        │
        └── Maintenance Breach
              ↓
          Forced Liquidation
              ↓
          Solvency Check
        ↓
Continue / End Session
        ↓
Post-Simulation Risk & Decision Review
        ↓
End
