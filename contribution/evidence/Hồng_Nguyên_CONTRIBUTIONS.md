# OBJECTIVE INDIVIDUAL CONTRIBUTION EVIDENCE

**Course:** Technology Applications in Banking and Finance (NHA408E) - FTU 2026  
**Project:** Free Fall 2.0 (Group 6)  
**Member:** Nguyễn Hồng Nguyên  
**Student ID:** 2412380038  
**Assigned Role:** Data Gatherer  


## 1. Executive Summary of Responsibilities

As the **Data Gatherer**, my core responsibility is designing, constructing, calibrating, and validating the market scenario datasets that drive the Free Fall 2.0 simulation.

Beyond dataset construction, I am also responsible for **quantitative gameplay calibration**. This includes testing portfolio combinations and leverage levels, calculating achievable wealth benchmarks, and using these results to evaluate appropriate property-target thresholds and margin tiers. The objective is to ensure that the financial goals remain challenging but achievable under effective strategies, while preventing leverage mechanics from becoming excessively powerful or making the game trivially easy.

I also contributed to the project's financial-mechanic development through **team discussions, iterative feedback, and quantitative feasibility testing**, using market and portfolio results to help challenge and refine proposed margin, target, market-constraint, liquidation, and savings rules.

| Area | Responsibility | Concrete Repository Deliverable |
|---|---|---|
| **Market Scenario Dataset** | Construct deterministic 1,800-second market datasets across 6 phases and 50 tradable assets used by the simulation engine. | `data/market_scenario_1.csv`, `data/market_scenario_2.csv` |
| **Scenario Calibration** | Design asset price behavior across Fake Positive News, True Positive News, Bull Market, FOMO, Market Euphoria, and Negative Shock phases. | `data/market_scenario_1.csv`, `data/market_scenario_2.csv` |
| **Asset Behavior Design** | Differentiate driver and non-driver assets, coordinate market movements, create volatility patterns and misleading opportunities, and calibrate the Phase 6 crash. | `data/market_scenario_1.csv`, `data/market_scenario_2.csv` |
| **Market Data Validation** | Audit market-price continuity, phase-level price constraints and numeric integrity for both scenarios. | `data/audit/market_scenario_audit_1.xlsm`, `data/audit/market_scenario_audit_2.xlsx` |
| **Portfolio Combination Testing** | Generate and evaluate alternative trading combinations across leverage tiers to determine achievable portfolio outcomes. | `analysis/best_case.py`, `analysis/whole_share_srlp_cycles.csv`, `analysis/whole_share_srlp_buy_allocations.csv` |
| **Target Threshold Calibration** | Calculate feasible wealth ranges and use benchmark results to evaluate property-target thresholds for Small House, Normal House, and ToLam Villa. | `analysis/target_calibration_3x_20x_100x.csv`, `analysis/target_robustness_both_scenarios.csv` |
| **Margin Tier Calibration** | Test different leverage tiers to evaluate how leverage increases potential wealth and liquidation exposure. | `analysis/whole_share_srlp_summary.csv`, `analysis/scenario_tier_comparison.csv`, `analysis/whole_share_srlp_margin_audit.csv` |
| **Financial-Mechanic Collaboration** | Contribute to team ideation and refinement of margin, target, market-constraint, liquidation, and Bank Savings mechanics using quantitative feasibility feedback. | Collaborative contribution to project solution structure, assumptions, input dictionary, and feature documentation |


## 2. Data, Calibration & Collaborative Evidence

### 2.1 Core Market Datasets (`data/market_scenario_1.csv` and `data/market_scenario_2.csv`)

The project uses two deterministic market datasets, each containing **1,800 global seconds**, representing one compressed 30-minute trading day.

Each scenario is divided into **6 phases of 300 seconds each**, with each phase containing an AM and PM session:

- **Phase 1 (1–300s):** Fake Positive News
- **Phase 2 (301–600s):** True Positive News
- **Phase 3 (601–900s):** Bull Market
- **Phase 4 (901–1200s):** Strong Growth (FOMO)
- **Phase 5 (1201–1500s):** Market Euphoria & Bull Traps
- **Phase 6 (1501–1800s):** Negative Shock & Systemic Crash

Each dataset covers **50 tradable assets** and provides the deterministic `fixed_price_path` consumed by the simulation engine.

The market paths are intentionally designed to create visible differences in asset behavior while preserving the overall six-phase narrative. Driver assets exhibit stronger coordinated movements and higher volatility, while non-driver assets provide diversification, noise, and misleading trading opportunities.

The asset previously named **SK Hynix** is represented as **Vintrumite** in the final game dataset. This is a naming change only; its underlying scenario behavior and role remain unchanged.

Scenario 2 was developed as an alternative market path to reduce predictability and allow the same trading mechanisms and property targets to be evaluated under different asset-price movements.

The finalized datasets are documented in:

- [Scenario 1 Dataset](../../data/market_scenario_1.csv)
- [Scenario 2 Dataset](../../data/market_scenario_2.csv)

### 2.2 Market Behavior & Scenario Calibration

The datasets were designed to support the project's behavioral-finance learning objectives rather than reproduce a purely random market.

Key scenario characteristics include:

- coordinated movements among major driver assets;
- visible intraday volatility and zigzag price behavior;
- stronger upside potential during bullish phases;
- misleading movements and decoy opportunities among non-driver assets;
- AM/PM session structure within each 300-second phase;
- amplified volatility as the simulation approaches the late-game market peak;
- synchronized systemic decline during Phase 6;
- deterministic price paths to ensure reproducible gameplay and testing.

The resulting datasets allow player decisions to be evaluated against predetermined market paths, making portfolio outcomes and leverage consequences reproducible.

**Market Data Validation**

Both scenarios were subsequently reviewed and corrected to comply with the finalized market-data constraints:

- Each scenario contains 1,800 consecutive global seconds and 50 tradable assets.
- Each phase lasts 300 seconds, divided into 150-second AM and PM sessions.
- Prices must remain within **70%–130% of the reference price at the beginning of the full 300-second phase**.
- The final AM price must equal the initial PM price.
- Adjacent phases must maintain price continuity.
- All asset prices must be positive, numeric and readable by the optimization script.

The final validation runs reported:

| Validation Criterion | Scenario 1 | Scenario 2 |
|---|---|---|
| 1,800 ticks × 50 assets | PASS | PASS |
| AM/PM price continuity | PASS | PASS |
| Adjacent-phase continuity | PASS | PASS |
| ±30% price limits per full phase | PASS | PASS |
| Numeric price integrity | PASS | PASS |

Scenario 1 required corrections to abnormal price discontinuities, including those affecting Phase 6. Scenario 2 required correction of session-boundary discontinuities and normalization of text-formatted numeric prices containing thousands separators.

The updated datasets were successfully accepted by the data-validation stage of `best_case.py`.

Supporting evidence:

- [Scenario 1 Audit Workbook](../../data/audit/market_scenario_audit_1.xlsm)
- [Scenario 2 Audit Workbook](../../data/audit/market_scenario_audit_2.xlsx)
- [Data and Sources Documentation](../../docs/data_and_sources.md)

### 2.3 Portfolio Combination Testing (`analysis/best_case.py`)

The portfolio optimization model is used to test alternative portfolio and trading combinations against both deterministic market scenarios.

The portfolio tests evaluate strategies under:

- Cash Only (1.0x), as a baseline strategy considered during earlier calibration;
- 2.0x Margin;
- 3.0x Margin;
- 4.0x Margin;
- different asset selections;
- different trading and rotation decisions;
- concentrated positions and staggered re-leveraging.

The current `best_case.py` directly optimizes the **2.0x, 3.0x and 4.0x leverage tiers**, using whole-share quantities and two complementary approaches.

**Approach 1 — Concentrated Dynamic Programming**

The optimizer selects a sequence of concentrated trades, with capital reinvested after each completed trading cycle and settlement period.

**Approach 2 — Staggered Re-Leveraging MILP**

The optimizer improves the concentrated strategy by allowing additional share purchases within an existing profitable trading cycle, subject to leverage and maintenance-margin constraints.

The current benchmark configuration includes:

| Parameter | Value |
|---|---|
| Initial Capital | $10,000 |
| Market Duration | 1,800 ticks |
| Tradable Assets | 50 |
| Leverage Tiers | 2.0x / 3.0x / 4.0x |
| Share Quantities | Whole Shares Only |
| Settlement Delay | 75 ticks |
| Maintenance-Margin Threshold | 20% |
| Survival Margin | At least 20.001% |
| MILP Relative Gap Target | 0.1% |
| MILP Time Limit | 60 seconds per cycle |

The purpose is not only to identify highly profitable strategies, but also to establish quantitative benchmarks against which the game's target requirements and leverage assumptions can be evaluated.

These tests answer several calibration questions:

- Can conservative or lower-leverage strategies reach the easiest target?
- Under which market scenarios does additional leverage become necessary?
- How much additional wealth can each leverage tier generate?
- Does staggered re-leveraging materially improve results over concentrated trading?
- Is the highest target attainable across both market scenarios?
- Does holding leveraged positions expose the player to meaningful maintenance-margin and liquidation risk?

**Latest Optimization Results**

The updated optimizer was executed on both corrected market scenarios. The resulting best-case benchmarks are:

| Scenario | Margin Tier | Concentrated DP | Staggered Re-Leveraging | Final Equity |
|---|---|---:|---:|---:|
| Scenario 1 | 2.0x | 25.007857x | **31.534604x** | $315,346.04 |
| Scenario 1 | 3.0x | 85.517668x | **156.869452x** | $1,568,694.52 |
| Scenario 1 | 4.0x | 257.709480x | **491.696973x** | $4,916,969.73 |
| Scenario 2 | 2.0x | 103.427759x | **137.817680x** | $1,378,176.80 |
| Scenario 2 | 3.0x | 545.345477x | **1,127.322099x** | $11,273,220.99 |
| Scenario 2 | 4.0x | 2,249.165859x | **5,990.443600x** | $59,904,436.00 |

The results demonstrate that Scenario 2 provides substantially greater optimized wealth-generation opportunities than Scenario 1 under the same leverage tiers.

Staggered re-leveraging also produces higher final equity than concentrated trading in every tested scenario-tier combination.

However, these figures represent **perfect-foresight optimization benchmarks**, not normal player performance or demonstrated global wealth ceilings. The model has access to future price movements that ordinary players cannot observe.

One Scenario 1 cycle under 2.0x leverage did not meet the configured 0.1% MILP gap target. Therefore, its returned solution should be treated as a feasible result rather than an optimality-certified cycle at the requested tolerance.

Supporting evidence:

- [Best-Case Optimization Script](../../analysis/best_case.py)
- [Combined Optimization Summary](../../analysis/whole_share_srlp_summary.csv)
- [Trading Cycle Results](../../analysis/whole_share_srlp_cycles.csv)
- [BUY Allocations](../../analysis/whole_share_srlp_buy_allocations.csv)
- [Margin Audit](../../analysis/whole_share_srlp_margin_audit.csv)
- [Best-Case Calibration Documentation](../../analysis/best_case_calibration_targets_3x_20x_100x.md)

### 2.4 Target Threshold & Margin Calibration (`analysis/target_calibration_3x_20x_100x.csv`)

The benchmark portfolio results are used to evaluate the game's financial thresholds.

Instead of selecting property targets arbitrarily, achievable portfolio wealth under different leverage tiers was compared against the finalized target multipliers:

| Target | Threshold | Intended Financial Requirement |
|---|---:|---|
| **Small House** | **3.0x Initial Capital** | Designed as an introductory target for relatively conservative trading |
| **Normal House** | **20.0x Initial Capital** | Designed to require stronger timing, compounding and effective management of market exposure |
| **ToLam Villa** | **100.0x Initial Capital** | Designed as an advanced target requiring exceptionally effective trading and risk management |

The calibration process seeks to establish meaningfully different difficulty levels rather than simply representing three arbitrary numbers.

**Target Attainment Under the Current Optimizer**

| Scenario | Margin Tier | Small House (3x) | Normal House (20x) | ToLam Villa (100x) |
|---|---|---|---|---|
| Scenario 1 | 2.0x | PASS | PASS | BELOW |
| Scenario 1 | 3.0x | PASS | PASS | PASS |
| Scenario 1 | 4.0x | PASS | PASS | PASS |
| Scenario 2 | 2.0x | PASS | PASS | PASS |
| Scenario 2 | 3.0x | PASS | PASS | PASS |
| Scenario 2 | 4.0x | PASS | PASS | PASS |

The results confirm that the optimizer finds strategies reaching the Small House and Normal House thresholds under all tested scenario-tier combinations.

For the ToLam Villa target, the tested strategy reaches 100x under 3.0x and 4.0x leverage in both scenarios, and under 2.0x leverage in Scenario 2. The tested Scenario 1 strategy at 2.0x leverage achieves 31.534604x and remains below the 100x threshold.

This indicates that **4.0x leverage is not a strict prerequisite for reaching the highest target** under the current dataset and optimizer assumptions.

Margin tiers were evaluated against the same benchmark results. The purpose was to avoid two opposite design failures:

**Margin Too Weak → High targets become unattainable under the tested strategies**

**Margin Too Powerful → Financial targets become trivial under effective strategies, reducing the intended educational challenge**

The final Cash / 2.0x / 3.0x / 4.0x structure was designed to balance **target feasibility, wealth-generation potential and liquidation exposure**.

This produces the intended progression:

**Higher Target → Higher Required Return → Greater Importance of Timing and Compounding → Potentially Greater Leverage Exposure → Greater Margin and Liquidation Risk**

Actual gameplay difficulty still requires testing with players who do not know future price movements.

Supporting evidence:

- [Property Target Calibration](../../analysis/target_calibration_3x_20x_100x.csv)
- [Cross-Scenario Tier Comparison](../../analysis/scenario_tier_comparison.csv)
- [Target Robustness Across Both Scenarios](../../analysis/target_robustness_both_scenarios.csv)

### 2.5 Relationship Between Dataset and Financial Mechanics

The market datasets and financial mechanics are calibrated together rather than independently.

The price paths determine the potential gains and losses available to the player. Portfolio benchmark testing then measures how these movements interact with leverage. These results are subsequently used to evaluate whether the property targets and margin tiers produce the intended difficulty.

The calibration loop is therefore:

`Market Price Paths → Data Integrity Checks → Portfolio Tests → Leverage Outcomes → Best-Case Benchmarks → Target Thresholds → Gameplay Feasibility Check`

This process helps ensure that the game's financial targets are supported by the simulated market rather than imposed independently of the dataset.

The benchmark outputs also provide quantitative evidence for comparing Scenario 1 and Scenario 2 under the same financial assumptions.

### 2.6 Collaborative Financial-Mechanic Ideation & Calibration

In addition to my direct responsibility for market data and quantitative calibration, I actively contributed to the development of the project's financial mechanics through team discussions, iterative feedback, and quantitative feasibility checks.

While the formal financial and risk logic was documented by the **Mechanism Designer**, I contributed to the **ideation, challenge, and refinement of these mechanics**, particularly by using the market datasets and benchmark results to assess whether proposed rules would produce reasonable gameplay outcomes.

Key collaborative contributions included:

- **Margin & Target Calibration:** Raised and discussed the need to quantitatively test leverage tiers against achievable portfolio returns rather than selecting margin levels and property targets arbitrarily. Portfolio benchmark results were used during these discussions to evaluate and refine the final **1.0x / 2.0x / 3.0x / 4.0x margin structure** and **3.0x / 20.0x / 100.0x property targets**.

- **Maintenance Margin & Liquidation Discussion:** Participated in discussions on how the maintenance-margin threshold should interact with the available leverage tiers, helping evaluate whether the liquidation trigger was sufficiently strict to create meaningful risk without making leveraged gameplay unplayable.

- **AM/PM Market Constraint Discussion:** Contributed feedback on the session structure and price-movement constraints so that the simulated price paths remained compatible with the intended gameplay volatility and Phase 6 crash. The finalized market-data rule applies the ±30% limit to each complete 300-second phase, with continuous prices across the AM/PM boundary.

- **Bank Savings Mechanic:** Proposed and discussed the inclusion of Bank Savings as a supporting alternative to stock exposure. Contributed to simplifying the final mechanic into a fixed **4.75% return after each completed AM/PM session**, allowing savings to provide a predictable low-risk allocation option without replacing leveraged stock trading as the main game mechanic.

- **Iterative Mechanic Review:** Continuously reviewed proposed financial rules against the generated market paths and benchmark portfolio outcomes, identifying cases where a mechanic could make a target excessively easy, mathematically unattainable under tested strategies, or inconsistent with the intended risk-return trade-off.

My contribution in this area was therefore primarily **collaborative ideation and quantitative feedback**, while the Mechanism Designer remained responsible for formalizing the final financial formulas and rules in the project documentation.


## 3. Individual Footprint Self-Check (Midterm Checklist Section 7)

1. **My Main Responsibility:**  
   Designing, constructing, calibrating, and validating the market scenario data and quantitative benchmark models used by Free Fall 2.0. This includes both market-data generation and the calibration of target thresholds and margin tiers.

2. **My Most Important Output So Far:**  
   The two finalized market scenario datasets, `market_scenario_1.csv` and `market_scenario_2.csv`, which each provide 1,800-second deterministic price paths for 50 tradable assets across all 6 market phases, together with `best_case.py` and its portfolio optimization outputs. These files support evaluation of achievable portfolio outcomes and calibration of the game's financial difficulty.

3. **Where the Evidence is Located:**  
   In the repository at `data/` and `analysis/`, including:
   - [market_scenario_1.csv](../../data/market_scenario_1.csv)
   - [market_scenario_2.csv](../../data/market_scenario_2.csv)
   - [market_scenario_audit_1.xlsm](../../data/audit/market_scenario_audit_1.xlsm)
   - [market_scenario_audit_2.xlsx](../../data/audit/market_scenario_audit_2.xlsx)
   - [best_case.py](../../analysis/best_case.py)
   - [best_case_calibration_targets_3x_20x_100x.md](../../analysis/best_case_calibration_targets_3x_20x_100x.md)
   - [whole_share_srlp_summary.csv](../../analysis/whole_share_srlp_summary.csv)
   - [whole_share_srlp_cycles.csv](../../analysis/whole_share_srlp_cycles.csv)
   - [whole_share_srlp_buy_allocations.csv](../../analysis/whole_share_srlp_buy_allocations.csv)
   - [whole_share_srlp_margin_audit.csv](../../analysis/whole_share_srlp_margin_audit.csv)
   - [scenario_tier_comparison.csv](../../analysis/scenario_tier_comparison.csv)
   - [target_calibration_3x_20x_100x.csv](../../analysis/target_calibration_3x_20x_100x.csv)
   - [target_robustness_both_scenarios.csv](../../analysis/target_robustness_both_scenarios.csv)

4. **How My Output Supports the Group Product:**  
   Provides the market-data backbone consumed by the simulation engine and establishes the quantitative basis for evaluating the game's intended difficulty. The benchmark analysis helps determine which property targets are achievable under optimized trading strategies, while margin tiers provide progressively greater potential upside and different levels of exposure to margin and liquidation risk. I also use these quantitative results to provide feedback during the team's development and refinement of the financial mechanics.

5. **Planned Improvements at Midterm and Subsequent Progress:**

   At midterm, the following improvements were identified:

   - Develop and calibrate **Scenario 2** as an alternative 1,800-second market path to reduce predictability and replay memorization.
   - Re-run portfolio benchmark tests against Scenario 2 to verify that the existing house-target thresholds and margin tiers remain feasible across different market paths.
   - Compare Scenario 1 and Scenario 2 outcomes to identify any unintended strategy that consistently dominates regardless of scenario.
   - Perform final dataset validation for phase transitions, AM/PM boundaries, price-limit compliance, ticker consistency, and missing or abnormal values before implementation.
   - Recalibrate target thresholds, leverage assumptions, or asset movements if testing shows that any difficulty level is either mathematically unrealistic or excessively easy.
   - Continue providing quantitative feedback on financial mechanics as the prototype is implemented to ensure that coded gameplay remains consistent with the calibrated dataset and intended risk-return structure.

   **Subsequent progress (October 2026):**

   Scenario 2 was developed and validated. Both market datasets underwent data-integrity checks and corrections for price continuity, phase-level constraints and numeric consistency.

   The best-case optimizer was extended to evaluate both scenarios using concentrated Dynamic Programming and staggered re-leveraging MILP under fixed 2.0x, 3.0x and 4.0x leverage tiers.

   The resulting outputs now include scenario-specific trading cycles, portfolio allocations, margin audits, combined performance comparisons, and robustness checks for the **3.0x / 20.0x / 100.0x** property targets.

   Remaining work includes confirming dataset integration with the final game engine, reconciling any outstanding differences between optimizer and implemented settlement rules, and evaluating difficulty through actual player testing.

---

**Individual Contribution Statement:** My contribution is not simply collecting stock prices. I designed and validated structured market environments and used reproducible portfolio analysis to evaluate whether the game meaningfully exposes players to the trade-off between return, leverage, margin safety and liquidation risk.
