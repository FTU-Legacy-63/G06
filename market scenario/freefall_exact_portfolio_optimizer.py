"""
Free Fall 2.0 — Exact Perfect-Foresight Portfolio Optimizer
===========================================================

INPUT
-----
market_scenario_1.csv

OBJECTIVE
---------
Starting from $10,000, maximize FINAL EQUITY over the complete known
1,800-second market path.

This version allows:
    - multiple stocks at the same time,
    - partial buys,
    - partial sells,
    - rebalancing,
    - 4x initial leverage,
    - T+0.5 on BOTH BUY and SELL,
    - account-level 20% maintenance margin,
    - unlimited execution at displayed prices.

ALGORITHM
---------
Mixed-Integer Linear Programming (MILP), solved with Gurobi.

Why MILP?
---------
The portfolio variables themselves are continuous, but the game's 4x rule is
conditional:

    IF a new BUY occurs at second t,
    THEN post-trade eligible margin ratio must be >= 25%.

A binary variable per second makes that rule exact. Gurobi indicator
constraints avoid a numerically ugly Big-M approximation.

IMPORTANT RULES ENCODED
-----------------------
1. Raw CSV price is divided by 1400.
2. 1 AM/PM session = 150 seconds.
3. T+0.5 = 75 seconds.
4. BUY at t:
       - executes immediately at P[t],
       - counts immediately in portfolio value/equity/margin,
       - cannot be sold until t+75.
5. SELL at t:
       - executes immediately at P[t],
       - removes the stock immediately,
       - proceeds count in total equity as a pending receivable,
       - proceeds cannot support a new BUY until t+75.
6. New BUYs require 25% initial margin (4x maximum initial leverage).
7. Effective leverage is allowed to drift above 4x after adverse price moves.
8. Margin Ratio <= 20% means forced liquidation.
   This optimizer searches only SURVIVING paths, so it enforces:
       Margin Ratio > 20%
   at every second.
9. No transaction fees, no spread, no slippage, unlimited matching.
10. Partial quantities are allowed. Therefore this is the exact continuous-share
    mathematical optimum / upper bound.
11. Final objective is mark-to-market equity at second 1800.
12. Forced-liquidation strategies are NOT allowed as an intentional shortcut.
    The 5% liquidation penalty is therefore irrelevant in the optimum searched.

INSTALL
-------
pip install gurobipy pandas numpy openpyxl

IMPORTANT:
The full 1,800 x 50 model exceeds Gurobi's tiny restricted/free model size.
For the full exact solve you need an Academic / WLS / commercial Gurobi license.

RUN
---
Put this script and market_scenario_1.csv in the same folder, then:

    python freefall_exact_portfolio_optimizer.py

OUTPUTS
-------
best_portfolio_optimizer_output.xlsx
    Tab 1: Market Scenario
    Tab 2: Results (summary + exact transaction list)

best_portfolio_transactions.csv
best_portfolio_state.csv
best_portfolio_positions.csv
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

try:
    import gurobipy as gp
    from gurobipy import GRB
except ImportError as e:
    raise SystemExit(
        "gurobipy is not installed.\n"
        "Run: pip install gurobipy pandas numpy openpyxl"
    ) from e


# ============================================================
# CONFIG
# ============================================================

INPUT_FILE = "market_scenario_1.csv"

INITIAL_CAPITAL = 10_000.0
PRICE_DIVISOR = 1400.0

LEVERAGE_TIER = 4.0
INITIAL_MARGIN = 1.0 / LEVERAGE_TIER      # 25%
MAINTENANCE_MARGIN = 0.20
MAINTENANCE_EPS = 1e-7                    # exactly 20% must not survive

SESSION_SECONDS = 150
SETTLEMENT_DELAY = SESSION_SECONDS // 2    # T+0.5 = 75 seconds

MIP_GAP = 0.0
TIME_LIMIT_SECONDS = None                 # e.g. 3600, or None for no limit
THREADS = 0                               # 0 = let Gurobi decide
OUTPUT_FLAG = 1
NUMERIC_FOCUS = 1
USE_TURNOVER_TIEBREAK = True

TRADE_REPORT_TOL_USD = 0.01
POSITION_REPORT_TOL_USD = 0.01

META_COLUMNS = [
    "Scenario",
    "Global_Second",
    "Phase",
    "Phase_Name",
    "Phase_Second",
    "Market_State",
]


# ============================================================
# DATA
# ============================================================

def load_market(path: str | Path):
    df = pd.read_csv(path)

    missing = [c for c in META_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    tickers = [c for c in df.columns if c not in META_COLUMNS]
    if not tickers:
        raise ValueError("No ticker columns found.")

    raw = df[tickers].apply(pd.to_numeric, errors="raise").to_numpy(float)

    if np.isnan(raw).any():
        raise ValueError("NaN price found.")
    if (raw <= 0).any():
        r, c = np.argwhere(raw <= 0)[0]
        raise ValueError(
            f"Non-positive price at CSV row {r+2}, ticker {tickers[c]}."
        )

    price = raw / PRICE_DIVISOR

    if len(df) != 1800:
        print(f"WARNING: expected 1800 rows, got {len(df)}.")

    expected = np.arange(1, len(df) + 1)
    actual = df["Global_Second"].to_numpy()
    if not np.array_equal(expected, actual):
        print(
            "WARNING: Global_Second is not exactly 1..T. "
            "Row order will be treated as time order."
        )

    return df, tickers, price


def timer_display(phase_second: int) -> str:
    remaining = max(0, 300 - int(phase_second))
    return f"{remaining // 60:02d}:{remaining % 60:02d}"


# ============================================================
# MODEL
# ============================================================

def build_model(price: np.ndarray):
    """
    All monetary variables are normalized by INITIAL_CAPITAL.

    B[i,t] = market value bought at t
    S[i,t] = market value sold at t
    X[i,t] = total current market value owned after actions at t
    Y[i,t] = current market value of settled/sellable shares after actions at t

    E[t]   = total equity
    F[t]   = eligible equity excluding pending SELL receivables
    Z[t]   = BUY indicator for exact initial-margin condition

    Portfolio V[t] = sum_i X[i,t]
    Pending sale receivable = E[t] - F[t]
    Settled net balance = F[t] - V[t]
    """

    T, A = price.shape
    D = SETTLEMENT_DELAY

    m = gp.Model("FreeFall_PerfectForesight_Portfolio")
    m.Params.OutputFlag = OUTPUT_FLAG
    m.Params.MIPGap = MIP_GAP
    m.Params.Threads = THREADS
    m.Params.NumericFocus = NUMERIC_FOCUS
    m.Params.Presolve = 2

    if TIME_LIMIT_SECONDS is not None:
        m.Params.TimeLimit = float(TIME_LIMIT_SECONDS)

    B = m.addVars(A, T, lb=0.0, vtype=GRB.CONTINUOUS, name="BUY_value")
    S = m.addVars(A, T, lb=0.0, vtype=GRB.CONTINUOUS, name="SELL_value")
    X = m.addVars(A, T, lb=0.0, vtype=GRB.CONTINUOUS, name="Total_position_value")
    Y = m.addVars(A, T, lb=0.0, vtype=GRB.CONTINUOUS, name="Sellable_position_value")
    E = m.addVars(T, lb=0.0, vtype=GRB.CONTINUOUS, name="Total_equity")
    F = m.addVars(T, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="Eligible_equity")
    Z = m.addVars(T, vtype=GRB.BINARY, name="BUY_indicator")

    # 1) Total position value recurrence.
    for i in range(A):
        m.addConstr(X[i, 0] == B[i, 0] - S[i, 0], name=f"X_init_{i}")

        for t in range(1, T):
            r = price[t, i] / price[t - 1, i]
            m.addConstr(
                X[i, t] == r * X[i, t - 1] + B[i, t] - S[i, t],
                name=f"X_{i}_{t}",
            )

    # 2) Settled / sellable position value recurrence.
    # BUY at k becomes sellable at k + 75.
    for i in range(A):
        m.addConstr(Y[i, 0] == -S[i, 0], name=f"Y_init_{i}")
        m.addConstr(Y[i, 0] <= X[i, 0], name=f"sellable_le_total_{i}_0")

        for t in range(1, T):
            r = price[t, i] / price[t - 1, i]

            if t >= D:
                k = t - D
                settlement_factor = price[t, i] / price[k, i]
                matured = settlement_factor * B[i, k]
            else:
                matured = 0.0

            m.addConstr(
                Y[i, t] == r * Y[i, t - 1] + matured - S[i, t],
                name=f"Y_{i}_{t}",
            )
            m.addConstr(
                Y[i, t] <= X[i, t],
                name=f"sellable_le_total_{i}_{t}",
            )

    # 3) Total equity recurrence.
    # Current-price trades do not change equity; only price changes do.
    m.addConstr(E[0] == 1.0, name="equity_init")

    for t in range(1, T):
        pnl = gp.quicksum(
            X[i, t - 1] * (price[t, i] / price[t - 1, i] - 1.0)
            for i in range(A)
        )
        m.addConstr(E[t] == E[t - 1] + pnl, name=f"equity_{t}")

    # 4) Eligible equity F excludes unsettled SELL receivables.
    total_sell_0 = gp.quicksum(S[i, 0] for i in range(A))
    m.addConstr(F[0] == 1.0 - total_sell_0, name="eligible_equity_init")

    for t in range(1, T):
        pnl = gp.quicksum(
            X[i, t - 1] * (price[t, i] / price[t - 1, i] - 1.0)
            for i in range(A)
        )
        current_sells = gp.quicksum(S[i, t] for i in range(A))
        settled_sells = (
            gp.quicksum(S[i, t - D] for i in range(A))
            if t >= D else 0.0
        )

        m.addConstr(
            F[t] == F[t - 1] + pnl - current_sells + settled_sells,
            name=f"eligible_equity_{t}",
        )

    # Pending sale receivable = E - F >= 0.
    for t in range(T):
        m.addConstr(E[t] >= F[t], name=f"pending_receivable_nonnegative_{t}")

    # 5) Maintenance margin at every tick.
    maintenance_required = MAINTENANCE_MARGIN + MAINTENANCE_EPS
    V_expr = []

    for t in range(T):
        V_t = gp.quicksum(X[i, t] for i in range(A))
        V_expr.append(V_t)
        m.addConstr(
            E[t] >= maintenance_required * V_t,
            name=f"maintenance_margin_{t}",
        )

    # 6) Exact 4x initial-margin rule using indicator constraints.
    # z=0 => no buy.
    # z=1 => F/V >= 25% after the current actions.
    for t in range(T):
        total_buy = gp.quicksum(B[i, t] for i in range(A))

        m.addGenConstrIndicator(
            Z[t], False, total_buy == 0.0,
            name=f"no_buy_when_z0_{t}",
        )
        m.addGenConstrIndicator(
            Z[t], True, F[t] >= INITIAL_MARGIN * V_expr[t],
            name=f"initial_margin_if_buy_{t}",
        )

    # 7) Objective.
    m.ModelSense = GRB.MAXIMIZE

    if USE_TURNOVER_TIEBREAK:
        total_turnover = gp.quicksum(
            B[i, t] + S[i, t]
            for i in range(A)
            for t in range(T)
        )

        m.setObjectiveN(
            E[T - 1], index=0, priority=2, weight=1.0,
            abstol=1e-9, reltol=1e-9, name="Max_Final_Equity",
        )
        m.setObjectiveN(
            -total_turnover, index=1, priority=1, weight=1.0,
            abstol=1e-9, reltol=1e-9, name="Min_Turnover_Tiebreak",
        )
    else:
        m.setObjective(E[T - 1], GRB.MAXIMIZE)

    return m, B, S, X, Y, E, F


# ============================================================
# SOLVE + EXTRACT
# ============================================================

def solve_model(model: gp.Model):
    model.optimize()

    if model.SolCount == 0:
        raise RuntimeError(
            "Gurobi did not find any feasible solution.\n"
            f"Status code: {model.Status}"
        )

    if model.Status == GRB.OPTIMAL:
        print("\nPROVEN GLOBAL OPTIMUM FOUND.")
    else:
        print("\nFeasible solution found, but optimality is not proven.")
        print(f"Status: {model.Status}")
        print(f"Best objective bound: {model.ObjBound}")
        print(f"MIP gap: {model.MIPGap:.8%}")


def extract_results(model, B, S, X, Y, E, F, market_df, tickers, price):
    T, A = price.shape

    Bv = np.zeros((T, A))
    Sv = np.zeros((T, A))
    Xv = np.zeros((T, A))
    Yv = np.zeros((T, A))

    for i in range(A):
        for t in range(T):
            Bv[t, i] = B[i, t].X
            Sv[t, i] = S[i, t].X
            Xv[t, i] = X[i, t].X
            Yv[t, i] = Y[i, t].X

    Ev = np.array([E[t].X for t in range(T)])
    Fv = np.array([F[t].X for t in range(T)])

    B_usd = Bv * INITIAL_CAPITAL
    S_usd = Sv * INITIAL_CAPITAL
    X_usd = Xv * INITIAL_CAPITAL
    Y_usd = Yv * INITIAL_CAPITAL
    equity_usd = Ev * INITIAL_CAPITAL
    eligible_usd = Fv * INITIAL_CAPITAL

    portfolio_usd = X_usd.sum(axis=1)
    sellable_usd = Y_usd.sum(axis=1)
    pending_sale_usd = (Ev - Fv) * INITIAL_CAPITAL

    settled_net_balance_usd = eligible_usd - portfolio_usd
    settled_cash_usd = np.maximum(settled_net_balance_usd, 0.0)
    margin_debt_usd = np.maximum(-settled_net_balance_usd, 0.0)

    with np.errstate(divide="ignore", invalid="ignore"):
        margin_ratio = np.where(
            portfolio_usd > 1e-9,
            equity_usd / portfolio_usd,
            np.nan,
        )
        effective_leverage = np.where(
            equity_usd > 1e-9,
            portfolio_usd / equity_usd,
            np.nan,
        )

    trade_rows = []

    for t in range(T):
        meta = market_df.iloc[t]
        gsec = int(meta["Global_Second"])
        phase = int(meta["Phase"])
        psec = int(meta["Phase_Second"])
        timer = timer_display(psec)

        for i, ticker in enumerate(tickers):
            buy_value = B_usd[t, i]
            sell_value = S_usd[t, i]

            if buy_value > TRADE_REPORT_TOL_USD:
                trade_rows.append({
                    "Global_Second": gsec,
                    "Phase": phase,
                    "Phase_Second": psec,
                    "Timer": timer,
                    "Action": "BUY",
                    "Ticker": ticker,
                    "Price_USD": price[t, i],
                    "Quantity": buy_value / price[t, i],
                    "Trade_Value_USD": buy_value,
                    "Settlement_Global_Second": gsec + SETTLEMENT_DELAY,
                    "Settlement_Effect": "Shares become sellable",
                    "Equity_USD": equity_usd[t],
                    "Portfolio_Value_USD": portfolio_usd[t],
                    "Sellable_Portfolio_USD": sellable_usd[t],
                    "Settled_Cash_USD": settled_cash_usd[t],
                    "Margin_Debt_USD": margin_debt_usd[t],
                    "Pending_Sale_Receivable_USD": pending_sale_usd[t],
                    "Margin_Ratio_pct": margin_ratio[t] * 100 if not np.isnan(margin_ratio[t]) else np.nan,
                    "Effective_Leverage_x": effective_leverage[t],
                })

            if sell_value > TRADE_REPORT_TOL_USD:
                trade_rows.append({
                    "Global_Second": gsec,
                    "Phase": phase,
                    "Phase_Second": psec,
                    "Timer": timer,
                    "Action": "SELL",
                    "Ticker": ticker,
                    "Price_USD": price[t, i],
                    "Quantity": sell_value / price[t, i],
                    "Trade_Value_USD": sell_value,
                    "Settlement_Global_Second": gsec + SETTLEMENT_DELAY,
                    "Settlement_Effect": "Cash becomes reusable",
                    "Equity_USD": equity_usd[t],
                    "Portfolio_Value_USD": portfolio_usd[t],
                    "Sellable_Portfolio_USD": sellable_usd[t],
                    "Settled_Cash_USD": settled_cash_usd[t],
                    "Margin_Debt_USD": margin_debt_usd[t],
                    "Pending_Sale_Receivable_USD": pending_sale_usd[t],
                    "Margin_Ratio_pct": margin_ratio[t] * 100 if not np.isnan(margin_ratio[t]) else np.nan,
                    "Effective_Leverage_x": effective_leverage[t],
                })

    trades_df = pd.DataFrame(trade_rows)
    if not trades_df.empty:
        trades_df.sort_values(
            ["Global_Second", "Action", "Ticker"],
            inplace=True,
            ignore_index=True,
        )

    state_df = market_df[[
        "Global_Second", "Phase", "Phase_Name", "Phase_Second", "Market_State"
    ]].copy()

    state_df["Timer"] = state_df["Phase_Second"].map(timer_display)
    state_df["Equity_USD"] = equity_usd
    state_df["Portfolio_Value_USD"] = portfolio_usd
    state_df["Sellable_Portfolio_USD"] = sellable_usd
    state_df["Settled_Cash_USD"] = settled_cash_usd
    state_df["Margin_Debt_USD"] = margin_debt_usd
    state_df["Pending_Sale_Receivable_USD"] = pending_sale_usd
    state_df["Eligible_Equity_USD"] = eligible_usd
    state_df["Margin_Ratio_pct"] = margin_ratio * 100
    state_df["Effective_Leverage_x"] = effective_leverage
    state_df["BUY_Value_USD"] = B_usd.sum(axis=1)
    state_df["SELL_Value_USD"] = S_usd.sum(axis=1)

    pos_rows = []
    for t in range(T):
        gsec = int(market_df.iloc[t]["Global_Second"])
        for i, ticker in enumerate(tickers):
            value = X_usd[t, i]
            if value > POSITION_REPORT_TOL_USD:
                pos_rows.append({
                    "Global_Second": gsec,
                    "Ticker": ticker,
                    "Price_USD": price[t, i],
                    "Position_Value_USD": value,
                    "Quantity": value / price[t, i],
                    "Sellable_Value_USD": Y_usd[t, i],
                    "Sellable_Quantity": Y_usd[t, i] / price[t, i],
                })
    positions_df = pd.DataFrame(pos_rows)

    valid_mr = margin_ratio[~np.isnan(margin_ratio)]
    valid_lev = effective_leverage[~np.isnan(effective_leverage)]
    final_equity = equity_usd[-1]

    summary_rows = [
        ("Solver_Status", model.Status),
        ("Is_Proven_Global_Optimum", model.Status == GRB.OPTIMAL),
        ("MIP_Gap", model.MIPGap if model.IsMIP else 0.0),
        ("Best_Objective_Bound_Normalized", model.ObjBound),
        ("Initial_Capital_USD", INITIAL_CAPITAL),
        ("Final_Equity_USD", final_equity),
        ("Final_Wealth_Multiple", final_equity / INITIAL_CAPITAL),
        ("Final_Return_pct", (final_equity / INITIAL_CAPITAL - 1.0) * 100.0),
        ("Minimum_Margin_Ratio_pct", float(np.min(valid_mr) * 100) if len(valid_mr) else np.nan),
        ("Maximum_Effective_Leverage_x", float(np.max(valid_lev)) if len(valid_lev) else np.nan),
        ("Settlement_Delay_seconds", SETTLEMENT_DELAY),
        ("Initial_Leverage_Tier_x", LEVERAGE_TIER),
        ("Initial_Margin_pct", INITIAL_MARGIN * 100),
        ("Maintenance_Margin_pct", MAINTENANCE_MARGIN * 100),
        ("Price_Divisor", PRICE_DIVISOR),
        ("Transaction_Rows", len(trades_df)),
        ("Continuous_Fractional_Shares", True),
        ("Unlimited_Liquidity", True),
        ("Forced_Liquidation_Path_Allowed", False),
    ]

    summary_df = pd.DataFrame(summary_rows, columns=["Metric", "Value"])
    return summary_df, trades_df, state_df, positions_df


# ============================================================
# OUTPUT
# ============================================================

def write_outputs(market_df, summary_df, trades_df, state_df, positions_df):
    trades_df.to_csv("best_portfolio_transactions.csv", index=False)
    state_df.to_csv("best_portfolio_state.csv", index=False)
    positions_df.to_csv("best_portfolio_positions.csv", index=False)

    with pd.ExcelWriter(
        "best_portfolio_optimizer_output.xlsx",
        engine="openpyxl",
    ) as writer:
        market_df.to_excel(writer, sheet_name="Market Scenario", index=False)
        summary_df.to_excel(writer, sheet_name="Results", index=False, startrow=0)
        trade_start_row = len(summary_df) + 3
        trades_df.to_excel(
            writer,
            sheet_name="Results",
            index=False,
            startrow=trade_start_row,
        )

    print("\nFiles written:")
    print("  best_portfolio_optimizer_output.xlsx")
    print("  best_portfolio_transactions.csv")
    print("  best_portfolio_state.csv")
    print("  best_portfolio_positions.csv")


# ============================================================
# MAIN
# ============================================================

def main():
    path = Path(INPUT_FILE)

    if not path.exists():
        raise FileNotFoundError(
            f"Cannot find {INPUT_FILE!r}.\n"
            "Put market_scenario_1.csv in the same folder as this script."
        )

    market_df, tickers, price = load_market(path)
    T, A = price.shape

    print("=" * 72)
    print("FREE FALL 2.0 — EXACT PERFECT-FORESIGHT PORTFOLIO OPTIMIZER")
    print("=" * 72)
    print(f"Ticks:                 {T:,}")
    print(f"Tickers:               {A:,}")
    print(f"Price observations:    {T*A:,}")
    print(f"Initial capital:        ${INITIAL_CAPITAL:,.2f}")
    print(f"Initial leverage tier:  {LEVERAGE_TIER:.1f}x")
    print(f"Initial margin:         {INITIAL_MARGIN:.2%}")
    print(f"Maintenance margin:     {MAINTENANCE_MARGIN:.2%}")
    print(f"T+0.5 delay:            {SETTLEMENT_DELAY} seconds")
    print(f"Price divisor:          {PRICE_DIVISOR}")
    print()

    model, B, S, X, Y, E, F = build_model(price)

    print("Model built.")
    print(f"Variables:   {model.NumVars:,}")
    print(f"Constraints: {model.NumConstrs:,}")
    print(f"GenConstrs:  {model.NumGenConstrs:,}")
    print()

    solve_model(model)

    summary_df, trades_df, state_df, positions_df = extract_results(
        model, B, S, X, Y, E, F,
        market_df, tickers, price,
    )

    print("\nSUMMARY")
    print(summary_df.to_string(index=False))

    if not trades_df.empty:
        print("\nFIRST 25 TRANSACTIONS")
        show_cols = [
            "Global_Second", "Timer", "Action", "Ticker",
            "Price_USD", "Quantity", "Trade_Value_USD",
            "Settlement_Global_Second", "Equity_USD",
            "Margin_Ratio_pct", "Effective_Leverage_x",
        ]
        print(trades_df[show_cols].head(25).to_string(index=False))

    write_outputs(
        market_df, summary_df, trades_df, state_df, positions_df
    )

    print("\nInterpretation:")
    print(
        "If Is_Proven_Global_Optimum = True, this is the mathematical "
        "continuous-share maximum under the encoded rules."
    )
    print(
        "If Gurobi stops because of a time limit, use MIP_Gap and "
        "Best_Objective_Bound to measure remaining uncertainty."
    )


if __name__ == "__main__":
    main()
