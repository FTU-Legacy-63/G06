# Known Limitations

This document records the financial, technical, and data constraints of Free Fall 2.0. In accordance with course guidelines, limitations are stated transparently rather than obscured.

---

## 1. Financial Model Constraints

| Limitation | Practical Consequence | Design Rationale |
|---|---|---|
| **Instant Tick Liquidity** | All orders and liquidations fill immediately at the current displayed tick price without market impact. | Real-world fire sales experience bid-ask spread widening and market slippage. Modeling order-book microstructure was deferred to protect the core focus on margin ratios. |
| **Frictionless Volume Execution** | Unlimited share volume can be bought or sold without partial fill delays or transaction fees. | Keeps accounting explainable and prevents execution complexity from obscuring the leverage feedback loop. |
| **Uniform Maintenance Threshold** | A single maintenance margin requirement of 20.00% is enforced across all 50 securities. | Real brokerages vary requirements based on individual asset beta and client risk profiles. A universal threshold ensures clean, explainable classroom evaluation. |
| **Compounded Session Limits** | Exchange limits are modeled as ±30% per session (allowing compounded phase moves of +69%/−51%), without intraday circuit breakers. | Simplified trading halts to preserve the continuous 1,800-second simulation clock. |
| **Amplified Bank Savings Yield** | Bank Savings yield +4.75% per completed session (compounded every 150 seconds). | Accelerated dramatically compared to real annual bank deposits to make de-risking and capital preservation a viable tactical alternative during gameplay. |
| **Static Property Multipliers** | Property targets are fixed multiples of initial capital (3×, 20×, 100×). | In reality, real estate prices do not scale linearly with an investor's initial trading balance. |
| **Single-Player Environment** | The simulation models an isolated retail trader without multi-party competition or institutional order routing. | Focuses cognitive load purely on personal risk management and emotional discipline. |

---

## 2. Market Data and Benchmark Constraints

| Limitation | Practical Consequence | Design Rationale |
|---|---|---|
| **Deterministic Price Paths** | Stock prices follow pre-computed synthetic time series. Players can memorize price turning points on repeat runs. | Deterministic paths guarantee identical, reproducible market conditions for fair academic benchmarking across student runs. |
| **Benchmark Optimization Assumptions** | The MILP benchmark (~109× concentrated, ~156× staggered) assumes perfect foresight of future prices, whole-share allocations, and frictionless execution. | Establishes a mathematical upper bound to verify target feasibility, not an expected average player outcome. |
| **Compressed Time Horizon** | The historical South Korea margin crisis is compressed from multi-week episodes into a 30-minute session. | Fast-forwards market cycles into a single class session, creating intense psychological pressure. |

---

## 3. Product Scope and Feature Boundaries

| Scope Decision | Current Status | Notes |
|---|---|---|
| **Postponed Features** | Scenario trade playback, automated behavioral typology classification, interactive candlestick charting, and CSV export. | Deferred to preserve stability of the core trading loop and margin engine. |
| **Removed Features** | User authentication, database accounts, and public leaderboards. | Excluded from the MVP to eliminate external database and server dependencies. |
| **Narrative Script Depth** | Granular tick-by-tick news alerts are implemented for Phase 1; Phases 2–6 rely on high-level phase sentiment banners. | Core price volatility drives late-phase risk rather than text-heavy narratives. |
| **Device Form Factor** | The trading dashboard is designed and optimized for desktop viewports (1280px+). | Mobile and tablet responsiveness is not supported in the MVP release. |
| **Educational Scope** | The software is an educational simulation designed for academic coursework at FTU; it does not constitute investment advice. | Educational disclaimer is embedded in the application. |

---

## 4. Documentation Reconciliations

Earlier working drafts contained minor discrepancies across working notes:
- **Test Suite Discrepancy:** Resolved. The repository now includes the full 66-test automated suite passing 100% in `tests/`, covering formal cases T01–T12 and defect regressions BUG-01 through BUG-06.
- **Attribution & Role Mapping:** Resolved. Team roles (QA Lead, Core Dev, Financial Analyst, Frontend Dev) are formally mapped to team members in `contribution_map.md` and individual footprint files.
- **Local Link Paths:** Resolved. All links in `contribution/evidence/` have been updated to repository-relative markdown paths.
