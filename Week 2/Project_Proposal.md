## Problem Direction

Traditional financial education teaches margin trading and liquidation mechanisms through static formulas and dry theory, leaving retail traders unprepared for real-world market crashes. Without experiencing the velocity of cascading liquidations, traders suffer from **"leverage blindness"**—failing to quantify downside exposure or manage emotional panic when cross-margin calls occur under extreme volatility.


## Target User and User Task

- **Target Users:** Retail investors, inexperienced day traders, and finance students seeking risk-management proficiency.
- **User Tasks:**
  - Manage a leveraged portfolio during volatile, simulated macro trading sessions.
  - Monitor maintenance margin levels, calculate liquidation thresholds, and execute dynamic hedging, deleveraging, or collateral rebalancing under time constraints.

## Desired User Outcome

- Develop an intuitive grasp of how leverage amplifies downside velocity and cascades cross-margin liquidations.
- Cultivate disciplined risk habits (e.g., proactive stop-loss placement, maintaining cash buffers) without risking real capital.
- Overcome cognitive biases like loss aversion and panic selling during high-stress market contractions.


## Product Statement

An interactive, web-based **market crash survival simulator** that recreates the mid-2026 South Korea margin crisis, transforming abstract behavioral finance concepts into a high-pressure, gamified trading experience.

---

## Main Output

- **Interactive Trading Simulator:** A simulated order book and portfolio dashboard tracking live PnL, margin utilization, and liquidation triggers against mid-2026 crash scenarios.
- **Post-Simulation Behavioral & Risk Diagnostic:** A comprehensive report analyzing user decision velocity, leverage distribution, margin call response times, and behavioral biases demonstrated throughout the run.
- **Scenario Playback Engine:** Turn-by-turn or tick-by-tick review showing alternative risk mitigation paths (e.g., early deleveraging vs. forced liquidation).


## Product Pattern

- **Simulated Environment / Serious Game (Web Application):** Combines tick-driven price feeds, event-driven news catalysts, and realistic exchange margin logic.
- **Core Architecture:**
  - **Frontend:** React / Next.js with interactive charting (e.g., Lightweight Charts / TradingView).
  - **Simulation Engine:** Deterministic state machine calculating margin levels, interest fees, and cascade liquidations in real time.

- **Feasibility:** High. The core game logic relies on simple mathematical formulas for margin ratio calculations and pre-scripted price drops, which can easily be built with standard web technologies.

- **Open Questions:**
  - How can we make the trading interface simple enough for beginners without leaving out essential numbers like the liquidation price?
  - How fast should the simulated crash happen so it feels stressful and engaging, but still gives users enough time to react and learn?
  - What kind of simple score or feedback (e.g., survival rank, cash saved) will best motivate users to replay and improve their risk habits?
