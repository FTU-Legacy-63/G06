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
| Post-game debrief layout and formulas not finalised (stated next steps) | Review screen is basic |
| Mobile/tablet responsiveness and micro-animations still planned | Presentation on small screens unverified |
| No measured learning-outcome study | Educational effect intended, not proven |
| Simulation only; not investment advice | — |

