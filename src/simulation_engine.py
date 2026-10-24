"""
Free Fall 2.0 - Core Financial Simulation Engine
Author: Nguyen Quang Minh (Technical Developer)
Student ID: 2412380031
Subject: Technology Applications in Banking and Finance (NHA408E)

Updated according to Phase 1 Workflow:
- Bank Savings mechanism (risk-free yield/idle cash storage)
- Settlement delay: T+0.5 holding pen (orders before tick 150 vs after tick 150 pending to Phase 2)
- Margin Call price threshold check
- Forced liquidation penalty deduction
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class MarginStatus(Enum):
    HEALTHY = "HEALTHY"            # No Margin Debt (or Margin Ratio >= 100%)
    NORMAL = "NORMAL"              # Margin Debt > 0 and Margin Ratio >= Initial Margin Ratio
    WARNING = "WARNING"            # Maintenance Margin <= Margin Ratio < Initial Margin Ratio (20% <= Margin Ratio < 25%)
    MARGIN_CALL = "MARGIN_CALL"    # Margin Ratio < Maintenance Margin (20%) or uncollateralized debt
    LIQUIDATED = "LIQUIDATED"      # Position liquidated due to margin call


class HouseType(Enum):
    SMALL_HOUSE = "Small House"        # 3.0x Initial Capital
    NORMAL_HOUSE = "Normal House"      # 20.0x Initial Capital
    TOLAM_VILLA = "ToLam Villa"        # 100.0x Initial Capital


HOUSE_MULTIPLIERS = {
    HouseType.SMALL_HOUSE: 3.0,
    HouseType.NORMAL_HOUSE: 20.0,
    HouseType.TOLAM_VILLA: 100.0,
}


@dataclass
class PendingDelivery:
    ticker: str
    shares: float
    delivery_tick: int
    deliver_in_phase: int  # e.g., Phase 2 if purchased after tick 150


@dataclass
class AccountState:
    cash: float
    bank_savings: float = 0.0
    margin_debt: float = 0.0
    holdings: Dict[str, float] = field(default_factory=dict)         # active deliverable shares
    pending_shares: Dict[str, float] = field(default_factory=dict)   # in T+0.5 holding pen or pending phase 2
    pending_queue: List[PendingDelivery] = field(default_factory=list)
    initial_margin_ratio: float = 0.25
    maintenance_margin_ratio: float = 0.20
    liquidation_penalty_pct: float = 0.05  # 5% liquidation penalty fee
    emergency_reserve: float = 0.0
    is_liquidated: bool = False
    margin_call_triggered: bool = False


@dataclass
class FinancialMetrics:
    portfolio_value: float
    bank_savings: float
    margin_debt: float
    cash: float
    equity: float
    trading_equity: float = 0.0
    leverage: float = 0.0
    margin_ratio: float = 1.0
    margin_status: MarginStatus = MarginStatus.HEALTHY
    target_progress: float = 0.0
    is_solvent: bool = True


class MarginEngine:
    """
    Financial Simulation Engine implementing workflow rules:
    - Total Portfolio Value = (Shares * Price) + Bank Savings
    - Equity / Net Worth = Cash + Total Portfolio Value - Margin Debt
    - Margin Ratio = Equity / (Shares * Price)
    """

    ALIAS_MAP = {
        "VNT": "Vintrumite", "Vintrumite": "VNT",
        "SEC": "Samsung Electronics", "Samsung Electronics": "SEC",
        "KODEX": "KODEX Semiconductor", "KODEX Semiconductor": "KODEX",
        "KODEX2X": "KODEX Leverage", "KODEX Leverage": "KODEX2X",
        "TIGER": "TIGER Semiconductor TOP10", "TIGER Semiconductor TOP10": "TIGER",
        "HYUNDAI": "Hyundai Motor", "Hyundai Motor": "HYUNDAI",
        "KIA": "Kia", "Kia": "KIA",
        "POSCO-FM": "POSCO Future M", "POSCO Future M": "POSCO-FM",
        "POSCO-HD": "POSCO Holdings", "POSCO Holdings": "POSCO-HD",
        "KZINC": "Korea Zinc", "Korea Zinc": "KZINC",
    }

    def __init__(
        self,
        initial_capital: float,
        target_house_type: HouseType = HouseType.NORMAL_HOUSE,
        initial_margin_ratio: float = 1.0,
        maintenance_margin_ratio: float = 0.20,
        liquidation_penalty_pct: float = 0.05,
    ):
        if not isinstance(initial_capital, (int, float)) or math.isnan(initial_capital) or math.isinf(initial_capital) or initial_capital <= 0:
            raise ValueError("Initial capital must be positive.")
        if not isinstance(initial_margin_ratio, (int, float)) or math.isnan(initial_margin_ratio) or math.isinf(initial_margin_ratio) or initial_margin_ratio <= 0 or initial_margin_ratio > 1.0:
            raise ValueError("Initial margin ratio must be in (0, 1.0].")
        if not isinstance(maintenance_margin_ratio, (int, float)) or math.isnan(maintenance_margin_ratio) or math.isinf(maintenance_margin_ratio) or maintenance_margin_ratio <= 0:
            raise ValueError("Maintenance margin ratio must be positive.")

        self.initial_capital = initial_capital
        self.target_house_type = target_house_type
        self.target_value = initial_capital * HOUSE_MULTIPLIERS[target_house_type]
        self.initial_margin_ratio = initial_margin_ratio
        self._base_maintenance_margin_ratio = maintenance_margin_ratio
        self.maintenance_margin_ratio = min(maintenance_margin_ratio, initial_margin_ratio * 0.80)
        self.liquidation_penalty_pct = liquidation_penalty_pct
        self.margin_multiplier = 1.0 / initial_margin_ratio

        self.state = AccountState(
            cash=initial_capital,
            bank_savings=0.0,
            margin_debt=0.0,
            holdings={},
            pending_shares={},
            pending_queue=[],
            initial_margin_ratio=initial_margin_ratio,
            maintenance_margin_ratio=self.maintenance_margin_ratio,
            liquidation_penalty_pct=liquidation_penalty_pct,
        )

    def deposit_to_savings(self, amount: float) -> bool:
        """Transfer free trading cash into bank savings."""
        if not isinstance(amount, (int, float)) or math.isnan(amount) or math.isinf(amount) or amount <= 0 or amount > self.state.cash:
            return False
        # HIGH-06: Prevent transferring collateral cash when margin positions are under margin call or uncollateralized
        if self.state.margin_debt > 0:
            if self.state.margin_call_triggered:
                return False
            remaining_cash = self.state.cash - amount
            if remaining_cash < 0:
                return False
            if not self.state.holdings and not self.state.pending_shares and remaining_cash < self.state.margin_debt:
                return False
        self.state.cash -= amount
        self.state.bank_savings += amount
        return True

    def withdraw_from_savings(self, amount: float, ignore_reserve: bool = False) -> bool:
        """Withdraw funds from bank savings to liquid trading cash."""
        if not isinstance(amount, (int, float)) or math.isnan(amount) or math.isinf(amount) or amount <= 0:
            return False
        available = self.state.bank_savings if ignore_reserve else (self.state.bank_savings - self.state.emergency_reserve)
        if amount > available:
            return False
        self.state.bank_savings -= amount
        self.state.cash += amount
        # HIGH-07: Maintain invariant emergency_reserve <= bank_savings
        if self.state.emergency_reserve > self.state.bank_savings:
            self.state.emergency_reserve = self.state.bank_savings
        return True

    def repay_margin_debt(self, amount: float, from_source: str = "bank") -> bool:
        """Directly repay margin debt using bank funds or liquid cash."""
        if not isinstance(amount, (int, float)) or math.isnan(amount) or math.isinf(amount) or amount <= 0 or self.state.margin_debt <= 0:
            return False
        # MOD-14: Strictly validate from_source
        if from_source not in ("bank", "cash"):
            return False
        repay_amt = min(amount, self.state.margin_debt)
        if from_source == "bank":
            available = self.state.bank_savings - self.state.emergency_reserve
            if repay_amt > available:
                return False
            self.state.bank_savings -= repay_amt
            self.state.margin_debt -= repay_amt
            return True
        else:
            if repay_amt > self.state.cash:
                return False
            self.state.cash -= repay_amt
            self.state.margin_debt -= repay_amt
            return True

    def set_emergency_reserve(self, amount: float) -> bool:
        """Lock or adjust the emergency reserve portion within bank savings."""
        if not isinstance(amount, (int, float)) or math.isnan(amount) or math.isinf(amount) or amount < 0 or amount > self.state.bank_savings:
            return False
        self.state.emergency_reserve = amount
        return True

    def calculate_max_purchasing_power(self) -> float:
        """Total purchasing power based on liquid cash + equity cushion."""
        if (
            self.state.cash <= 0
            or self.state.is_liquidated
            or self.state.margin_call_triggered
            or math.isnan(self.state.cash)
            or math.isinf(self.state.cash)
        ):
            return 0.0
        if math.isnan(self.state.initial_margin_ratio) or math.isinf(self.state.initial_margin_ratio) or self.state.initial_margin_ratio <= 0:
            return 0.0
        gross_power = self.state.cash / self.state.initial_margin_ratio
        if self.state.margin_debt > 0:
            return max(0.0, gross_power - self.state.margin_debt)
        return gross_power

    def set_margin_multiplier(self, multiplier: float) -> float:
        """Sets margin multiplier (1.0x to 4.0x max) and adjusts initial & maintenance margin ratios."""
        if not isinstance(multiplier, (int, float)) or math.isnan(multiplier) or math.isinf(multiplier):
            raise ValueError("Multiplier must be a valid finite number.")
        multiplier = max(1.0, min(4.0, float(multiplier)))
        self.margin_multiplier = multiplier
        self.initial_margin_ratio = 1.0 / multiplier
        # MOD-07: Respect configured base maintenance margin ratio instead of hardcoding 0.20
        self.maintenance_margin_ratio = min(self._base_maintenance_margin_ratio, self.initial_margin_ratio * 0.80)
        self.state.initial_margin_ratio = self.initial_margin_ratio
        self.state.maintenance_margin_ratio = self.maintenance_margin_ratio
        return multiplier

    def calculate_stock_portfolio_value(self, current_prices: Dict[str, float]) -> float:
        """Value of all stock shares (both delivered and in pending delivery)."""
        total = 0.0
        alias_map = self.ALIAS_MAP
        # Active holdings
        for ticker, shares in self.state.holdings.items():
            price = current_prices.get(ticker, 0.0)
            if price <= 0.0 and ticker in alias_map:
                price = current_prices.get(alias_map[ticker], 0.0)
            total += shares * price
        # Pending delivery shares (if any remain)
        for ticker, shares in self.state.pending_shares.items():
            price = current_prices.get(ticker, 0.0)
            if price <= 0.0 and ticker in alias_map:
                price = current_prices.get(alias_map[ticker], 0.0)
            total += shares * price
        return total

    def calculate_total_portfolio_value(self, current_prices: Dict[str, float]) -> float:
        """Total Portfolio Value = (Shares * Current_Stock_Price) + Bank Savings."""
        stock_val = self.calculate_stock_portfolio_value(current_prices)
        return stock_val + self.state.bank_savings

    def evaluate(self, current_prices: Dict[str, float]) -> FinancialMetrics:
        if self.state.is_liquidated:
            equity = self.state.cash + self.state.bank_savings - self.state.margin_debt
            return FinancialMetrics(
                portfolio_value=self.state.bank_savings,
                bank_savings=self.state.bank_savings,
                margin_debt=self.state.margin_debt,
                cash=self.state.cash,
                equity=equity,
                leverage=0.0,
                margin_ratio=0.0,
                margin_status=MarginStatus.LIQUIDATED,
                # MOD-08: Guard against ZeroDivisionError if target_value <= 0
                target_progress=max(0.0, (equity / self.target_value * 100.0) if self.target_value > 0 else 0.0),
                is_solvent=equity > 0,
            )

        stock_portfolio_value = self.calculate_stock_portfolio_value(current_prices)
        total_portfolio_value = stock_portfolio_value + self.state.bank_savings
        cash = self.state.cash
        margin_debt = self.state.margin_debt

        # Total Net Worth / Global Equity = Cash + Total Portfolio Value (including bank savings) - Margin Debt
        equity = cash + total_portfolio_value - margin_debt

        # Trading Equity = Cash + Stock Portfolio Value - Margin Debt
        # Bank savings are 100% immune from broker custody & liquidation, so they do NOT act as margin collateral!
        trading_equity = cash + stock_portfolio_value - margin_debt

        # Margin Ratio = Trading Equity / (Shares * Current Price)
        if stock_portfolio_value > 0:
            leverage = stock_portfolio_value / trading_equity if trading_equity > 0 else float("inf")
            margin_ratio = max(0.0, trading_equity / stock_portfolio_value)
        else:
            leverage = 0.0 if margin_debt == 0 else float("inf")
            margin_ratio = 1.0 if margin_debt == 0 else 0.0

        # CRIT-01 & HIGH-04: Uncollateralized debt triggers MARGIN_CALL, not HEALTHY
        if margin_debt == 0:
            status = MarginStatus.HEALTHY
        elif stock_portfolio_value == 0 and margin_debt > 0:
            status = MarginStatus.MARGIN_CALL
        elif margin_ratio < self.maintenance_margin_ratio:
            status = MarginStatus.MARGIN_CALL
        elif margin_ratio < self.initial_margin_ratio:
            status = MarginStatus.WARNING
        elif margin_ratio >= 1.0:
            status = MarginStatus.HEALTHY
        else:
            status = MarginStatus.NORMAL

        # HIGH-03: Reset margin_call_triggered when account returns to healthy/normal status
        if status == MarginStatus.MARGIN_CALL:
            self.state.margin_call_triggered = True
        elif status in (MarginStatus.HEALTHY, MarginStatus.NORMAL):
            self.state.margin_call_triggered = False

        target_progress = (equity / self.target_value * 100.0) if self.target_value > 0 else 0.0

        return FinancialMetrics(
            portfolio_value=total_portfolio_value,
            bank_savings=self.state.bank_savings,
            margin_debt=margin_debt,
            cash=cash,
            equity=equity,
            trading_equity=trading_equity,
            leverage=leverage,
            margin_ratio=margin_ratio,
            margin_status=status,
            target_progress=target_progress,
            is_solvent=equity > 0,
        )

    def execute_order(
        self,
        ticker: str,
        action: str,
        shares: float,
        price: float,
        use_margin: bool = False,
        current_tick: Optional[int] = None,
        current_phase: int = 1,
        margin_multiplier: float = None,
    ) -> bool:
        if margin_multiplier is not None and margin_multiplier > 0:
            self.set_margin_multiplier(margin_multiplier)

        if self.state.is_liquidated:
            raise RuntimeError("Account is liquidated. Trading is disabled.")

        ticker = str(ticker).strip()
        action = action.upper()

        # HIGH-05: Block new leveraged buys if account is under margin call
        if action == "BUY" and use_margin and self.state.margin_call_triggered:
            raise RuntimeError("Account is under margin call. New margin purchases are restricted.")

        if (
            not isinstance(shares, (int, float))
            or not isinstance(price, (int, float))
            or math.isnan(shares)
            or math.isinf(shares)
            or math.isnan(price)
            or math.isinf(price)
        ):
            raise ValueError("Shares and price must be finite numbers")
        if shares <= 0 or price <= 0:
            raise ValueError("Shares and price must be valid positive numbers.")

        order_cost = shares * price
        EPSILON = 1e-9

        if action == "BUY":
            # HIGH-01: Remove $0.10 tolerance buffer to prevent free money creation
            if not use_margin:
                if order_cost > self.state.cash + EPSILON:
                    return False
                self.state.cash = max(0.0, self.state.cash - order_cost)
            else:
                mult = self.margin_multiplier if (self.margin_multiplier and self.margin_multiplier > 1.0) else (1.0 / self.initial_margin_ratio)
                required_cash = order_cost / mult
                if self.state.cash + EPSILON < required_cash:
                    return False

                actual_cash_used = min(self.state.cash, required_cash)
                new_debt = max(0.0, order_cost - actual_cash_used)
                self.state.cash = max(0.0, self.state.cash - actual_cash_used)
                self.state.margin_debt += new_debt

            if current_tick is not None:
                # Phase-relative tick (1-300 or 0-299)
                phase_tick = ((current_tick - 1) % 300) + 1 if current_tick > 300 else current_tick
                if phase_tick < 150:
                    delivery_tick = phase_tick + 30
                    deliver_in_phase = current_phase
                elif (current_phase or 1) >= 6:
                    # CRIT-04: Final phase orders after tick 150 deliver within Phase 6 (30 ticks later, capped at 300)
                    delivery_tick = min(phase_tick + 30, 300)
                    deliver_in_phase = 6
                else:
                    delivery_tick = 1
                    deliver_in_phase = (current_phase or 1) + 1
                self.state.pending_shares[ticker] = self.state.pending_shares.get(ticker, 0.0) + shares
                self.state.pending_queue.append(
                    PendingDelivery(
                        ticker=ticker,
                        shares=shares,
                        delivery_tick=delivery_tick,
                        deliver_in_phase=deliver_in_phase,
                    )
                )
            else:
                self.state.holdings[ticker] = self.state.holdings.get(ticker, 0.0) + shares
            return True

        elif action == "SELL":
            # MOD-06: Match ticker case-insensitively or via alias if exact key not present
            matched_key = ticker
            if matched_key not in self.state.holdings:
                for k in self.state.holdings:
                    if k.lower() == ticker.lower() or self.ALIAS_MAP.get(ticker) == k:
                        matched_key = k
                        break

            current_shares = self.state.holdings.get(matched_key, 0.0)
            # MOD-05: Allow 1e-9 float precision tolerance on SELL and clamp to exact owned shares
            if shares > current_shares + EPSILON:
                return False
            shares = min(shares, current_shares)
            order_cost = shares * price

            proceeds = order_cost
            if self.state.margin_debt > 0:
                repayment = min(self.state.margin_debt, proceeds)
                self.state.margin_debt -= repayment
                proceeds -= repayment

            self.state.cash += proceeds
            self.state.holdings[matched_key] -= shares
            # MOD-04: Clean up floating-point ghost shares <= EPSILON
            if self.state.holdings[matched_key] <= EPSILON:
                del self.state.holdings[matched_key]
            return True
        else:
            raise ValueError(f"Unknown action: {action}.")

    def process_deliveries(self, current_tick: int, current_phase: int):
        """Processes pending stock deliveries into active holdings when delivery conditions met."""
        EPSILON = 1e-9
        phase_tick = ((current_tick - 1) % 300) + 1 if current_tick > 300 else current_tick
        remaining_queue = []
        for item in self.state.pending_queue:
            # Deliver if advanced past target phase, or within same phase and tick reached delivery_tick
            should_deliver = (current_phase > item.deliver_in_phase) or (current_phase == item.deliver_in_phase and phase_tick >= item.delivery_tick)
            if should_deliver:
                # Deliver stocks to account
                self.state.holdings[item.ticker] = self.state.holdings.get(item.ticker, 0.0) + item.shares
                self.state.pending_shares[item.ticker] = self.state.pending_shares.get(item.ticker, 0.0) - item.shares
                # MOD-04: Clean up floating-point ghost shares <= EPSILON
                if self.state.pending_shares[item.ticker] <= EPSILON:
                    del self.state.pending_shares[item.ticker]
            else:
                remaining_queue.append(item)
        self.state.pending_queue = remaining_queue

    def trigger_forced_liquidation(self, current_prices: Dict[str, float]) -> Dict[str, float]:
        """
        System forcefully sells stock shares to repay margin debt.
        Applies liquidation penalty to Cash / Equity.
        """
        # MOD-03: Idempotency guard if account is already liquidated
        if self.state.is_liquidated:
            final_equity = self.state.cash + self.state.bank_savings - self.state.margin_debt
            return {
                "gross_proceeds": 0.0,
                "penalty": 0.0,
                "net_proceeds": 0.0,
                "debt_repaid": 0.0,
                "remaining_debt": self.state.margin_debt,
                "final_cash": self.state.cash,
                "final_equity": final_equity,
            }

        gross_proceeds = 0.0
        # Liquidate both delivered holdings and pending shares
        all_shares = dict(self.state.holdings)
        for t, s in self.state.pending_shares.items():
            all_shares[t] = all_shares.get(t, 0.0) + s

        # CRIT-02: Resolve ticker aliases during forced liquidation so proceeds are never $0
        alias_map = self.ALIAS_MAP
        for ticker, shares in all_shares.items():
            price = current_prices.get(ticker, 0.0)
            if price <= 0.0 and ticker in alias_map:
                price = current_prices.get(alias_map[ticker], 0.0)
            gross_proceeds += shares * price

        self.state.holdings.clear()
        self.state.pending_shares.clear()
        self.state.pending_queue.clear()

        # Deduct liquidation penalty fee (e.g. 5%)
        penalty = gross_proceeds * self.state.liquidation_penalty_pct
        net_proceeds = max(0.0, gross_proceeds - penalty)

        # Trading cash and net stock liquidation proceeds are used to pay down margin debt
        # IMPORTANT: Bank savings are 100% immune from broker forced liquidation!
        total_available = self.state.cash + net_proceeds
        if total_available >= self.state.margin_debt:
            debt_repaid = self.state.margin_debt
            remaining_funds = total_available - self.state.margin_debt
            self.state.margin_debt = 0.0
            self.state.cash = remaining_funds
        else:
            debt_repaid = total_available
            self.state.margin_debt -= total_available
            self.state.cash = 0.0

        self.state.is_liquidated = True
        final_equity = self.state.cash + self.state.bank_savings - self.state.margin_debt

        return {
            "gross_proceeds": gross_proceeds,
            "penalty": penalty,
            "net_proceeds": net_proceeds,
            "debt_repaid": debt_repaid,
            "remaining_debt": self.state.margin_debt,
            "final_cash": self.state.cash,
            "final_equity": final_equity,
        }

    def get_margin_call_price(self, ticker: str, current_prices: Optional[Dict[str, float]] = None) -> Optional[float]:
        """
        Calculates the margin call trigger price for a given stock holding.
        Accounts for available liquid cash buffering the margin debt, ticker aliases (MOD-02),
        and optional multi-asset collateral contributions when current_prices is provided (MOD-01).
        """
        alias = self.ALIAS_MAP.get(ticker)
        total_shares = self.state.holdings.get(ticker, 0.0) + self.state.pending_shares.get(ticker, 0.0)
        if alias:
            total_shares += self.state.holdings.get(alias, 0.0) + self.state.pending_shares.get(alias, 0.0)

        if total_shares <= 0 or self.state.margin_debt <= 0:
            return None

        # C-4 Fix: Cash buffers the margin debt before forced liquidation occurs
        net_debt = max(0.0, self.state.margin_debt - self.state.cash)

        # MOD-01: Account for collateral value contributed by other stocks if current_prices is provided
        if current_prices:
            other_stock_value = 0.0
            target_keys = {ticker, alias} if alias else {ticker}
            all_pos = dict(self.state.holdings)
            for t, s in self.state.pending_shares.items():
                all_pos[t] = all_pos.get(t, 0.0) + s
            for t, s in all_pos.items():
                if t not in target_keys and s > 0:
                    p = current_prices.get(t, 0.0)
                    if p <= 0.0 and t in self.ALIAS_MAP:
                        p = current_prices.get(self.ALIAS_MAP[t], 0.0)
                    other_stock_value += s * p
            net_debt = max(0.0, net_debt - other_stock_value * (1.0 - self.maintenance_margin_ratio))

        if net_debt <= 0:
            return None
        denom = total_shares * (1.0 - self.maintenance_margin_ratio)
        if denom <= 0:
            return None
        return net_debt / denom


# Alias for backward compatibility with fix instructions
SimulationEngine = MarginEngine

