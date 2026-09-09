# Source–Use Map

This file records where external information is used in the MVP and the limitations of each source.

| Source | Claim / Use in Product | Limitation |
| :--- | :--- | :--- |
| Historical KOSPI and CFD market reports from the April 2023 Korea margin crisis | Used as problem evidence and as a reference for designing realistic market declines in Phases 4–6. | The real event occurred over multiple days, while the simulation compresses the market sequence into approximately 30 minutes. Real-world circuit breakers are excluded from the MVP. |
| Standard Korean brokerage margin requirements (e.g., Kiwoom Securities) | Used as a reference for defining leverage limits and margin mechanics. | The MVP applies standardized margin rules and does not model differences across brokers, securities, or client tiers. |

## Source-Use Principle

External data is used to establish **realistic boundaries and assumptions**, while the actual six-phase price paths remain deterministic and are created specifically for the simulation.
