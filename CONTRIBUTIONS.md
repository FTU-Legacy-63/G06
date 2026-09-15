# OBJECTIVE INDIVIDUAL CONTRIBUTION EVIDENCE

**Course:** Technology Applications in Banking and Finance (NHA408E) - FTU 2026  
**Project:** Free Fall 2.0 (Group 6)  
**Member:** Nguyễn Quang Minh  
**Student ID:** 2412380031  
**Assigned Role:** Technical Developer  

---

## 1. Executive Summary of Responsibilities

As the **Technical Developer**, my core responsibility is formalizing, programming, and validating the backend mathematical simulation engine, ensuring that all financial logic and workflow requirements (from Week 3, Week 4, and the Phase 1 System Workflow) are translated into executable, verifiable, and explainable software code.

| Area | Responsibility | Concrete Repository Deliverable |
|---|---|---|
| **Core Simulation Engine** | Implement real-time portfolio valuation, bank savings yield storage, settlement delays (T+0.5 holding pen), margin ratio calculation, and maintenance margin monitoring. | [`src/simulation_engine.py`](file:///c:/Users/Admin/Desktop/Study/ung%20dung%20ttin/src/simulation_engine.py) |
| **Event & State Controller** | Implement phase transitions across 6 market phases (1,800 ticks), order execution (Buy/Sell/Savings deposit), and auto forced-liquidation triggers with penalties. | [`src/game_controller.py`](file:///c:/Users/Admin/Desktop/Study/ung%20dung%20ttin/src/game_controller.py) |
| **Workflow Architecture Alignment** | Full implementation of the `phase 1 workflow.jpg` logic diagram (Start Screen -> Bank Savings -> T+0.5 delay -> Liquidation Penalty). | [`phase 1 workflow.jpg`](file:///c:/Users/Admin/Desktop/Study/ung%20dung%20ttin/phase%201%20workflow.jpg) |
| **Dataset Integration** | Integrated the realistic dataset (`market scenario/market_scenario.csv`) consisting of 1,800 ticks and 50 asset tickers (e.g. Vintrumite, Samsung Electronics, KOSPI ETFs) directly into the state controller. | [`market scenario/market_scenario.csv`](file:///c:/Users/Admin/Desktop/Study/ung%20dung%20ttin/market%20scenario/market_scenario.csv) |
| **Logic Verification** | Create automated unit tests validating edge cases against Week 4 specification & Phase 1 workflow (4x Wipeout, Liquidation Penalty, Bank Savings, and T+0.5 Settlement Delay). | [`tests/test_simulation_engine.py`](file:///c:/Users/Admin/Desktop/Study/ung%20dung%20ttin/tests/test_simulation_engine.py) |
| **Interactive Prototype** | Standalone executable simulation script calibrated with empirical backtest parameters for live defense. | [`interactive_demo.py`](file:///c:/Users/Admin/Desktop/Study/ung%20dung%20ttin/interactive_demo.py) |

---

## 2. Technical Evidence & Implementation Details

### 2.1 Core Financial Logic (`src/simulation_engine.py`)
Directly mapped from **`phase 1 workflow.jpg`**:
- **Total Portfolio Value:**
  $$\text{Total Portfolio Value} = (\sum \text{Shares}_i \times \text{Current Stock Price}_i) + \text{Bank Savings}$$
- **Equity / Net Worth:**
  $$\text{Equity / Net Worth} = \text{Cash} + \text{Total Portfolio Value} - \text{Margin Debt}$$
- **Margin Ratio:**
  $$\text{Margin Ratio} = \frac{\text{Equity}}{\sum \text{Shares}_i \times \text{Current Stock Price}_i}$$
- **Settlement Delay Mechanism (Holding Pen):**
  - Orders executed before tick 150 (`Tick < 150`): Shares enter a T+0.5 holding pen exposed to live price movement, then convert to active holdings.
  - Orders executed after tick 150 (`Tick >= 150`): Logged as pending delivery for Phase 2.
- **Forced Liquidation & Penalty:**
  - When $\text{Stock Price} < \text{Margin Call Price}$ (or $\text{Margin Ratio} < 20\%$), the broker automatically fire-sales all shares.
  - Applies a liquidation penalty fee to cash/equity before determining solvency (`Is Equity > 0`).

### 2.2 Dataset Integration (`market scenario/`)
- Loaded 1,800 global seconds across 6 market phases:
  - **Phase 1 (1–300s):** Fake Positive News
  - **Phase 2 (301–600s):** True Positive News
  - **Phase 3 (601–900s):** Bull Market
  - **Phase 4 (901–1200s):** Strong Growth (FOMO)
  - **Phase 5 (1201–1500s):** Market Euphoria & Bull Traps
  - **Phase 6 (1501–1800s):** Negative Shock & Cascade Plunge (-57% collapse)
- Aligned target difficulty with empirical benchmark models (`best_case_portfolio_summary.csv`):
  - Small House: 3.0x Capital (Achievable with Cash 1.0x)
  - Normal House: 20.0x Capital (Requires 2.0x - 3.0x Margin)
  - ToLam Villa: 100.0x Capital (Requires 4.0x Margin)

### 2.3 Automated Logic Verification (`tests/test_simulation_engine.py`)
All financial logic is verified with 100% pass rate across 4 comprehensive tests:
```bash
python -m unittest discover tests
# Ran 4 tests in 0.000s -> OK
```
- **Test 1 (High Leverage Wipeout with Liquidation Penalty):** Validates 10m KRW capital, 4x leverage (30m debt), 20% price shock -> Margin ratio falls to 6.25% (< 20%), triggering Margin Call and forced liquidation with penalty fee deducted.
- **Test 2 (Cash-Only Position):** Validates 50m KRW capital with 0 debt, 10% price shock -> Remains solvent with 100% margin ratio.
- **Test 3 (Bank Savings Workflow):** Validates risk-free savings deposits and withdrawals adding to Total Portfolio Value.
- **Test 4 (Settlement Delay Holding Pen):** Validates delivery delay before tick 150 vs holding pen delivery into Phase 2.

---

## 3. Individual Footprint Self-Check (Midterm Checklist Section 7)

1. **My Main Responsibility:**  
   Architecting, programming, and verifying the Core Financial Engine, Phase 1 Workflow rules, CSV data pipeline, and State Controller in Python.
2. **My Most Important Output So Far:**  
   The fully tested `src/simulation_engine.py` (implementing Bank Savings, T+0.5 holding pens, and Liquidation penalties), `src/game_controller.py`, and the automated test suite `tests/test_simulation_engine.py`.
3. **Where the Evidence is Located:**  
   In the repository at `/src`, `/tests`, `market scenario/`, and `interactive_demo.py`.
4. **How My Output Supports the Group Product:**  
   Translates the visual system flowchart (`phase 1 workflow.jpg`) and empirical market data into exact, mathematically rigorous Python classes that the web frontend can reliably consume.
5. **What I Will Improve or Complete Next (Post-Midterm):**  
   - Expose the engine via FastAPI to stream real-time price ticks to the web frontend.
   - Add dynamic slippage modeling during Phase 6 cascade sales.
   - Implement post-game behavioral analytics (Max Drawdown, Panic selling index).
