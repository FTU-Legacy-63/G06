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
| `bank_savings` | Amount of player funds currently allocated to Bank Savings. | KRW/USD (Numeric) | User action / System-updated | Savings balance, Net Worth, and available liquidity |
| `savings_return_rate` | Fixed return credited to Bank Savings after each completed AM or PM session. | Percentage: **4.75% per session** | System-defined constant | Bank Savings balance and Net Worth |

## Calibrated House Target Difficulty Matrix

*Empirically calibrated against benchmark backtests (`best_case_portfolio_summary.csv`).*

| House Type (`target_house_type`) | Target Multiplier | Required Strategy / Benchmark Feasibility | Consequence / Ending Narrative |
| :--- | :---: | :--- | :--- |
| **Small House** *(Easy / Safe)* | **$3.0\times$ Capital** | Achievable using **Cash Only (1.0×)**. Benchmark yield is $2.92\times$ (1 trade/phase) to $5.20\times$ (AM/PM rotation). | **Normie Ending:** Survived the crisis safely with zero margin debt, but wealth growth is modest. Life remains plain, mundane, and unexciting. |
| **Normal House** *(Medium / Balanced)* | **$20.0\times$ Capital** | Requires active trading with **2.0× or 3.0× Margin**. Benchmark yield spans $7.02\times$ to $72.84\times$. | **Middle-Class Stability Ending:** Navigated market turbulence with disciplined leverage. Enjoy comfortable suburban living and solid financial security. |
| **ToLam Villa** *(Extreme / Hard)* | **$100.0\times$ Capital** | Mathematically with **4.0× Margin** the player could reach a maximum of over $2.17 million - theoretical ceiling reaches **$217.45\times$ (+21,645%)** under perfect 10-trade execution before Phase 6 collapse. | **Extravagant Luxury Ending:** Flawless timing generates supreme multi-generational wealth and endless fun. A single misstep triggers total wipeout. |

## Margin Tier Specification
*The assumed margin maintenance level is 20%*

| Tier Level | Multiplier / Borrowing Capacity | Max Purchasing Power | Max Margin Debt (per $1 Equity) | Benchmark Wealth Ceiling (Phase 1–5) | Margin Call Trigger (20% Maintenance Margin) | Risk Profile |
|---|---|---|---|---|---|---|
| **Cash (1.0×)** | 1.0× Buying Power | 1.0× Equity | 0.0× Equity | **2.92× – 5.20×** | **N/A** | Zero liquidation risk; immune to broker margin calls. |
| **2×** | 2.0× Buying Power | 2.0× Equity | 1.0× Equity | **7.02× – 21.27×** | **−37.50%** | Moderate Risk: A 10% asset decline produces approximately a 20% equity loss. Theoretical equity wipeout occurs at a 50% decline. |
| **3×** | 3.0× Buying Power | 3.0× Equity | 2.0× Equity | **14.72× – 72.84×** | **−16.67%** | High Risk: A 10% asset decline produces approximately a 30% equity loss. Theoretical equity wipeout occurs at a 33.3% decline. |
| **4×** | 4.0× Buying Power | 4.0× Equity | 3.0× Equity | **27.99× – 217.45×** | **−6.25%** | Extreme Risk: A 10% asset decline produces approximately a 40% equity loss. Theoretical equity wipeout occurs at a 25% decline. |

## Core Input Flow

> `assigned_scenario_id` (Random 1 or 2) → Sets `initial_capital` + `fixed_price_path` (`market_scenario.csv`) → User selects `target_house_type` (Difficulty: $3\times$, $20\times$, or $100\times$) → Sets `property_target_value` → User executes `orders` with selected `margin_tier` (`2x`, `3x`, `4x`) → Real-time Margin & Equity Valuation → Financial & Narrative Outcome
