# OBJECTIVE INDIVIDUAL CONTRIBUTION EVIDENCE

**Course:** Technology Applications in Banking and Finance (NHA408E) - FTU 2026  
**Project:** Free Fall 2.0 (Group 6)  
**Member:** Nguyễn Hồng Nguyên  
**Student ID:**  2412380038
**Assigned Role:** Data Gatherer  


## 1. Executive Summary of Responsibilities

As the **Data Gatherer**, my core responsibility is designing, constructing, calibrating, and validating the market scenario dataset that drives the Free Fall 2.0 simulation.

Beyond dataset construction, I am also responsible for **quantitative gameplay calibration**. This includes testing portfolio combinations and leverage levels, calculating achievable wealth ceilings, and using these results to determine appropriate property-target thresholds and margin tiers. The objective is to ensure that the financial goals remain challenging but mathematically achievable, while preventing leverage mechanics from becoming excessively powerful or making the game trivially easy.

I also contributed to the project's financial-mechanic development through **team discussions, iterative feedback, and quantitative feasibility testing**, using empirical market and portfolio results to help challenge and refine proposed margin, target, market-constraint, liquidation, and savings rules.

| Area | Responsibility | Concrete Repository Deliverable |
|---|---|---|
| **Market Scenario Dataset** | Construct the deterministic 1,800-second market dataset across 6 phases and 50 tradable assets used by the simulation engine. | `market scenario/market_scenario.csv` |
| **Scenario Calibration** | Design asset price behavior across Fake Positive News, True Positive News, Bull Market, FOMO, Market Euphoria, and Negative Shock phases. | `market scenario/market_scenario.csv` |
| **Asset Behavior Design** | Differentiate driver and non-driver assets, coordinate market movements, create volatility patterns and misleading opportunities, and calibrate the synchronized Phase 6 crash. | `market scenario/market_scenario.csv` |
| **Portfolio Combination Testing** | Generate and evaluate alternative trading combinations across leverage tiers to determine achievable portfolio outcomes. | `market scenario/best_case_portfolio_combos.csv` |
| **Target Threshold Calibration** | Calculate feasible wealth ranges and use benchmark results to determine appropriate property-target thresholds for Small House, Normal House, and ToLam Villa. | `market scenario/best_case_portfolio_summary.csv` |
| **Margin Tier Calibration** | Test Cash 1.0x, 2.0x, 3.0x, and 4.0x strategies to ensure leverage increases upside and liquidation risk without making financial targets excessively easy. | `market scenario/best_case_portfolio_combos.csv`, `market scenario/best_case_portfolio_summary.csv` |
| **Financial-Mechanic Collaboration** | Contribute to team ideation and refinement of margin, target, market-constraint, liquidation, and Bank Savings mechanics using quantitative feasibility feedback from the market dataset and portfolio benchmarks. | Collaborative contribution to `SOLUTION_STRUCTURE.md`, `ASSUMPTIONS.md`, `INPUT_DICTIONARY.md`, and `FEATURE_MAP.md` |


## 2. Data, Calibration & Collaborative Evidence

### 2.1 Core Market Dataset (`market scenario/market_scenario.csv`)

The primary dataset contains **1,800 global seconds**, representing one compressed 30-minute trading day.

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


### 2.2 Market Behavior & Scenario Calibration

The dataset was designed to support the project's behavioral-finance learning objectives rather than reproduce a purely random market.

Key scenario characteristics include:

- coordinated movements among major driver assets;
- visible intraday volatility and zigzag price behavior;
- stronger upside potential during bullish phases;
- misleading movements and decoy opportunities among non-driver assets;
- AM/PM session structure within each 300-second phase;
- amplified volatility as the simulation approaches the late-game market peak;
- synchronized systemic decline during Phase 6;
- deterministic price paths to ensure reproducible gameplay and testing.

The resulting dataset allows every player decision to be evaluated against the same underlying market path within a given scenario, making portfolio outcomes and leverage consequences reproducible.


### 2.3 Portfolio Combination Testing (`best_case_portfolio_combos.csv`)

`best_case_portfolio_combos.csv` is used to test alternative portfolio and trading combinations against the deterministic market scenario.

The portfolio tests evaluate strategies under:

- Cash Only (1.0x);
- 2.0x Margin;
- 3.0x Margin;
- 4.0x Margin;
- different asset selections;
- different trading and rotation decisions.

The purpose is not only to identify the theoretical best strategy, but also to establish the **feasible outcome range of the game**.

These tests answer several calibration questions:

- Can a conservative player realistically reach the easiest target?
- At what target does leverage become necessary?
- How much additional wealth can each margin tier generate?
- Does 4.0x leverage provide a meaningful advantage without making every target trivial?
- Is the highest target achievable only through aggressive and highly accurate execution?
- Does holding excessive leverage into the Phase 6 crash create a sufficiently severe downside consequence?

The resulting portfolio combinations therefore provide quantitative evidence for both the game's **reward structure and risk structure**.


### 2.4 Target Threshold & Margin Calibration (`best_case_portfolio_summary.csv`)

The benchmark portfolio results are summarized in `best_case_portfolio_summary.csv` and used to calibrate the game's financial thresholds.

Instead of selecting property targets arbitrarily, achievable portfolio wealth under different leverage tiers was compared before determining the final target multipliers:

| Target | Threshold | Intended Financial Requirement |
|---|---:|---|
| **Small House** | **3.0x Initial Capital** | Designed around conservative / Cash 1.0x gameplay |
| **Normal House** | **20.0x Initial Capital** | Designed to require effective use of approximately 2.0x–3.0x margin |
| **ToLam Villa** | **100.0x Initial Capital** | Designed to require aggressive 4.0x leveraged trading and highly effective execution |

The calibration process ensures that the targets occupy meaningfully different difficulty levels rather than simply representing three arbitrary numbers.

Margin tiers were evaluated against the same benchmark results. The purpose was to avoid two opposite design failures:

**Margin Too Weak → High targets become mathematically impossible**

**Margin Too Powerful → Financial targets become trivial and leverage risk loses meaning**

The final Cash / 2.0x / 3.0x / 4.0x structure therefore balances **target feasibility, wealth-generation potential, and liquidation exposure**.

This produces the intended progression:

**Higher Target → Higher Required Return → Greater Need for Leverage → Greater Exposure to Margin Call and Forced Liquidation**


### 2.5 Relationship Between Dataset and Financial Mechanics

The market dataset and financial mechanics are calibrated together rather than independently.

The price paths determine the potential gains and losses available to the player. Portfolio benchmark testing then measures how these movements interact with leverage. These results are subsequently used to evaluate whether the property targets and margin tiers produce the intended difficulty.

The calibration loop is therefore:

`Market Price Paths → Portfolio Tests → Leverage Outcomes → Wealth Ceilings → Target Thresholds → Gameplay Feasibility Check`

This process ensures that the game's financial targets are supported by the actual simulated market rather than being imposed independently of the dataset.


### 2.6 Collaborative Financial-Mechanic Ideation & Calibration

In addition to my direct responsibility for market data and quantitative calibration, I actively contributed to the development of the project's financial mechanics through team discussions, iterative feedback, and quantitative feasibility checks.

While the formal financial and risk logic was documented by the **Mechanism Designer**, I contributed to the **ideation, challenge, and refinement of these mechanics**, particularly by using the market dataset and benchmark results to assess whether proposed rules would produce reasonable gameplay outcomes.

Key collaborative contributions included:

- **Margin & Target Calibration:** Raised and discussed the need to quantitatively test leverage tiers against achievable portfolio returns rather than selecting margin levels and property targets arbitrarily. Portfolio benchmark results were used during these discussions to evaluate and refine the final **1.0x / 2.0x / 3.0x / 4.0x margin structure** and **3.0x / 20.0x / 100.0x property targets**.

- **Maintenance Margin & Liquidation Discussion:** Participated in discussions on how the maintenance-margin threshold should interact with the available leverage tiers, helping evaluate whether the liquidation trigger was sufficiently strict to create meaningful risk without making leveraged gameplay unplayable.

- **AM/PM Market Constraint Discussion:** Contributed feedback on the session structure and price-movement constraints so that the simulated price paths remained compatible with the intended gameplay volatility and Phase 6 crash.

- **Bank Savings Mechanic:** Proposed and discussed the inclusion of Bank Savings as a supporting alternative to stock exposure. Contributed to simplifying the final mechanic into a fixed **4.75% return after each completed AM/PM session**, allowing savings to provide a predictable low-risk allocation option without replacing leveraged stock trading as the main game mechanic.

- **Iterative Mechanic Review:** Continuously reviewed proposed financial rules against the generated market paths and benchmark portfolio outcomes, identifying cases where a mechanic could make a target excessively easy, mathematically impossible, or inconsistent with the intended risk-return trade-off.

My contribution in this area was therefore primarily **collaborative ideation and quantitative feedback**, while the Mechanism Designer remained responsible for formalizing the final financial formulas and rules in the project documentation.


## 3. Individual Footprint Self-Check (Midterm Checklist Section 7)

1. **My Main Responsibility:**  
   Designing, constructing, calibrating, and validating the market scenario data and quantitative benchmark models used by Free Fall 2.0. This includes both market-data generation and the calibration of target thresholds and margin tiers.

2. **My Most Important Output So Far:**  
   `market_scenario.csv`, which provides the 1,800-second deterministic price paths for 50 tradable assets across all 6 market phases, together with `best_case_portfolio_combos.csv` and `best_case_portfolio_summary.csv`, which are used to evaluate achievable portfolio outcomes and calibrate the game's financial difficulty.

3. **Where the Evidence is Located:**  
   In the repository at `market scenario/`, including:
   - `market_scenario.csv`
   - `best_case_portfolio_combos.csv`
   - `best_case_portfolio_summary.csv`

4. **How My Output Supports the Group Product:**  
   Provides the market-data backbone consumed by the simulation engine and establishes the quantitative basis for the game's difficulty. The benchmark analysis helps ensure that property targets are achievable under the intended strategies, while margin tiers provide progressively greater upside without eliminating leverage and liquidation risk. I also use these quantitative results to provide feedback during the team's development and refinement of the financial mechanics.

5. **What I Will Improve or Complete Next (Post-Midterm):**
   - Develop and calibrate **Scenario 2** as an alternative 1,800-second market path to reduce predictability and replay memorization.
   - Re-run portfolio benchmark tests against Scenario 2 to verify that the existing house-target thresholds and margin tiers remain feasible across different market paths.
   - Compare Scenario 1 and Scenario 2 outcomes to identify any unintended strategy that consistently dominates regardless of scenario.
   - Perform final dataset validation for phase transitions, AM/PM boundaries, price-limit compliance, ticker consistency, and missing or abnormal values before implementation.
   - Recalibrate target thresholds, leverage assumptions, or asset movements if testing shows that any difficulty level is either mathematically unrealistic or excessively easy.
   - Continue providing quantitative feedback on financial mechanics as the prototype is implemented to ensure that the coded gameplay remains consistent with the calibrated dataset and intended risk-return structure.
