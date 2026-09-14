# FEATURE_MAP.md

## Product: Seoul Margin Crisis Simulator (2026 Korean Stock Market Simulation Game)
> **Goal:** Map the complete functional engine and Phase 1 interactive workflow directly to core vs. supporting features, validation logic, and team ownership before Week 6 implementation[cite: 3].

---

## 1. Feature Map by MVP Priority

Features are categorized into **Core Features** (must work for final product evaluation), **Supporting Features** (enhance usability, visual telemetry, and behavioral feedback), and **Removed / Postponed Features** (out of scope to protect technical feasibility)[cite: 3].
[ Seoul 2026 Crisis Simulator ]
                                             |
     +---------------------------------------+---------------------------------------+
     |                                       |                                       |
     ---

## 2. Feature Decision Table

Every planned feature has a concrete decision, operational purpose, and designated owner[cite: 3].

| Feature Name | Feature Type | Purpose in Product / Workflow | Decision | Owner[cite: 3] |
| :--- | :---: | :--- | :---: | :--- |
| **Scenario & Capital Assignment** | Core | Randomly assigns Scenario 1 or 2, sets starting cash ($10,000 USD / 20,000,000 KRW), and locks the 1,800s price series. | **Keep** | Nguyễn Hồng Nguyên *(Data Gatherer)* |
| **Housing Goal Selector** | Core | Player selects financial difficulty (`Small House 3.0x`, `Normal House 20.0x`, `ToLam Villa 100.0x`) to set the win-condition threshold. | **Keep** | Cáp Phan Quang Khánh *(Scenario Designer)* |
| **Margin Tier Selector** | Core | Configures player purchasing power (`Cash 1.0x`, `2x`, `3x`, `4x`) and sets initial debt borrowing capacity. | **Keep** | Trần Hữu Dụ *(Mechanism Designer)* |
| **1,800s Deterministic Tick Engine** | Core | Drives continuous 30-minute market progression across 6 distinct phases (300 seconds each). | **Keep** | Nguyễn Quang Minh *(Technical Developer)* |
| **Order Entry & Purchasing Power Validation** | Core | Validates Buy/Sell orders against available purchasing power; rejects invalid volumes with user-facing alerts. | **Keep** | Nguyễn Quang Minh *(Technical Developer)* |
| **Continuous Valuation Pipeline** | Core | Calculates Gross Exposure, Net Equity, and Effective Leverage tick-by-tick upon price updates and transactions. | **Keep** | Trần Hữu Dụ *(Mechanism Designer)* |
| **Forced Liquidation Engine** | Core | Automatically executes a market fire-sale of 100% of holdings when Effective Leverage reaches $\ge 5.0\times$ (Margin Ratio $\le 20\%$). | **Keep** | Trần Hữu Dụ *(Mechanism Designer)* |
| **Solvency & Terminal Check** | Core | Triggers instant Game Over / Account Wipeout if $\text{Net Equity} \le 0$ after liquidation. | **Keep** | Trần Hữu Dụ *(Mechanism Designer)* |
| **End-Game Narrative Debrief** | Core | Renders one of four outcome screens (Normie, Middle-Class, Extravagant Luxury, or Wipeout) with behavioral explanations. | **Keep** | Cáp Phan Quang Khánh *(Scenario Designer)* |
| **Dynamic Leverage Health Gauge** | Supporting | Color-coded visual widget showing Safe Zone ($\le 2.5\times$), Warning Zone ($2.5\times - 5.0\times$), and Breach Zone ($\ge 5.0\times$). | **Keep** | Triệu Đức Lương *(UI/UX Designer)* |
| **Target Progress Indicator** | Supporting | Dynamic percentage gauge showing $(\text{Net Equity} / \text{Property Target Value}) \times 100$. | **Keep** | Triệu Đức Lương *(UI/UX Designer)* |
| **Amber Warning Notification** | Supporting | Flashes an active alert during the Warning Zone to prompt voluntary de-risking before broker liquidation. | **Keep** | Triệu Đức Lương *(UI/UX Designer)* |
| **Phase Headline News Banner** | Supporting | Displays deterministic news triggers (fake vs. real headlines) to explain macro price movements. | **Keep** | Cáp Phan Quang Khánh *(Scenario Designer)* |
| **Recent Order Log** | Supporting | Displays filled transaction history (Asset, Volume, Execution Price, Debt Impact). | **Keep** | Triệu Đức Lương *(UI/UX Designer)* |
| **Order-Book Depth & Bid-Ask Spread** | Complex | Simulates liquidity pool depletion and order queues. | **Remove** | Team *(Scope protection)*[cite: 3] |
| **Execution Price Slippage** | Complex | Calculates execution penalties on fire-sales based on market volume. | **Remove** | Team *(Scope protection)*[cite: 3] |
| **Multiplayer Lobbies & Leaderboards** | Social | Real-time competitive scoring between multiple connected users. | **Remove** | Team *(Scope protection)*[cite: 3] |
| **Derivative / Put Option Hedging** | Complex | Allows purchasing options contracts to hedge margin downside. | **Remove** | Team *(Scope protection)*[cite: 3] |
| **Tiered Daily Margin Interest Fees** | Minor | Deducts continuous interest rates on borrowed margin balances. | **Postpone** | Team *(Excluded from MVP)*[cite: 3] |

---

## 3. Workflow Node-to-Feature Specification (Phase 1 Engine)

Directly mapped from the Phase 1 architectural flow diagram:
### Detailed Node Specifications

| Diagram Node / Step | System Action & Algorithmic Rule | Feature Status | Responsible Owner[cite: 3] |
| :--- | :--- | :---: | :--- |
| **Node 1: Start Scenario & Initial State** | Initializes Scenario ID (`1` or `2`), sets Cash to `initial_capital` ($10,000 / 20m KRW), Stock Balance = 0, initial leverage = 1.0×. | **Core** | Nguyễn Hồng Nguyên |
| **Node 2: Set Financial Goal & Leverage** | Captures player difficulty (`Small House 3.0x`, `Normal House 20.0x`, `ToLam Villa 100.0x`) and margin tier (`1x`, `2x`, `3x`, `4x`). | **Core** | Cáp Phan Quang Khánh / Trần Hữu Dụ |
| **Node 3: Begin Trading Dashboard** | Mounts the trading UI, begins streaming the 50-stock ticker data, and starts the 1-second tick timer. | **Core / Supporting** | Triệu Đức Lương / Nguyễn Quang Minh |
| **Node 4: Order Validation Check** | Evaluates order volume: <br>• $\text{IF Order Value} \le \text{Purchasing Power} \implies$ execute trade<br>• $\text{IF Order Value} > \text{Purchasing Power} \implies$ reject with inline error banner | **Core** | Nguyễn Quang Minh |
| **Node 5: Execute Order** | Updates player balance: deducts/adds cash, recalculates margin debt liability, updates asset share inventory. | **Core** | Nguyễn Quang Minh |
| **Node 6: Valuation Pipeline** | Recalculates dynamically every tick: <br>• $\text{Gross Exposure} = \sum (\text{Shares}_i \times \text{Price}_i)$<br>• $\text{Net Equity} = \text{Cash} + \text{Gross Exposure} - \text{Margin Debt}$<br>• $\text{Effective Leverage} = \text{Gross Exposure} / \text{Net Equity}$ | **Core** | Trần Hữu Dụ |
| **Node 7: Margin Health Gate** | Categorizes risk state: <br>• $\text{Effective Leverage} \le 2.5\times \implies$ **Safe Zone**<br>• $2.5\times < \text{Effective Leverage} < 5.0\times \implies$ **Amber Warning Zone**<br>• $\text{Effective Leverage} \ge 5.0\times \implies$ **Forced Liquidation Trigger** | **Core** | Trần Hữu Dụ |
| **Node 8: Forced Liquidation Execution** | Auto-sells 100% of open equity holdings at the current tick price to immediately repay `Margin Debt`. Deducts losses from equity. | **Core** | Nguyễn Quang Minh |
| **Node 9: Solvency Evaluation** | Checks account solvency post-liquidation: <br>• $\text{IF Net Equity} \le 0 \implies$ **Game Over (Bankruptcy)**<br>• $\text{IF Net Equity} > 0 \implies$ Resumes session in cash-only mode with remaining funds | **Core** | Trần Hữu Dụ |
| **Node 10: Phase Timer Gate ($T \ge 300\text{s}$)** | If tick count reaches 300s, executes Phase 1 conclusion: computes Target Progress % and seamlessly transitions game state to Phase 2. | **Core** | Nguyễn Quang Minh |

---

## 4. Scope Boundaries & Cut Criteria

To maintain strict alignment with Week 5 studio goals and prevent implementation bottlenecks in Week 6, all features must satisfy the following filter tests[cite: 3]:

1. **Direct Problem Relevance:** Does the feature demonstrate the core risk of excessive margin leverage during unexpected market downturns[cite: 3]?
2. **Logic Integration:** Does it rely exclusively on the defined financial formulas ($\text{Gross Exposure}$, $\text{Margin Debt}$, $\text{Effective Leverage}$)[cite: 3]?
3. **Feasibility by Week 6:** Can it be built and verified by the technical developer within a deterministic single-player loop without complex external backend servers[cite: 3]?
4. **Deterministic Testability:** Can the feature be checked directly against the pre-calculated test figures in `SAMPLE_INPUT_OUTPUT.md`[cite: 3]?

*Any feature failing two or more criteria is definitively categorized as **Removed** or **Postponed**.*[cite: 3]
