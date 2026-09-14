
# USER_FLOW.md

## Product: Seoul Margin Crisis Simulator (2026 Korean Stock Market Simulation Game)
> **Goal:** Specify the complete end-to-end user experience, detailing the Happy Path, Alternative Paths, Error Paths, input validation rules, and outcome explanation models before Week 6 implementation[cite: 3].

---

## 1. High-Level User Journey


```

[Screen 1: Onboarding & Goal Setup]
│
├─► Select Lifestyle Target (Small House 3x / Normal House 20x / ToLam Villa 100x)
├─► Select Initial Margin Tier (Cash 1.0x / 2x / 3x / 4x)
└─► System generates Scenario ID (1 or 2) & initial capital ($10,000 / 20m KRW)
│
▼
[Screen 2: Active Trading Simulation (1,800s across 6 Phases)]
│
├─► 1-second Tick Engine streams price changes across 50 Korean assets
├─► Player monitors Portfolio Valuation, Target Progress %, and Leverage Gauge
├─► Player inputs market orders (Buy / Sell / Hold with selected volume)
│
▼
[Continuous Risk Engine Checks (Per Tick & Action)]
│
├─► Safe Zone (Effective Leverage <= 2.5x) ────────────► Continue Trading
├─► Warning Zone (2.5x < Effective Leverage < 5.0x) ──► Amber Alert: Voluntary De-risking
└─► Breach Zone (Effective Leverage >= 5.0x) ──────────► Broker Forced Liquidation
│
▼
[Solvency Check: Net Equity <= 0?]
│
┌─────────────────────┴─────────────────────┐
▼                                           ▼
(YES: Bankruptcy)                           (NO: Residual Cash)
│                                           │
▼                                           ▼
[Screen 3: Post-Game Debrief] <────── Final Game Over                      Resume Trading (Cash)

```

---

## 2. Detailed Path Specifications

### 2.1. Happy Path: Disciplined Leverage & Target Achievement
* **User Context:** Player chooses a balanced goal and executes a disciplined growth and de-risking strategy[cite: 3].
1. **Start Screen:** User launches the app, receives Scenario 1 ($10,000 USD initial capital), and selects `Normal House` (Difficulty: $20.0\times$, Target Equity: $200,000 USD).
2. **Setup:** User selects the `2x` Margin Tier (Max purchasing power: $20,000 USD; Borrowing capacity: $10,000 USD).
3. **Phases 1–3 (Accumulation):** User allocates capital into upward-trending technology assets (e.g., Samsung Electronics, POSCO Future M). Portfolio value rises to $85,000 USD; Effective Leverage remains healthy at $1.4\times$ to $1.8\times$.
4. **Phase 4 (FOMO Phase):** Volatility surges. User resists taking 4× leverage, taking partial profits to pay off accumulated margin debt.
5. **Phase 5 (Euphoria / Bull Trap):** User recognizes peak euphoria headlines and closes all stock positions, converting portfolio into 100% liquid cash ($210,000 USD). Target Progress reaches **105%**.
6. **Phase 6 (Systemic Shock):** System-wide crash occurs (-57% drop across holdings). Because user holds 100% cash and 0% debt, net equity is completely preserved.
7. **Conclusion (Second 1800):** Simulation completes. Target condition ($\text{Net Equity} \ge \$200,000$) is met.
8. **Output Screen:** Renders **Middle-Class Stability Ending** with performance analytics and risk metrics.

---

### 2.2. Alternative Path A: Warning Zone & Voluntary De-risking
* **User Context:** Player over-leverages during the rally, encounters the Amber Alert, and successfully de-risks before forced liquidation[cite: 3].
1. **Setup:** User selects `Normal House` ($20.0\times$) and operates on `3x` Margin.
2. **Phase 4 Shock:** A sharp intra-phase correction occurs (-12% dip).
3. **Trigger:** Gross stock value drops, eroding net equity. Effective Leverage jumps from $2.1\times$ to **$3.8\times$** (entering the Warning Zone: $2.5\times < \text{Leverage} < 5.0\times$).
4. **System Response:** 
   * Dashboard turns Amber.
   * Audio/visual alert: *"WARNING: Effective leverage at 3.8x. Maintenance liquidation triggers at 5.0x. De-leverage immediately!"*
5. **User Action:** Player immediately navigates to open positions and clicks **"De-risk 50%"** or sells high-beta shares at market tick.
6. **Resolution:** Proceeds automatically pay down margin debt. Effective Leverage drops back to **$1.9\times$** (Safe Zone).
7. **Consequence:** Broker does not intervene. Player sacrifices profit potential but preserves account solvency.

---

### 2.3. Alternative Path B: Conservative Cash-Only Survival
* **User Context:** Player pursues capital preservation with zero borrowing.
1. **Setup:** User selects `Small House` ($3.0\times$) and opts for `Cash Only (1.0x)`.
2. **Gameplay:** Trades execute strictly bounded by available cash. Margin borrowing capacity is disabled ($0 debt).
3. **Risk State:** Effective Leverage remains locked at $\le 1.0\times$ (Margin Ratio = 100%) throughout all 1,800 seconds.
4. **Phase 6 Impact:** Market drops -57%. Holding unleveraged stocks results in a draw-down, but liquidation cannot physically trigger.
5. **Output Screen:** Renders **Normie Ending** (Capital preserved, modest growth, zero default risk).

---

### 2.4. Error Path: Greed Trap, Forced Liquidation & Insolvency
* **User Context:** Player attempts maximum leverage into the systemic shock without hedging[cite: 3].
1. **Setup:** User selects `ToLam Villa` (Difficulty: $100.0\times$, Target: $1,000,000 USD) and toggles `4x` Margin Tier.
2. **Phase 5 Euphoria:** User rides the rally, borrowing $30,000 USD on $10,000 USD equity to hold a $40,000 USD position.
3. **Phase 6 Plunge:** Second 1501 begins. Asset prices plummet.
4. **Breach Condition:** At a **-6.25%** price drop, position value declines to $37,500 USD while debt remains fixed at $30,000 USD, leaving $7,500 USD equity. Effective Leverage reaches:
   $$\frac{\$37,500}{\$7,500} = \mathbf{5.0\times} \quad (\text{Margin Ratio} = 20\%)$$
5. **Trigger:** Effective Leverage reaches $\ge 5.0\times$. Broker risk engine halts user control and executes **Automatic Forced Liquidation**.
6. **Execution:** All shares are dumped into the collapsing market at current tick prices.
7. **Solvency Evaluation:** Because prices cascade faster than debt can be covered, Net Equity hits **$0**.
8. **Terminal State:** **GAME OVER (Bankruptcy / Wipeout)** screen mounts immediately. Gameplay terminates prior to Second 1800.

---

## 3. Input Validation & Error Handling Plan

Finance applications must reject invalid input gracefully without crashing or creating calculation errors (`NaN`)[cite: 3].

| Input Field | User Action / Value | System Validation Rule | System Response & User-Facing Error Message[cite: 3] |
| :--- | :--- | :--- | :--- |
| **Order Volume** | Negative integer (e.g., `-50`) | $\text{Volume} > 0$ | Reject order. Inline alert: *"Invalid volume. Enter a positive number of shares."*[cite: 3] |
| **Order Volume** | Non-numeric or decimal string | $\text{Volume} \in \mathbb{Z}^+$ | Reject order. Inline alert: *"Shares must be whole integer units."* |
| **Buy Value** | Exceeds purchasing power | $\text{Cost} \le \text{Cash} + \text{Remaining Margin}$ | Reject order. Inline banner: *"Order exceeds maximum purchasing power ($X). Max shares you can buy: Y."*[cite: 3] |
| **Sell Volume** | Exceeds held shares | $\text{Volume} \le \text{Held Shares}_i$ | Reject order. Inline banner: *"Insufficient shares. You currently own Z shares of this asset."* |
| **Margin Toggle** | Switching to 4x during Warning Zone | $\text{Effective Leverage} < 2.5\times$ | Modal lock: *"Cannot increase leverage tier while account is in Margin Warning Zone."* |
| **Trade Execution** | Rapid multi-clicking | Debounce threshold (200ms) | Disables order button during execution tick to prevent double-order submission. |

---

## 4. Output Explanation Framework

All output metrics and consequence screens must follow the standardized explanation pattern to ensure behavioral clarity[cite: 3]:

$$\text{Result} \longrightarrow \text{Reason} \longrightarrow \text{Meaning} \longrightarrow \text{Action} \longrightarrow \text{Limitation}$$

### Example 1: Mid-Game Forced Liquidation Notification[cite: 3]
* **Result:** Broker has executed an emergency market-sell of 100% of your holdings.
* **Reason:** Your portfolio dropped -6.25% while holding maximum 4.0× leverage, causing Effective Leverage to breach 5.0×.
* **Meaning:** Your collateral equity fell below 20% of your total borrowed debt. The brokerage liquidated your positions to guarantee debt recovery.
* **Action:** To survive future runs, maintain an equity buffer above 40% (Leverage $\le 2.5\times$) or manually sell assets before Phase 6.
* **Limitation:** Assumes instant market execution at current tick price, omitting real-world order-book freeze and spread slippage.

### Example 2: Post-Game Insolvency Debrief (Terminal Wipeout)[cite: 3]
* **Result:** Total Account Insolvency (Game Over). Net Equity: $0 USD.
* **Reason:** You held full margin exposure into Phase 6, where systemic collapse dropped core assets by -57%.
* **Meaning:** 4× borrowing power amplifies losses fourfold; a 25% asset decline erases 100% of owner equity.
* **Action:** Review the trade log to pinpoint where leverage should have been reduced during Phase 5 euphoria.
* **Limitation:** The simulation models a compressed 30-minute historical crisis without regulatory circuit breakers.

---

## 5. Flow Audit & Ownership Matrix

| Flow Segment | Primary Step | Critical User Touchpoint | Flow Owner[cite: 3] |
| :--- | :--- | :--- | :--- |
| **Onboarding Flow** | Scenario & Target Setup | Dropdowns for Goal and Margin Tier; initial capital card[cite: 3]. | Cáp Phan Quang Khánh |
| **Execution Flow** | Order Entry & Validation | Order ticket modal, buy/sell buttons, inline validation tooltips[cite: 3]. | Nguyễn Quang Minh |
| **Monitoring Flow** | Dynamic Health Tracking | Color-changing leverage gauge, amber warning banner, tick timer[cite: 3]. | Triệu Đức Lương |
| **Risk Enforcement** | Liquidation & Solvency | Broker takeover overlay, balance wipeout animation[cite: 3]. | Trần Hữu Dụ |
| **Debrief Flow** | Post-Game Narrative | Consequence cards, benchmark comparison graphs, restart button[cite: 3]. | Cáp Phan Quang Khánh |

```
