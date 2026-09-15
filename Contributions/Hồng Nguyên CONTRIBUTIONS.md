# OBJECTIVE INDIVIDUAL CONTRIBUTION EVIDENCE

**Course:** Technology Applications in Banking and Finance (NHA408E) - FTU 2026  
**Project:** Free Fall 2.0 (Group 6)  
**Member:** Nguyễn Hồng Nguyên  
**Student ID:**   
**Assigned Role:** Data Gatherer  

---

## 1. Executive Summary of Responsibilities

As the **Data Gatherer**, my core responsibility is designing, constructing, calibrating, and validating the market scenario dataset that drives the Free Fall 2.0 simulation. My work converts the project's six-phase behavioral-finance scenario into deterministic asset price paths and provides quantitative benchmark portfolios used to calibrate leverage levels, house-target difficulty, and expected gameplay outcomes.

| Area | Responsibility | Concrete Repository Deliverable |
|---|---|---|
| **Market Scenario Dataset** | Construct the deterministic 1,800-second market dataset across 6 phases and 50 tradable assets used by the simulation engine. | `market scenario/market_scenario.csv` |
| **Scenario Calibration** | Design asset price behavior across Fake Positive News, True Positive News, Bull Market, FOMO, Market Euphoria, and Negative Shock phases. | `market scenario/market_scenario.csv` |
| **Asset Behavior Design** | Differentiate driver and non-driver assets, create coordinated market movements, volatility patterns, decoy movements, and the synchronized Phase 6 crash. | `market scenario/market_scenario.csv` |
| **Portfolio Combination Testing** | Generate and evaluate portfolio combinations under different market and leverage conditions to test gameplay feasibility. | `market scenario/best_case_portfolio_combos.csv` |
| **Benchmark & Difficulty Calibration** | Summarize best-case portfolio performance to evaluate achievable wealth multipliers and calibrate house targets and margin tiers. | `market scenario/best_case_portfolio_summary.csv` |
| **Dataset Documentation & Validation** |  |  |

---

## 2. Data Evidence & Scenario Design

### 2.1 Core Market Dataset (`market scenario/market_scenario.csv`)

The primary dataset contains **1,800 global seconds** representing one compressed 30-minute trading day.

The market is divided into **6 phases of 300 seconds each**, with each phase containing an AM and PM session:

- **Phase 1 (1–300s):** Fake Positive News
- **Phase 2 (301–600s):** True Positive News
- **Phase 3 (601–900s):** Bull Market
- **Phase 4 (901–1200s):** Strong Growth (FOMO)
- **Phase 5 (1201–1500s):** Market Euphoria & Bull Traps
- **Phase 6 (1501–1800s):** Negative Shock & Systemic Crash

The dataset covers **50 tradable assets** and provides the deterministic `fixed_price_path` consumed by the simulation engine.

The market paths are intentionally designed to create visible differences in asset behavior while preserving the overall six-phase narrative. Driver assets exhibit stronger coordinated movements and higher volatility, while non-driver assets provide diversification, noise, and misleading trading opportunities.

The asset previously named **SK Hynix** is represented as **Vintrumite** in the final game dataset. This is a naming change only; its underlying scenario behavior and role remain unchanged.

---

### 2.2 Market Behavior & Scenario Calibration

The dataset was designed to support the project's behavioral-finance learning objectives rather than reproduce a purely random market.

Key scenario characteristics include:

- coordinated movements among major driver assets;
- visible intraday volatility and zigzag price behavior;
- stronger upside potential during the bullish phases;
- misleading movements and decoy opportunities among non-driver assets;
- AM/PM session structure within each 300-second phase;
- amplified volatility as the simulation approaches the late-game market peak;
- synchronized systemic decline during Phase 6;
- deterministic price paths to ensure reproducible gameplay and testing.

The resulting dataset allows every player decision to be evaluated against the same underlying market path within a given scenario, making portfolio outcomes and leverage consequences reproducible.

---

### 2.3 Portfolio Benchmark Testing (`best_case_portfolio_combos.csv`)

`best_case_portfolio_combos.csv` is used to test alternative portfolio and trading combinations against the market scenario.

The purpose of the benchmark testing is to determine:

- whether the simulated market provides sufficient upside for active trading;
- how leverage changes achievable portfolio outcomes;
- whether different trading strategies produce materially different results;
- whether the financial targets are mathematically achievable;
- whether high leverage creates sufficiently severe downside consequences.

These tests provide quantitative evidence that the gameplay difficulty is linked to the underlying dataset rather than being assigned arbitrarily.

---

### 2.4 Best-Case Portfolio Summary (`best_case_portfolio_summary.csv`)

The portfolio-combination results are summarized in `best_case_portfolio_summary.csv`.

The benchmark results are used to calibrate the three property-target difficulty levels:

- **Small House:** 3.0× Initial Capital
- **Normal House:** 20.0× Initial Capital
- **ToLam Villa:** 100.0× Initial Capital

The benchmark demonstrates that lower targets can be approached with conservative or cash-only strategies, while the highest target requires aggressive leveraged trading and near-optimal execution.

This creates the intended risk-return trade-off of Free Fall 2.0:

**Higher Target → Greater Required Exposure → Greater Leverage → Greater Liquidation Risk**

---

## 3. Individual Footprint Self-Check (Midterm Checklist Section 7)

1. **My Main Responsibility:**  
   Designing, constructing, calibrating, and validating the market scenario data and quantitative benchmark portfolios used by Free Fall 2.0.

2. **My Most Important Output So Far:**  
   `market_scenario.csv`, which provides the 1,800-second deterministic price paths for 50 tradable assets across all 6 market phases, together with `best_case_portfolio_combos.csv` and `best_case_portfolio_summary.csv` for quantitative gameplay calibration.

3. **Where the Evidence is Located:**  
   In the repository at `market scenario/`, including:
   - `market_scenario.csv`
   - `best_case_portfolio_combos.csv`
   - `best_case_portfolio_summary.csv`

4. **How My Output Supports the Group Product:**  
   Provides the market-data backbone consumed by the simulation engine and supplies quantitative evidence for calibrating leverage mechanics, property-target difficulty, portfolio outcomes, and the Phase 6 crash experience.

5. **What I Will Improve or Complete Next (Post-Midterm):**  
   - Create the market scenario data for Scenario 2
