"""
Free Fall 2.0 - Week 6 Comprehensive Integration & Boundary Test Suite
Author: Nguyen Quang Minh (Technical Developer)
Student ID: 2412380031
Subject: Technology Applications in Banking and Finance (NHA408E) - FTU 2026

Validates:
- T01: Normal Cash Trading
- T02: Normal Leveraged Trading
- T03: Boundary Maintenance Margin (Exactly 20.00% - No Liquidation)
- T04: Boundary Breach (< 20.00% - Forced Liquidation Trigger)
- T05: Invalid Case (Over-leveraging beyond buying power)
- T06: Invalid Case (Short selling unowned shares)
- T07: Invalid Case (Negative order quantities)
- T08: Financial Consistency with Week 4 Specification
"""

import unittest
from src.simulation_engine import MarginEngine, HouseType, MarginStatus


class TestWeek6Integration(unittest.TestCase):

    def setUp(self):
        self.engine = MarginEngine(
            initial_capital=10000.0,
            target_house_type=HouseType.NORMAL_HOUSE,
            initial_margin_ratio=0.25,
            maintenance_margin_ratio=0.20,
            liquidation_penalty_pct=0.05,
        )

    def test_t01_normal_cash_trading(self):
        """T01: Normal Cash Trading - Full equity cushion, 100% margin ratio."""
        ok = self.engine.execute_order("VINTRUMITE", "BUY", 10.0, 500.0, use_margin=False)
        self.assertTrue(ok)
        metrics = self.engine.evaluate({"VINTRUMITE": 500.0})
        self.assertEqual(metrics.cash, 5000.0)
        self.assertEqual(metrics.margin_debt, 0.0)
        self.assertEqual(metrics.equity, 10000.0)
        self.assertEqual(metrics.margin_ratio, 2.0)  # Equity ($10k) / Stock ($5k) = 2.0 (200%)
        self.assertEqual(metrics.margin_status, MarginStatus.HEALTHY)

    def test_t02_normal_leveraged_trading(self):
        """T02: Normal Leveraged Trading - 4x Tier deployment."""
        ok = self.engine.execute_order("VINTRUMITE", "BUY", 400.0, 100.0, use_margin=True)
        self.assertTrue(ok)
        metrics = self.engine.evaluate({"VINTRUMITE": 100.0})
        self.assertEqual(metrics.cash, 0.0)
        self.assertEqual(metrics.margin_debt, 30000.0)
        self.assertEqual(metrics.equity, 10000.0)
        self.assertAlmostEqual(metrics.leverage, 4.0, places=2)
        self.assertAlmostEqual(metrics.margin_ratio, 0.25, places=4)
        self.assertEqual(metrics.margin_status, MarginStatus.NORMAL)

    def test_t03_boundary_exactly_at_maintenance_margin(self):
        """
        T03: Boundary Case - Exactly 20.00% Margin Ratio.
        Position = $40,000, Debt = $30,000.
        Stock drops exactly -6.25% to price 93.75 -> Value = 400 * 93.75 = $37,500.
        Equity = $37,500 - $30,000 = $7,500.
        Margin Ratio = $7,500 / $37,500 = 0.2000 (20.00%).
        Expected: Margin status WARNING, Margin Call NOT yet triggered.
        """
        self.engine.execute_order("VINTRUMITE", "BUY", 400.0, 100.0, use_margin=True)
        metrics = self.engine.evaluate({"VINTRUMITE": 93.75})
        self.assertAlmostEqual(metrics.margin_ratio, 0.20, places=4)
        self.assertEqual(metrics.margin_status, MarginStatus.WARNING)
        self.assertFalse(self.engine.state.is_liquidated)

    def test_t04_boundary_breach_triggers_liquidation(self):
        """
        T04: Boundary Breach - Price drops -6.26% to price 93.74.
        Value = 400 * 93.74 = $37,496.
        Equity = $37,496 - $30,000 = $7,496.
        Margin Ratio = $7,496 / $37,496 = 0.199914 (< 20.00%).
        Expected: MARGIN_CALL status and auto liquidation.
        """
        self.engine.execute_order("VINTRUMITE", "BUY", 400.0, 100.0, use_margin=True)
        metrics = self.engine.evaluate({"VINTRUMITE": 93.74})
        self.assertLess(metrics.margin_ratio, 0.20)
        self.assertEqual(metrics.margin_status, MarginStatus.MARGIN_CALL)

        liq = self.engine.trigger_forced_liquidation({"VINTRUMITE": 93.74})
        self.assertTrue(self.engine.state.is_liquidated)
        self.assertGreater(liq["penalty"], 0.0)

    def test_t05_invalid_exceeds_buying_power(self):
        """T05: Invalid Case - Buying beyond maximum purchasing power."""
        # Max purchasing power for $10k at 25% margin = $40,000
        # Attempting to buy $50,000 worth of stock
        ok = self.engine.execute_order("VINTRUMITE", "BUY", 500.0, 100.0, use_margin=True)
        self.assertFalse(ok)
        self.assertEqual(self.engine.state.cash, 10000.0)
        self.assertEqual(self.engine.state.margin_debt, 0.0)

    def test_t06_invalid_short_selling_unowned_shares(self):
        """T06: Invalid Case - Selling unowned shares."""
        ok = self.engine.execute_order("SAMSUNG_ELEC", "SELL", 50.0, 100.0)
        self.assertFalse(ok)
        self.assertEqual(self.engine.state.cash, 10000.0)

    def test_t07_invalid_negative_quantity(self):
        """T07: Invalid Case - Negative shares parameter raises ValueError."""
        with self.assertRaises(ValueError):
            self.engine.execute_order("VINTRUMITE", "BUY", -10.0, 100.0)

    def test_t08_financial_consistency_week4_spec(self):
        """T08: Financial Consistency Check with approved Week 4 Sample Case."""
        self.engine.execute_order("VINTRUMITE", "BUY", 400.0, 100.0, use_margin=True)
        # Market Shock = -20% -> Price = 80.0
        metrics = self.engine.evaluate({"VINTRUMITE": 80.0})
        self.assertAlmostEqual(metrics.portfolio_value, 32000.0, places=2)
        self.assertAlmostEqual(metrics.equity, 2000.0, places=2)
        self.assertAlmostEqual(metrics.margin_ratio, 0.0625, places=4)
        self.assertEqual(metrics.margin_status, MarginStatus.MARGIN_CALL)

    def test_t09_bank_savings_safe_haven(self):
        """T09: Safe Haven Bank Integration - Bank savings immune to stock market crash."""
        ok = self.engine.deposit_to_savings(4000.0)
        self.assertTrue(ok)
        self.assertEqual(self.engine.state.bank_savings, 4000.0)
        self.assertEqual(self.engine.state.cash, 6000.0)
        # Buy stock with remaining cash
        self.engine.execute_order("VINTRUMITE", "BUY", 10.0, 500.0, use_margin=False)
        # Market drops 50%
        metrics = self.engine.evaluate({"VINTRUMITE": 250.0})
        self.assertEqual(metrics.bank_savings, 4000.0)
        self.assertEqual(metrics.portfolio_value, 6500.0)  # 2500 stock + 4000 savings
        self.assertEqual(metrics.equity, 7500.0)  # 1000 cash + 6500 total portfolio

    def test_t10_settlement_workflow_holding_pen(self):
        """T10: Settlement Workflow Delay - Order at Tick 50 (T+30) vs Tick 200 (Phase 2)."""
        # Order placed before tick 150 (tick 50)
        self.engine.execute_order("VINTRUMITE", "BUY", 10.0, 100.0, current_tick=50, current_phase=1)
        self.assertIn("VINTRUMITE", self.engine.state.pending_shares)
        self.assertEqual(self.engine.state.holdings.get("VINTRUMITE", 0), 0)

        # Before delivery tick (tick 79)
        self.engine.process_deliveries(current_tick=79, current_phase=1)
        self.assertEqual(self.engine.state.holdings.get("VINTRUMITE", 0), 0)

        # At delivery tick (tick 80)
        self.engine.process_deliveries(current_tick=80, current_phase=1)
        self.assertEqual(self.engine.state.holdings.get("VINTRUMITE", 0), 10.0)

        # Order placed after tick 150 (tick 200) -> Delivered upon Phase 2
        self.engine.execute_order("SAMSUNG_ELEC", "BUY", 5.0, 100.0, current_tick=200, current_phase=1)
        self.engine.process_deliveries(current_tick=250, current_phase=1)
        self.assertEqual(self.engine.state.holdings.get("SAMSUNG_ELEC", 0), 0)

        # Phase 2 entry
        self.engine.process_deliveries(current_tick=1, current_phase=2)
        self.assertEqual(self.engine.state.holdings.get("SAMSUNG_ELEC", 0), 5.0)


if __name__ == "__main__":
    unittest.main()
