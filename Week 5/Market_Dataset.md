# MARKET_DATASET.md

## 1. Purpose

The market dataset provides the deterministic stock-price paths used by the **Free Fall 2.0** simulation engine.

Its purpose is to create a controlled but volatile market environment in which players experience:

> **Market Movement → Portfolio Revaluation → Leverage Change → Margin Pressure → Margin Call → Forced Liquidation**

The dataset is designed for **simulation and educational purposes**, not for predicting real market prices.

**Main file:** `market_scenario.csv`


## 2. Dataset Structure

The scenario contains **50 Korean stocks and ETFs** observed at **1-second intervals** throughout the simulated trading session.

| Item | Specification |
|---|---|
| **Market** | South Korea |
| **Assets** | 50 stocks / ETFs |
| **Market Drivers** | 5 |
| **Price Frequency** | 1 simulated second |
| **Market Phases** | 6 |
| **Time per Phase** | 300 seconds |
| **Total Simulation Time** | 1,800 seconds |
| **Price Observations per Asset** | 1,800 |
| **Total Price Cells** | 90,000 |
| **Scenario Type** | Deterministic |
| **Primary Format** | CSV |

Each row represents one simulated second and each asset column contains the corresponding market price.


## 3. Market Lifecycle

The dataset follows the six-phase market structure defined for the MVP.

| Phase | Market State | Intended Behaviour |
|---|---|---|
| **P1 — Fake Positive News** | Early uncertainty | Drivers may initially move sideways or decline before positive momentum develops; temporary decoy spikes create noise |
| **P2 — True Positive News** | Fundamental validation | Positive momentum becomes more visible, but non-driver assets may still generate misleading signals |
| **P3 — Bull Market** | Broad rally | Main drivers accelerate while market-wide volatility remains high |
| **P4 — Strong Growth (FOMO)** | Rapid expansion | Driver momentum strengthens and speculative participation increases |
| **P5 — Market Euphoria** | Peak leverage environment | Major drivers reach their strongest bullish movements with frequent spikes and high volatility |
| **P6 — Negative Shock** | Market crash | Prices fall sharply, triggering margin pressure, circuit-breaker conditions, and potential forced liquidation |

The phases are deterministic so that different players can face the same underlying market conditions while producing different outcomes through their own decisions.


## 4. Main Market Drivers

Five assets are designated as the primary market drivers in the current scenario:

| Driver | Simulation Role |
|---|---|
| **SK hynix** | Primary high-volatility driver with strong upside movements before the crash |
| **Samsung Electronics** | Major technology-market driver following the broader bullish-to-crash cycle |
| **KODEX Leverage** | Leveraged market exposure that amplifies major market movements |
| **KODEX Semiconductor** | Semiconductor-sector exposure linked to the technology rally |
| **TIGER Semiconductor TOP10** | Delayed driver with relatively weaker early movement followed by stronger acceleration in later phases |

The drivers do **not** move identically. Differences in timing, volatility and spike intensity prevent the market signal from becoming mechanically obvious to the player.


## 5. Driver and Decoy Logic

The scenario separates assets conceptually into:

> **Main Drivers + Market Followers + Decoy / Noise Assets**

### Driver Behaviour

Drivers are designed to show an identifiable underlying market trend while remaining volatile.

Typical pattern:

`Early Weakness / Sideways Movement → Bullish Acceleration → Volatility Spikes → Euphoria → Crash`

Some drivers react faster than others. The delayed-driver structure prevents all major assets from moving simultaneously.

### Decoy Behaviour

Non-driver assets create informational noise.

Across the bullish phases, selected non-driver assets may:

- rise sharply for a short period;
- generate temporary spikes;
- outperform drivers within an individual trading window;
- return toward their previous level;
- move sideways after a spike; or
- reverse into a significant decline.

These movements are intended to create realistic decision pressure and prevent the optimal market signal from being immediately obvious.

The decoys therefore support the behavioral-finance objective of the game:

> **Distinguishing persistent market signals from short-term noise under time pressure.**


## 6. Price-Path Design

The dataset is **scenario-based rather than a direct replay of historical prices**.

Historical market behaviour and the South Korean margin-crisis setting provide the scenario context, while the final second-by-second price paths are constructed for the simulation.

The design prioritizes four characteristics:

| Requirement | Implementation |
|---|---|
| **Trend** | Drivers follow the intended six-phase market lifecycle |
| **Volatility** | Prices contain frequent short-term movements rather than smooth linear paths |
| **Noise** | Non-driver assets can generate temporary misleading rallies and spikes |
| **Crash Behaviour** | Phase 6 introduces broad negative shocks and liquidation pressure |

Therefore, individual simulated prices should not be interpreted as historical observations or forecasts.


## 7. Connection to Financial Logic

The market dataset supplies **market prices only**.

Player-specific financial states are calculated separately by the simulation engine.

```text
market_scenario.csv
        ↓
Current Market Price
        ↓
Player Holdings
        ↓
Portfolio Value
        ↓
Cash + Portfolio Value − Margin Debt
        ↓
Equity / Net Worth
        ↓
Leverage & Margin Ratio
        ↓
Margin Health
        ↓
Margin Call / Forced Liquidation
```

For asset `i`:

`Position Value_i = Shares_i × Current Price_i`

Total portfolio value:

`Portfolio Value = Σ Position Value_i`

The dataset therefore serves as the market-price input for the financial logic defined in Week 4.


## 8. Integration Route

The intended technical route is:

`CSV → Simulation Engine → Current Second → Asset Prices → Portfolio Revaluation → Financial Logic → UI`

At each simulated second, the engine:

1. identifies the current simulation time;
2. retrieves the corresponding asset prices;
3. updates the player's portfolio value;
4. recalculates equity, leverage and margin health;
5. checks for margin-related events; and
6. sends the updated financial state to the trading interface.

The deterministic structure also allows the same scenario to be replayed for testing and post-simulation analysis.


## 9. Data Validation

The finalized dataset was audited before integration.

| Validation Check | Result |
|---|---:|
| Price-series columns | **50** |
| Rows per asset | **1,800** |
| Total price cells | **90,000** |
| Missing price values | **0** |
| Non-numeric price values | **0** |
| Non-positive prices | **0** |
| Inconsistent row width | **0** |
| Duplicate asset headers | **0** |

The audit checks structural integrity only. It does not alter the existing simulated price paths.


## 10. Assumptions and Limitations

### Assumptions

- Market prices update once per simulated second.
- All players facing the same scenario receive the same underlying price path.
- Market-driver behaviour is predetermined.
- Decoy movements are intentionally included as part of the scenario design.
- The simulation focuses on leverage, portfolio risk and liquidation rather than exact exchange microstructure.

### Limitations

- Simulated prices are not forecasts of future Korean stock prices.
- The dataset does not reproduce the full Korean exchange order book.
- Bid-ask spread, market depth, latency and transaction costs are not fully represented in the current MVP.
- Market behaviour is simplified to fit the compressed gameplay period.
- Player-specific variables such as cash, holdings, margin debt and equity are not stored in this dataset; they are generated by the financial engine.
- Historical evidence informs the scenario context, but the final price paths are synthetic and designed for gameplay.


## 11. Scope Decision

Additional data originally considered for the project included:

- USD/KRW exchange rates;
- institutional market-maker parameters;
- foreign-fund flows;
- central-bank reserve data; and
- additional leveraged-market indicators.

These variables are **not included in the current MVP dataset unless directly required by the simulation engine**.

This follows the Week 5 scope principle:

> Keep data that directly supports the core user flow and postpone inputs that increase complexity without changing the main simulation outcome.


## 12. Dataset Ownership

| Item | Responsibility |
|---|---|
| **Output** | Market Scenario Dataset |
| **Role** | Data Gatherer |
| **Owner** | Nguyễn Hồng Nguyên |
| **Primary Evidence** | `market_scenario.csv` |
| **Documentation** | `MARKET_DATASET.md` |
| **Used By** | Simulation Engine → Financial Logic → Trading Interface |

The dataset contribution is complete when the finalized market-price file can be read by the simulation engine and used to generate the player's financial states during gameplay.
