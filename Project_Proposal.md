# 📉 Market Crash Survival Simulator
> An interactive, web-based serious game recreating the mid-2026 South Korea margin crisis to transform abstract behavioral finance concepts into a high-pressure trading experience.

---

## 🎯 Problem Statement
Traditional financial education teaches margin trading and liquidation mechanisms through static formulas and dry theory, leaving retail traders unprepared for real-world market crashes. 

Without experiencing the velocity of cascading liquidations, traders suffer from **leverage blindness**—failing to quantify downside exposure or manage emotional panic when cross-margin calls occur under extreme volatility.

---

## 👥 Target Users & Core Tasks

### **Target Audience**
* Retail investors & inexperienced day traders
* Finance students seeking practical risk-management proficiency

### **Core Tasks**
1. **Portfolio Management:** Manage a leveraged portfolio during volatile, simulated macro trading sessions.
2. **Dynamic Risk Control:** Monitor maintenance margin levels, calculate liquidation thresholds, and execute dynamic hedging, deleveraging, or collateral rebalancing under strict time constraints.

---

## 🏆 Desired Outcomes
* **Intuitive Mechanics:** Develop an intuitive grasp of how leverage amplifies downside velocity and cascades cross-margin liquidations.
* **Disciplined Habits:** Cultivate disciplined risk habits (e.g., proactive stop-loss placement, maintaining cash buffers) without risking real capital.
* **Emotional Mastery:** Overcome cognitive biases like loss aversion and panic selling during high-stress market contractions.

---

## 📦 Key Deliverables & Features

| Feature | Description |
| :--- | :--- |
| **Interactive Trading Simulator** | Live simulated order book and portfolio dashboard tracking PnL, margin utilization, and liquidation triggers against crash scenarios. |
| **Behavioral & Risk Diagnostic** | Post-simulation report analyzing decision velocity, leverage distribution, margin call response times, and behavioral biases. |
| **Scenario Playback Engine** | Turn-by-turn / tick-by-tick review showing alternative risk mitigation paths (e.g., proactive deleveraging vs. forced liquidation). |

---

## 🏗️ Architecture & Pattern

**Pattern:** Simulated Environment / Serious Game (Web Application)

* **Frontend:** React / Next.js with interactive charting (e.g., Lightweight Charts / TradingView)
* **Simulation Engine:** Deterministic state machine calculating margin levels, interest fees, and cascade liquidations in real time

---

## 🔍 Feasibility & Open Questions

### **Feasibility: High**
The core game logic relies on deterministic margin-ratio formulas and event-driven market price trajectories, fully implementable using standard modern web stacks.

### **Open Design Questions**
- [ ] **UI Complexity vs. Clarity:** How do we keep the interface accessible for beginners without omitting critical data points (e.g., exact liquidation price, maintenance margin buffer)?
- [ ] **Pacing & Cognitive Load:** What tick speed creates realistic psychological stress without preventing users from reading metrics and learning from decisions?
- [ ] **Engagement & Scoring:** What feedback mechanism (e.g., survival grade, capital retained, risk-adjusted score) drives optimal replay value and skill retention?
