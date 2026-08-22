# 📉 Market Crash Survival Simulator

## Project Overview

**Free Fall 2.0** is a financial learning game designed around a key problem: understanding margin trading in theory does not necessarily prepare inexperienced investors to make sound decisions when markets move rapidly against them.

The project focuses on the gap between **knowing how leverage works** and **understanding its consequences while making real-time investment decisions**.

---

## Problem & Pain Point

Margin immediately makes its benefit visible: investors gain greater purchasing power and can amplify returns with limited initial capital. However, its downside is less intuitive. Inexperienced investors may struggle to anticipate how quickly leverage can reduce their equity, consume available liquidity, trigger margin calls, and eventually result in forced liquidation during a severe market decline.

This creates the project's central pain point:

> **The consequences of leverage are difficult to perceive before they materialize, particularly under time pressure and rapidly changing market conditions.**

The problem, therefore, is whether investors can **recognize risk and make appropriate decisions while their financial position is changing**.

---

## Target Users

The primary users are:

- **Retail and inexperienced investors** who have limited practical experience with leveraged trading.
- **Finance students** who understand financial concepts academically but lack a safe environment in which to experience their consequences.

Their core task is to **manage investment exposure and leverage as market conditions change while protecting their financial position from excessive losses and liquidation**.

---

## Desired User Outcome

After completing the simulation, users should be able to better understand:

- How leverage changes both return and downside exposure.
- How declining asset prices affect equity and margin health.
- Why liquidity becomes important during a margin call.
- How excessive leverage can lead to forced liquidation.
- How investment decisions made under FOMO or panic affect financial outcomes.

The intended outcome is not simply to teach users that **"margin is risky,"** but to help them recognize **when and why a leveraged position becomes financially vulnerable**.

---

## Product Direction

The proposed product is a **scenario-based stock-market simulation** inspired by the mid-2026 South Korean market episode.

Players manage a portfolio through changing market conditions and make decisions involving:

> **Buy / Sell / Hold → Position Size → Cash / Margin → Risk Management**

Each decision changes the player's financial state and influences the decisions available in subsequent scenarios.

The learning loop is:

> **Scenario → Information → Decision → Financial State Update → Consequence → Feedback → Next Decision**

---

## Main Output

The main output is a **Final Financial Outcome Dashboard** that summarizes the player's financial position and progress toward the target at the end of the simulation.

The dashboard displays:

**Final Net Worth | Portfolio Return | Cash Balance | Margin Debt | Maximum Leverage | Margin Ratio | Margin Calls | Liquidation Status | Maximum Drawdown | Financial Target Progress**

The output allows players to directly observe the financial outcome of their investment and leverage decisions and determine whether they successfully achieved the target while remaining solvent.

---

## MVP Direction

The player begins with **initial savings and a major financial objective**, such as accumulating enough capital for a high-value property down payment within a **limited period**.

Deposits provide safety but insufficient growth, while stock investment offers a faster path toward the target.

During the early market phases, stock prices repeatedly rise and the player earns positive returns. However, ordinary investment alone remains insufficient to reach the financial target. The game introduces **margin** as a way to increase purchasing power and potentially close the remaining funding gap.

The player is not required to use margin, but the game environment makes leverage increasingly attractive:

> **Financial Target → Insufficient Capital → Stock Gains → Remaining Funding Gap → Margin Opportunity → Higher Buying Power**

If the player uses margin, subsequent gains bring the financial target increasingly within reach, reinforcing the decision to take additional leverage. When market conditions eventually reverse, the same leverage amplifies losses and may lead to **margin calls, liquidity pressure, forced liquidation, or negative net worth**.

The core MVP experience therefore follows:

> **Need Capital → Invest → Earn → Fall Short → Use Margin → Approach Target → Market Crash → Manage or Suffer the Consequences**

### Core Mechanics

- Buy / Sell / Hold
- Position sizing
- Cash and margin financing
- Financial-target progress
- Margin monitoring
- Market shocks
- Margin calls
- Forced liquidation

The intended learning experience is not that the game explicitly tells players to use margin, but that players experience **why leverage can appear rational and attractive before its downside becomes visible**.
