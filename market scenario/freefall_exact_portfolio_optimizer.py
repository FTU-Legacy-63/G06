from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

try:
    from pyscipopt import Model, quicksum, SCIP_PARAMEMPHASIS
except ImportError as e:
    raise SystemExit(
        "Install dependencies first:\n"
        "pip install pyscipopt pandas numpy openpyxl"
    ) from e

# ============================================================
# CONFIG
# ============================================================
INPUT_FILE = "market_scenario_1.csv"
INITIAL_CAPITAL = 10_000.0
PRICE_DIVISOR = 1400.0

LEVERAGE_TIER = 4.0
INITIAL_MARGIN = 1.0 / LEVERAGE_TIER          # 25%
MAINTENANCE_MARGIN = 0.20
MARGIN_EPS = 0.00001                          # 20.001% survival floor
SURVIVAL_MARGIN = MAINTENANCE_MARGIN + MARGIN_EPS

SESSION_SECONDS = 150
SETTLEMENT_DELAY = SESSION_SECONDS // 2       # T+0.5 = 75 sec

INTEGER_SHARES = False                        # False = continuous upper bound
RELATIVE_GAP = 0.0                            # 0 = prove optimum if possible
TIME_LIMIT_SECONDS = None                     # e.g. 3600 for a 1-hour run
SAFE_PRUNING = True
USE_WARM_START = True
TRY_MIP_START = True

TRADE_TOL = 1e-8
POSITION_VALUE_TOL = 0.01

META_COLUMNS = [
    "Scenario",
    "Global_Second",
    "Phase",
    "Phase_Name",
    "Phase_Second",
    "Market_State",
]

# Previously found concentrated T+0.5 route.
# It is revalidated against the CURRENT input file before use.
WARM_ROUTE = [
    ("KODEX KOSDAQ150 Leverage", 27, 112),
    ("Hyundai Mobis",            193, 268),
    ("LG Chem",                  345, 452),
    ("POSCO Future M",           551, 628),
    ("Kakao",                    703, 860),
    ("LG Chem",                  992, 1067),
    ("Vintrumite",               1142, 1220),
    ("Vintrumite",               1295, 1527),
    ("Wonik IPS",                1650, 1725),
]


# ============================================================
# INPUT
# ============================================================
def locate_input_file() -> Path:
    p = Path(INPUT_FILE)

    if p.exists():
        return p

    matches = sorted(Path(".").glob("market_scenario_1*.csv"))

    if matches:
        print(f"Using {matches[0].name!r}")
        return matches[0]

    raise FileNotFoundError(
        "Put market_scenario_1.csv in the same folder as this script."
    )


def load_market(path: Path):
    df = pd.read_csv(path)

    missing = [c for c in META_COLUMNS if c not in df.columns]

    if missing:
        raise ValueError(f"Missing metadata columns: {missing}")

    tickers = [
        c
        for c in df.columns
        if c not in META_COLUMNS
    ]

    if not tickers:
        raise ValueError("No ticker columns found.")

    raw = (
        df[tickers]
        .apply(pd.to_numeric, errors="raise")
        .to_numpy(float)
    )

    if np.isnan(raw).any():
        raise ValueError("NaN price found.")

    if (raw <= 0).any():
        r, c = np.argwhere(raw <= 0)[0]

        raise ValueError(
            f"Non-positive price at row {r}, ticker {tickers[c]}"
        )

    price = raw / PRICE_DIVISOR

    return df, tickers, price


def timer_display(phase_second: int) -> str:
    remain = max(
        0,
        300 - int(phase_second),
    )

    return f"{remain // 60:02d}:{remain % 60:02d}"


# ============================================================
# SAFE PRUNING
# ============================================================
def future_max_matrix(
    price: np.ndarray,
) -> np.ndarray:

    T, A = price.shape

    out = np.empty_like(price)

    out[-1] = price[-1]

    running = price[-1].copy()

    for t in range(
        T - 2,
        -1,
        -1,
    ):
        out[t] = running

        running = np.maximum(
            running,
            price[t],
        )

    return out


def no_future_upside_mask(
    price: np.ndarray,
) -> np.ndarray:
    """
    BUY[i,t] can be removed if ticker i never trades above
    its current price again.

    With long-only trading and zero dividends,
    cash weakly dominates such a position.
    """

    if not SAFE_PRUNING:
        mask = np.ones_like(
            price,
            dtype=bool,
        )

        mask[-1] = False

        return mask

    future_max = future_max_matrix(
        price
    )

    allowed = (
        future_max
        >
        price * (1.0 + 1e-12)
    )

    allowed[-1] = False

    return allowed


def dominance_prune(
    price: np.ndarray,
    buy_mask: np.ndarray,
):
    """
    Exact pruning when fractional shares are allowed.

    At second t, B dominates A if for every future u > t:

        P_B[u] / P_B[t]
        >=
        P_A[u] / P_A[t]

    Then the same dollar exposure in B never has lower
    mark-to-market value than A.

    Therefore B gives:
        - no worse P&L,
        - no worse margin safety,
        - same settlement timing,
        - no worse exit value.

    So BUY(A,t) can safely be removed.
    """

    if (
        not SAFE_PRUNING
        or INTEGER_SHARES
    ):
        return buy_mask.copy(), 0

    T, A = price.shape

    dominated = np.zeros(
        (T, A),
        dtype=bool,
    )

    tol = 1e-12

    for a in range(A):

        for b in range(
            a + 1,
            A,
        ):

            ratio = (
                price[:, b]
                /
                price[:, a]
            )

            fut_min = np.empty(T)
            fut_max = np.empty(T)

            run_min = ratio[-1]
            run_max = ratio[-1]

            fut_min[-1] = ratio[-1]
            fut_max[-1] = ratio[-1]

            for t in range(
                T - 2,
                -1,
                -1,
            ):

                fut_min[t] = run_min
                fut_max[t] = run_max

                run_min = min(
                    run_min,
                    ratio[t],
                )

                run_max = max(
                    run_max,
                    ratio[t],
                )

            b_dom_a = (
                fut_min
                >=
                ratio * (1.0 - tol)
            )

            a_dom_b = (
                fut_max
                <=
                ratio * (1.0 + tol)
            )

            b_dom_a[-1] = False
            a_dom_b[-1] = False

            both = (
                b_dom_a
                &
                a_dom_b
            )

            dominated[:, a] |= (
                b_dom_a
                &
                ~both
            )

            # If future relative paths are identical,
            # keep lower-index ticker a.
            dominated[:, b] |= (
                a_dom_b
                |
                both
            )

    pruned = (
        buy_mask
        &
        dominated
    )

    final_mask = (
        buy_mask
        &
        ~dominated
    )

    return (
        final_mask,
        int(pruned.sum()),
    )


def compute_buy_mask(
    price: np.ndarray,
):
    basic = no_future_upside_mask(
        price
    )

    total = (
        price.shape[0]
        *
        price.shape[1]
    )

    basic_pruned = (
        total
        -
        int(basic.sum())
    )

    final, dom_pruned = dominance_prune(
        price,
        basic,
    )

    return (
        final,
        basic_pruned,
        dom_pruned,
    )


def earliest_sell_times(
    buy_mask: np.ndarray,
) -> np.ndarray:

    T, A = buy_mask.shape

    out = np.full(
        A,
        T + 1,
        dtype=int,
    )

    for i in range(A):

        idx = np.flatnonzero(
            buy_mask[:, i]
        )

        if len(idx):
            out[i] = int(
                idx[0]
                +
                SETTLEMENT_DELAY
            )

    return out


def equity_upper_bound(
    price: np.ndarray,
) -> np.ndarray:
    """
    Rigorous optimistic equity upper bound.

    Used only for tightening MILP variable upper bounds.

    Before each price move:

        Gross Exposure
        <=
        Equity / maintenance margin

    The bound assumes all exposure can magically be placed
    in the best one-tick winner.

    This is intentionally optimistic, therefore safe.
    """

    T, _ = price.shape

    ub = np.empty(T)

    ub[0] = INITIAL_CAPITAL

    for t in range(
        1,
        T,
    ):

        best_ret = max(
            0.0,
            float(
                np.max(
                    price[t]
                    /
                    price[t - 1]
                    -
                    1.0
                )
            ),
        )

        ub[t] = (
            ub[t - 1]
            *
            (
                1.0
                +
                best_ret
                /
                SURVIVAL_MARGIN
            )
        )

        if (
            not np.isfinite(ub[t])
            or ub[t] > 1e250
        ):

            ub[t:] = 1e250

            break

    return ub


# ============================================================
# ROUTE SIMULATOR / VALIDATOR
# ============================================================
def simulate_actions(
    price: np.ndarray,
    Bq: np.ndarray,
    Sq: np.ndarray,
):
    """
    Timing inside second t:

    1. New market price arrives.
    2. Existing holdings are marked to market.
    3. Maintenance Margin is checked BEFORE player action.
    4. BUY / SELL executes.
    5. Settlement queues update.

    Important:
    The player cannot sell on the exact tick of a margin call
    to escape liquidation.
    """

    T, A = price.shape

    D = SETTLEMENT_DELAY

    # Total shares economically owned.
    H = np.zeros(
        (T, A)
    )

    # Shares that are settled and sellable.
    R = np.zeros(
        (T, A)
    )

    # Total account equity,
    # including pending sale receivables.
    E = np.zeros(T)

    # Eligible equity,
    # excluding pending sale receivables.
    F = np.zeros(T)

    # Any BUY at second t?
    Z = np.zeros(T)

    # --------------------------------------------------------
    # t = 0
    # --------------------------------------------------------
    E[0] = INITIAL_CAPITAL

    H[0] = (
        Bq[0]
        -
        Sq[0]
    )

    R[0] = -Sq[0]

    F[0] = (
        INITIAL_CAPITAL
        -
        float(
            np.dot(
                Sq[0],
                price[0],
            )
        )
    )

    Z[0] = (
        1.0
        if np.dot(
            Bq[0],
            price[0],
        ) > 1e-10
        else 0.0
    )

    if (
        np.min(H[0]) < -1e-8
        or
        np.min(R[0]) < -1e-8
    ):

        return {
            "feasible": False,
            "reason": "Invalid t=0 holdings/sale.",
        }

    V0 = float(
        np.dot(
            H[0],
            price[0],
        )
    )

    if (
        Z[0] > 0.5
        and
        F[0] + 1e-7
        <
        INITIAL_MARGIN * V0
    ):

        return {
            "feasible": False,
            "reason": "Initial-margin violation at t=0.",
        }

    # --------------------------------------------------------
    # t >= 1
    # --------------------------------------------------------
    for t in range(
        1,
        T,
    ):

        # Mark previous holdings to current price.
        pnl = float(
            np.dot(
                H[t - 1],
                price[t]
                -
                price[t - 1],
            )
        )

        E[t] = (
            E[t - 1]
            +
            pnl
        )

        # Pre-trade portfolio value at current price.
        pre_value = float(
            np.dot(
                H[t - 1],
                price[t],
            )
        )

        # Maintenance Margin check BEFORE actions.
        if pre_value > 1e-10:

            mr = (
                E[t]
                /
                pre_value
            )

            if (
                mr + 1e-10
                <
                SURVIVAL_MARGIN
            ):

                return {
                    "feasible": False,
                    "reason": (
                        f"Maintenance breach before action "
                        f"at second {t + 1}: "
                        f"{mr:.8%}"
                    ),
                }

        # Execute current BUY / SELL.
        H[t] = (
            H[t - 1]
            +
            Bq[t]
            -
            Sq[t]
        )

        # BUY from 75 seconds ago becomes sellable now.
        matured_buy = (
            Bq[t - D]
            if t >= D
            else 0.0
        )

        R[t] = (
            R[t - 1]
            +
            matured_buy
            -
            Sq[t]
        )

        # Current SELL proceeds become pending.
        current_sell = float(
            np.dot(
                Sq[t],
                price[t],
            )
        )

        # SELL from 75 seconds ago settles now.
        settled_sell = (
            float(
                np.dot(
                    Sq[t - D],
                    price[t - D],
                )
            )
            if t >= D
            else 0.0
        )

        F[t] = (
            F[t - 1]
            +
            pnl
            -
            current_sell
            +
            settled_sell
        )

        Z[t] = (
            1.0
            if np.dot(
                Bq[t],
                price[t],
            ) > 1e-10
            else 0.0
        )

        # Cannot have negative holdings.
        if np.min(H[t]) < -1e-7:

            return {
                "feasible": False,
                "reason": (
                    f"Negative holdings "
                    f"at second {t + 1}."
                ),
            }

        # Cannot sell unsettled shares.
        if np.min(R[t]) < -1e-7:

            return {
                "feasible": False,
                "reason": (
                    f"Sold unsettled shares "
                    f"at second {t + 1}."
                ),
            }

        # Eligible equity cannot exceed total equity.
        if F[t] > E[t] + 1e-6:

            return {
                "feasible": False,
                "reason": (
                    f"F > E "
                    f"at second {t + 1}."
                ),
            }

        # New BUY requires 25% initial margin.
        if Z[t] > 0.5:

            post_value = float(
                np.dot(
                    H[t],
                    price[t],
                )
            )

            if (
                F[t] + 1e-7
                <
                INITIAL_MARGIN
                *
                post_value
            ):

                return {
                    "feasible": False,
                    "reason": (
                        f"25% initial-margin violation "
                        f"after BUY at second {t + 1}."
                    ),
                }

    return {
        "feasible": True,
        "reason": "OK",
        "H": H,
        "R": R,
        "E": E,
        "F": F,
        "Z": Z,
        "final_equity": float(E[-1]),
    }


def max_safe_leverage(
    relative_prices: np.ndarray,
) -> float:
    """
    Concentrated warm-start trade.

    Initial exposure = L * Equity.

    At relative price r:

        Portfolio = L * E * r

        Equity =
            E + L * E * (r - 1)

    Require:

        Equity / Portfolio
        >=
        SURVIVAL_MARGIN
    """

    min_r = float(
        np.min(
            relative_prices
        )
    )

    denom = (
        1.0
        -
        min_r
        *
        (
            1.0
            -
            SURVIVAL_MARGIN
        )
    )

    if denom <= 0:
        return LEVERAGE_TIER

    bound = (
        1.0
        /
        denom
    )

    return max(
        0.0,
        min(
            LEVERAGE_TIER,
            bound
            *
            (1.0 - 1e-8),
        ),
    )


def build_verified_warm_start(
    price: np.ndarray,
    tickers: list[str],
):
    """
    Reconstructs the previous concentrated path.

    It is NOT trusted automatically.

    It must pass the same:
        - T+0.5 rule,
        - pre-trade maintenance rule,
        - 25% initial margin rule,
        - current CSV prices.
    """

    if not USE_WARM_START:
        return None

    T, A = price.shape

    idx = {
        ticker: i
        for i, ticker
        in enumerate(tickers)
    }

    # Validate route references.
    for ticker, bsec, ssec in WARM_ROUTE:

        if ticker not in idx:
            return None

        if (
            bsec < 1
            or
            ssec > T
            or
            ssec - bsec
            <
            SETTLEMENT_DELAY
        ):
            return None

    # Cash from previous SELL must settle
    # before the next concentrated BUY.
    for k in range(
        1,
        len(WARM_ROUTE),
    ):

        if (
            WARM_ROUTE[k][1]
            <
            WARM_ROUTE[k - 1][2]
            +
            SETTLEMENT_DELAY
        ):
            return None

    Bq = np.zeros(
        (T, A)
    )

    Sq = np.zeros(
        (T, A)
    )

    equity = INITIAL_CAPITAL

    rows = []

    for (
        ticker,
        bsec,
        ssec,
    ) in WARM_ROUTE:

        i = idx[ticker]

        b = bsec - 1
        s = ssec - 1

        buy_p = price[b, i]
        sell_p = price[s, i]

        if sell_p <= buy_p:
            return None

        relative_path = (
            price[b:s + 1, i]
            /
            buy_p
        )

        L = max_safe_leverage(
            relative_path
        )

        if L <= 1e-9:
            return None

        qty = (
            L
            *
            equity
            /
            buy_p
        )

        Bq[b, i] += qty
        Sq[s, i] += qty

        end_equity = (
            equity
            +
            qty
            *
            (
                sell_p
                -
                buy_p
            )
        )

        rows.append({
            "Ticker": ticker,
            "Buy_Global_Second": bsec,
            "Sell_Global_Second": ssec,
            "Leverage_x": L,
            "Quantity": qty,
            "Buy_Price_USD": buy_p,
            "Sell_Price_USD": sell_p,
            "Starting_Equity_USD": equity,
            "Ending_Equity_USD": end_equity,
        })

        equity = end_equity

    sim = simulate_actions(
        price,
        Bq,
        Sq,
    )

    if not sim["feasible"]:

        print(
            "Warm route rejected:",
            sim["reason"],
        )

        return None

    return {
        "Bq": Bq,
        "Sq": Sq,
        "route": pd.DataFrame(rows),
        **sim,
    }


# ============================================================
# MILP MODEL
# ============================================================
def build_model(
    price: np.ndarray,
    tickers: list[str],
    buy_mask: np.ndarray,
    earliest_sell: np.ndarray,
    eq_ub: np.ndarray,
    incumbent,
):
    T, A = price.shape

    D = SETTLEMENT_DELAY

    model = Model(
        "FreeFall_PerfectForesight_Portfolio"
    )

    model.setRealParam(
        "limits/gap",
        RELATIVE_GAP,
    )

    if TIME_LIMIT_SECONDS is not None:

        model.setRealParam(
            "limits/time",
            float(TIME_LIMIT_SECONDS),
        )

    model.setIntParam(
        "display/verblevel",
        4,
    )

    model.setEmphasis(
        SCIP_PARAMEMPHASIS.OPTIMALITY
    )

    qty_type = (
        "I"
        if INTEGER_SHARES
        else "C"
    )

    B = {}
    S = {}
    H = {}
    R = {}
    E = {}
    F = {}
    Z = {}

    # A surviving account cannot have gross exposure
    # above Equity / maintenance margin.
    gross_ub = (
        eq_ub
        /
        SURVIVAL_MARGIN
    )

    # --------------------------------------------------------
    # EQUITY VARIABLES
    # --------------------------------------------------------
    for t in range(T):

        E[t] = model.addVar(
            lb=0.0,
            ub=float(eq_ub[t]),
            vtype="C",
            name=f"E_{t}",
        )

        F[t] = model.addVar(
            lb=None,
            ub=float(eq_ub[t]),
            vtype="C",
            name=f"F_{t}",
        )

    # --------------------------------------------------------
    # POSITION / TRADE VARIABLES
    # --------------------------------------------------------
    for i in range(A):

        for t in range(T):

            p = price[t, i]

            h_ub = float(
                gross_ub[t]
                /
                p
            )

            H[i, t] = model.addVar(
                lb=0.0,
                ub=h_ub,
                vtype="C",
                name=f"H_{i}_{t}",
            )

            R[i, t] = model.addVar(
                lb=0.0,
                ub=h_ub,
                vtype="C",
                name=f"R_{i}_{t}",
            )

            # BUY variable created only when
            # safe preprocessing keeps it.
            if bool(
                buy_mask[t, i]
            ):

                b_ub = float(
                    LEVERAGE_TIER
                    *
                    eq_ub[t]
                    /
                    p
                )

                B[i, t] = model.addVar(
                    lb=0.0,
                    ub=b_ub,
                    vtype=qty_type,
                    name=f"B_{i}_{t}",
                )

            # SELL cannot occur before any
            # potentially purchased shares settle.
            if t >= earliest_sell[i]:

                S[i, t] = model.addVar(
                    lb=0.0,
                    ub=h_ub,
                    vtype=qty_type,
                    name=f"S_{i}_{t}",
                )

    buy_times = sorted({
        t
        for (_, t)
        in B
    })

    # One binary variable per second where BUY is possible.
    for t in buy_times:

        Z[t] = model.addVar(
            vtype="B",
            name=f"BUY_ACTIVE_{t}",
        )

    def b(i, t):
        return B.get(
            (i, t),
            0.0,
        )

    def s(i, t):
        return S.get(
            (i, t),
            0.0,
        )

    # ========================================================
    # TOTAL HOLDINGS
    # ========================================================
    for i in range(A):

        model.addCons(
            H[i, 0]
            ==
            b(i, 0)
            -
            s(i, 0),
            name=f"H_init_{i}",
        )

        for t in range(
            1,
            T,
        ):

            model.addCons(
                H[i, t]
                ==
                H[i, t - 1]
                +
                b(i, t)
                -
                s(i, t),
                name=f"H_{i}_{t}",
            )

    # ========================================================
    # SELLABLE / SETTLED SHARES
    # ========================================================
    #
    # BUY at t becomes sellable at t+75.
    #
    # R >= 0 automatically prevents
    # selling unsettled shares.
    #
    # R <= H is redundant and therefore omitted.
    # ========================================================
    for i in range(A):

        model.addCons(
            R[i, 0]
            ==
            -s(i, 0),
            name=f"R_init_{i}",
        )

        for t in range(
            1,
            T,
        ):

            matured = (
                b(
                    i,
                    t - D,
                )
                if t >= D
                else 0.0
            )

            model.addCons(
                R[i, t]
                ==
                R[i, t - 1]
                +
                matured
                -
                s(i, t),
                name=f"R_{i}_{t}",
            )

    # ========================================================
    # TOTAL EQUITY
    # ========================================================
    model.addCons(
        E[0]
        ==
        INITIAL_CAPITAL,
        name="E_init",
    )

    for t in range(
        1,
        T,
    ):

        pnl = quicksum(
            H[i, t - 1]
            *
            (
                price[t, i]
                -
                price[t - 1, i]
            )
            for i in range(A)
        )

        model.addCons(
            E[t]
            ==
            E[t - 1]
            +
            pnl,
            name=f"E_{t}",
        )

    # ========================================================
    # ELIGIBLE EQUITY
    # ========================================================
    #
    # F excludes pending SELL receivables.
    #
    # A SELL today decreases F.
    #
    # That exact sale value is added back
    # 75 seconds later when cash settles.
    # ========================================================
    sell0 = quicksum(
        s(i, 0)
        *
        price[0, i]
        for i in range(A)
    )

    model.addCons(
        F[0]
        ==
        INITIAL_CAPITAL
        -
        sell0,
        name="F_init",
    )

    for t in range(
        1,
        T,
    ):

        pnl = quicksum(
            H[i, t - 1]
            *
            (
                price[t, i]
                -
                price[t - 1, i]
            )
            for i in range(A)
        )

        current_sell = quicksum(
            s(i, t)
            *
            price[t, i]
            for i in range(A)
        )

        settled_sell = (
            quicksum(
                s(
                    i,
                    t - D,
                )
                *
                price[t - D, i]
                for i in range(A)
            )
            if t >= D
            else 0.0
        )

        model.addCons(
            F[t]
            ==
            F[t - 1]
            +
            pnl
            -
            current_sell
            +
            settled_sell,
            name=f"F_{t}",
        )

    # Pending receivable cannot be negative.
    for t in range(T):

        model.addCons(
            F[t]
            <=
            E[t],
            name=f"F_le_E_{t}",
        )

    # ========================================================
    # PRE-TRADE MAINTENANCE MARGIN
    # ========================================================
    #
    # New price arrives first.
    #
    # Margin call is checked before current-tick SELLs.
    #
    # So a player cannot sell on the margin-call tick
    # to escape liquidation.
    # ========================================================
    for t in range(
        1,
        T,
    ):

        pre_value = quicksum(
            H[i, t - 1]
            *
            price[t, i]
            for i in range(A)
        )

        model.addCons(
            SURVIVAL_MARGIN
            *
            pre_value
            <=
            E[t],
            name=f"maintenance_pre_{t}",
        )

    # ========================================================
    # CONDITIONAL 4x INITIAL MARGIN
    # ========================================================
    #
    # If no BUY:
    #     portfolio may remain between 20% and 25%.
    #
    # If BUY:
    #     F / post-trade gross portfolio >=25%.
    # ========================================================
    for t in buy_times:

        total_buy = quicksum(
            B[i, t]
            *
            price[t, i]
            for i in range(A)
            if (i, t) in B
        )

        post_value = quicksum(
            H[i, t]
            *
            price[t, i]
            for i in range(A)
        )

        # z = 0 -> no BUY.
        model.addConsIndicator(
            total_buy
            <=
            0.0,
            binvar=Z[t],
            activeone=False,
            name=f"no_buy_if_z0_{t}",
        )

        # z = 1 -> 25% initial margin.
        model.addConsIndicator(
            INITIAL_MARGIN
            *
            post_value
            -
            F[t]
            <=
            0.0,
            binvar=Z[t],
            activeone=True,
            name=f"init_margin_if_buy_{t}",
        )

    # ========================================================
    # VERIFIED INCUMBENT OBJECTIVE FLOOR
    # ========================================================
    if incumbent is not None:

        model.addCons(
            E[T - 1]
            >=
            incumbent["final_equity"]
            *
            (1.0 - 1e-9),
            name="verified_incumbent_floor",
        )

    # ========================================================
    # OBJECTIVE
    # ========================================================
    model.setObjective(
        E[T - 1],
        "maximize",
    )

    return (
        model,
        B,
        S,
        H,
        R,
        E,
        F,
        Z,
    )


# ============================================================
# MIP START
# ============================================================
def add_mip_start(
    model,
    B,
    S,
    H,
    R,
    E,
    F,
    Z,
    incumbent,
):
    if (
        not TRY_MIP_START
        or incumbent is None
    ):
        return False

    try:

        Bq = incumbent["Bq"]
        Sq = incumbent["Sq"]

        Hv = incumbent["H"]
        Rv = incumbent["R"]

        Ev = incumbent["E"]
        Fv = incumbent["F"]
        Zv = incumbent["Z"]

        T, A = Bq.shape

        sol = model.createOrigSol()

        for (
            i,
            t,
        ), var in B.items():

            model.setSolVal(
                sol,
                var,
                float(
                    Bq[t, i]
                ),
            )

        for (
            i,
            t,
        ), var in S.items():

            model.setSolVal(
                sol,
                var,
                float(
                    Sq[t, i]
                ),
            )

        for i in range(A):

            for t in range(T):

                model.setSolVal(
                    sol,
                    H[i, t],
                    float(
                        Hv[t, i]
                    ),
                )

                model.setSolVal(
                    sol,
                    R[i, t],
                    float(
                        Rv[t, i]
                    ),
                )

        for t in range(T):

            model.setSolVal(
                sol,
                E[t],
                float(Ev[t]),
            )

            model.setSolVal(
                sol,
                F[t],
                float(Fv[t]),
            )

        for t, var in Z.items():

            model.setSolVal(
                sol,
                var,
                float(Zv[t]),
            )

        feasible = model.checkSol(
            sol,
            printreason=False,
            completely=True,
            original=True,
        )

        if not feasible:

            print(
                "SCIP rejected warm MIP start; "
                "objective floor is still active."
            )

            return False

        accepted = model.addSol(
            sol
        )

        if accepted:

            print(
                "Warm MIP start accepted."
            )

        else:

            print(
                "Warm MIP start not stored."
            )

        return bool(
            accepted
        )

    except Exception as exc:

        print(
            f"Warm MIP start skipped: {exc}"
        )

        print(
            "Verified objective floor is still active."
        )

        return False


# ============================================================
# EXTRACT RESULTS
# ============================================================
def extract_results(
    model,
    B,
    S,
    H,
    R,
    E,
    F,
    market_df,
    tickers,
    price,
    stats,
    incumbent,
):
    T, A = price.shape

    Bq = np.zeros(
        (T, A)
    )

    Sq = np.zeros(
        (T, A)
    )

    Hq = np.zeros(
        (T, A)
    )

    Rq = np.zeros(
        (T, A)
    )

    for (
        i,
        t,
    ), var in B.items():

        Bq[t, i] = model.getVal(
            var
        )

    for (
        i,
        t,
    ), var in S.items():

        Sq[t, i] = model.getVal(
            var
        )

    for i in range(A):

        for t in range(T):

            Hq[t, i] = model.getVal(
                H[i, t]
            )

            Rq[t, i] = model.getVal(
                R[i, t]
            )

    equity = np.array([
        model.getVal(
            E[t]
        )
        for t in range(T)
    ])

    eligible = np.array([
        model.getVal(
            F[t]
        )
        for t in range(T)
    ])

    # --------------------------------------------------------
    # PORTFOLIO STATE
    # --------------------------------------------------------
    position_value = (
        Hq
        *
        price
    )

    sellable_value = (
        Rq
        *
        price
    )

    portfolio = (
        position_value.sum(
            axis=1
        )
    )

    sellable_portfolio = (
        sellable_value.sum(
            axis=1
        )
    )

    pending_sale = (
        equity
        -
        eligible
    )

    # Eligible Equity =
    # Portfolio + Settled Cash - Margin Debt
    settled_net = (
        eligible
        -
        portfolio
    )

    settled_cash = np.maximum(
        settled_net,
        0.0,
    )

    margin_debt = np.maximum(
        -settled_net,
        0.0,
    )

    # --------------------------------------------------------
    # PRE-TRADE PORTFOLIO
    # --------------------------------------------------------
    pre_value = np.zeros(T)

    for t in range(
        1,
        T,
    ):

        pre_value[t] = float(
            np.dot(
                Hq[t - 1],
                price[t],
            )
        )

    # --------------------------------------------------------
    # MARGIN RATIOS
    # --------------------------------------------------------
    pre_mr = np.full(
        T,
        np.nan,
    )

    active_pre = (
        pre_value > 1e-9
    )

    pre_mr[active_pre] = (
        equity[active_pre]
        /
        pre_value[active_pre]
    )

    post_mr = np.full(
        T,
        np.nan,
    )

    active_post = (
        portfolio > 1e-9
    )

    post_mr[active_post] = (
        equity[active_post]
        /
        portfolio[active_post]
    )

    # --------------------------------------------------------
    # EFFECTIVE LEVERAGE
    # --------------------------------------------------------
    leverage = np.full(
        T,
        np.nan,
    )

    alive = (
        equity > 1e-9
    )

    leverage[alive] = (
        portfolio[alive]
        /
        equity[alive]
    )

    # ========================================================
    # TRANSACTION LOG
    # ========================================================
    trade_rows = []

    for t in range(T):

        meta = market_df.iloc[t]

        gsec = int(
            meta["Global_Second"]
        )

        psec = int(
            meta["Phase_Second"]
        )

        for i, ticker in enumerate(
            tickers
        ):

            for (
                action,
                qty,
            ) in (
                (
                    "BUY",
                    Bq[t, i],
                ),
                (
                    "SELL",
                    Sq[t, i],
                ),
            ):

                if qty <= TRADE_TOL:
                    continue

                trade_rows.append({
                    "Global_Second": gsec,
                    "Phase": int(
                        meta["Phase"]
                    ),
                    "Phase_Second": psec,
                    "Timer": timer_display(
                        psec
                    ),
                    "Action": action,
                    "Ticker": ticker,
                    "Price_USD": price[t, i],
                    "Quantity": qty,
                    "Trade_Value_USD": (
                        qty
                        *
                        price[t, i]
                    ),
                    "Settlement_Global_Second": (
                        gsec
                        +
                        SETTLEMENT_DELAY
                    ),
                    "Settlement_Effect": (
                        "Shares become sellable"
                        if action == "BUY"
                        else "Cash becomes reusable"
                    ),
                    "Equity_USD": equity[t],
                    "Portfolio_Value_USD": portfolio[t],
                    "Settled_Cash_USD": settled_cash[t],
                    "Margin_Debt_USD": margin_debt[t],
                    "Pending_Sale_Receivable_USD": pending_sale[t],
                    "PreTrade_Margin_Ratio_pct": (
                        pre_mr[t] * 100
                        if not np.isnan(
                            pre_mr[t]
                        )
                        else np.nan
                    ),
                    "PostTrade_Margin_Ratio_pct": (
                        post_mr[t] * 100
                        if not np.isnan(
                            post_mr[t]
                        )
                        else np.nan
                    ),
                    "Effective_Leverage_x": leverage[t],
                })

    trades = pd.DataFrame(
        trade_rows
    )

    if not trades.empty:

        trades.sort_values(
            [
                "Global_Second",
                "Action",
                "Ticker",
            ],
            inplace=True,
            ignore_index=True,
        )

    # ========================================================
    # SECOND-BY-SECOND STATE
    # ========================================================
    state = market_df[
        [
            "Global_Second",
            "Phase",
            "Phase_Name",
            "Phase_Second",
            "Market_State",
        ]
    ].copy()

    state["Timer"] = (
        state["Phase_Second"]
        .map(timer_display)
    )

    state["Equity_USD"] = equity

    state[
        "PreTrade_Portfolio_Value_USD"
    ] = pre_value

    state[
        "Portfolio_Value_USD"
    ] = portfolio

    state[
        "Sellable_Portfolio_USD"
    ] = sellable_portfolio

    state[
        "Eligible_Equity_USD"
    ] = eligible

    state[
        "Settled_Cash_USD"
    ] = settled_cash

    state[
        "Margin_Debt_USD"
    ] = margin_debt

    state[
        "Pending_Sale_Receivable_USD"
    ] = pending_sale

    state[
        "PreTrade_Margin_Ratio_pct"
    ] = (
        pre_mr * 100
    )

    state[
        "PostTrade_Margin_Ratio_pct"
    ] = (
        post_mr * 100
    )

    state[
        "Effective_Leverage_x"
    ] = leverage

    state[
        "BUY_Value_USD"
    ] = (
        Bq * price
    ).sum(
        axis=1
    )

    state[
        "SELL_Value_USD"
    ] = (
        Sq * price
    ).sum(
        axis=1
    )

    # ========================================================
    # LONG-FORM POSITION AUDIT
    # ========================================================
    position_rows = []

    for t in range(T):

        gsec = int(
            market_df.iloc[t][
                "Global_Second"
            ]
        )

        for i, ticker in enumerate(
            tickers
        ):

            pv = position_value[t, i]

            if pv <= POSITION_VALUE_TOL:
                continue

            position_rows.append({
                "Global_Second": gsec,
                "Ticker": ticker,
                "Price_USD": price[t, i],
                "Quantity": Hq[t, i],
                "Position_Value_USD": pv,
                "Sellable_Quantity": Rq[t, i],
                "Sellable_Value_USD": sellable_value[t, i],
            })

    positions = pd.DataFrame(
        position_rows
    )

    # ========================================================
    # SOLVER SUMMARY
    # ========================================================
    status = str(
        model.getStatus()
    )

    try:

        gap = model.getGap()

    except Exception:

        gap = np.nan

    try:

        dual_bound = (
            model.getDualbound()
        )

    except Exception:

        dual_bound = np.nan

    valid_pre = pre_mr[
        ~np.isnan(
            pre_mr
        )
    ]

    valid_leverage = leverage[
        ~np.isnan(
            leverage
        )
    ]

    warm_equity = (
        incumbent[
            "final_equity"
        ]
        if incumbent is not None
        else np.nan
    )

    summary = pd.DataFrame(
        [
            (
                "Scenario",
                str(
                    market_df.iloc[0][
                        "Scenario"
                    ]
                ),
            ),
            (
                "Solver",
                "SCIP via PySCIPOpt",
            ),
            (
                "Solver_Status",
                status,
            ),
            (
                "Proven_Global_Optimum",
                status == "optimal",
            ),
            (
                "Relative_MIP_Gap",
                gap,
            ),
            (
                "Best_Dual_Bound_USD",
                dual_bound,
            ),
            (
                "Initial_Capital_USD",
                INITIAL_CAPITAL,
            ),
            (
                "Verified_Warm_Incumbent_USD",
                warm_equity,
            ),
            (
                "Final_Equity_USD",
                float(
                    equity[-1]
                ),
            ),
            (
                "Final_Wealth_Multiple",
                float(
                    equity[-1]
                )
                /
                INITIAL_CAPITAL,
            ),
            (
                "Final_Return_pct",
                (
                    float(
                        equity[-1]
                    )
                    /
                    INITIAL_CAPITAL
                    -
                    1.0
                )
                *
                100,
            ),
            (
                "Minimum_PreTrade_Margin_Ratio_pct",
                (
                    float(
                        valid_pre.min()
                        *
                        100
                    )
                    if len(
                        valid_pre
                    )
                    else np.nan
                ),
            ),
            (
                "Maximum_Effective_Leverage_x",
                (
                    float(
                        valid_leverage.max()
                    )
                    if len(
                        valid_leverage
                    )
                    else np.nan
                ),
            ),
            (
                "Settlement_Delay_seconds",
                SETTLEMENT_DELAY,
            ),
            (
                "Leverage_Tier_x",
                LEVERAGE_TIER,
            ),
            (
                "Initial_Margin_pct",
                INITIAL_MARGIN * 100,
            ),
            (
                "Maintenance_Trigger_pct",
                MAINTENANCE_MARGIN * 100,
            ),
            (
                "Optimization_Survival_Floor_pct",
                SURVIVAL_MARGIN * 100,
            ),
            (
                "Integer_Shares",
                INTEGER_SHARES,
            ),
            (
                "Unlimited_Liquidity",
                True,
            ),
            (
                "Price_Divisor",
                PRICE_DIVISOR,
            ),
            (
                "BUY_Variables_Kept",
                stats[
                    "buy_kept"
                ],
            ),
            (
                "BUY_Variables_Pruned",
                stats[
                    "buy_pruned"
                ],
            ),
            (
                "BUY_Prune_pct",
                stats[
                    "buy_prune_pct"
                ],
            ),
            (
                "BUY_Pruned_No_Future_Upside",
                stats[
                    "basic_pruned"
                ],
            ),
            (
                "BUY_Pruned_Cross_Asset_Dominance",
                stats[
                    "dominance_pruned"
                ],
            ),
            (
                "SELL_Variables_Kept",
                stats[
                    "sell_kept"
                ],
            ),
            (
                "Binary_BUY_Times",
                stats[
                    "binary_times"
                ],
            ),
            (
                "Transaction_Log_Rows",
                len(trades),
            ),
        ],
        columns=[
            "Metric",
            "Value",
        ],
    )

    return (
        summary,
        trades,
        state,
        positions,
    )


# ============================================================
# OUTPUT
# ============================================================
def write_outputs(
    market_df,
    summary,
    trades,
    state,
    positions,
    incumbent,
):
    trades.to_csv(
        "best_portfolio_transactions.csv",
        index=False,
    )

    state.to_csv(
        "best_portfolio_state.csv",
        index=False,
    )

    positions.to_csv(
        "best_portfolio_positions.csv",
        index=False,
    )

    if incumbent is not None:

        incumbent[
            "route"
        ].to_csv(
            "verified_warm_incumbent_route.csv",
            index=False,
        )

    # ========================================================
    # EXCEL
    #
    # Tab 1 = Market Scenario
    # Tab 2 = Results
    # ========================================================
    with pd.ExcelWriter(
        "best_portfolio_optimizer_output.xlsx",
        engine="openpyxl",
    ) as writer:

        market_df.to_excel(
            writer,
            sheet_name="Market Scenario",
            index=False,
        )

        summary.to_excel(
            writer,
            sheet_name="Results",
            index=False,
            startrow=0,
        )

        row = (
            len(summary)
            +
            3
        )

        if incumbent is not None:

            pd.DataFrame({
                "Section": [
                    "VERIFIED WARM INCUMBENT ROUTE"
                ]
            }).to_excel(
                writer,
                sheet_name="Results",
                index=False,
                startrow=row,
            )

            row += 2

            incumbent[
                "route"
            ].to_excel(
                writer,
                sheet_name="Results",
                index=False,
                startrow=row,
            )

            row += (
                len(
                    incumbent[
                        "route"
                    ]
                )
                +
                3
            )

        pd.DataFrame({
            "Section": [
                "OPTIMAL / BEST-FOUND TRANSACTIONS"
            ]
        }).to_excel(
            writer,
            sheet_name="Results",
            index=False,
            startrow=row,
        )

        row += 2

        trades.to_excel(
            writer,
            sheet_name="Results",
            index=False,
            startrow=row,
        )

    print(
        "\nCreated:"
    )

    print(
        "  best_portfolio_optimizer_output.xlsx"
    )

    print(
        "  best_portfolio_transactions.csv"
    )

    print(
        "  best_portfolio_state.csv"
    )

    print(
        "  best_portfolio_positions.csv"
    )

    if incumbent is not None:

        print(
            "  verified_warm_incumbent_route.csv"
        )


# ============================================================
# MAIN
# ============================================================
def main():
    path = locate_input_file()

    (
        market_df,
        tickers,
        price,
    ) = load_market(
        path
    )

    T, A = price.shape

    print(
        "=" * 72
    )

    print(
        "FREE FALL 2.0 — PERFECT-FORESIGHT PORTFOLIO OPTIMIZER"
    )

    print(
        "=" * 72
    )

    print(
        f"Input:                {path}"
    )

    print(
        f"Ticks:                {T:,}"
    )

    print(
        f"Tickers:              {A:,}"
    )

    print(
        f"Initial capital:      ${INITIAL_CAPITAL:,.2f}"
    )

    print(
        f"Price divisor:        {PRICE_DIVISOR:g}"
    )

    print(
        f"T+0.5 delay:          {SETTLEMENT_DELAY} sec"
    )

    print(
        f"Initial leverage:     {LEVERAGE_TIER:.1f}x"
    )

    print(
        f"Initial margin:       {INITIAL_MARGIN:.3%}"
    )

    print(
        f"Maintenance trigger: <= {MAINTENANCE_MARGIN:.3%}"
    )

    print(
        f"Survival constraint: >= {SURVIVAL_MARGIN:.3%}"
    )

    print(
        f"Integer shares:       {INTEGER_SHARES}"
    )

    # ========================================================
    # PREPROCESS
    # ========================================================
    print(
        "\nPreprocessing..."
    )

    (
        buy_mask,
        basic_pruned,
        dominance_pruned,
    ) = compute_buy_mask(
        price
    )

    earliest_sell = earliest_sell_times(
        buy_mask
    )

    eq_ub = equity_upper_bound(
        price
    )

    total_slots = (
        T
        *
        A
    )

    buy_kept = int(
        buy_mask.sum()
    )

    buy_pruned = (
        total_slots
        -
        buy_kept
    )

    sell_kept = sum(
        max(
            0,
            T - x,
        )
        for x in earliest_sell
        if x < T
    )

    binary_times = int(
        np.any(
            buy_mask,
            axis=1,
        ).sum()
    )

    stats = {
        "buy_kept": buy_kept,
        "buy_pruned": buy_pruned,
        "buy_prune_pct": (
            100.0
            *
            buy_pruned
            /
            total_slots
        ),
        "basic_pruned": basic_pruned,
        "dominance_pruned": dominance_pruned,
        "sell_kept": int(
            sell_kept
        ),
        "binary_times": binary_times,
    }

    print(
        f"BUY pruned total:     "
        f"{buy_pruned:,}/{total_slots:,} "
        f"({stats['buy_prune_pct']:.2f}%)"
    )

    print(
        f"  no future upside:   {basic_pruned:,}"
    )

    print(
        f"  cross-asset dom.:   {dominance_pruned:,}"
    )

    print(
        f"BUY vars kept:        {buy_kept:,}"
    )

    print(
        f"SELL vars kept:       {sell_kept:,}"
    )

    print(
        f"BUY-time binaries:    {binary_times:,}/{T:,}"
    )

    # ========================================================
    # WARM START
    # ========================================================
    incumbent = build_verified_warm_start(
        price,
        tickers,
    )

    if incumbent is not None:

        print(
            f"\nVerified warm incumbent: "
            f"${incumbent['final_equity']:,.2f} "
            f"= "
            f"{incumbent['final_equity']/INITIAL_CAPITAL:.4f}x"
        )

    else:

        print(
            "\nNo verified warm incumbent available."
        )

    # ========================================================
    # BUILD MODEL
    # ========================================================
    print(
        "\nBuilding MILP..."
    )

    (
        model,
        B,
        S,
        H,
        R,
        E,
        F,
        Z,
    ) = build_model(
        price,
        tickers,
        buy_mask,
        earliest_sell,
        eq_ub,
        incumbent,
    )

    print(
        f"Variables:            {model.getNVars():,}"
    )

    print(
        f"Constraints:          {model.getNConss():,}"
    )

    # ========================================================
    # MIP START
    # ========================================================
    add_mip_start(
        model,
        B,
        S,
        H,
        R,
        E,
        F,
        Z,
        incumbent,
    )

    # ========================================================
    # SOLVE
    # ========================================================
    print(
        "\nSolving with SCIP..."
    )

    model.optimize()

    status = str(
        model.getStatus()
    )

    print(
        f"\nSCIP status: {status}"
    )

    if model.getNSols() == 0:

        raise RuntimeError(
            "SCIP found no feasible solution."
        )

    if status == "optimal":

        print(
            "PROVEN GLOBAL OPTIMUM FOUND."
        )

    else:

        print(
            "Best-known feasible solution found; "
            "proof not complete."
        )

    try:

        print(
            f"Relative gap: "
            f"{model.getGap():.8%}"
        )

    except Exception:

        pass

    try:

        print(
            f"Dual bound:   "
            f"{model.getDualbound():,.6f}"
        )

    except Exception:

        pass

    # ========================================================
    # EXTRACT
    # ========================================================
    (
        summary,
        trades,
        state,
        positions,
    ) = extract_results(
        model,
        B,
        S,
        H,
        R,
        E,
        F,
        market_df,
        tickers,
        price,
        stats,
        incumbent,
    )

    print(
        "\nSUMMARY"
    )

    print(
        summary.to_string(
            index=False
        )
    )

    if not trades.empty:

        print(
            "\nFIRST 30 TRANSACTIONS"
        )

        cols = [
            "Global_Second",
            "Timer",
            "Action",
            "Ticker",
            "Price_USD",
            "Quantity",
            "Trade_Value_USD",
            "Settlement_Global_Second",
            "Equity_USD",
            "PreTrade_Margin_Ratio_pct",
            "PostTrade_Margin_Ratio_pct",
            "Effective_Leverage_x",
        ]

        print(
            trades[
                cols
            ]
            .head(30)
            .to_string(
                index=False
            )
        )

    # ========================================================
    # WRITE OUTPUTS
    # ========================================================
    write_outputs(
        market_df,
        summary,
        trades,
        state,
        positions,
        incumbent,
    )

    print(
        "\nInterpretation:"
    )

    print(
        "  Proven_Global_Optimum=True "
        "and Relative_MIP_Gap=0"
    )

    print(
        "  => no legal portfolio can finish "
        "with more equity under these rules."
    )


if __name__ == "__main__":
    main()
