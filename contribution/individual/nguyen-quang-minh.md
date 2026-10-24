# Nguyễn Quang Minh — Individual Footprint

- **Student ID:** 2412380031  
- **Role:** Technical Developer · Software & Engine Architect  
- **Group:** Group 06 (Free Fall 2.0)  
- **Course:** Technology Applications in Finance and Banking (NHA408E) — Foreign Trade University (FTU) 2026  
- **Production Deployments:** [Live Cloudflare Workers](https://phan-dung.ngqminh6979.workers.dev/) · [GitHub Pages Static Terminal](https://ftu-legacy-63.github.io/G06/)  

---

## 1. My Main Responsibility
I owned the full-stack software architecture, the executable Python financial simulation backend, the real-time market timeline controller, the zero-dependency HTTP REST API, the interactive browser-based single-page application (`web/index.html`), the dynamic Web Audio engine, the CLI prototype, and the automated verification suite. My primary duty was translating the theoretical margin mechanics and the Phase 1 system flowchart designed by Trần Hữu Dụ into executable, reproducible, and explainable software code across both Python and browser runtime environments.

## 2. My Concrete Outputs
- **Core Financial Engine (`src/simulation_engine.py`):** Implemented continuous portfolio valuation, trading equity isolation, margin debt tracking, effective leverage, margin ratio monitoring, Safe Haven Bank isolation, T+0.5 settlement holding pens, and forced liquidation triggers with a 5% penalty fee deduction.
- **State & Scenario Controller (`src/game_controller.py`):** Implemented 1,800-tick phase management across 6 market phases, order intake validation, live CSV price loading, KRW/USD dual-currency normalization (`is_usd_mode = initial_capital <= 50,000.0`), canonical ticker alias mapping, and mid-phase liquidation detection.
- **HTTP REST API Server (`src/api_server.py`):** Developed a zero-dependency HTTP server using Python's standard library (`http.server` and `socketserver.TCPServer`) with full CORS preflight support, thread safety, and floating-point sanitization to bridge simulation state with the web frontend.
- **Interactive CLI Demo (`src/interactive_demo.py`):** Built a standalone terminal-based simulation client for command-line verification and testing.
- **Production Web Terminal (`web/index.html`):** Engineered a 24,750-line institutional single-page application featuring real-time Chart.js telemetry with dual y-axes, 7 distinct operational screens, an administrative testing gate (passcode: `6979`), and a client-side `ClientEngine` for zero-latency standalone execution.
- **Dynamic Audio Engine & Original Soundtrack (`assets/music/`):** Programmed a Web Audio API state machine with dynamic gain staging, biquad low-pass filter sweeps (20,000 Hz down to 600 Hz during news releases), and composed/produced 17 original BGM soundtrack tracks (64.3 MB).
- **Tactical Visual Assets & Cinematic Endings (`assets`):** Integrated 20 tactical demon HUD overlays (`buy_sell_demon/`) that advance with leverage, and 5 MP4 ending video sequences (`ending/`) representing Tiers A through F.
- **Automated Test Suite (`tests/`):** Created 66 automated unit tests across 6 test modules, verifying normal trades, boundary conditions, invalid inputs, financial consistency, and regression defect fixes.

## 3. Evidence Links
- Simulation Engine: [`src/simulation_engine.py`](../../src/simulation_engine.py)
- State Controller: [`src/game_controller.py`](../../src/game_controller.py)
- REST API Server: [`src/api_server.py`](../../src/api_server.py)
- CLI Demo Harness: [`src/interactive_demo.py`](../../src/interactive_demo.py)
- Web Application Terminal: [`web/index.html`](../../web/index.html)
- Dynamic Soundtrack Manifest: [`assets/music/`](../../assets/music/)
- Visual & Ending Assets: [`assets`](../../assets)
- Test Suite: [`tests/`](../../tests/) (including [`tests/test_simulation_engine.py`](../../tests/test_simulation_engine.py) and [`tests/test_week6_integration.py`](../../tests/test_week6_integration.py))
- Original Submission Evidence: [`contribution/evidence/QUANG_MINH_CONTRIBUTIONS.md`](../evidence/QUANG_MINH_CONTRIBUTIONS.md)

## 4. How My Work Is Used
The software architecture functions as the operational core of Free Fall 2.0. In the web terminal (`web/index.html`), the simulation processes orders against the active scenario dataset, computes leverage and margin health in sub-second cycles, enforces T+0.5 delivery queues, modulates audio filters during panics, and displays real-time telemetry. In headless or grading environments, `src/simulation_engine.py` and `src/api_server.py` execute identical arithmetic to validate player behavior and automated test assertions.

## 5. Integration, Testing, and Revision
- **Test Coverage:** All financial logic passes 100% across 66 unit tests (`python -m unittest discover tests`). Key verified scenarios include:
  - Exact boundary maintenance (Test T03: 20.00% margin ratio triggers `WARNING` without liquidation; Test T04: 19.9914% triggers immediate liquidation).
  - High-leverage wipeout (Test T09: $10,000 USD / ₩10m capital at 4× margin with a −20% shock deducts a 5% liquidation penalty, leaving exactly $400 / ₩400,000 cash).
  - Safe Haven Bank protection (Test T10: Bank savings remain immune to equity market shocks).
  - Settlement holding pen (Test T11: Deliveries before tick 150 deliver in 30 seconds; deliveries at or after tick 150 hold until Phase 2).
- **Defect Resolution:** Diagnosed, resolved, and verified key backend and frontend defects:
  - **BUG-01 (Critical):** Fixed the intra-phase delivery queue boolean condition (`process_deliveries`) so orders placed after tick 150 correctly hold for Phase 2 entry while intra-phase orders maintain the 30-tick delay.
  - **BUG-02 (Critical):** Initialized `margin_multiplier` in the engine constructor to prevent crashes during margin BUY orders.
  - **BUG-04 (Major):** Implemented state locks in `execute_order` to prevent order submissions after an account has been liquidated.
  - **BUG-05 (Major):** Capped the displayed margin ratio for cash-only positions at 100% to eliminate UI ambiguity.
  - **Deployment Optimization:** Purged 202.67 MB of redundant/dead files from `web/`, repaired an inverted `AudioManager.resolveSrc()` path bug, and relocated loose background images into `assets` for clean GitHub Pages hosting.

## 6. Remaining Limitations
- **Instant Fills Without Slippage:** All orders and liquidation sales execute immediately at the current tick price. Modeling order-book depth, bid-ask spreads, and market impact slippage was deferred as out of MVP scope.
- **Fixed Maintenance Threshold:** The maintenance margin floor is globally set to 20.00% across all 50 securities rather than varying dynamically by individual asset volatility tier.
- **Local Browser Storage:** In the static web build, settings and session history persist via HTML5 `localStorage` rather than a centralized cloud database.

---
*Verified and signed off by Nguyễn Quang Minh.*
