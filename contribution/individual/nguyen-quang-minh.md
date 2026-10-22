# Nguyễn Quang Minh — Individual Footprint

*Technical developer*

## My main responsibility
Owned the executable simulation engine, event/state controller, CSV pipeline, API, CLI demo and automated tests.

## My concrete outputs
- `simulation_engine.py`: valuation, bank savings, T+0.5 holding pen, margin ratio, maintenance monitoring, forced liquidation with penalty
- `game_controller.py`: 1,800-tick phase control, order execution, scenario loading
- `tests/test_simulation_engine.py` (4 tests in the committed file)
- `interactive_demo.py`, `api_server.py`

## Evidence links
- [src/simulation_engine.py](../../src/simulation_engine.py)
- [src/game_controller.py](../../src/game_controller.py)
- [tests/test_simulation_engine.py](../../tests/test_simulation_engine.py)
- [src/interactive_demo.py](../../src/interactive_demo.py), [src/api_server.py](../../src/api_server.py)
- Original evidence: [QUANG_MINH_CONTRIBUTIONS.md](../evidence/QUANG_MINH_CONTRIBUTIONS.md)

## How my work is used
It turns the Phase 1 workflow diagram, formulas and price data into code that the web interface consumes through the API.

## Integration, testing and revision
Tests cover the wipeout with penalty (final cash ₩400,000), cash-only solvency, Bank Savings and settlement delay; `python -m unittest discover tests`. Week 6 logs credit engine fixes to roles such as Core Dev / Backend Dev — `[confirm which fixes were yours]`. The original file's links pointed to a local Windows (`C:` drive) path; they are replaced by repository paths.

## Remaining limitation
The committed test file has 4 tests while the Week 6 documentation reports 14; the engine assumes instant fills and no slippage. Stated next steps (slippage modelling, behavioural analytics) conflict with the Week 5 decision to treat slippage as out of scope.

> Short version of [evidence/QUANG_MINH_CONTRIBUTIONS.md](../evidence/QUANG_MINH_CONTRIBUTIONS.md). **Nguyễn Quang Minh should review, correct and sign off.**
