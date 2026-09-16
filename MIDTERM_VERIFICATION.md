# MIDTERM VERIFICATION

**Course:** Technology Applications in Finance and Banking (NHA408E)  
**Project:** Free Fall 2.0  
**Group:** 6  
**Date:**  16/09/2026
**Team Representative:**  
**Repository:**  https://github.com/FTU-Legacy-63/G06


# A. GROUP VERIFICATION

## 1. What is the biggest issue your team still needs to solve before Week 6?

Our biggest issue is clearly differentiating **Free Fall 2.0 (K63)** from **Free Fall 1 (K62)**. Although both projects are financial learning games based on market-crisis scenarios and require players to make investment decisions, K63 needs to establish a clearly distinct core gameplay experience and learning objective.

Free Fall 2.0 focuses on **leverage blindness and the consequences of margin trading**. Its core mechanics involve **Initial Capital, Margin Tier, Margin Debt, Equity, Effective Leverage, Margin Ratio, Margin Calls, Forced Liquidation, and Property Target Progress**. The player experiences how leverage can amplify both gains and losses and create liquidity and solvency pressure during a market downturn.

Therefore, our main issue before Week 6 is ensuring that these **margin-trading and leverage mechanics remain central to K63**, rather than allowing the game to appear too similar to K62's broader financial decision-making structure.


## 2. Why is this issue important?

This issue is important because the core identity of Free Fall 2.0 depends on its specific learning objective and financial mechanics. If the similarities between K63 and K62 are not clearly addressed, our project may be perceived as a variation of the same product rather than a distinct simulation.

For K63, the player should understand the relationship between **leverage, market price movements, equity, margin requirements, margin calls, and forced liquidation**. If these elements are not sufficiently central to the gameplay, the project could lose its intended focus on **leverage blindness**.


## 3. What has your team done about this issue so far?

Our team has reviewed the existing K63 structure and identified the main elements that distinguish it from K62. We focused on K63's **financial logic, player inputs, market price paths, and margin-related outcomes**.

We identified that K63 is centered on direct portfolio actions such as **Buy, Sell, and Hold**, with **Bank Savings as a supporting allocation option**, while its financial engine continuously tracks **Portfolio Value, Cash, Bank Savings, Margin Debt, Equity, Effective Leverage, and Margin Ratio**. We also incorporated the **Margin Call and Forced Liquidation sequence** and connected the player's financial position to **Property Target Progress**.

Through this review, we found that the strongest differentiation for K63 is its focus on the **financial consequences of leveraged trading**, rather than simply making investment decisions during a market crisis.


## 4. What will your team do next about this issue?

Before or during Week 6, our team will review the **MVP flow and interface** to ensure that the margin-trading mechanism remains the central gameplay element.

We will specifically test whether the player can clearly experience the sequence of:

**Selecting Initial Capital and a Margin Tier → Placing Trades → Experiencing Market Movements → Observing Changes in Equity and Margin Ratio → Responding to Margin Pressure → Potentially Experiencing Forced Liquidation**

We will also remove or avoid features that make K63 unnecessarily similar to K62 and keep the MVP focused on its own learning objective: **demonstrating how leverage can amplify potential gains while also increasing the risk of rapid financial loss and forced liquidation**.



# B. MEMBER CONTRIBUTION VERIFICATION

| Member | What did this member actually produce? | How is it used in the project? | What can this member personally explain, calculate, demonstrate, or reproduce? |
|---|---|---|---|
| **Trần Hữu Dụ** | Produced the project's **financial-mechanic framework and rulebook**, including portfolio/equity formulas, leverage and Margin Ratio logic, the **20% maintenance-margin threshold**, T+0.5 settlement rules, Bank Savings rule, target matrix, and core Phase 1 feature flow. Main outputs include `SOLUTION_STRUCTURE.md`, `ASSUMPTIONS.md`, `INPUT_DICTIONARY.md`, `FEATURE_MAP.md`, `SAMPLE_INPUT_OUTPUT.md`, and `MIDTERM_REVIEW.md`. | Provides the mathematical and rule-based foundation for the simulator. These rules determine how player actions change cash, savings, exposure, margin debt, equity, leverage, target progress, and forced-liquidation states. They also provide specifications for the backend, scenario, dataset, and UI work. | Can **derive and calculate Gross Exposure, Net Equity, Effective Leverage, Margin Ratio, and Target Progress**; explain the **20% maintenance-margin threshold** and its relationship with effective leverage; reproduce margin-call and liquidation sample cases; and explain the T+0.5 settlement, Bank Savings, margin-tier, and target rules. |
| **Nguyễn Hồng Nguyên** | Produced `market_scenario.csv`, containing a **1,800-second × 50-asset deterministic market dataset**, and designed/calibrated asset price paths across the six phases. Also produced `best_case_portfolio_combos.csv` and `best_case_portfolio_summary.csv` to benchmark achievable returns under **Cash / 2× / 3× / 4×** strategies. Contributed quantitative feedback to the development of target, margin, market-constraint, liquidation, and savings mechanics. | Provides the market-data backbone consumed by the simulation engine. Portfolio benchmarks are used to test gameplay feasibility and calibrate the **3× / 20× / 100× property targets** and **1× / 2× / 3× / 4× leverage structure**, preventing targets from being either mathematically impossible or trivially easy. | Can **reproduce the market-scenario dataset and portfolio benchmark tests**; explain driver/non-driver asset behavior and six-phase price paths; calculate achievable wealth ceilings under different leverage levels; demonstrate how benchmark results support target and margin calibration; and validate AM/PM price constraints and Phase 6 crash behavior. |
| **Cáp Phan Quang Khánh** | Produced the **Scenario Tree and user-flow paths**, six-phase player-facing scenario structure, Phase 1 market/company news and event scripts, player-action mapping, and alternative/critical-risk decision paths. Main outputs are reflected in `USER_FLOW.md`, `MARKET_DATASET.md`, `INPUT_DICTIONARY.md`, `FEATURE_MAP.md`, and related scenario materials. | Converts the deterministic market path and financial rules into the player experience: **Scenario → Information → Decision → Financial State Update → Consequence → Feedback → Next Decision**. It determines what information players receive, what decisions they face, and how those decisions connect to subsequent financial and risk states. | Can **reproduce and walk through the Scenario Tree/User Flow**; explain the purpose of each of the six phases; demonstrate Happy, Alternative, and Critical-Risk paths; map Buy/Sell/Hold/Margin/Savings decisions to financial consequences; and explain or recreate the Phase 1 news/event sequence. |
| **Nguyễn Quang Minh** | Produced the executable backend implementation, including `src/simulation_engine.py`, `src/game_controller.py`, `tests/test_simulation_engine.py`, and `interactive_demo.py`. Integrated the 1,800-tick market dataset and implemented portfolio valuation, margin monitoring, Bank Savings, T+0.5 settlement delays, phase transitions, order execution, forced liquidation, and automated tests. | Converts the project's documented financial rules, workflow, and market dataset into **executable simulation logic**. The engine maintains player state, processes orders and price ticks, evaluates margin conditions, triggers liquidation, and provides backend outputs for the web interface. | Can **run and demonstrate the simulation engine**; trace a player state through price and order updates; explain the code implementation of financial formulas and state transitions; integrate the CSV price data; and reproduce automated tests for leveraged wipeout, cash-only positions, Bank Savings, and T+0.5 settlement. |
| **Triệu Đức Lương** | Produced the **UI/UX design system and trading-terminal interface architecture**, including the dark-mode visual system, Introduction screen, Account Overview, live market display, order-entry interface, Margin Health and Leverage gauges, Property Target Progress, news display, and frontend component specifications/wireframes. | Translates backend financial states and scenario information into an understandable player-facing interface. It allows players to monitor Net Worth, Cash, Bank Savings, Margin Debt, Effective Leverage, Margin Health, Target Progress, prices, and news, and to execute trading decisions during the simulation. | Can **reproduce and explain the UI hierarchy and wireframes**; demonstrate the live trading interface; explain how backend variables map to visual components; demonstrate Margin Health and Target Progress visualization; and justify the information hierarchy, warning states, and interaction design used in the simulator. |
