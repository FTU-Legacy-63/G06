# Input Dictionary

This file defines the minimum inputs and state variables required by the MVP before implementation.

| Variable | Meaning | Unit / Format | Source | Output Affected |
| :--- | :--- | :--- | :--- | :--- |
| `assigned_scenario_capital` | Randomly assigned scenario (1, 2, or 3) that determines both starting capital and the fixed market path. | Integer: `1`, `2`, or `3` | System-generated at launch | Initial wealth and market conditions |
| `fixed_price_path` | Predetermined sequence of stock-price changes across Phases 1–6 for the assigned scenario. | Array of percentage changes | Team-created | Portfolio valuation across all phases |
| `target_house_type` | Player's selected financial goal. Mini Apartment requires 2× initial capital; Gangnam Villa requires 8× initial capital. | Categorical: `Mini Apartment` / `Gangnam Villa` | User input | Financial target and ending |
| `initial_capital` | Starting cash balance assigned to the player. | KRW, numeric | System-generated based on scenario | Starting Net Worth and purchasing power |
| `initial_margin_ratio` | Margin ratio selected by the player. | Percentage: 25%–50% | User input | Leverage, Margin Call and Forced Liquidation risk |
| `orders` | Trading decisions submitted by the player during each phase. | Buy / Sell / Hold + Volume + Cash/Margin | User input | Portfolio holdings, cash, debt and investment return |

## Core Input Flow

> `assigned_scenario_capital` → `initial_capital` + `fixed_price_path` → `target_house_type` → `orders` + `initial_margin_ratio` → Financial Outcome
