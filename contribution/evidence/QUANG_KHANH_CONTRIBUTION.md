# OBJECTIVE INDIVIDUAL CONTRIBUTION EVIDENCE

Course: Technology Applications in Banking and Finance (NHA408E) – FTU 2026  
Project: Free Fall 2.0 (Group 6)  
Member: Cáp Phan Quang Khánh  
Student ID: 2412380020  
Assigned Role: Scenario Designer / Content Lead

---

# 1. Executive Summary of Responsibilities

As the Scenario Designer, my primary responsibility is developing the player-facing scenarios and news content for Free Fall 2.0. My work focuses on creating market narratives across six phases, preparing news for two different scenarios, and connecting the information presented to players with the decisions they can make throughout the simulation.


| Area | Responsibility | Concrete Repository Deliverable |
|---|---|---|
| Scenario Tree & User Flow Design | Generate step-by-step user-flow paths based on the deterministic market scenario, including normal, alternative, and critical-risk paths. | `docs/user_flow.md` |
| Scenario-Specific News and Events | Develop market/industry news and asset-specific information across the six phases for both deterministic scenarios. | `docs/Scenario2 news.md`; `docs/Scenario1 news.md` |
| Six-Phase Scenario Narrative | Translate the six market phases into a progressive scenario structure from deceptive positive signals to market growth, euphoria, and negative shock. | `docs/Scenario1 news.md`; `docs/Scenario2 news.md`; `archive/Week 2/Solution_Structure.md`; `archive/Week 5/Market_Dataset.md` |
| Input Dictionary & Player Action Mapping | Use the existing input definitions to identify player choices relevant to the scenarios and explain how these choices relate to the narrative. | `Week 3/INPUT_DICTIONARY.md`; `docs/user_flow.md`  |
| Scenario Decision Paths | Structure scenario-related decision paths by connecting market information and player choices with possible consequences. | `SOLUTION_STRUCTURE.md`; `docs/user_flow.md` |
| Scenario Consistency | Ensure news content is appropriate for the intended phase and consistent with the relevant scenario context without changing underlying market data. | `docs/Scenario1 news.md`; `docs/Scenario2 news.md`; `docs/user_flow.md`  |
| Behavioral Learning Through Scenarios | Design narratives that expose players to optimism, FOMO, overconfidence, bull-trap risk, and the consequences of excessive leverage. | `archive/Week 2/Project_Proposal.md`; `archive/Week 2/Solution_Structure.md` |archive

My contribution is concentrated on the scenario and content layer of the project. The market datasets, predetermined price paths, Input Dictionary, financial rules, and simulation engine provide the existing foundation on which I develop the scenarios. I do not claim responsibility for creating these underlying components.

---

# 2. Scenario Design & Implementation Details

## 2.1 Six-Phase Scenario Structure (`docs/user_flow.md`)

My main responsibility is to develop the narrative progression across the six phases of Free Fall 2.0. Each phase presents a different market environment and creates a different behavioral challenge for players.

The project's overall learning loop is:

Scenario → Information → Decision → Financial State Update → Consequence → Feedback → Next Decision

I organized the scenario paths into three main categories:

Happy Path — normal valid interactions where the player remains solvent and reaches the end of the phase.
Alternative Paths — valid choices that lead to different holdings, cash positions, or financial outcomes.
Error & Critical-Risk Paths — invalid actions, margin breaches, forced liquidation, and Game Over states.

The simulation lasts 1,800 seconds and is divided into six phases of 300 seconds each. I use this existing structure to organize the scenario news and develop a progressive narrative throughout the game.

| Phase | Phase Name | Market Dynamics | Scenario Purpose |
|---|---|---|---|
| 1 | Fake Positive News | Uncertainty and misleading bullish signals | Introduce positive information that may encourage premature market entry or excessive confidence. |
| 2 | True Positive News | More credible positive signals and improving market sentiment | Strengthen the positive narrative and test whether players become more confident in their positions. |
| 3 | Bull Market | Broad upward momentum | Show how rising prices can encourage players to increase exposure or pursue more ambitious targets. |
| 4 | Strong Growth / FOMO | Rapid growth and increasing pressure to participate | Illustrate the temptation to follow market momentum and take on greater risk. |
| 5 | Market Euphoria | Peak optimism, volatility, and bull-trap risk | Test whether players continue pursuing gains or recognize the importance of managing their exposure. |
| 6 | Negative Shock | Severe market decline | Reveal the potential consequences of excessive leverage and inadequate risk management. |

My role is to communicate this progression through the scenario narrative and phase-specific news. The existing market data determines the underlying price movements, while my content provides the information and context that players encounter as those movements unfold.

## 2.2 Scenario 1 News & Event Design (`docs/Scenario1 news.md`)

Scenario 1 presents a market narrative built around the Korean semiconductor and technology investment environment. My contribution is to develop industry-level context and asset-specific news that evolves across the six phases.

The content introduces the market environment, develops positive expectations, increases the pressure to participate during the growth phases, and eventually presents a more challenging environment as the market deteriorates.

The scenario covers five assets:

| Asset | Main News Drivers | Intended Scenario Context |
|---|---|---|
| Vintrumite | AI memory demand, HBM development, advanced memory solutions, and semiconductor investment | Present the growth narrative surrounding AI-related memory demand while retaining uncertainty about future market performance. |
| Samsung Electronics | Semiconductor strategy, AI partnerships, manufacturing capabilities, and next-generation chip development | Provide company-specific information within the broader Korean technology and semiconductor market. |
| KODEX Semiconductor | Semiconductor-sector demand, memory-chip outlook, and industry-wide sentiment | Represent broader exposure to changes in semiconductor market expectations. |
| KODEX Leverage | Korean equity-market momentum and leveraged market exposure | Provide context for the risks associated with leveraged market instruments. |
| TIGER Semiconductor TOP10 | Major Korean semiconductor companies, sector concentration, and semiconductor-cycle sensitivity | Illustrate the opportunities and risks associated with concentrated semiconductor exposure. |

The news content differentiates the assets rather than treating them as interchangeable investments. Company-specific developments, industry expectations, broad sector movements, and leveraged exposure provide different perspectives on the market environment.

Across the six phases, the news moves from potentially misleading positive signals to stronger growth expectations, FOMO, market euphoria, and the final negative shock.

The purpose is not to predict or create asset prices. Instead, the news provides contextual information that players can use when deciding whether to buy, sell, or hold their positions.

## 2.3 Scenario 2 News & Event Design (`docs/Scenario2 news.md`)

Scenario 2 uses a separate narrative and asset universe. My contribution is to develop news that reflects the relevant industries and companies while maintaining the overall six-phase behavioral progression.

Unlike Scenario 1, which focuses on semiconductor and Korean technology investments, Scenario 2 includes assets from shipping, the broader Korean equity market, semiconductor equipment, batteries, and automotive manufacturing.

| Asset | Main News Drivers | Intended Scenario Context |
|---|---|---|
| HMM | Shipping demand, freight rates, global trade conditions, and maritime-sector developments | Illustrate how changes in global trade and shipping conditions can influence market expectations. |
| KODEX 200 | Korean equity-market performance, large-cap sentiment, and broad market movements | Represent broader Korean equity exposure and changes in overall market risk appetite. |
| Wonik IPS | Semiconductor manufacturing equipment demand, investment cycles, and technology-sector capital expenditure | Connect company-specific developments with changes in semiconductor investment expectations. |
| LG Energy Solution | Battery demand, electric-vehicle market conditions, production capacity, and battery-sector competition | Illustrate how changing industry expectations can influence investor sentiment. |
| Hyundai Motor | Vehicle demand, automotive-sector developments, export conditions, and electric-vehicle strategy | Present company-specific information within the broader automotive and Korean equity-market environment. |

The news is structured to evolve throughout the six phases. Early information establishes the context, subsequent developments change the market narrative, and the later phases introduce greater uncertainty and downside risk.

Although Scenario 1 and Scenario 2 follow the same broad phase structure, their news content differs according to their respective assets and industry drivers. This provides two distinct narrative experiences within the same simulation framework.

The underlying price paths remain determined by the project's existing scenario data. My responsibility is to develop the corresponding narrative rather than create or modify that data.

## 2.4 Input Dictionary & Player Action Mapping (`Week 3/INPUT_DICTIONARY.md`)

The Input Dictionary provides the existing definitions of the inputs used by the simulation. I refer to this document when developing scenario content so that the news and narrative remain relevant to the decisions available to players.

My role is not to create the Input Dictionary or implement its variables. Instead, I use the documented inputs to understand the initial conditions, player choices, and scenario context that should be reflected in the narrative.

| Input Name | Meaning / Possible Values | Relevance to Scenario Design |
|---|---|---|
| `assigned_scenario_capital` | Scenario-capital selection represented by 1 / 2 / 3 in the documented MVP inputs | Provides context for the initial conditions under which the player experiences the scenario. |
| `fixed_price_path` | Predetermined market price path across the phases | Provides the market context against which phase-specific news and narrative developments are designed. |
| `target_house_type` | Selection of the player's property target | Helps explain why players may feel pressure to pursue higher returns as the scenario progresses. |
| `initial_capital` | The player's initial capital | Establishes the starting financial context for the player's experience. |
| `initial_margin_ratio` | Initial margin setting, with values described in the original MVP dictionary | Provides context for the player's initial leverage configuration and the risk-related narrative. |
| `orders` | Trading decisions involving Buy / Sell / Hold, with the relevant asset and volume | Identifies the main player actions around which scenario decision points can be organized. |

The following table explains how the documented player actions relate to the scenario narrative.

| Player Action | Scenario Meaning | Relevance to My Contribution |
|---|---|---|
| Buy | Enter or increase a position in a selected asset | News can provide context for the player's decision to enter the market or increase exposure. |
| Sell | Reduce or close an existing position | Scenario developments can create opportunities for players to reconsider their exposure. |
| Hold | Maintain the current position | News provides information that players can evaluate before deciding whether to maintain their positions. |
| Select Margin Tier | Choose the available leverage configuration defined by the game | The narrative can demonstrate the temptation and risks associated with increasing exposure. |
| Select Property Target | Choose the target the player wants to reach | The target can provide context for the player's level of ambition and willingness to take risks. |
| Use Bank Savings | Allocate funds to the savings mechanism | The narrative can provide context for the trade-off between market exposure and preserving funds outside direct stock-market positions. |

By using the Input Dictionary as a reference, I can design news and decision points that correspond to the existing game mechanics. This keeps the scenario content connected to actual player choices without requiring me to create the underlying inputs or financial calculations.

The variable names and configurations in the final report should follow the final version of `Week 3/INPUT_DICTIONARY.md` and the implemented game.

## 2.5 Scenario Decision Paths (`SOLUTION_STRUCTURE.md` & `docs/user_flow.md`)

My scenario decision-path contribution focuses on organizing the narrative around the choices players may face as market conditions change.

I use the existing Solution Structure and user-flow documentation as references for understanding the intended player experience and the relationship between scenario conditions, player actions, and possible outcomes. These documents provide the existing project structure; my contribution is to develop the scenario-related content that fits within it.

The main decision paths can be summarized as follows:

| Scenario Condition | Player Decision | Relevant Input / Action | Possible Scenario Direction |
|---|---|---|---|
| Positive market information appears | Enter the market | `orders` — Buy, asset, and volume | The narrative continues with the player holding a market position and facing subsequent market developments. |
| News supports a specific asset | Consider trading that asset | `orders` — Buy / asset / volume | The player increases exposure to the selected asset and remains exposed to subsequent market movements. |
| The player expects further growth | Maintain the current position | `orders` — Hold | The player continues with the existing position as the scenario progresses. |
| Market information becomes less favorable | Reduce or close a position | `orders` — Sell / asset / volume | The narrative can emphasize the player's decision to reduce exposure as uncertainty increases. |
| The player wants greater purchasing power | Choose a higher margin configuration | Existing margin-tier setting | The narrative highlights the trade-off between greater exposure and increased risk. |
| The player wants to preserve funds | Retain cash or use Bank Savings | Existing cash-management options | The narrative emphasizes liquidity and alternatives to direct market exposure. |
| Market conditions deteriorate significantly | Reassess the current position | Buy / Sell / Hold and available account-management actions | The player faces a decision between maintaining exposure and reducing risk. |
| The player's financial condition reaches a critical state | Respond using the actions available in the game | Existing player actions and account-management options | The outcome may involve continued play, forced liquidation, or Game Over, depending on the implemented financial rules. |

These decision paths help structure the scenarios around meaningful choices rather than presenting news as isolated information.

The Solution Structure and user-flow documents are therefore supporting references for my scenario design. I do not claim authorship of the overall system structure or the underlying financial engine.

## 2.6 Scenario Design Principles and Behavioral Learning

My scenario content is designed to make the market environment understandable and engaging while supporting the project's financial-learning objectives.

The main principles are:

1. Phase progression: Each phase has a distinct narrative purpose and contributes to the overall development of the scenario.
2. Scenario differentiation: Scenario 1 and Scenario 2 use different asset universes and news drivers.
3. Asset differentiation: News reflects the relevant business, industry, or market exposure of each asset.
4. Consistency with existing data: The narrative is designed around the existing scenario conditions rather than creating or changing market prices.
5. Meaningful decisions: News and events provide context for the Buy / Sell / Hold decisions available to players.
6. Behavioral learning: The narrative illustrates how optimism, FOMO, overconfidence, and fear can influence investment decisions.
7. Risk awareness: Later phases create opportunities to understand the importance of liquidity management and controlling exposure during adverse market conditions.

Through these principles, my contribution supports the project's objective of teaching players about leverage and investment risk through a scenario-based simulation.

---

# 3. Individual Footprint Self-Check (Midterm Checklist Section 7)

## 1. Main Responsibility

My main responsibility is designing the player-facing scenarios and news content for Free Fall 2.0. This includes developing scenario-specific news for Scenario 1 and Scenario 2, organizing the narrative across six phases, and structuring scenario-related decision paths around the actions available to players.

## 2. Most Important Outputs So Far

My main outputs are the two scenario news documents covering the six-phase narrative progression. I also use the existing Input Dictionary, Solution Structure, and user-flow documentation as references to ensure that my scenarios correspond to the project's existing inputs, player actions, and intended gameplay.

## 3. Where the Evidence Is Located

The main repository evidence for my scenario-design contribution includes:

- `docs/Scenario1 news.md` 
- `docs/Scenario2 news.md`
- `Week 3/INPUT_DICTIONARY.md` 
- `SOLUTION_STRUCTURE.md` 
- `docs/user_flow.md` 
- `archive/Week 5/Market_Dataset.md`
- `archive/Week 2/Project_Proposal.md`

## 4. How My Work Supports the Group Product

My work transforms the existing market scenarios into player-facing narratives. The news provides contextual information, while the six-phase structure creates a progression of market conditions and behavioral challenges. By connecting the narrative to the actions already available in the game, my contribution helps players understand how their decisions may interact with optimism, FOMO, leverage, liquidity, and market declines.

The existing market data and financial rules determine the underlying movements and outcomes. My contribution focuses on presenting the scenario information and organizing the narrative around the decisions players may encounter.

## 5. What I Will Improve or Complete Next

- Continue refining the news content for Scenario 1 and Scenario 2 across all six phases.
- Check that the news remains consistent with the corresponding scenario conditions and does not contradict the predetermined price paths.
- Improve the differentiation between asset-specific news and broader market news.
- Refine the connection between phase-specific information and the player decisions relevant to each scenario.
- Review the Input Dictionary and Solution Structure references to ensure that the scenario descriptions remain consistent with the final project documentation.
- Strengthen the narrative progression from positive market expectations to FOMO, euphoria, and negative shock.
- Ensure that descriptions of possible financial consequences are consistent with the existing game rules without claiming responsibility for implementing those rules.

In summary, my individual contribution to Free Fall 2.0 is focused on scenario design and content. I develop the news and narratives that players experience across the two scenarios and six phases, using the project's existing inputs, solution structure, and financial mechanics as references. I do not claim responsibility for creating the underlying market data, predetermined price paths, or simulation engine.
