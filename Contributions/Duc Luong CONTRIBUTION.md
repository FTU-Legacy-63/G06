# OBJECTIVE INDIVIDUAL CONTRIBUTION EVIDENCE

**Course:** Technology Applications in Banking and Finance (NHA408E) - FTU 2026  
**Project:** Free Fall 2.0 (Group 6)  
**Member:** Triệu Đức Lương  
**Student ID:** [Điền Mã Số Sinh Viên Của Bạn]  
**Assigned Role:** UI/UX & Frontend Interface Designer  

---

## 1. Executive Summary of Responsibilities

As the **UI/UX & Frontend Interface Designer**, my core responsibility is conceptualizing, designing, and structuring the entire visual hierarchy, user experience (UX), and component architecture for *Free Fall 2.0*. I translate backend market simulation mechanics and financial risk logic (from Week 3, Week 4, and the Phase 1 System Workflow) into an intuitive, high-pressure dark-mode trading terminal interface deployed on GitHub Pages.

| Area | Responsibility | Concrete Repository Deliverable |
|---|---|---|
| **Design System & Terminal Aesthetic** | Formulated the visual identity, dark-mode color palette (`#05070A` background, `#00E676` green, `#EF4444` red), glassmorphism UI components, and typography hierarchy. | [`docs/UI_Design_System.md`](https://github.com/FTU-Legacy-63/G06) / Figma Wireframes |
| **Introduction & Narrative Onboarding** | Designed the high-impact landing screen focusing on story context, educational mission ("leverage blindness"), and player learning outcomes without cluttering early setup choices. | [`index.html`](https://ftu-legacy-63.github.io/G06/) (Introduction Screen View) |
| **Trading Terminal Dashboard UI** | Architected the multi-panel layout including Account Overview, Live Market Tickers, Quick Order Execution Panel, and Interactive Price Chart. | [`index.html`](https://ftu-legacy-63.github.io/G06/) (Main Simulator Dashboard) |
| **Risk & Efficiency Visual Gauges** | Created visual indicators for Margin Health Ratio (with a prominent $20\%$ liquidation threshold), Leverage Multipliers, and Property Target Progress bars. | Dashboard UI Component Spec / [`index.html`](https://ftu-legacy-63.github.io/G06/) |
| **Frontend Handover & Live Web Demo** | Provided component blueprints, asset specs, and layout logic to the frontend developer, validating the live Web Demo on GitHub Pages. | Live Deployment at [FTU-Legacy-63 Web Demo](https://ftu-legacy-63.github.io/G06/) |

---

## 2. Technical & UX Evidence & Implementation Details

### 2.1 Dark Mode Trading Terminal Design System
Designed a professional stock-exchange visual aesthetic to simulate the realistic environment of a South Korean margin-driven market crisis:
- **Color Palette:**
  - **Background Base:** Pitch Black (`#05070A`) with dark grid lines to minimize visual noise during high-speed trading.
  - **Terminal Green (`#00E676` / `#10B981`):** Indicates positive PnL, healthy margin status, and active system feeds.
  - **Crimson Red (`#EF4444`):** Flags high risk, order side alerts, and maintenance margin call warnings.
  - **Glassmorphism Panels (`#0F172A` with 60% opacity):** Encapsulates data cards with crisp slate borders (`#1E293B`) for clear information hierarchy.
- **Typography:** Combined ultra-bold display headings (e.g., `FREE FALL 2.0`) with uppercase Monospace fonts (`JetBrains Mono`) for real-time tickers, timestamps (`05:00 [PRE-MARKET]`), and system status logs (`+ SYS.ACTIVE`).

### 2.2 Introduction & Storytelling Screen Architecture
Designed a dedicated introductory experience that sets the narrative context before entering the simulation:
- **Structured 3-Card Narrative Grid:**
  1. *The Crisis:* Introduces the mid-2026 South Korean stock crash and compressed 30-minute high-pressure session.
  2. *Our Mission:* Explains the core educational goal of bridging static formulas with real-world decision-making to overcome "leverage blindness".
  3. *Your Takeaway:* Highlights key learning outcomes, including leverage amplification, liquidation risk control, and managing behavioral traps (FOMO, panic selling).
- **Clean Call-To-Action (CTA):** Positioned a high-contrast `LAUNCH SIMULATOR →` button to smoothly transition players to scenario configuration.

### 2.3 Trading Dashboard Component Hierarchy & Risk Visualizations
Mapped complex financial backend state variables into real-time UI widgets on the live web demo:
- **Account Overview Widget:** Displays real-time `Total Net Worth (Equity)`, `Trading Cash`, `Margin Debt`, and `Safe Haven Bank` balance.
- **Risk & Efficiency Panel:**
  - **Margin Health Ratio Gauge:** Renders dynamic visual feedback based on the formula:
    $$\text{Margin Health Ratio} = \frac{\text{Net Equity}}{\text{Gross Exposure}} \times 100\%$$
    Includes a highlighted red indicator line at $\text{Liq. Floor: } 20.0\%$ to visually alert players before forced liquidation executes.
  - **Leverage Multiplier Gauge:** Displays real-time borrowing leverage ($0\times$ to $4.0\times$).
  - **Property Target Progress Bar:** Tracks current net worth against selected targets (Small House $3\times$, Normal House $20\times$, ToLam Villa $100\times$).
- **Market Flash News & Order Execution:** Positioned news ticker feeds on the bottom left and quick order buttons (`BUY` / `SELL` / `Confirm Buy Order`) on the lower center panel for seamless user execution.

### 2.4 Frontend Prototyping Alignment & Web Verification
- Collaborated closely with the frontend developer by providing detailed wireframes, asset specifications, color codes, and layout coordinates.
- Validated the responsive layout across key browser viewports to ensure zero visual overlap during live simulation ticks.
- Ensured seamless integration between raw financial metrics (e.g., KOSPI tickers, Vintrumite prices, phase timers) and user-friendly visual elements.

---

## 3. Individual Footprint Self-Check (Midterm Checklist Section 7)

1. **My Main Responsibility:**  
   Architecting the UI/UX design system, conceptualizing the narrative Introduction screen, and designing the multi-panel trading terminal layout for the web simulator.
2. **My Most Important Output So Far:**  
   The complete UI/UX layout blueprint, color system, and screen wireframes implemented directly into the live web prototype on GitHub Pages (`index.html`).
3. **Where the Evidence is Located:**  
   In the public repository at [`FTU-Legacy-63/G06`](https://github.com/FTU-Legacy-63/G06) and the live interactive demo at [https://ftu-legacy-63.github.io/G06/](https://ftu-legacy-63.github.io/G06/).
4. **How My Output Supports the Group Product:**  
   Translates complex financial logic (leverage, margin calls, liquidation thresholds) into a clean, intuitive, and visually engaging user interface, allowing players to instantly grasp risk metrics under high-pressure market conditions.
5. **What I Will Improve or Complete Next (Post-Midterm):**  
   - Refine interactive micro-animations (e.g., glowing warning animations when Margin Health falls below $30\%$).
   - Finalize the layout for the post-game **Behavioral Debrief & Performance Review** screen.
   - Optimize dark-mode contrast ratios and responsive viewports for mobile/tablet presentation during the final project defense.
