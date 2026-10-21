<div align="center">

# 📉 Free Fall 2.0: Korea Margin Crisis Simulation
**An Interactive FinTech Risk Engine & Margin Liquidation Simulator**

[![Course](https://img.shields.io/badge/Course-NHA408E%20FinTech-800020?style=for-the-badge)](https://github.com/FTU-Legacy-63/NHA408E)
[![Institution](https://img.shields.io/badge/FTU-Advanced%20Program-blue?style=for-the-badge)](https://ftu.edu.vn)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](./LICENSE)

[**📄 Final Report**](./deliverables/report/G06_NHA408E_Final_Report.pdf) •
[**📊 Defense Deck**](./deliverables/presentation/G06_NHA408E_Defense_Deck.pdf) •
[**🎥 Video Demo**](./deliverables/demo/G06_Product_Demo_Link.md) •
[**📐 Financial Mechanics**](./docs/financial_mechanics.md)

</div>

---

## 1. Executive Summary & Product Pitch

**Free Fall 2.0** is an interactive quantitative simulation and educational FinTech platform modeled on the mechanics of systemic retail and institutional margin cascades in the South Korean equity market (e.g., KOSPI/KOSDAQ leveraged unwinds and CFD/margin debt crunches). 

Retail investors frequently underestimate the non-linear asymmetry of leveraged trading: while leverage amplifies returns linearly in bull regimes, mark-to-market drawdowns trigger **maintenance margin breaches**, **forced brokerage liquidations**, and **illiquidity slippage spirals**. Free Fall 2.0 places the user inside a live, event-driven trading terminal during a multi-stage market liquidity crisis, testing their ability to manage leverage ratios, collateral buffers, and dynamic margin calls in real time.

---

## 2. System Architecture & Tech Stack

The repository follows a strict **three-tier decoupled architecture**, isolating the mathematical risk engine from the interactive presentation layer to ensure auditability and unit-test coverage.

```text
+-----------------------------------------------------------------------+
|                        PRESENTATION LAYER (UI)                        |
|  Streamlit State Machine | Plotly Real-Time Charts | Margin Gauges    |
+-----------------------------------+-----------------------------------+
                                    |  User Orders / Collateral Actions
                                    v
+-----------------------------------------------------------------------+
|                    QUANTITATIVE FINANCIAL ENGINE                      |
|  Leverage Calculator | Mark-to-Market Valuation | Liquidation Engine  |
|  Dynamic Margin Call Triggers | Slippage & Market Impact Simulator    |
+-----------------------------------+-----------------------------------+
                                    |  Tick & Regime Queries
                                    v
+-----------------------------------------------------------------------+
|                       DATA & SCENARIO LAYER                           |
|  Historical Crisis Regimes | Volatility Shock Generators | Audit Logs |
+-----------------------------------------------------------------------+
```

| Layer | Technologies Used | Purpose |
| :--- | :--- | :--- |
| **Core Risk Engine** | `Python 3.10+`, `NumPy`, `SciPy`, `Pandas` | Vectorized mark-to-market accounting, leverage boundary checks, maintenance margin triggers, and forced liquidation cascades. |
| **Frontend & Visualization** | `Streamlit`, `Plotly` | Low-latency reactive trading dashboard, interactive candlestick/equity curves, and real-time margin health telemetry. |
| **Quality Assurance** | `Pytest` | Automated verification of boundary conditions (zero-equity floor, extreme gap-down liquidations, margin call resolution). |

---

## 3. Repository Directory Structure

```text
G06/
├── data/
│   ├── raw/                            # Historical Korean market crisis OHLCV & volatility datasets
│   └── processed/                      # Calibrated simulation scenarios and shock trajectories
├── deliverables/
│   ├── report/                         # Final NHA408E Academic Report (PDF)
│   ├── presentation/                   # Final Oral Defense Slide Deck (PDF)
│   └── demo/                           # Product Walkthrough Video & GIF Previews
├── docs/
│   ├── architecture.md                 # Component state diagrams and data flow specifications
│   ├── financial_mechanics.md          # Complete mathematical derivations and edge-case proofs
│   ├── user_flow.md                    # Core user-facing feature flows and state transitions
│   └── assets/                         # UI screenshots and architectural diagrams
├── notebooks/
│   └── 01_crisis_volatility_eda.ipynb  # Empirical calibration of crisis drawdown parameters
├── src/
│   ├── config.py                       # Global simulation parameters, fee schedules, and margin tiers
│   ├── engine/                         # Pure quantitative logic (Leverage, Margin, Liquidation, Win/Loss)
│   ├── ui/                             # Streamlit views, Plotly chart builders, and HUD components
│   └── utils/                          # Data loaders, state validators, and formatting helpers
├── tests/                              # Unit test suite covering core financial mechanics
├── app.py                              # Main application entry point
├── requirements.txt                    # Locked dependency manifest
└── README.md                           # Project overview and quickstart guide
```

---

## 4. Core FinTech Mechanics & Mathematical Formulation

All trading rules in `src/engine/` are governed by transparent, deterministic financial equations:

### 4.1 Leverage & Buying Power
Given initial cash equity $E_0$ and selected leverage multiplier $\lambda \in [1.0, \lambda_{\max}]$, total position notional $V_0$ and borrowed margin debt $D_0$ are defined as:

$$V_0 = E_0 \cdot \lambda, \quad D_0 = V_0 - E_0 = E_0(\lambda - 1)$$

The **Initial Margin Requirement ($IMR$)** is enforced prior to order execution:

$$IMR = \frac{1}{\lambda} \ge IMR_{\min}$$

### 4.2 Mark-to-Market Equity & Margin Maintenance
At each discrete simulation step $t$, as asset price moves from $P_0$ to $P_t$ and accrued financing interest $I_t$ accumulates on debt $D_{t-1}$:

$$V_t = Q_t \cdot P_t, \quad D_t = D_{t-1}(1 + r_{\text{margin}}\Delta t)$$

$$E_t = V_t - D_t - C_{\text{tx}}$$

The **Live Margin Ratio ($MR_t$)** is continuously evaluated against the broker's **Maintenance Margin Requirement ($MMR$)**:

$$MR_t = \frac{E_t}{V_t} = \frac{Q_t P_t - D_t}{Q_t P_t}$$

### 4.3 Margin Call & Forced Liquidation Waterfall
1. **Normal State ($MR_t \ge IMR$):** Full trading and leverage adjustments permitted.
2. **Warning / Restricted State ($MMR \le MR_t < IMR$):** New leveraged buying power is frozen; user cannot withdraw cash.
3. **Margin Call Trigger ($MR_{\text{liq}} < MR_t < MMR$):** User must inject cash collateral $\Delta C$ or manually deleverage $\Delta Q$ within the grace window to restore $MR_t \ge IMR$:
   $$\Delta C_{\text{required}} = D_t - V_t(1 - IMR)$$
4. **Forced Liquidation ($MR_t \le MR_{\text{liq}}$):** The brokerage risk engine overrides user control, executing a market sell order with crisis slippage penalty $\delta_{\text{slip}}$:
   $$P_{\text{exec}} = P_t (1 - \delta_{\text{slip}})$$
   If $E_t \le 0$ post-liquidation, the account enters **Technical Insolvency (Game Over)**.

### 4.4 Win / Loss Terminal Conditions
* **Victory (Crisis Survivor):** Completing all crisis trading sessions ($t = T_{\text{final}}$) with positive net equity above the survival threshold ($E_T \ge E_{\text{target}}$) and zero unresolved margin calls.
* **Defeat (Liquidated / Insolvent):** Triggering forced full-account liquidation ($MR_t \le MR_{\text{liq}}$) or exhausting total capital below the minimum exchange lot threshold.

---

## 5. Local Quickstart & Execution Instructions

### Prerequisites
* **Python:** `3.10` or higher (`python --version`)
* **Git:** Installed and configured

### Step 1: Clone the Repository
```bash
git clone [https://github.com/FTU-Legacy-63/G06.git](https://github.com/FTU-Legacy-63/G06.git)
cd G06
```

### Step 2: Create & Activate Virtual Environment

**macOS / Linux (Bash/Zsh):**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Launch the Simulation Platform
```bash
streamlit run app.py
```
The application will automatically open in your default browser at `http://localhost:8501`.

### Step 5: Run Automated Unit Tests (For Evaluators)
To verify the mathematical integrity of the leverage, maintenance margin, and liquidation engines:
```bash
pytest tests/ -v
```

---

## 6. Core User-Facing Feature Flow

1. **Scenario & Risk Profile Selection:** Choose historical Korean market stress regimes, initial capital allocation, and brokerage margin tier.
2. **Interactive Trading & Leverage Terminal:** Execute long/short leveraged positions with real-time pre-trade margin impact previews.
3. **Live Crisis Feed & Shock Events:** Experience historical macro and liquidity shocks that shift asset volatility and widen bid-ask slippage.
4. **Margin Call Resolution Modal:** When $MR_t < MMR$, an interactive crisis resolution prompt forces the user to choose between injecting emergency collateral, partial position liquidation, or risking forced brokerage closeout.
5. **Post-Mortem Quantitative Analytics:** End-of-game performance attribution comparing user equity drawdown, maximum leverage utilization, and Sharpe/Sortino metrics against an unleveraged KOSPI benchmark.

---

## 7. Team Members & Contribution Matrix (Group 06)

All four team members contributed collaboratively to system integration, testing, and defense preparation. Primary module ownership is structured below:

| Member Name | Primary Role | Core Modules & Deliverables Owned |
| :--- | :--- | :--- |
| **Trần Hữu Dụ** | Lead Quantitative Architect & Product Flow Designer | • Core game mechanics & state machine (`src/engine/game_state.py`)<br>• Leverage, margin maintenance, and forced liquidation formulas (`src/engine/leverage.py`, `margin_maintenance.py`, `liquidation.py`)<br>• Win/loss terminal logic & core user-facing feature flows (`src/ui/views.py`)<br>• Cross-functional technical integration supporting all team workstreams |
| **Nguyễn Hồng Nguyên** | Market Data & Scenario Engineer | • Korean market crisis data pipeline & historical calibration (`data/`, `notebooks/`)<br>• Volatility shock generators and macroeconomic event scripting (`src/utils/data_loader.py`)<br>• Empirical background section in Final Report |
| **Triệu Đức Lương** | Frontend & Visualization Engineer | • Interactive Plotly financial charting & drawdown telemetry (`src/ui/charts.py`)<br>• UI component styling, margin health gauges, and responsive layout (`src/ui/components.py`)<br>• Product demo video recording and visual assets |
| **Cáp Phan Quang Khánh** | Quality Assurance & Documentation Lead | • Edge-case testing & input validation (`tests/`, `src/utils/validators.py`)<br>• System documentation, academic report formatting, and presentation deck synthesis (`deliverables/`, `docs/`) |

---

## 8. Academic Deliverables & Documentation Links

* 📄 **[Final Project Report (PDF)](./deliverables/report/G06_NHA408E_Final_Report.pdf)** — Comprehensive literature review, Korean margin crisis case study, mathematical methodology, and system evaluation.
* 📊 **[Oral Defense Presentation Deck (PDF)](./deliverables/presentation/G06_NHA408E_Defense_Deck.pdf)** — Executive slides prepared for the NHA408E final defense interview.
* 🎥 **[Product Walkthrough & Live Demo](./deliverables/demo/G06_Product_Demo_Link.md)** — Recorded end-to-end simulation showing normal trading, margin call triggers, and forced liquidation.
* 📐 **[Mathematical & Financial Specification](./docs/financial_mechanics.md)** — Detailed derivations of leverage, maintenance margin, and slippage equations.
* 🔄 **[User Flow & State Machine Diagram](./docs/user_flow.md)** — End-to-end user journey and state transition logic.

---

<div align="center">
  <sub>Developed by <b>Group 06</b> for <b>NHA408E: FinTech</b> — Foreign Trade University (FTU), Hanoi.</sub>
</div>
