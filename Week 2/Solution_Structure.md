# SOLUTION_STRUCTURE.md

## Korean Stock Market Simulation Game

> **Core Structure:** User → Input → Process → Output → User Action


## 1. User → Input → Process → Output → User Action

| Stage | Definition |
|---|---|
| **User** | Retail investors, inexperienced day traders, and finance students |
| **Input** | Initial capital, deposit allocation, property target, margin ratio, Buy / Sell / Hold orders |
| **Process** | Market movement → Portfolio valuation → Margin calculation → Margin health check → Margin call / liquidation |
| **Output** | Portfolio value, net worth, leverage, margin status, target progress, risk & behavioral performance |
| **User Action** | Buy / Sell / Hold, adjust leverage, preserve cash, deleverage, respond to margin calls |

**Core learning loop:**  
`Decision → Financial Consequence → Market Stress → Risk Feedback → New Decision`


## 2. Initial Required Information

| Input | Meaning | Source |
|---|---|---|
| **Initial Capital / Salary** | Starting financial resources | Scenario |
| **Bank Deposit Allocation** | Safe and liquid reserve | User |
| **Property Target** | Financial goal to achieve | User / Scenario |
| **Initial Margin Ratio** | Determines available leverage | User |
| **Orders** | Buy / Sell / Hold + volume + Cash / Margin | User |
| **Market Price Path** | Predetermined market movement across six phases | System |

The market path is **system-generated rather than user-defined**, allowing the same scenario to be tested and replayed consistently.


## 3. Core Process Type

> **Deterministic, event-driven financial market simulation with real-time user decisions.**

One Korean trading day (**09:00–15:30**) is compressed into approximately **30 minutes**.

| Financial Process | Core Logic |
|---|---|
| **Trading** | Capital → Cash / Margin → Stock Position |
| **Valuation** | Price Movement → Portfolio Revaluation → Equity / Net Worth |
| **Leverage** | Equity → Leverage → Amplified Purchasing Power & Risk |
| **Risk Control** | Equity / Portfolio Value → Margin Health |
| **Downturn** | Asset Depreciation → Margin Violation → Margin Call → Forced Liquidation |


## 4. MVP Flow

| Phase | Market State | Main Purpose |
|---|---|---|
| **1. Fake Positive News** | Initial market uptick | Margin unlocked; encourage initial risk-taking |
| **2. True Positive News** | Secondary rally | Validate bullish expectations |
| **3. Bull Market** | Momentum acceleration | Reward increasing market exposure |
| **4. Strong Growth (FOMO)** | Rapid valuation surge | Encourage aggressive participation |
| **5. Market Euphoria** | Peak leverage | Maximize leverage temptation |
| **6. Negative Shock** | Crash → Circuit Breaker → Liquidation | Test leverage survival and risk response |

**During the session:**  
`Market Update → Portfolio Revaluation → Margin Check → User Decision → Next Market Update`

**Available decisions:** `Buy` · `Sell` · `Hold` · `Use Margin` · `Deleverage` · `Preserve Cash`


## 5. Target / Fallback / Out of Scope

| | Definition |
|---|---|
| **Target MVP** | Playable web simulator with capital allocation, stock trading, margin, live portfolio monitoring, margin calls / liquidation, property target, and post-game evaluation |
| **Fallback** | Simplified interface using predetermined scenarios, Buy / Sell / Hold decisions, core portfolio & margin calculations, and final risk evaluation |
| **Out of Scope** | Real-money trading, brokerage integration, live exchange execution, full order-book simulation, derivatives/options, crypto, multiplayer, institutional/broker/regulator playable roles |

The fallback must preserve the core relationship:

> **Leverage → Market Movement → Margin Risk → User Decision → Financial Outcome**


## 6. Initial Route Hypothesis

### Solution Route

`Historical Evidence → Scenario Design → Price Path → Simulation Engine → Financial Logic → Trading Interface → User Decisions → Final Evaluation`

### Technical Route

`Scenario Data → Simulation Engine → Financial Engine → React / Next.js UI → Results`

| Component | Function |
|---|---|
| **Scenario Data** | Stores predetermined market paths and events |
| **Simulation Engine** | Controls time, phases, events, and market progression |
| **Financial Engine** | Calculates portfolio value, cash, debt, equity, leverage, margin ratio, margin calls, liquidation, and target progress |
| **Trading Interface** | Displays market/portfolio states and receives player decisions |
| **Evaluation** | Produces financial and behavioral results after the simulation |

The financial engine should remain separate from the interface so that calculations can be independently tested.


## 7. Responsibility by Output

Responsibility is assigned by **reviewable output**, not only by general team roles.

| Main Output | Responsibility | Reviewable Evidence |
|---|---|---|
| **Interactive Trading Simulator** | Build the playable market environment, trading interface, simulation flow, portfolio tracking, and margin mechanics | Application / source code / simulation test |
| **Post-Simulation Behavioral & Risk Diagnostic** | Define and calculate financial outcomes, leverage exposure, margin-call response, target progress, and behavioral/risk feedback | Calculation logic / test cases / result screen |
| **Scenario Playback Engine** | Build deterministic market scenarios and allow tick-by-tick / phase-by-phase review of market events and alternative decisions | Scenario data / playback logic / scenario tests |

### Supporting Responsibilities

| Supporting Output | Responsibility | Evidence |
|---|---|---|
| **Market Scenario & Data** | Design and validate the six-phase price paths and market events | Scenario dataset / scripts |
| **Financial Logic** | Formalize portfolio, leverage, margin, liquidation, and outcome calculations | Formula documentation / calculation tests |
| **Integration & Validation** | Connect scenario, financial logic, and UI; verify expected vs. actual results | Integrated build / test results |

> **Member ownership:** Assign specific member names to each output once team responsibilities are finalized.


## Solution Summary

`Retail Investor → Capital & Target → Cash / Margin Decisions → Six-Phase Market Simulation → Portfolio & Margin Logic → Crash / Liquidation → Financial & Behavioral Evaluation`

**Purpose:** Transform margin trading from a static financial concept into an interactive decision-making experience under market stress.
