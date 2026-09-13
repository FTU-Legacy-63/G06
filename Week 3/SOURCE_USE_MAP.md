# Source–Use Map

This file records where external information is used in the MVP, how it was modified, and the limitations of each source.

| Source | Claim / Use in Product | Limitation & Team Modification |
| :--- | :--- | :--- |
| Historical KOSPI, CFD, and tech-stock price action from the April 2023 Korea margin crisis | Used as empirical problem evidence and historical baseline for modeling systemic cascade liquidations across 50 Korean equity and ETF tickers (`market_scenario.csv`). | **Team Modification:** The historical crisis unfolded over multiple weeks. The team **synthetically intensified the price series and compressed it into an 1,800-second (30-minute), 6-phase sequence**. Phase 5 features aggressive bull-trap fakeouts, followed by an extreme Phase 6 systemic collapse where core assets drop over **−57%** within 300 seconds. Circuit breakers are omitted. |
| Empirical Strategy Optimization Dataset (`best_case_portfolio_summary.csv` & `best_case_portfolio_combos.csv`) | Used to verify maximum mathematical wealth ceilings and establish defensible house target multipliers ($3\times$, $20\times$, and $200\times$). | **Benchmark Limitation:** Assumes frictionless instant execution, perfect trade timing (capturing exact AM/PM local peaks across tickers like Vintrumite, POSCO Future M, and Kakao), and full compounding without slippage. |
| Standard Korean brokerage margin regulations (e.g., Kiwoom Securities) | Used as a regulatory baseline for defining initial margin tiers (`2x`, `3x`, `4x`) and the 30% maintenance margin threshold. | The MVP standardizes margin into 3 discrete borrowing multipliers and applies a universal liquidation rule across all 50 assets, omitting tiered interest rate brackets. |

## Source-Use Principle

External crisis data provided the **historical foundation**, which was **modified by the team into an intensified deterministic simulation model**. Benchmark algorithmic runs confirmed that peak margin returns can reach **~200×** under optimal conditions, providing empirical justification for the ToLam Villa difficulty tier.
