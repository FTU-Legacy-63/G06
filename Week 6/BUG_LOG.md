# BUG LOG

## 1. Purpose

This document records material bugs identified during Week 6 integration testing.

Only issues that affect the core gameplay flow, financial logic, or consistency between the documented rules and deployed implementation are included.

Minor visual, wording, and cosmetic issues are excluded unless they affect the player's understanding of a financial mechanic.

## 2. Bug Status

| Status | Definition |
|---|---|
| OPEN | Bug has been identified but not yet fixed |
| IN PROGRESS | Fix is currently being implemented |
| FIXED | Fix has been implemented but not yet independently verified |
| VERIFIED | Fix has been re-tested and confirmed |
| CLOSED | Issue is fully resolved |

## 3. Bug Summary

| ID | Severity | Component | Issue | Status |
|---|---|---|---|---|
| BUG-01 | High | Leverage Selection | 3× leverage option is missing from the initialization screen | OPEN |
| BUG-02 | Critical | T+0.5 Settlement | Deployed description indicates a settlement mechanism inconsistent with the defined T+0.5 rule | OPEN |
| BUG-03 | Critical | Margin Engine | Liquidation threshold is inconsistently defined as `< 20%` instead of `≤ 20%` | OPEN |

## 4. Detailed Bug Reports

### BUG-01 — Missing 3× Leverage Option

**Severity:** High  
**Component:** Initial Setup / Leverage Selection  
**Status:** OPEN  

**Description**

The initial leverage-selection interface does not provide the complete set of leverage tiers defined by the project.

The project specification uses:

- 1× Cash
- 2× Leverage
- 3× Leverage
- 4× Leverage

However, the initialization interface currently presents only 1×, 2×, and 4×.

**Expected Result**

The player should be able to select any of the four defined leverage tiers:

`1× → 2× → 3× → 4×`

**Actual Result**

The 3× leverage option is unavailable during initialization.

**Impact**

This prevents the deployed product from reproducing one of the leverage strategies used in the project's quantitative calibration and benchmark analysis.

It also creates an inconsistency between the documented financial model, market benchmark files, and playable implementation.

**Required Fix**

Add the 3× leverage option to the initialization screen and ensure that it passes the correct leverage value to the simulation engine.

**Re-test**

After the fix:

1. Select 3× leverage.
2. Start the simulation.
3. Verify that the selected leverage is displayed correctly.
4. Execute a trade.
5. Verify that Buying Power, Margin Debt, Effective Leverage, and Margin Ratio are calculated using the 3× setting.

### BUG-02 — T+0.5 Settlement Logic Inconsistency

**Severity:** Critical  
**Component:** Settlement / Trading Engine  
**Status:** OPEN  

**Description**

The deployed interface describes the T+0.5 mechanism as orders or purchased shares remaining in a holding pen before becoming active deliverable shares.

This is inconsistent with the project's intended liquidity-management rule.

The defined T+0.5 mechanic is based on delayed availability of sale proceeds:

`AM Sale → Settlement Pending → Cash Available in PM`

**Expected Result**

When a player sells shares during the AM session:

1. The shares are removed from the active position.
2. Sale proceeds enter the settlement holding state.
3. The proceeds cannot immediately be reused as available cash.
4. The proceeds become available during the PM session according to the defined T+0.5 rule.

**Actual Result**

The deployed description indicates that the holding mechanism may instead apply to orders or purchased shares before they become deliverable.

The implementation must therefore be verified to determine whether this is only a description error or an actual settlement-engine error.

**Impact**

T+0.5 directly affects liquidity management, Buying Power, and the player's ability to respond to margin pressure.

An incorrect implementation can materially change the financial outcome of the simulation.

**Required Fix**

Verify the settlement logic against the documented rule.

If the backend already follows the correct rule, update the interface description.

If the backend follows the incorrect interpretation, revise the settlement engine so that AM sale proceeds remain unavailable until PM settlement.

**Re-test**

1. Sell a position during AM.
2. Record available cash immediately after the sale.
3. Confirm that the proceeds are not immediately reusable.
4. Advance to PM.
5. Confirm that the proceeds become available.
6. Verify that total account value remains financially consistent throughout settlement.

### BUG-03 — Incorrect Margin Liquidation Boundary

**Severity:** Critical  
**Component:** Margin Engine / Margin Call  
**Status:** OPEN  

**Description**

The deployed product contains inconsistent definitions of the Maintenance Margin trigger.

One part of the interface states that liquidation occurs when the Margin Ratio falls below 20%.

The defined project rule is:

`Margin Ratio ≤ 20%`

Therefore, exactly 20.00% must trigger a Margin Call and immediate Forced Liquidation.

**Expected Result**

| Margin Ratio | Expected State |
|---:|---|
| 20.01% | Position remains active |
| 20.00% | Margin Call + Immediate Forced Liquidation |
| 19.99% | Margin Call + Immediate Forced Liquidation |

The engine condition should therefore follow:

`Margin Ratio <= 20%`

**Actual Result**

The deployed interface contains a `< 20%` interpretation in at least one location.

The backend condition must be verified to determine whether this inconsistency also exists in the simulation engine.

**Impact**

The 20% Maintenance Margin is one of the central financial rules of Free Fall 2.0.

Using `< 20%` instead of `≤ 20%` creates a boundary-condition error and makes the implementation inconsistent with the documented margin model.

**Required Fix**

Standardize the rule throughout the frontend, backend, documentation, and tests as:

`Margin Ratio ≤ 20% → Immediate Forced Liquidation`

**Re-test**

Run the following three boundary cases:

| Test | Margin Ratio | Expected Result |
|---|---:|---|
| A | 20.01% | No liquidation |
| B | 20.00% | Immediate liquidation |
| C | 19.99% | Immediate liquidation |

BUG-03 can be marked VERIFIED only if all three cases produce the expected result.

## 5. Re-Testing Record

| Bug ID | Fix Implemented By | Re-Test Result | Final Status | Notes |
|---|---|---|---|---|
| BUG-01 | — | — | OPEN | Awaiting fix |
| BUG-02 | — | — | OPEN | Backend settlement logic requires verification |
| BUG-03 | — | — | OPEN | Backend threshold condition requires verification |

## 6. Week 6 Bug Priority

The team should resolve bugs in the following functional order:

`Margin Engine → T+0.5 Settlement → Leverage Selection`

BUG-02 and BUG-03 directly affect financial outcomes and therefore must be verified before final quantitative testing.

BUG-01 should be resolved before benchmark testing because 3× leverage is part of the defined calibration framework.

Minor cosmetic issues should not delay stabilization of the core gameplay flow.
