# TEST CASES — FREE FALL 2.0

## 1. Purpose

This document verifies that the core gameplay flow of Free Fall 2.0 works correctly and that all financial calculations are consistent with the defined assumptions.

The testing process focuses on four categories:

1. Normal Cases
2. Boundary Cases
3. Invalid Cases
4. Financial Consistency Checks

Each test compares the expected result with the actual result produced by the deployed game.


## 2. Test Environment

- Initial Capital: $10,000
- Available Leverage: 1×, 2×, 3×, 4×
- Maintenance Margin Threshold: 20%
- Margin Call Rule: Instant Forced Liquidation
- Market Structure: 6 Phases
- Phase Duration: 300 ticks
- Trading Sessions:
  - AM: Tick 1–150
  - PM: Tick 151–300
- Settlement Rule: T+0.5
- Market Scenarios: Scenario 1 and Scenario 2


## 3. Test Case Table

| ID | Category | Test Case | Input / Action | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|
| N01 | Normal | Cash purchase | Buy a stock using 1× leverage with sufficient cash | Order executed; cash decreases; holdings and portfolio value increase; margin debt remains 0 | TBD | ⬜ |
| N02 | Normal | Leveraged purchase | Buy a stock using 2× leverage | Order executed; gross exposure increases and margin debt is created correctly | TBD | ⬜ |
| N03 | Normal | Maximum leverage purchase | Buy using 4× leverage within available buying power | Order executed and leverage is calculated correctly | TBD | ⬜ |
| N04 | Normal | Sell existing shares | Sell shares currently held in portfolio | Holdings decrease; sale proceeds follow settlement rule; portfolio updates | TBD | ⬜ |
| N05 | Normal | T+0.5 settlement | Sell shares during AM session | Sale proceeds become available according to the defined PM settlement rule | TBD | ⬜ |
| N06 | Normal | Bank Savings | Transfer available cash into Bank Savings | Cash decreases and Bank Savings balance increases by the same amount | TBD | ⬜ |
| N07 | Normal | Property Target progress | Increase Net Worth through profitable trading | Property Target Progress updates based on current Net Worth | TBD | ⬜ |
| N08 | Normal | Scenario switch | Run Scenario 1 and Scenario 2 separately | Correct market dataset is loaded without mixing price paths | TBD | ⬜ |

| B01 | Boundary | Margin Ratio slightly above threshold | Margin Ratio = 20.01% | No margin call; position remains active | TBD | ⬜ |
| B02 | Boundary | Margin Ratio exactly at threshold | Margin Ratio = 20.00% | Margin call is triggered and forced liquidation occurs immediately | TBD | ⬜ |
| B03 | Boundary | Margin Ratio below threshold | Margin Ratio = 19.99% | Immediate forced liquidation | TBD | ⬜ |
| B04 | Boundary | Maximum buying power | Place an order equal to exactly available buying power | Order is accepted | TBD | ⬜ |
| B05 | Boundary | Market ceiling | Stock price reaches +30% session limit | Price may reach +30% but must not exceed it | TBD | ⬜ |
| B06 | Boundary | Market floor | Stock price reaches -30% session limit | Price may reach -30% but must not fall below it | TBD | ⬜ |

| I01 | Invalid | Insufficient buying power | Place an order exceeding available buying power | Order rejected; portfolio and cash remain unchanged | TBD | ⬜ |
| I02 | Invalid | Sell more than holdings | Attempt to sell quantity greater than shares owned | Order rejected | TBD | ⬜ |
| I03 | Invalid | Zero quantity | Submit Buy/Sell order with quantity = 0 | Order rejected | TBD | ⬜ |
| I04 | Invalid | Negative quantity | Submit Buy/Sell order with quantity < 0 | Order rejected | TBD | ⬜ |
| I05 | Invalid | Invalid ticker | Submit an order for a ticker not included in the 50-stock universe | Order rejected without affecting game state | TBD | ⬜ |

| F01 | Financial | Gross Exposure calculation | Hold multiple stock positions | Gross Exposure equals total market value of open stock positions | TBD | ⬜ |
| F02 | Financial | Margin Debt calculation | Open leveraged position | Margin Debt equals financed portion of leveraged exposure | TBD | ⬜ |
| F03 | Financial | Net Equity calculation | Portfolio contains leveraged positions | Net Equity = Assets − Margin Debt | TBD | ⬜ |
| F04 | Financial | Leverage calculation | Open leveraged position | Leverage = Gross Exposure / Net Equity | TBD | ⬜ |
| F05 | Financial | Margin Ratio calculation | Use manually calculated Equity and Gross Exposure | Margin Ratio = Net Equity / Gross Exposure | TBD | ⬜ |
| F06 | Financial | Forced liquidation | Market decline causes Margin Ratio ≤ 20% | All affected positions are liquidated immediately according to the defined rule | TBD | ⬜ |
| F07 | Financial | Post-liquidation state | Complete forced liquidation | Holdings, debt, cash/equity and liquidation status update consistently | TBD | ⬜ |
| F08 | Financial | Final Net Worth | Reach end of simulation | Final Net Worth equals the value implied by cash, investments, savings and outstanding liabilities | TBD | ⬜ |
| F09 | Financial | Property Target Progress | Calculate progress at end of simulation | Progress percentage matches Final Net Worth relative to selected Property Target | TBD | ⬜ |
| F10 | Financial | Scenario price-limit consistency | Run Scenario 1/2 through all sessions | No market price exceeds ±30% of its relevant session reference | TBD | ⬜ |


## 4. Manual Financial Verification

At least one leveraged portfolio should be recalculated manually and compared with the game output.

### Example

Assume:

- Initial Equity = $10,000
- Leverage = 2×
- Gross Exposure = $20,000
- Margin Debt = $10,000

Then:

**Net Equity**

Net Equity = Gross Exposure − Margin Debt

Net Equity = $20,000 − $10,000 = $10,000

**Leverage**

Leverage = Gross Exposure / Net Equity

Leverage = $20,000 / $10,000 = 2.00×

**Margin Ratio**

Margin Ratio = Net Equity / Gross Exposure

Margin Ratio = $10,000 / $20,000 = 50%

Expected game output:

- Gross Exposure = $20,000
- Margin Debt = $10,000
- Net Equity = $10,000
- Leverage = 2.00×
- Margin Ratio = 50%
- Margin Call = No


## 5. Critical Margin Test

The most important boundary test is the 20% Maintenance Margin threshold.

| Margin Ratio | Expected Result |
|---:|---|
| 20.01% | Position remains active |
| 20.00% | Margin Call + Instant Forced Liquidation |
| 19.99% | Margin Call + Instant Forced Liquidation |

The implementation must follow:

Margin Call Triggered if:

Margin Ratio ≤ 20%

There is no grace period between the Margin Call and Forced Liquidation.


## 6. Market Data Verification

Scenario datasets are separately audited for the ±30% session price limit.

For each ticker:

Price Change (%) = (Current Price / Session Reference Price) − 1

Acceptable range:

-30% ≤ Price Change ≤ +30%

A price exactly at +30% or -30% is valid.

A price above +30% or below -30% is classified as a data breach.

The Excel Market Scenario Audit file is used as supporting evidence for this test.


## 7. Bug Handling

If a test fails:

1. Record the issue in `BUG_LOG.md`.
2. Assign the bug to the responsible developer.
3. Fix the implementation.
4. Run the same test again.
5. Record the new Actual Result.
6. Mark the test as PASS only after verification.


## 8. Test Status

- ⬜ Not Tested
- ✅ Pass
- ❌ Fail

A test is considered passed only when both:

1. The technical behavior matches the expected result; and
2. The financial result is mathematically consistent.
