# Known Limitations

## Financial model
| Limitation | Effect |
|---|---|
| Instant liquidity: trades and liquidations fill at the displayed tick price | Real fire sales suffer slippage |
| Unlimited volume, 100 % fill; no depth, spread, latency or costs | Ignores partial fills |
| Single 20 % maintenance margin for all assets | Brokers vary by security/client |
| ±30 % AM/PM limit; no circuit breakers | Not exact exchange rules |
| Bank Savings +4.75 % per session | Amplified, not a realistic rate |
| Targets fixed at 3× / 20× / 100× of capital | Real property prices do not scale |
| Single-player individual investor | No institutions, regulators, multiplayer |

## Data and benchmarks
| Limitation | Effect |
|---|---|
| Prices are synthetic and deterministic | Players can memorise peaks; not a forecast |
| Scenario 2 exists but is not benchmarked or fully validated | Target feasibility on Scenario 2 unproven |
| Scenario 1 CSV jumps ≈ +30 % at second 1,651; Scenario 2 has larger session-boundary jumps and text-formatted numbers | Crash depth and parsing need re-checking |
| Benchmarks (109× / 156×; earlier 217.45×) assume perfect foresight, whole shares, frictionless execution | Ceilings are theoretical |
| Optimiser uses a 75 s settlement delay; engine uses 30 ticks | Benchmark not exactly the game rules |
| Real episode compressed from weeks to 30 minutes | Simplified dynamics |

## Product scope
| Limitation | Effect |
|---|---|
| Postponed: scenario playback, behavioural classification, advanced charts, export | Debrief is less detailed |
| Removed: login, leaderboard | No saved history |
| Phase 1 news only (market + five assets); Phases 2–6 not scripted | Information layer incomplete after Phase 1 |
| Post-game debrief layout and formulas not finalised (stated next steps) | Review screen is basic |
| Mobile/tablet responsiveness and micro-animations still planned | Presentation on small screens unverified |
| No measured learning-outcome study | Educational effect intended, not proven |
| Simulation only; not investment advice | — |

## Documentation and process
| Limitation | Effect |
|---|---|
| Documents disagree (maintenance 20 % vs 30 %; net equity; phase names; tick 150 boundary; benchmark ceilings) | See reconciliation lists in [financial_logic.md](financial_logic.md) and [data_and_sources.md](data_and_sources.md) |
| Committed test file has 4 tests; documentation claims 14 | See [testing.md](testing.md) §4 |
| `Interface_design.md`, `Revision_log.md` empty; UI design-system file and wireframes not in the upload | UI and revision history undocumented |
| Source URLs missing | Weaker traceability |
| Test/bug logs record roles; individual files mention a “frontend developer” who is not named | Attribution needs confirmation |
| Contribution links in `Quang_Minh_CONTRIBUTIONS.md` point to a local `C:\` path | Links broken on GitHub (fixed in the new individual file) |
