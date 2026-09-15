# OBJECTIVE INDIVIDUAL CONTRIBUTION EVIDENCE

**Course:** Technology Applications in Banking and Finance (NHA408E) - FTU 2026  
**Project:** Free Fall 2.0 (Group 6)  
**Member:** Cáp Phan Quang Khánh  
**Student ID:**  
**Assigned Role:** Scenario Designer  

---

## 1. Executive Summary of Responsibilities

As the **Scenario Designer**, my core responsibility is translating the project's deterministic market scenario and financial mechanics into structured player-facing scenarios, user-flow paths, events, and decision points. My work connects the six-phase market environment with the actions available to players, allowing different player decisions to lead to different financial consequences and risk states.

| Area | Responsibility | Concrete Repository Deliverable |
|---|---|---|
| **Scenario Tree & User Flow Design** | Generate step-by-step user-flow paths based on the deterministic market scenario, including normal, alternative, and critical-risk paths. | `USER_FLOW.md` |
| **Six-Phase Scenario Design** | Translate the six market phases into a progressive scenario structure from deceptive positive signals to market growth, euphoria, and negative shock. | `MARKET_DATASET.md`, `SOLUTION_STRUCTURE.md` |
| **Phase 1 News & Event Design** | Generate Phase 1 market and company-specific news corresponding to the **Fake Positive News** environment and the intended player behaviour. | Phase 1 News / Event Script |
| **Player Action Mapping** | Map the available player decisions to the project's defined inputs, including Buy / Sell / Hold, asset selection, volume, margin toggle, and Bank Savings. | `INPUT_DICTIONARY.md`, `USER_FLOW.md` |
| **Scenario Decision Paths** | Define how different player actions lead to alternative scenario paths, financial-state updates, margin-risk states, and subsequent decisions. | `USER_FLOW.md`, `FEATURE_MAP.md`, `SOLUTION_STRUCTURE.md` |
| **Behavioral Scenario Design** | Connect market conditions, information, and player decisions to the project's behavioral-finance objectives, including leverage blindness, FOMO, greed, complacency, and risk management. | `PROJECT_PROPOSAL.md`, `README.md`, `SOLUTION_STRUCTURE.md` |

---

## 2. Scenario Design & Implementation Details

### 2.1 Scenario Tree & User Flow Design (`USER_FLOW.md`)

My main contribution is designing the player-flow paths that translate the market scenario into a sequence of user decisions and system consequences.

The project's overall learning loop is:

> **Scenario → Information → Decision → Financial State Update → Consequence → Feedback → Next Decision**

This structure ensures that market events are connected directly to player decisions and their resulting financial states.

For Phase 1, the main user journey is structured as:

> **Start → Initialize Account → Enter Dashboard → Observe Market → Submit Action → Validate → Execute → Update Financial State → Evaluate Margin Risk → Continue / Liquidate → Calculate Target Progress → Proceed to Phase 2**

The user-flow documentation defines the process from the initial screen through market observation, player actions, order validation, execution, financial-state updates, margin evaluation, and phase transition.

I organized the scenario paths into three main categories:

- **Happy Path** — normal valid interactions where the player remains solvent and reaches the end of the phase.
- **Alternative Paths** — valid choices that lead to different holdings, cash positions, or financial outcomes.
- **Error & Critical-Risk Paths** — invalid actions, margin breaches, forced liquidation, and Game Over states.

The detailed Phase 1 interaction therefore follows:

> **Observe Market → Submit Action → Validate → Execute → Update Balances → Recalculate Financial State → Check Margin Status → Refresh UI → Observe Market**

The loop continues until the phase ends, forced liquidation occurs, or another terminal state is reached.

---

### 2.2 Six-Phase Scenario Structure (`MARKET_DATASET.md` & `SOLUTION_STRUCTURE.md`)

I based the Scenario Tree on the six-phase deterministic market lifecycle defined in the project documentation.

The market contains six phases of 300 seconds each within the 1,800-second simulation:

| Phase | Phase Name | Market Dynamics | Scenario Purpose |
|---|---|---|---|
| **1** | Fake Positive News | Early uncertainty and deceptive bullish signals | Encourage players to consider entering the market and taking early exposure |
| **2** | True Positive News | Fundamental validation and stronger positive momentum | Reinforce confidence in earlier decisions |
| **3** | Bull Market | Broad rally and accelerating market movement | Encourage players to consider higher leverage and larger targets |
| **4** | Strong Growth (FOMO) | Rapid expansion and increasing volatility | Create pressure to participate and increase exposure |
| **5** | Market Euphoria & Bull Traps | Peak valuations with misleading recovery signals | Test whether players take profits or continue holding risky positions |
| **6** | Negative Shock | Severe market decline and systemic crash | Expose the consequences of excessive leverage and inadequate risk management |

The scenario progression is also connected to the project's intended behavioral progression:

> **Understand Leverage → Build Confidence → Recognize Vulnerability → Respond to Warning Signs → Manage Liquidity & Exposure → Reduce Liquidation Risk**

This structure forms the main backbone of the Scenario Tree, where the same underlying deterministic market path can lead to different player outcomes depending on the decisions made during each phase.

---

### 2.3 Phase 1 News & Event Script

My completed news/event-design work so far focuses on **Phase 1 — Fake Positive News**.

Phase 1 is designed as the initial information environment of the simulation. The market dataset describes this phase as an early period of uncertainty where temporary positive movements and decoy signals can create misleading opportunities.

The project also defines Phase 1 as a period in which players should learn the opportunity cost of holding cash while becoming exposed to the attractiveness of borrowing and increased purchasing power.

Based on this structure, I generated Phase 1 news at two levels:

#### Market-Level News

The Phase 1 market-news queue contains three fixed public-information events:

1. **0:00 — South Korea's Semiconductor Outlook Strengthens**
   - Strong AI-related demand supports expectations for Korean semiconductor exports and memory-chip demand.
   - Major Korean technology stocks are highlighted as part of the AI infrastructure growth theme.

2. **2:30 — AI Infrastructure Investment Supports Korean Chipmakers**
   - Continued AI data-center spending strengthens expectations for HBM and advanced semiconductor demand.
   - The positive sector outlook supports broader interest in Korean semiconductor equities and ETFs.

3. **4:00 — Investor Sentiment Improves Across Korean Technology Stocks**
   - Improving risk appetite draws attention back to large-cap technology and semiconductor shares.
   - Market participants remain optimistic while the sector remains sensitive to global demand and valuation changes.

These are fixed Phase 1 information events and are designed to provide context without revealing or modifying the predetermined synthetic price path.

#### Company / Asset-Specific News

I also generated company/asset-specific news for the five assets used in the Phase 1 information environment:

| Asset | Phase 1 News Focus |
|---|---|
| **Vintrumite (SK hynix data)** | AI memory demand, HBM, future memory solutions, full-stack memory solutions and 3D memory |
| **Samsung Electronics** | AI partnerships, semiconductor strategy, ASML collaboration and next-generation semiconductor manufacturing |
| **KODEX Semiconductor** | Improving expectations for AI-driven memory and chip demand and broader semiconductor-sector exposure |
| **KODEX Leverage** | Positive Korean market sentiment and the effect of approximately 2× KOSPI200 daily exposure |
| **TIGER Semiconductor TOP10** | Strength of major Korean chipmakers, sector concentration and semiconductor-cycle sensitivity |

The asset-specific information is designed to provide plausible public context while maintaining the game's predetermined synthetic price path.

---

### 2.4 Player Action Mapping (`INPUT_DICTIONARY.md` & `FEATURE_MAP.md`)

I used the project's Input Dictionary and Feature Map to define the actions that can be incorporated into the Scenario Tree.

The main player-controlled inputs relevant to scenario decisions are:

- `target_house_type`
- `margin_tier`
- `orders`
- `bank_savings`

The `orders` variable represents **Buy / Sell / Hold** decisions together with the selected asset and volume. The `margin_tier` determines the player's available leverage capacity, while `bank_savings` represents funds allocated outside direct market exposure.

The Feature Map similarly identifies the core user-facing actions and processes, including asset selection, order entry, Buy / Sell / Hold decisions, margin selection, cash management, and Bank Savings.

I therefore structured the main player decisions as follows:

| Player Action | Scenario Meaning | Main Financial Consequence |
|---|---|---|
| **Buy** | Increase exposure to a selected asset | Increases portfolio exposure and can increase potential gains or losses |
| **Sell** | Reduce or exit an existing position | Reduces exposure and realizes the resulting trading outcome |
| **Hold** | Maintain the existing position | Keeps the player exposed to subsequent market movements |
| **Select Margin Tier** | Choose the level of available leverage | Higher leverage increases purchasing power and financial risk |
| **Use Cash / Preserve Liquidity** | Maintain funds outside risky positions | Provides greater flexibility when market conditions deteriorate |
| **Put Money into Bank Savings** | Allocate funds to a lower-risk alternative | Reduces direct market exposure while generating the simulated savings return |

The project's core interaction is structured around:

> **Buy / Sell / Hold → Position Size → Cash / Margin → Risk Management**

---

### 2.5 Scenario Decision Paths

I developed the scenario decision paths by connecting the information presented to the player with the actions defined in the project's Input Dictionary and User Flow.

| Scenario Condition | Player Decision | Relevant Input / Action | Possible Next Scenario Path |
|---|---|---|---|
| Positive Phase 1 market information | Enter the market | Buy + Asset + Volume | Continue observing the market with an active position |
| Positive information on a specific asset | Trade the relevant asset | Buy / Asset / Volume | Portfolio exposure changes and the player continues monitoring the market |
| Player does not want to change the position | Maintain current position | Hold | Continue to the next market tick with the existing position |
| Player wants to reduce an existing position | Exit or reduce position | Sell | Cash and shares are updated before the next decision |
| Player wants greater purchasing power | Use a selected margin tier | Margin Tier + Margin Toggle | Higher exposure and corresponding margin risk |
| Player wants to keep funds outside direct market exposure | Allocate funds to savings | Bank Savings | Funds are transferred to Bank Savings and the player continues the simulation |
| Market movement changes the player's financial state | Reassess position | Buy / Sell / Hold | Continue through the decision loop based on the updated financial state |
| Margin condition reaches a critical state | Continue or respond through available actions | Buy / Sell / Hold / Cash Management | Normal continuation, forced liquidation, or Game Over depending on the financial state |

This structure follows the documented user-flow sequence:

> **Observe Market → Submit Action → Validate → Execute → Update Balances → Recalculate Financial State → Check Margin Status → Refresh UI → Observe Market**

It also ensures that scenario branches are based on the project's existing inputs and financial logic rather than introducing unsupported trading mechanisms.

---

### 2.6 Connecting Player Decisions to Scenario Consequences

The Scenario Tree is designed so that player decisions become increasingly important as the market progresses.

For example, the same Buy decision can have different consequences depending on the market phase and the margin tier selected.

The project's margin specification defines the following exposure choices:

| Margin Tier | Maximum Leverage | Risk Level |
|---|---:|---|
| **Cash** | 1.0× | Zero liquidation risk |
| **2×** | 2.0× | Moderate risk |
| **3×** | 3.0× | High risk |
| **4×** | 4.0× | Extreme risk |

The assumed maintenance margin is 20%, with the risk of a margin call increasing significantly as leverage increases.

This allows the Scenario Tree to produce progressively different consequences:

> **Low Exposure → Market Movement → Manageable Financial Change**

versus:

> **High Leverage → Market Decline → Falling Equity → Margin Pressure → Margin Call → Forced Liquidation**

The project's overall scenario structure is therefore not simply a narrative story. It is designed to make the financial consequences of different decisions visible through the simulation.

---

## 3. Individual Footprint Self-Check (Midterm Checklist Section 7)

1. **My Main Responsibility:**  
   Designing the player-facing scenario structure of Free Fall 2.0 by generating user-flow paths based on the market scenario, developing phase-based events and news, mapping available player actions, and creating scenario decision paths.

2. **My Most Important Output So Far:**  
   The Scenario Tree and user-flow paths based on the six-phase market scenario, the Phase 1 market and company-specific news/event design, and the scenario decision paths connecting player actions with financial and risk consequences.

3. **Where the Evidence is Located:**  
   In the project documentation and scenario materials, including:
   - `USER_FLOW.md`
   - `MARKET_DATASET.md`
   - `INPUT_DICTIONARY.md`
   - `FEATURE_MAP.md`
   - `PROJECT_PROPOSAL.md`
   - `SOLUTION_STRUCTURE.md`
   - `ASSUMPTIONS.md`
   - `SAMPLE_INPUT_OUTPUT.md`
   - Phase 1 News / Event Script

4. **How My Output Supports the Group Product:**  
   My work connects the deterministic market scenario with the player's experience. The market dataset provides the six-phase market environment, while the project's input and financial-logic documents define the actions and consequences available to the player. My Scenario Tree, Phase 1 event design, and scenario decision paths organize these elements into understandable decision paths, supporting the project's core learning loop of **Scenario → Information → Decision → Financial State Update → Consequence → Feedback → Next Decision**.

5. **What I Will Improve or Complete Next (Post-Midterm):**  
   - Extend the event and news design from Phase 1 to the remaining market phases.
   - Expand the Scenario Tree to cover additional alternative and critical-risk paths.
   - Further develop the scenario decision paths according to the different market conditions across the six phases.
   - Connect phase-specific events more clearly with the project's defined financial outcomes, including Target Progress, Margin Health, Margin Calls, Forced Liquidation, and final narrative outcomes.
   - Refine the scenario branches so that player decisions remain directly connected to the project's behavioral-finance learning objectives.
