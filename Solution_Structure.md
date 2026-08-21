# 📈 Korean Stock Market Simulation Game
<br/>

A strategic simulation game focused on stock investment, margin trading mechanics, and market volatility based on the South Korean financial market.

---

## 🎮 Product Overview
<br/>

* **Current Playable Role:** Individual Investor (Retail)  
* **Planned Roles:** Institutional Investor, Brokerage Firm, Government / Financial Regulator  

---

## 🔄 Core Gameplay Loop
<br/>

Each session simulates a **09:00 – 15:30 Korean trading day**, compressed into approximately **30 minutes** of real-time gameplay.

<br/>

```text
[Income / Salary]
       │
       ▼
[Deposit / Allocate Funds] ──► [Deploy Margin Leverage]
                                      │
                                      ▼
                               [Market Movement]
                                      │
                                      ▼
                            [Portfolio Rebalancing]
                                      │
                                      ▼
                            [Property Target Check]
```

---

## 💼 Player Resources
<br/>

| Resource | Description |
| :--- | :--- |
| **Initial Capital / Salary** | Starting cash and recurring periodic income |
| **Bank Deposits** | Safe, low-yield liquid reserves |
| **Stock Portfolio** | Total equities held across market sectors |
| **Margin Borrowing** | Leverage provided by the brokerage with interest and maintenance terms |
| **Property Target** | The ultimate financial acquisition goal |

---

## 📊 Investment Universe
<br/>

Players can **Buy**, **Sell**, or **Hold** assets using either settled cash or margin leverage:

<br/>

* **Samsung Electronics** (Large-cap tech benchmark)  
* **SK Hynix** (Semiconductor / growth equity)  
* **KOSPI Index ETF** (Broad market-tracking fund)  

---

## 📉 Market Lifecycle (6 Phases)
<br/>

```text
[Phase 1] Fake Positive News   ──► Margin trading unlocked; initial market uptick
     │
[Phase 2] True Positive News   ──► Fundamental validation; secondary rally
     │
[Phase 3] Bull Market          ──► Broad-based momentum acceleration
     │
[Phase 4] Strong Growth (FOMO) ──► Heavy retail participation; rapid valuation surge
     │
[Phase 5] Market Euphoria      ──► Peak leverage saturation across participants
     │
[Phase 6] Negative Shock       ──► Market crash ──► Circuit breaker ──► Forced liquidation
```

---

## ⚡ Margin Mechanics
<br/>

### Standard Conditions
<br/>

$$\text{Equity} \longrightarrow \text{Leverage} \longrightarrow \text{Amplified Purchasing Power} \longrightarrow \text{Higher Risk / Return}$$

<br/>

### Volatility & Downturn
<br/>

$$\text{Asset Depreciation} \longrightarrow \text{Margin Ratio Violation} \longrightarrow \text{Margin Call} \longrightarrow \text{Forced Liquidation} \longrightarrow \text{Potential Negative Net Worth}$$

---

## 🏆 Victory Conditions & Evaluation
<br/>

### Win Objective
Successfully purchase the **Property Target** while maintaining total financial solvency.

<br/>

### Score Metrics
* **Total Net Worth**  
* **Property Target Progress (%)**  
* **Outstanding Debt & Leverage Exposure**  
* **Cumulative Investment Return (ROI)**  
* **Risk Management Score (Margin Health)**  
README.md
Displaying README.md.
