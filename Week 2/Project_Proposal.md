# PROJECT_PROPOSAL.md

# Market Crash Survival Simulator — Project Proposal

## 1. Problem Direction

Traditional financial education often explains margin trading and liquidation through static formulas, leaving inexperienced investors unprepared for the speed and pressure of real market crashes.

The project addresses **leverage blindness**: the tendency to underestimate downside exposure and make poor decisions when leverage, margin calls, and forced liquidation interact under extreme volatility.

---

## 2. Target User and User Task

| | Definition |
|---|---|
| **Target Users** | Retail investors, inexperienced day traders, and finance students |
| **Primary Task** | Manage a leveraged stock portfolio during a highly volatile simulated market session |
| **Risk Task** | Monitor leverage and margin health, maintain liquidity, and respond to margin pressure |
| **Decision Task** | Buy, Sell, Hold, use margin, deleverage, or preserve cash under time pressure |

---

## 3. Desired User Outcome

After completing the simulation, users should be able to:

- understand how leverage amplifies both gains and losses;
- recognize how falling asset prices can trigger margin calls and forced liquidation;
- manage leverage, liquidity, and cash buffers more proactively;
- make more disciplined decisions under market stress;
- recognize behavioral biases such as loss aversion and panic selling.

> **Desired change:** From understanding leverage theoretically to managing leverage under simulated market stress.

---

## 4. Product Statement

> An interactive, web-based **market crash survival simulator** that recreates the mid-2026 South Korean margin crisis and transforms abstract leverage and behavioral-finance concepts into a high-pressure trading experience.

The player manages a portfolio through a compressed trading session in which market conditions evolve from bullish momentum and leverage expansion to a severe negative shock and forced liquidation risk.

---

## 5. Main Output

| Output | Description |
|---|---|
| **Interactive Trading Simulator** | Trading interface displaying market prices, portfolio value, PnL, leverage, margin health, and liquidation risk |
| **Post-Simulation Behavioral & Risk Diagnostic** | Evaluates financial outcome, leverage exposure, margin-call response, risk management, and behavioral decisions |
| **Scenario Playback Engine** | Replays market events and player decisions to compare alternative risk-management paths |

**Core result:**  
`Player Decisions → Financial Consequences → Risk Feedback`

---

## 6. Product Pattern

**Pattern:** `Simulated Environment / Serious Game / Web Application`

| Component | Initial Approach |
|---|---|
| **Market Environment** | Deterministic, event-driven market scenarios |
| **Price Feed** | Tick-driven simulated price movements |
| **Financial Logic** | Portfolio, leverage, margin, and liquidation calculations |
| **User Interaction** | Real-time trading and risk-management decisions |
| **Frontend** | React / Next.js interactive trading interface |
| **Simulation Engine** | Deterministic state machine controlling market phases and financial states |

---

## 7. Feasibility and Open Questions

### Feasibility

**Initial assessment: High.**

The MVP relies primarily on predetermined market scenarios, portfolio calculations, margin rules, and event-driven state transitions. These components can be implemented using standard web technologies without requiring live brokerage or exchange integration.

### Open Questions

| Question | Why It Matters |
|---|---|
| **How simple should the trading interface be?** | Beginners need essential risk information without excessive complexity |
| **How fast should the crash occur?** | The simulation must create pressure while leaving enough time for meaningful decisions |
| **What feedback should determine performance?** | The scoring system should reward risk management rather than only final wealth |
| **How realistic should market behavior be?** | The simulation must balance financial realism, learning value, and gameplay clarity |

---

## Proposal Summary

**Problem:** Leverage blindness under extreme market stress  
**User:** Inexperienced retail investors and finance students  
**Solution:** Interactive leveraged-market crash simulator  
**Learning Goal:** Better leverage, liquidity, and behavioral risk management  
**Main Outputs:** Trading Simulator · Risk Diagnostic · Scenario Playback
