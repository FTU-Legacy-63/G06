# WEEK 4 — FINANCIAL LOGIC, TECHNICAL READINESS AND MIDTERM

## 1. Week 4 Objective

Week 4 formalizes how the six existing MVP inputs are converted into financial outcomes.

The main question is:

> How are the defined inputs converted into outputs through financial logic, and can this logic be tested?

The focus is on connecting the existing Input Dictionary with financial formulas, margin rules, sample calculations, assumptions, and technical implementation.


## 2. What is Financial Logic?

For Free Fall 2.0, the main financial logic includes:

- portfolio valuation;
- cash and margin debt calculation;
- equity / net worth calculation;
- leverage calculation;
- margin ratio and margin health;
- margin call and forced liquidation;
- property target progress;
- final outcome classification.

No additional player input is required. Financial states are calculated from the existing inputs.


## 3. Completing the Project Logic Chain

The project logic chain is:

> Problem → Target User → User Task → Input → Financial Logic → Output → User Action

For Free Fall 2.0:

> Leverage blindness → Inexperienced investors → Manage a leveraged portfolio → Scenario + Capital + Margin Ratio + Orders + Price Path → Portfolio, debt, equity, and margin calculations → Net Worth + Target Progress + Liquidation Status → Adjust leverage and trading decisions

The system automatically updates the player's financial state after each order and market phase.


## 4. Formalizing the Input–Logic–Output Mapping

| **Input** | **Financial Meaning** | **Financial Logic / Process** | **Output** |
|---|---|---|---|
| `assigned_scenario_capital` | Determines starting scenario | Assigns capital and corresponding market path | Initial Capital + Market Conditions |
| `fixed_price_path` | Market movement | Updates stock prices and revalues holdings | Portfolio Value + P&L |
| `target_house_type` | Player's financial goal | Sets target at 2× or 8× initial capital | Target Value + Target Progress |
| `initial_capital` | Starting cash/equity | Determines initial purchasing power | Initial Net Worth |
| `initial_margin_ratio` | Player's leverage choice | Determines borrowing capacity and maximum position | Leverage + Margin Risk |
| `orders` | Buy/Sell/Hold decisions | Updates holdings, cash, and margin borrowing | Portfolio Value + Cash + Margin Debt + Return |

The outputs are calculated states, not additional player inputs.


## 5. Formula, Rules, and Scoring

The financial state of the player is calculated using the following rules.

| **Component** | **Formula / Rule** | **Interpretation** |
|---|---|---|
| **Maximum Position** | `Initial Capital / Initial Margin Ratio` | The `initial_margin_ratio` determines the maximum position. A lower margin ratio allows greater leverage and therefore greater risk. |
| **Portfolio Value** | `Shares × Current Price` | For each stock. The current price comes from the existing `fixed_price_path`. |
| **Total Portfolio Value** | `Σ (Shares_i × Current Price_i)` | Used when the player holds multiple stocks. |
| **Equity / Net Worth** | `Cash + Portfolio Value − Margin Debt` | Represents the player's remaining financial position after accounting for borrowed money. |
| **Leverage** | `Portfolio Value / Equity` | Higher leverage means greater market exposure relative to the player's own equity. |
| **Margin Ratio** | `Equity / Portfolio Value` | Compared with the predefined maintenance threshold to determine margin health. |
| **Margin Call Price** | `Margin Debt / [Shares × (1 − Maintenance Margin)]` | The price at which the player's margin ratio reaches the maintenance margin. |
| **Mini Apartment Target** | `2 × Initial Capital` | Determined by the existing `target_house_type`. |
| **Gangnam Villa Target** | `8 × Initial Capital` | Determined by the existing `target_house_type`. |
| **Target Progress** | `Equity / Target Value × 100%` | Measures progress toward the selected property target. |

### Maximum Leverage

| **Initial Margin Ratio** | **Maximum Leverage** |
|---:|---:|
| 50% | 2× |
| 40% | 2.5× |
| 33.3% | 3× |
| 25% | 4× |

### Margin Health

The calculated margin ratio is compared with the predefined maintenance threshold:

**Healthy → Warning → Below Maintenance Threshold → Margin Call → Unresolved Margin Call → Forced Liquidation**

The maintenance threshold should be clearly stated as either a sourced rule or an MVP assumption.

For the Margin Call Price:

- `Margin Debt` = outstanding borrowed amount;
- `Shares` = shares currently held;
- `Maintenance Margin` = minimum required margin ratio.

No additional player input is required because shares and margin debt are generated from the player's existing `orders`.


## 6. Explainability

The game should explain why each financial outcome occurs.

> “You selected a 25% margin ratio, allowing up to 4× leverage. After the market declined, your portfolio value decreased while margin debt remained. This reduced your equity and margin ratio, triggering a margin call.”

The player can therefore understand the financial chain:

**Margin Ratio → Leverage → Position Size → Market Loss → Equity Loss → Margin Health → Liquidation Risk**

The simulation demonstrates financial consequences but does not predict real market outcomes.


## 7. Sample Calculation and Logic Test

Two cases are used to test whether the financial logic produces the expected outcomes.

### Case 1 — High Leverage

**Existing inputs:** Initial Capital = ₩10m | Initial Margin Ratio = 25% | Orders = Maximum Leveraged Position | Market Shock = −20%

| **Calculation** | **Result** |
|---|---:|
| Maximum Position = ₩10m / 25% | **₩40m** |
| Margin Debt = ₩40m − ₩10m | **₩30m** |
| Market Loss = ₩40m × 20% | **₩8m** |
| Remaining Equity = ₩40m − ₩30m − ₩8m | **₩2m** |
| Remaining Portfolio Value = ₩40m − ₩8m | **₩32m** |

**Outcome:** Margin Breach → Margin Call → Forced Liquidation

This tests whether leverage, portfolio loss, and margin logic work correctly.

### Case 2 — No Margin

**Existing inputs:** Initial Capital = ₩50m | Orders = Cash-only | Market Shock = −10% | Margin Debt = ₩0

| **Calculation** | **Result** |
|---|---:|
| Portfolio Value = ₩50m × 90% | **₩45m** |
| Equity = ₩45m − ₩0 | **₩45m** |

**Outcome:** Portfolio Loss → No Margin Debt → No Margin Call → Remains Solvent

This provides a baseline comparison against leveraged trading.

## 8. Technical Readiness

The technical structure connects the user interface directly to the simulation engine and financial logic.

### Main Route

| **Layer** | **Function** |
|---|---|
| **React** | Main development framework |
| **Trading Interface** | Receives and displays player decisions |
| **Simulation Engine** | Processes the existing inputs and updates the game state |
| **Financial Logic** | Calculates portfolio, debt, equity, leverage, margin health, and target progress |
| **Results** | Displays the player's financial outcome |

**System flow:** React → Trading Interface → Simulation Engine → Financial Logic → Results

### Simulation Engine

The engine uses the six existing inputs and converts them into calculated financial states:

| **Existing Inputs** | **Calculated States** |
|---|---|
| Scenario | Holdings |
| Initial Capital | Cash |
| Margin Ratio | Portfolio Value |
| Orders | Margin Debt |
| Price Path | Equity |
| House Type | Leverage |
|  | Margin Health |
|  | Target Progress |
|  | Final Outcome |

**Logic flow:**  
Scenario + Initial Capital + Margin Ratio + Orders + Price Path + House Type  
→ Holdings → Cash → Portfolio Value → Margin Debt → Equity → Leverage → Margin Health → Target Progress → Final Outcome

The predefined market paths can be stored as **JSON/JavaScript data** because the MVP uses deterministic scenarios.

### Fallback

**Streamlit + Python** can be used as the fallback implementation.

The fallback uses the same financial logic with a simpler interface.
