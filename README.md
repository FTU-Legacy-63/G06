# 📉 Free Fall 2.0

## Project Overview

**Free Fall 2.0** is a financial learning game designed around a key problem: understanding margin trading in theory does not necessarily prepare inexperienced investors to make sound decisions when markets move rapidly against them.

The project focuses on the gap between **knowing how leverage works** and **understanding its consequences while making real-time investment decisions**.


## Problem & Pain Point

Margin immediately makes its benefit visible: investors gain greater purchasing power and can amplify returns with limited initial capital. However, its downside is less intuitive. Inexperienced investors may struggle to anticipate how quickly leverage can reduce their equity, consume available liquidity, trigger margin calls, and eventually result in forced liquidation during a severe market decline.

This creates the project's central pain point:

> **The consequences of leverage are difficult to perceive before they materialize, particularly under time pressure and rapidly changing market conditions.**

The problem, therefore, is whether investors can **recognize risk and make appropriate decisions while their financial position is changing**.


## Target Users

The primary users are:

- **Retail and inexperienced investors** who have limited practical experience with leveraged trading.
- **Finance students** who understand financial concepts academically but lack a safe environment in which to experience their consequences.

Their core task is to **manage investment exposure and leverage as market conditions change while protecting their financial position from excessive losses and liquidation**.


## Desired User Outcome

After completing the simulation, users should be able to better understand:

- How leverage changes both return and downside exposure.
- How declining asset prices affect equity and margin health.
- Why liquidity becomes important during a margin call.
- How excessive leverage can lead to forced liquidation.
- How investment decisions made under FOMO or panic affect financial outcomes.

The intended outcome is not simply to teach users that **"margin is risky,"** but to help them recognize **when and why a leveraged position becomes financially vulnerable**.


## Product Direction

The proposed product is a **scenario-based stock-market simulation** inspired by the mid-2026 South Korean market episode.

Players manage a portfolio through changing market conditions and make decisions involving:

> **Buy / Sell / Hold → Position Size → Cash / Margin → Risk Management**

Each decision changes the player's financial state and influences the decisions available in subsequent scenarios.

The learning loop is:

> **Scenario → Information → Decision → Financial State Update → Consequence → Feedback → Next Decision**


## Main Output

The main output is the user's **ability to recognize how leverage develops from an attractive opportunity into a financial vulnerability, and how poor risk management can eventually lead to forced liquidation**.

The learning outcome develops progressively across the six phases:

- **Phase 1 – Slightly Green Market & Deceptive Hype:** Players understand basic trading mechanics and the opportunity cost of holding cash. More importantly, they learn how borrowing increases purchasing power and makes aggressive investment more attractive.

- **Phase 2 – Fundamental Shift & Building Confidence:** Players experience how genuine fundamentals can support market growth. Repeated gains build confidence in their investment decisions and gradually encourage greater risk-taking.

- **Phase 3 – Market Euphoria & Maximum Leverage:** Players experience the peak of **leverage blindness**. Their Net Worth and Property-Target Progress rise rapidly, while Margin Debt and financial vulnerability increase at the same time.

- **Phase 4 – Minor Correction:** Players experience **complacency risk**. Because the decline appears small compared with previous gains, they may dismiss early warning signs as a temporary correction instead of reducing leverage.

- **Phase 5 – Crisis Begins & Bull Traps:** Players experience how temporary rebounds and misleading recovery signals can encourage them to hold or average down. Meanwhile, their Margin Health deteriorates and available liquidity becomes increasingly important.

- **Phase 6 – Margin Cascade & Forced Liquidation:** Players experience the ultimate consequence of excessive leverage. Once Maintenance Margin requirements are breached, Margin Calls and Forced Liquidation can remove the player's ability to control the position and convert temporary market losses into permanent capital loss.

The overall user outcome is:

> **Understand Leverage → Build Confidence → Recognize Vulnerability → Respond to Warning Signs → Manage Liquidity & Exposure → Reduce Liquidation Risk**

---

## MVP Scope

The Minimum Viable Product focuses strictly on the **core simulation loop required to reproduce the six-phase learning experience and demonstrate the behavioral and mathematical consequences of leverage**.

### Six-Phase Simulation

1. **Slightly Green Market & Deceptive Hype**
   - Fake or misleading positive news
   - Slightly rising stock prices
   - Basic Buy / Sell / Hold mechanics
   - Cash vs. Margin financing
   - Buying Power and initial leverage

2. **Fundamental Shift & Building Confidence**
   - Verified positive corporate news
   - Continued market growth
   - Portfolio gains
   - Financial-Target Progress

3. **Market Euphoria & Maximum Leverage**
   - Strong bullish market
   - Higher Margin availability
   - Position sizing / MAX
   - Net Worth vs. Margin Debt
   - Leverage Ratio and Property-Target Progress

4. **Minor Correction**
   - Mild negative market movement
   - Genuine but moderately bearish news
   - Hold / Sell / Reduce Exposure decisions
   - Margin Health monitoring

5. **Crisis Begins & Bull Traps**
   - Sharp declines followed by temporary rebounds
   - Misleading recovery signals
   - Hold / Sell / Average Down decisions
   - Liquidity pressure
   - Margin Health deterioration and warnings

6. **Margin Cascade & Forced Liquidation**
   - Severe market decline
   - Maintenance Margin breach
   - Margin Calls
   - Deleveraging / collateral response
   - Forced Liquidation
   - Possible negative Net Worth

### Core Mechanics

1. Buy / Sell / Hold decisions.
2. Position sizing.
3. Cash vs. Margin financing.
4. Financial-Target Progress.
5. Margin Health monitoring and Maintenance Margin thresholds.
6. Margin Calls and Forced Liquidation.

### Product Structure

1. **Home:** Dashboard of Net Worth, Cash, Portfolio Value, Margin Debt, and Property-Target Progress.
2. **Market:** Stock prices, Stock News feed, Buy / Sell / Hold, and position sizing.
3. **Margin:** Buying Power, Margin Debt, Leverage Ratio, Margin Health, and Margin Call alerts.
4. **Results:** Final Net Worth, Margin Debt, Property-Target Progress, Maximum Leverage, Maximum Drawdown, Margin Calls, and Liquidation Status.

> **Core MVP Flow: Hype → Confidence → Maximum Leverage → Complacency → Bull Trap → Margin Cascade**
