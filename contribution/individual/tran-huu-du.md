# Trần Hữu Dụ — Individual Footprint

*Coordinator · Mechanism designer*

## My main responsibility
Owned the financial mechanics: how actions and prices become equity, leverage, margin status, liquidation and target progress, and the system flow of the game (Phase 1 interaction loop and its workflow diagram).

## My concrete outputs
- Formulas: gross exposure, net equity (cash + savings + stock − debt), effective leverage, margin ratio
- Rules: 20 % maintenance, ≥ 5.0× trigger, 5 % penalty, T+0.5 settlement, ±30 % AM/PM limits (+69 % / −51 % per phase), 4.75 % Bank Savings per session
- Target matrix 3× / 20× / 100× from backtest benchmarks
- System flow: Phase 1 interaction loop (start screen → 1-second price trigger → order validation → recalculation → margin check → liquidation / solvency check → T+0.5 settlement → phase conclusion), drawn in `phase_1_workflow.jpg` and written up in the Feature Map
- Documents: Solution Structure (Week 2), Assumptions and Input Dictionary (Week 3), Feature Map (Week 5), Sample Input–Output, Week 4 financial-logic review

## Evidence links
- [docs/financial_logic.md](../../docs/financial_logic.md)
- [docs/user_flow.md](../../docs/user_flow.md) §1–2 and [docs/img/phase_1_workflow.jpg](../../docs/img/phase_1_workflow.jpg) (system flow)
- [docs/data_and_sources.md](../../docs/data_and_sources.md) (assumptions, input dictionary)
- Original evidence: [HUU_DU_CONTRIBUTIONS.md](../evidence/HUU_DU_CONTRIBUTIONS.md)

## How my work is used
The Technical Developer codes the rules, the Technical Developer implements the workflow diagram step by step, the Scenario Designer builds player paths on the system flow, margin tiers and targets, the Data Gatherer shapes data around the ±30 % limits, and the UI Designer visualises net equity, target progress and margin warnings.

## Integration, testing and revision
Engine defaults match the rules (maintenance 0.20, penalty 0.05); the hand calculation in T09 matches exactly (final cash ₩400,000). Targets changed from 2×/8× (Week 4) to 3×/20×/100× (Week 5). `[TODO: link commits]`

## Remaining limitation
Stated next steps are still open: the Phase 6 execution-penalty logic, target-progress % for the dashboard, and the formulas for the post-game debrief. The settlement boundary is written as tick ≤ 150 here but < 150 in the engine.

> Short version of [evidence/HUU_DU_CONTRIBUTIONS.md](../evidence/HUU_DU_CONTRIBUTIONS.md). **Trần Hữu Dụ should review, correct and sign off.**
