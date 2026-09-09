# WEEK 4 — FINANCIAL LOGIC, TECHNICAL READINESS AND MIDTERM

## 1. Week 4 Objective

Week 4 formalizes how the **six existing MVP inputs** are converted into measurable financial outcomes.

The central question is:

> **How are the defined inputs converted into outputs through financial logic, and can this logic be tested?**

The focus is not on creating new inputs or redesigning the MVP. Instead, Week 4 connects the existing **Input Dictionary**, assumptions, and sample data with:

- financial formulas;
- margin rules;
- outcome classification;
- sample calculations;
- logic testing;
- technical implementation.

---

## 2. Financial Logic

For **Free Fall 2.0**, financial logic represents the rules that continuously transform player decisions and market movements into financial states.

The main calculations include:

| **Financial Logic** | **Purpose** |
|---|---|
| Portfolio Valuation | Revalue current holdings after each market movement |
| Cash & Margin Debt | Track available cash and borrowed funds |
| Equity / Net Worth | Measure the player's remaining financial position |
| Leverage | Measure market exposure relative to player equity |
| Margin Ratio | Determine margin health |
| Margin Call & Liquidation | Identify when leveraged positions become unsustainable |
| Property Target Progress | Measure progress toward the selected financial goal |
| Final Outcome Classification | Determine the player's end-game financial status |

> **No additional player input is required.**  
> These financial states are calculated automatically from the six existing MVP inputs.

---

## 3. Project Logic Chain

The project follows the logic chain:

> **Problem → Target User → User Task → Input → Financial Logic → Output → User Action**

For **Free Fall 2.0**:

> **Leverage Blindness**  
> → Inexperienced Investors  
> → Manage a Leveraged Portfolio  
> → Scenario + Capital + Margin Ratio + Orders + Price Path + House Type  
> → Portfolio, Debt, Equity, Leverage and Margin Calculations  
> → Net Worth + Target Progress + Liquidation Status  
> → Adjust Leverage and Trading Decisions

After every **order** and **market phase**, the system automatically recalculates the player's financial state.

---

## 4. Input → Logic → Output Mapping

The six existing MVP inputs are directly connected to financial calculations.

| **Input** | **Financial Meaning** | **Financial Logic / Process** | **Main Output** |
|---|---|---|---|
| `assigned_scenario_capital` | Determines the starting scenario | Assigns starting capital and the corresponding predetermined market scenario | Initial Capital, Market Conditions |
| `fixed_price_path` | Represents market movements | Updates security prices and revalues current holdings | Portfolio Value, P&L |
| `target_house_type` | Defines the player's financial target | Converts the selected property into a target value | Target Value, Target Progress |
| `initial_capital` | Player's starting equity | Determines initial purchasing power | Initial Net Worth |
| `initial_margin_ratio` | Determines leverage capacity | Defines maximum allowable position size and borrowing capacity | Maximum Leverage, Margin Risk |
| `orders` | Represents Buy / Sell / Hold decisions | Updates holdings, cash balance and margin debt | Holdings, Cash, Debt, Return |

> **Outputs are calculated financial states, not additional player inputs.**

---

## 5. Core Financial Logic

### 5.1 Portfolio and Leverage

| **Metric** | **Formula** | **Meaning** |
|---|---|---|
| **Maximum Position** | `Initial Capital / Initial Margin Ratio` | Maximum market exposure allowed by the selected margin level |
| **Position Value** | `Shares × Current Price` | Market value of each security position |
| **Portfolio Value** | `Σ(Shares_i × Current Price_i)` | Total value of all securities held |
| **Equity / Net Worth** | `Cash + Portfolio Value − Margin Debt` | Player wealth after deducting borrowing |
| **Leverage** | `Portfolio Value / Equity` | Market exposure relative to player-owned capital |
| **Margin Ratio** | `Equity / Portfolio Value` | Current equity cushion supporting the leveraged position |

### 5.2 Maximum Leverage

The selected initial margin ratio directly determines the player's maximum leverage.

| **Initial Margin Ratio** | **Maximum Leverage** |
|---:|---:|
| 50.0% | 2.0× |
| 40.0% | 2.5× |
| 33.3% | 3.0× |
| 25.0% | 4.0× |

Therefore:

> **Lower Initial Margin Ratio → Higher Leverage → Larger Position → Greater Sensitivity to Market Losses**

---

### 5.3 Margin Health and Liquidation

The calculated margin ratio is compared with a predefined **Maintenance Margin Threshold**.

The margin state follows the sequence:

> **Healthy → Warning → Below Maintenance → Margin Call → Unresolved Margin Call → Forced Liquidation**

The maintenance threshold must be explicitly documented as either:

- a sourced market rule; or
- an MVP assumption.

#### Margin Call Price

For a single-security position:

`Margin Call Price = Margin Debt / [Shares × (1 − Maintenance Margin)]`

Where:

- `Margin Debt` = outstanding borrowed amount;
- `Shares` = number of shares currently held;
- `Maintenance Margin` = minimum required equity-to-position ratio.

Shares and margin debt are generated automatically from the player's existing `orders`.

---

### 5.4 Property Target

The selected house type determines the player's financial objective.

| **Target** | **Rule** |
|---|---:|
| **Mini Apartment** | `2 × Initial Capital` |
| **Gangnam Villa** | `8 × Initial Capital` |

Target progress is calculated as:

`Target Progress = Equity / Target Value × 100%`

This allows the game to continuously show how trading decisions affect progress toward the player's goal.

---

## 6. Explainability

Every major financial outcome should be traceable to the player's previous decisions.

For example:

> *“You selected a 25% initial margin ratio, allowing up to 4× leverage. After the market declined, your portfolio value fell while margin debt remained unchanged. Your equity therefore declined faster than the portfolio itself, reducing the margin ratio and triggering a margin call.”*

The financial chain is:

> **Initial Margin Ratio → Leverage → Position Size → Market Movement → Portfolio P&L → Equity → Margin Ratio → Liquidation Risk**

The simulator therefore explains **why** the player's financial condition changes rather than displaying only the final result.

> **Limitation:** Free Fall 2.0 demonstrates financial mechanics under predefined scenarios. It does not predict actual market prices or future investment performance.

---

## 7. Sample Calculation and Logic Test

The logic is tested using manually verifiable cases.

### Case 1 — High Leverage

**Inputs**

`Initial Capital = ₩10m`  
`Initial Margin Ratio = 25%`  
`Order = Maximum Leveraged Position`  
`Market Shock = −20%`

| **Step** | **Calculation** | **Result** |
|---:|---|---:|
| 1 | Maximum Position = ₩10m / 25% | **₩40m** |
| 2 | Margin Debt = ₩40m − ₩10m | **₩30m** |
| 3 | Market Loss = ₩40m × 20% | **₩8m** |
| 4 | Remaining Portfolio = ₩40m − ₩8m | **₩32m** |
| 5 | Remaining Equity = ₩32m − ₩30m | **₩2m** |
| 6 | Margin Ratio = ₩2m / ₩32m | **6.25%** |

**Expected Outcome**

> **Margin Breach → Margin Call → Forced Liquidation**

This case tests whether:

- leverage is calculated correctly;
- losses are amplified through leverage;
- margin debt remains outstanding after the price decline;
- equity falls correctly;
- the margin threshold triggers the expected liquidation logic.

---

### Case 2 — Cash-Only Position

**Inputs**

`Initial Capital = ₩50m`  
`Margin Debt = ₩0`  
`Order = Cash-Only Position`  
`Market Shock = −10%`

| **Step** | **Calculation** | **Result** |
|---:|---|---:|
| 1 | Portfolio Value = ₩50m × 90% | **₩45m** |
| 2 | Equity = ₩45m − ₩0 | **₩45m** |
| 3 | Margin Debt | **₩0** |

**Expected Outcome**

> **Portfolio Loss → No Margin Debt → No Margin Call → Remains Solvent**

This case provides a baseline comparison showing that a market loss alone does not create a margin call when the player has no leveraged debt.

---

## 8. Technical Readiness

### 8.1 Main Technical Route

The MVP uses a lightweight architecture in which the interface passes player actions directly into the simulation and financial-logic layer.

> **React → Trading Interface → Simulation Engine → Financial Logic → Results**

| **Layer** | **Role** |
|---|---|
| **React** | Main development framework and application structure |
| **Trading Interface** | Receives Buy / Sell / Hold decisions and displays the portfolio |
| **Simulation Engine** | Controls phases, scenarios, orders and game-state updates |
| **Financial Logic** | Calculates portfolio value, cash, debt, equity, leverage, margin health and target progress |
| **Results Layer** | Displays financial outcomes and final performance |

---

### 8.2 Simulation Engine

The engine transforms the six existing inputs into calculated game states.

| **Existing Inputs** | **Calculated States** |
|---|---|
| Scenario | Holdings |
| Initial Capital | Cash |
| Initial Margin Ratio | Portfolio Value |
| Orders | Margin Debt |
| Price Path | Equity / Net Worth |
| House Type | Leverage |
|  | Margin Ratio / Margin Health |
|  | Target Progress |
|  | Final Outcome |

The processing sequence is:

> **Scenario + Initial Capital + Margin Ratio + Orders + Price Path + House Type**  
> ↓  
> **Holdings + Cash + Portfolio Value + Margin Debt**  
> ↓  
> **Equity + Leverage + Margin Ratio**  
> ↓  
> **Margin Health + Target Progress**  
> ↓  
> **Final Outcome**

Because the MVP uses deterministic scenarios, predefined market paths can be stored directly as **JSON or JavaScript objects**.

---

### 8.3 Technical Principle

The financial engine should remain separate from the interface.

This allows the team to:

- test formulas independently;
- compare manual calculations with system outputs;
- change the interface without rewriting financial logic;
- reuse the same calculations in a fallback implementation.

---

### 8.4 Fallback Route

If the React implementation becomes technically infeasible within the MVP timeline:

> **Streamlit + Python**

can be used as the fallback.

The fallback preserves:

- the same six inputs;
- the same deterministic price paths;
- the same financial formulas;
- the same margin rules;
- the same output metrics.

Only the user interface is simplified.

---

## 9. Week 4 Validation

Week 4 is considered complete when the team can demonstrate the full chain:

> **Input → Financial Logic → Calculated State → Output → Player Interpretation**

The repository should therefore contain enough evidence to show that:

- all six MVP inputs have a defined financial role;
- formulas and rules are explicitly documented;
- leverage and margin mechanics are explainable;
- at least one leveraged and one non-leveraged case can be manually verified;
- assumptions and thresholds are visible;
- financial logic can be implemented independently from the interface;
- the React route is feasible;
- a simpler technical fallback exists.

The goal is not to complete the final game in Week 4.

The goal is to prove that the MVP's **financial mechanics are logically defined, testable, explainable, and technically implementable**.
