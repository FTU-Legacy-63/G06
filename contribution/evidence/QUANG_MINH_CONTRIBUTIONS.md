# OBJECTIVE INDIVIDUAL CONTRIBUTION EVIDENCE

**Course:** Technology Applications in Banking and Finance (NHA408E) - FTU 2026  
**Project:** Free Fall 2.0 (Group 6)  
**Member:** Nguyễn Quang Minh  
**Student ID:** 2412380031  
**Assigned Role:** Technical Developer · Software & Engine Architect  
**Live Production Deployments:** [Cloudflare Workers Edge](https://phan-dung.ngqminh6979.workers.dev/) · [GitHub Pages Static Terminal](https://ftu-legacy-63.github.io/G06/)  

---

## 1. Executive Summary of Responsibilities

As the **Technical Developer and Software Architect**, my primary duty was translating the theoretical margin mechanics, game rules, and Phase 1 interaction flowchart into executable, verifiable, and explainable software code across both Python backend and browser runtime environments. I owned the full-stack architecture, the mathematical simulation engine, the zero-dependency REST API, the interactive single-page web terminal, the Web Audio engine and original soundtrack, and the automated verification suite.

| Functional Area | Primary Engineering Responsibility | Concrete Repository Deliverable |
|---|---|---|
| **Core Simulation Engine** | Implemented real-time portfolio valuation, Bank Savings collateral isolation, settlement delays (T+0.5 holding pen), margin ratio calculation, and maintenance margin monitoring. | [`src/simulation_engine.py`](../../src/simulation_engine.py) |
| **Event & State Controller** | Implemented 6-phase timeline management (1,800 ticks), automated CSV ingestion, KRW/USD currency normalization, canonical ticker aliasing, and mid-phase liquidation detection. | [`src/game_controller.py`](../../src/game_controller.py) |
| **Zero-Dependency REST API** | Engineered a native HTTP server (`http.server` & `socketserver.TCPServer`) with 5 REST endpoints, CORS preflight, thread safety, and floating-point sanitization. | [`src/api_server.py`](../../src/api_server.py) · [`api_server.py`](../../api_server.py) |
| **Interactive CLI Prototype** | Built a standalone terminal-based simulation client for command-line verification, scenario playback, and headless grading. | [`src/interactive_demo.py`](../../src/interactive_demo.py) |
| **Production Web Terminal** | Engineered a 25,000-line institutional single-page application with real-time Chart.js telemetry, 7-screen flow, an admin testing gate (`6979`), and browser `ClientEngine`. | [`index.html`](../../index.html) · [`web/index.html`](../../web/index.html) |
| **Dynamic Audio Engine & OST** | Programmed a Web Audio API state machine with real-time biquad low-pass filter sweeps (20,000 Hz down to 600 Hz) and composed/produced 17 original BGM soundtrack tracks (64.3 MB). | [`assets/music/`](../../assets/music/) |
| **Visual Assets & Endings** | Integrated 20 tactical demon HUD overlays (`buy_sell_demon/`) and 5 MP4 cinematic ending videos (`ending/`) representing Tiers A through F. | [`assets/`](../../assets/) · [`assets/buy_sell_demon/`](../../assets/buy_sell_demon/) · [`assets/ending/`](../../assets/ending/) |
| **Workflow Alignment** | Full implementation of the `phase 1 workflow.jpg` logic diagram (Start Screen -> Bank Savings -> T+0.5 delay -> Liquidation Penalty). | [`docs/img/phase_1_workflow.jpg`](../../docs/img/phase_1_workflow.jpg) |
| **Dataset Integration** | Integrated realistic 1,800-tick × 50-asset market datasets (`market_scenario_1.csv`) with automatic USD conversion and canonical ticker mapping. | [`data/market_scenario_1.csv`](../../data/market_scenario_1.csv) |
| **Automated Verification** | Created 66 automated unit tests across 6 test modules in `tests/`, asserting boundary conditions, 5% liquidation penalties, and defect resolutions. | [`tests/`](../../tests/) · [`tests/test_simulation_engine.py`](../../tests/test_simulation_engine.py) |
| **Formal Contribution Report** | Authored the 12-page comprehensive individual contribution report adhering to standard academic formatting and verified against repository metrics. | [`reports/individual/Nguyen_Quang_Minh_Contribution_Report.docx`](../../reports/individual/Nguyen_Quang_Minh_Contribution_Report.docx) |

---

## 2. Technical Evidence & Implementation Details

### 2.1 Core Financial Logic (`src/simulation_engine.py`)
Directly mapped from **`docs/img/phase_1_workflow.jpg`** and formal specifications:
- **Gross Exposure:**
  $$\text{Gross Exposure} = \sum_{i} \text{Shares}_i \times \text{Current Stock Price}_i$$
  *(Reflects deliverable active holdings; pending queue inventory is strictly excluded from active collateral).*
- **Net Equity (Global Net Worth):**
  $$\text{Net Equity} = \text{Cash} + \text{Bank Savings} + \text{Gross Exposure} - \text{Margin Debt}$$
- **Trading Equity (Margin Collateral Basis):**
  $$\text{Trading Equity} = \text{Cash} + \text{Gross Exposure} - \text{Margin Debt}$$
  *(Strictly isolates Bank Savings from margin borrowing collateral to prevent players from gaming margin calls with protected cash).*
- **Effective Leverage & Margin Ratio:**
  $$\text{Effective Leverage} = \frac{\text{Gross Exposure}}{\max(\text{Trading Equity}, 0.001)}$$
  $$\text{Margin Ratio} = \frac{\text{Trading Equity}}{\text{Gross Exposure}}$$
- **Margin-Call Boundary Price:**
  $$\text{Margin Call Price} = \frac{\text{Margin Debt}}{\text{Shares} \times (1 - \text{Maintenance Margin Ratio})}$$
  *(With maintenance margin set to 20.00%, stock value must equal $\text{Margin Debt} / 0.80$ to avoid liquidation).*
- **Settlement Delay Mechanism (Holding Pen):**
  - **Orders executed before tick 150 (`Tick < 150`):** Shares enter a T+0.5 holding pen exposed to live price movement, converting to deliverable holdings at $\text{tick} + 30$.
  - **Orders executed at or after tick 150 (`Tick >= 150`):** Locked in the deferred holding pen across the phase boundary, settling upon Phase 2 entry.
- **Forced Liquidation & Penalty:**
  - When $\text{Margin Ratio} < 20.00\%$ (or $\text{Effective Leverage} \ge 5.0\times$), the engine triggers `trigger_forced_liquidation()`.
  - The broker fire-sales 100% of holdings at the current tick price.
  - A **5% gross liquidation penalty fee** is deducted from gross proceeds:
    $$\text{Penalty} = \text{Gross Proceeds} \times 0.05$$
    $$\text{Net Proceeds} = \text{Gross Proceeds} \times 0.95$$
  - Net proceeds repay active margin debt; remaining cash survives in the account. If net equity $\le 0$, solvency wipeout is triggered.

### 2.2 Dataset Integration & Dual-Currency Normalization (`src/game_controller.py`)
- Coordinates 1,800 global seconds across 6 market phases:
  - **Phase 1 (1–300s):** Normal Market / The Mirage
  - **Phase 2 (301–600s):** Creeping Doubt / Warning Tremors
  - **Phase 3 (601–900s):** Systemic Contagion / The Crack
  - **Phase 4 (901–1200s):** Dead Cat Bounce / False Hope
  - **Phase 5 (1201–1500s):** Liquidity Black Hole / Panic Capitulation
  - **Phase 6 (1501–1800s):** Terminal Liquidation & Aftermath
- **Dual-Currency Normalization:** Ingests raw Korean Won (KRW) datasets (e.g., Samsung Electronics at ₩55,700) and automatically normalizes to the calibrated $10,000 USD starting capital:
  ```python
  is_usd_mode = (self.engine.initial_capital <= 50000.0)
  ```
- **Target Difficulty Alignment:** Calibrated against quantitative backtest models:
  - **Small House (3.0× Capital):** Achievable with Cash 1.0× and defensive Bank Savings rotation.
  - **Normal House (20.0× Capital):** Requires disciplined 2.0×–3.0× leverage management.
  - **ToLam Villa (100.0× Capital):** High-skill threshold requiring 4.0× leverage with precise market timing.

### 2.3 Automated Logic Verification (`tests/`)
All financial logic is verified with a **100% pass rate across 66 automated unit tests** in `tests/`:
```bash
python -m unittest discover tests
# Ran 66 tests in 2.543s -> OK
```
- **Foundational Engine Tests ([`tests/test_simulation_engine.py`](../../tests/test_simulation_engine.py)):**
  - **Test 1 (High-Leverage Wipeout with 5% Liquidation Penalty):** Validates $10,000 USD (₩10m) capital at 4× leverage ($30,000 debt) under a −20% price shock. Margin ratio drops to 6.25% (< 20%), triggering forced liquidation. The 5% penalty ($1,600) is deducted from $32,000 gross proceeds, leaving $30,400 net. After repaying $30,000 debt, **exactly $400 cash survives**, matching hand calculations to the cent.
  - **Test 2 (Cash-Only Position Immunity):** Validates $50,000 capital with 0 debt under a −10% shock, remaining completely solvent at 100% margin ratio.
  - **Test 3 (Bank Savings Workflow):** Validates risk-free savings deposits/withdrawals, confirming savings are protected from market drawdowns while excluded from margin collateral.
  - **Test 4 (Settlement Delay Holding Pen):** Validates the 30-tick delivery delay for morning orders vs holding pen deferral across phase boundaries for afternoon orders.
- **Comprehensive Bug & Integration Suites:**
  - [`tests/test_bug_fixes_5_to_11.py`](../../tests/test_bug_fixes_5_to_11.py) (Tests BUG-05 through BUG-11)
  - [`tests/test_critical_bugs_c1_to_c5.py`](../../tests/test_critical_bugs_c1_to_c5.py) (Tests Critical fixes C1 through C5)
  - [`tests/test_complete_bug_report_45.py`](../../tests/test_complete_bug_report_45.py) (Regression tests across all 45 triage cases)
  - [`tests/test_moderate_and_visual_fixes.py`](../../tests/test_moderate_and_visual_fixes.py) (UI formatting and telemetry tests)
  - [`tests/test_week6_integration.py`](../../tests/test_week6_integration.py) (End-to-end multi-phase simulation integration)

---

## 3. Individual Footprint Self-Check (Course Rubric Criteria)

1. **My Main Responsibility:**  
   Architecting, programming, and verifying the Core Financial Engine, Phase 1 Workflow rules, CSV data pipeline, zero-dependency REST API, single-page web terminal, Web Audio engine, and automated test suite.
2. **My Concrete Outputs:**  
   The fully tested [`src/simulation_engine.py`](../../src/simulation_engine.py), [`src/game_controller.py`](../../src/game_controller.py), [`src/api_server.py`](../../src/api_server.py), the 25,000-line single-page application [`index.html`](../../index.html) (and [`web/index.html`](../../web/index.html)), 17 original soundtrack tracks in [`assets/music/`](../../assets/music/), 20 demon HUD assets and 5 ending videos in [`assets/`](../../assets/), and the 66-test automated verification suite in [`tests/`](../../tests/).
3. **Where the Evidence is Located:**  
   Directly verifiable in the repository under [`src/`](../../src/), [`tests/`](../../tests/), [`index.html`](../../index.html), [`assets/`](../../assets/), [`data/`](../../data/), and [`reports/individual/Nguyen_Quang_Minh_Contribution_Report.docx`](../../reports/individual/Nguyen_Quang_Minh_Contribution_Report.docx).
4. **How My Output Supports the Group Product:**  
   Translates the visual system flowchart ([`phase_1_workflow.jpg`](../../docs/img/phase_1_workflow.jpg)) and empirical market datasets into mathematically rigorous, executable software. In browser execution, the client engine and UI telemetry turn abstract risk formulas into an immediate, high-tension interactive experience for players.
5. **Integration, Testing, and Defect Resolution:**  
   - Diagnosed and resolved **BUG-01** (intra-phase delivery queue condition for morning vs afternoon orders).
   - Diagnosed and resolved **BUG-02** (`margin_multiplier` initialization in engine constructor).
   - Diagnosed and resolved **BUG-04** (post-liquidation trading lockout).
   - Diagnosed and resolved **BUG-05** (100% margin ratio display cap for cash-only positions).
   - Achieved 100% pass rate across 66 automated unit tests in `tests/`.

---

## 4. Full Production Engineering Deliverables & Deployment

1. **Zero-Dependency REST API ([`src/api_server.py`](../../src/api_server.py) · [`api_server.py`](../../api_server.py)):**
   - Implemented standard-library HTTP server (`http.server` & `socketserver.TCPServer`) with 5 endpoints (`GET /api/state`, `POST /api/trade`, `POST /api/savings`, `POST /api/phase/advance`, `GET /api/ticks`), full CORS support, and `sanitized_float()` JSON protection.
2. **Production Web Application Terminal ([`index.html`](../../index.html) · [`web/index.html`](../../web/index.html)):**
   - Engineered the 25,000-line institutional single-page application featuring real-time Chart.js telemetry with dual y-axes, 7 distinct operational screens, an administrative testing gate (`6979`), and client-side `ClientEngine` execution.
3. **Dynamic Web Audio API Engine & 17-Track Soundtrack ([`assets/music/`](../../assets/music/)):**
   - Programmed the `AudioManager` module with real-time biquad low-pass filter modulation (20,000 Hz down to 600 Hz during news releases and market halts).
   - Composed and produced 17 custom BGM soundtrack tracks (64.3 MB) covering all phases, demon order stems, bank sanctuary, and news dossiers.
4. **Tactical Visual Assets & Cinematic Endings ([`assets/`](../../assets/)):**
   - Integrated 20 tactical demon HUD overlays ([`assets/buy_sell_demon/`](../../assets/buy_sell_demon/)) and 5 MP4 ending video sequences ([`assets/ending/`](../../assets/ending/)) representing Tiers A through F.
5. **Production Cloud Deployments:**
   - **Cloudflare Workers Edge:** Live global deployment at [`https://phan-dung.ngqminh6979.workers.dev/`](https://phan-dung.ngqminh6979.workers.dev/).
   - **GitHub Pages Static Terminal:** Fully optimized deployment at [`https://ftu-legacy-63.github.io/G06/`](https://ftu-legacy-63.github.io/G06/) with 100% 200 OK asset resolution across all audio, video, and image requests.
6. **Academic Documentation:**
   - Authored the 12-page contribution report: [`reports/individual/Nguyen_Quang_Minh_Contribution_Report.docx`](../../reports/individual/Nguyen_Quang_Minh_Contribution_Report.docx).

---
*Verified and submitted by Nguyễn Quang Minh (Student ID: 2412380031).*
