# Cáp Phan Quang Khánh — Individual Footprint

*Scenario designer*

## My main responsibility
Owned the player-facing scenario structure: scenario tree and scenario paths, six-phase scenario, events and news, player-action mapping and decision paths. (The system flow and its workflow diagram were designed by Trần Hữu Dụ.)

## My concrete outputs
- Scenario tree with Happy, Alternative and Critical-risk player paths
- Six-phase scenario structure tied to the behavioural progression
- Phase 1 news: three market items (0:00, 2:30, 4:00) and company news for Vintrumite, Samsung Electronics, KODEX Semiconductor, KODEX Leverage, TIGER Semiconductor TOP10
- Player action mapping and scenario decision paths

## Evidence links
- [docs/user_flow.md](../../docs/user_flow.md) §5–7 (paths, news script, decision paths)
- Original evidence: [QUANG_KHANH_CONTRIBUTION.md](../evidence/QUANG_KHANH_CONTRIBUTION.md)

## How my work is used
It builds on the system flow, formulas and data to link the deterministic market to what players see and do, supporting the loop Scenario → Information → Decision → State update → Consequence → Feedback → Next decision.

## Integration, testing and revision
Actions come from the Input Dictionary and Feature Map, so branches use only supported mechanics; the paths follow the Phase 1 system flow designed by Trần Hữu Dụ and implemented in the engine. `[TODO: link evidence]`

## Remaining limitation
News and events exist for Phase 1 only; Phases 2–6, additional alternative and critical-risk paths, and links to target progress and margin outcomes are still to be written (stated next steps). Student ID is blank in the original file.

> Short version of [evidence/QUANG_KHANH_CONTRIBUTION.md](../evidence/QUANG_KHANH_CONTRIBUTION.md). **Cáp Phan Quang Khánh should review, correct and sign off.**
