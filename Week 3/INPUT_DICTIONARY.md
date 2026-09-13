# Input Dictionary

This file defines the minimum inputs and state variables required by the MVP before implementation.

| Variable | Meaning | Unit / Format | Source | Output Affected |
| :--- | :--- | :--- | :--- | :--- |
| `assigned_scenario_id` | Randomly assigned scenario (`1` or `2`) that determines initial cash balance and the locked six-phase price path (`market_scenario.csv`). | Integer: `1` or `2` | System-generated at launch | Sets `initial_capital` and `fixed_price_path` |
| `initial_capital` | Starting liquid cash balance assigned to the player based on the scenario. | KRW/USD (Numeric: e.g., $10,000 USD / 20,000,000 KRW) | System-generated via `assigned_scenario_id` | Starting Net Worth and initial purchasing power |
| `fixed_price_path` | Predetermined 1,800-second sequence (30 minutes across 6 phases) covering 50 asset tickers, phase states, and news triggers. | CSV time-series (`market_scenario.csv`) | Team-created data structure | Real-time portfolio revaluation, margin alerts, and liquidation checks |
| `target_house_type` | Selected financial goal defining game difficulty, required multiplier, and final narrative ending. | Categorical: `Small House` / `Normal House` / `ToLam Villa` | User input at start screen | Sets `property_target_value` and ending narrative |
| `property_target_value` | Mandatory financial threshold required to purchase the chosen house and win. | Numeric: Multiplier × `initial_capital` | Calculated (`initial_capital` × house multiplier) | Target Progress UI gauge and Win/Loss state |
| `margin_tier` | Selected margin financing tier determining maximum purchasing power and debt capacity. | Categorical / Tier: `2x`, `3x`, `4x` (or Cash-only / 1.0x) | User input | Purchasing power, Margin Debt, Margin Call, and Forced Liquidation triggers |
| `orders` | Player trading actions executed during each phase window. | Categorical (Buy / Sell / Hold) + Asset Ticker + Volume + Margin Toggle | User input | Cash balance, asset share volume, margin debt, and net equity |

## Calibrated House Target Difficulty Matrix

*Empirically calibrated against benchmark backtests (`best_case_portfolio_summary.csv`).*

| House Type (`target_house_type`) | Target Multiplier | Required Strategy / Benchmark Feasibility | Consequence / Ending Narrative |
| :--- | :---: | :--- | :--- |
| **Small House** *(Easy / Safe)* | **3.0× Capital** | Achievable using **Cash Only (1.0×)**. Benchmark yield is 2.92× (1 trade/phase) to 5.20× (AM/PM rotation). | **Normie Ending:** Survived the crisis safely with zero margin debt, but wealth growth is modest. Life remains plain, mundane, and unexciting. |
| **Normal House** *(Medium / Balanced)* | **20.0× Capital** | Requires active trading with **2.0× or 3.0× Margin**. Benchmark yield spans 7.02× to 72.84×. | **Middle-Class Stability Ending:** Navigated market turbulence with disciplined leverage. Enjoy comfortable suburban living and solid financial security. |
| **ToLam Villa** *(Extreme / Hard)* | **100.0× Capital** | Mathematically impossible without **4.0× Margin** (3.0× peaks at 72.84×). Requires near-flawless multi-phase compounding before the Phase 6 collapse. | **Extravagant Luxury Ending:** Flawless timing generates supreme multi-generational wealth and elite status. A single misstep triggers total wipeout. |

## Margin Tier Specification

| Tier Level | Multiplier / Borrowing Capacity | Max Purchasing Power | Max Margin Debt (per $1 Equity) | Drop to Breach 20% Maintenance Margin | Risk Profile |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **Cash (1.0x)** | 1.0× Buying Power | 1.0 × Equity | 0.0 × Equity | N/A (Cannot Liquidate) | Zero liquidation risk; immune to broker margin calls. |
| **2x** | 2.0× Buying Power | 2.0 × Equity | 1.0 × Equity | **-37.50%** | Moderate: High cushion against normal intraday volatility; liquidates in catastrophic systemic shocks. |
| **3x** | 3.0× Buying Power | 3.0 × Equity | 2.0 × Equity | **-16.67%** | High Risk: Vulnerable to sharp corrections and Phase 5 bull traps (max yield: 72.84×). |
| **4x** | 4.0× Buying Power | 4.0 × Equity | 3.0 × Equity | **-6.25%** | Extreme Risk (CFD-level): Unlocks the 100.0× ceiling; highly fragile to even minor price dips. |

## Core Input Flow

> `assigned_scenario_id` (Random 1 or 2) → Sets `initial_capital` + `fixed_price_path` (`market_scenario.csv`) → User selects `target_house_type` (Difficulty: 3×, 20×, or 100×) → Sets `property_target_value` → User executes `orders` with selected `margin_tier` (`2x`, `3x`, `4x`) → Real-time Margin & Equity Valuation → Financial & Narrative Outcome
