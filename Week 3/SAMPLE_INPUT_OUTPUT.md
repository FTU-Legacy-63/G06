# Sample Input–Output

This file demonstrates how fixed scenarios combined with different player decisions produce predictable financial consequences.

## Sample Case 1: Scenario 1 + Gangnam Villa — The Wipeout

### Sample Input

| Input | Value |
| :--- | :--- |
| Scenario | Scenario 1 |
| Initial Capital | 10,000,000 KRW |
| Financial Target | Gangnam Villa |
| Target Value | 80,000,000 KRW |
| Market Path | Aggressive bull run followed by a sudden crash |
| Phase 5 Shock | −30% |
| Player Strategy | Maximum margin exposure |
| Maximum Leverage | 1:4 |

### Intended Consequence

The player uses maximum leverage during the bull market to pursue the 8× financial target.

When the predetermined **−20% market shock** occurs, the leveraged position suffers a disproportionately large equity loss. Equity falls below the required maintenance level, triggering:

> **Market Crash → Maintenance Margin Breach → Margin Call → Forced Liquidation**

**Final Outcome:** Forced Liquidation / Wipeout  
**Financial Target:** Failed

---

## Sample Case 2: Scenario 3 + Mini Apartment — The Normie

### Sample Input

| Input | Value |
| :--- | :--- |
| Scenario | Scenario 3 |
| Initial Capital | 50,000,000 KRW |
| Financial Target | Mini Apartment |
| Target Value | 100,000,000 KRW |
| Market Path | Moderate growth followed by a correction |
| Market Shock | −30% |
| Player Strategy | Cash-only investment |
| Margin Used | 0% |

### Intended Consequence

The player's portfolio declines during the predetermined correction. However, because the player has no Margin Debt, the decline does not trigger a Margin Call or Forced Liquidation.
