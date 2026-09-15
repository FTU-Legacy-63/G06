"""
Free Fall 2.0 - Automated Financial Logic Unit Tests
Author: Nguyen Quang Minh (Technical Developer)
Student ID: 2412380031
Subject: Technology Applications in Banking and Finance (NHA408E)

Updated according to Phase 1 Workflow:
- Validates Case 1 (High Leverage Wipeout with Liquidation Penalty)
- Validates Case 2 (Cash-only Solvency)
- Validates Bank Savings integration
- Validates T+0.5 Settlement Delay (Deliveries before vs after tick 150)
"""

import unittest
from src.simulation_engine import MarginEngine, HouseType, MarginStatus


class TestMarginEngine(unittest.TestCase):

    def test_case_1_high_leverage_wipeout_with_penalty(self):
        """
        Validates Case 1 from Week 4 Document + Phase 1 Workflow:
        - Initial Capital: 10,000,000 KRW
        - Margin Tier: 4x (Initial Margin Ratio: 25%)
        - Max Position: 40,000,000 KRW (Debt: 30,000,000 KRW)
        - Market Shock: -20%
        - Remaining Stock Value: 32,000,000 KRW
        - Equity: 2,000,000 KRW -> Margin Ratio: 6.25% (< 20% maintenance margin)
        - System forcefully sells stock shares to repay Margin Debt.
        - Applies liquidation penalty (5% of 32m = 1.6m) -> Net Proceeds = 30.4m -> Final Equity = 400,000 KRW
        """
        engine = MarginEngine(
            initial_capital=10_000_000.0,
            target_house_type=HouseType.TOLAM_VILLA,
            initial_margin_ratio=0.25,
            maintenance_margin_ratio=0.20,
            liquidation_penalty_pct=0.05,
        )

        success = engine.execute_order(
            ticker="VINTRUMITE",
            action="BUY",
            shares=400.0,
            price=100_000.0,
            use_margin=True,
            current_tick=10,
            current_phase=1,
        )
        self.assertTrue(success)
        self.assertEqual(engine.state.cash, 0.0)
        self.assertAlmostEqual(engine.state.margin_debt, 30_000_000.0, places=2)

        # Market shock: Price drops -20% to 80,000 KRW
        current_prices = {"VINTRUMITE": 80_000.0}
        metrics = engine.evaluate(current_prices)

        self.assertAlmostEqual(metrics.portfolio_value, 32_000_000.0, places=2)
        self.assertAlmostEqual(metrics.equity, 2_000_000.0, places=2)
        self.assertAlmostEqual(metrics.margin_ratio, 0.0625, places=4)
        self.assertEqual(metrics.margin_status, MarginStatus.MARGIN_CALL)
        self.assertTrue(engine.state.margin_call_triggered)

        # Forced liquidation with penalty
        liq = engine.trigger_forced_liquidation(current_prices)
        self.assertAlmostEqual(liq["gross_proceeds"], 32_000_000.0, places=2)
        self.assertAlmostEqual(liq["penalty"], 1_600_000.0, places=2)
        self.assertAlmostEqual(liq["net_proceeds"], 30_400_000.0, places=2)
        self.assertAlmostEqual(liq["remaining_debt"], 0.0, places=2)
        self.assertAlmostEqual(liq["final_cash"], 400_000.0, places=2)
        self.assertTrue(engine.state.is_liquidated)

    def test_case_2_cash_only_safe_position(self):
        """
        Validates Case 2: Cash-only position immune to liquidation.
        """
        engine = MarginEngine(
            initial_capital=50_000_000.0,
            target_house_type=HouseType.SMALL_HOUSE,
            initial_margin_ratio=1.0,
            maintenance_margin_ratio=0.20,
        )

        engine.execute_order(
            ticker="SAMSUNG_ELEC",
            action="BUY",
            shares=500.0,
            price=100_000.0,
            use_margin=False,
            current_tick=20,
        )
        current_prices = {"SAMSUNG_ELEC": 90_000.0}
        metrics = engine.evaluate(current_prices)

        self.assertAlmostEqual(metrics.equity, 45_000_000.0, places=2)
        self.assertEqual(metrics.margin_debt, 0.0)
        self.assertEqual(metrics.margin_status, MarginStatus.HEALTHY)
        self.assertTrue(metrics.is_solvent)

    def test_bank_savings_workflow(self):
        """
        Validates Phase 1 Workflow: Bank Savings deposit and withdrawal.
        Total Portfolio Value = (Shares * Price) + Bank Savings.
        """
        engine = MarginEngine(initial_capital=20_000_000.0)
        # Put 10m into Bank Savings
        ok = engine.deposit_to_savings(10_000_000.0)
        self.assertTrue(ok)
        self.assertEqual(engine.state.cash, 10_000_000.0)
        self.assertEqual(engine.state.bank_savings, 10_000_000.0)

        # Evaluate without stocks
        metrics = engine.evaluate({})
        self.assertEqual(metrics.bank_savings, 10_000_000.0)
        self.assertEqual(metrics.equity, 20_000_000.0)

    def test_settlement_delay_holding_pen(self):
        """
        Validates Phase 1 Workflow:
        - Order before tick 150: delivered via T+0.5 delay (tick + 30).
        - Order after tick 150: logged as pending for Phase 2 delivery.
        """
        engine = MarginEngine(initial_capital=20_000_000.0)
        # Order at tick 50 (< 150)
        engine.execute_order("VINTRUMITE", "BUY", 10.0, 100_000.0, current_tick=50, current_phase=1)
        self.assertIn("VINTRUMITE", engine.state.pending_shares)
        self.assertEqual(engine.state.holdings.get("VINTRUMITE", 0), 0)

        # Before delivery tick (tick 70)
        engine.process_deliveries(current_tick=70, current_phase=1)
        self.assertEqual(engine.state.holdings.get("VINTRUMITE", 0), 0)

        # At delivery tick (tick 80)
        engine.process_deliveries(current_tick=80, current_phase=1)
        self.assertEqual(engine.state.holdings.get("VINTRUMITE", 0), 10.0)

        # Order at tick 200 (> 150) -> Delivered in Phase 2
        engine.execute_order("SAMSUNG_ELEC", "BUY", 20.0, 50_000.0, current_tick=200, current_phase=1)
        engine.process_deliveries(current_tick=299, current_phase=1)
        self.assertEqual(engine.state.holdings.get("SAMSUNG_ELEC", 0), 0)

        # Advance to Phase 2
        engine.process_deliveries(current_tick=1, current_phase=2)
        self.assertEqual(engine.state.holdings.get("SAMSUNG_ELEC", 0), 20.0)


if __name__ == "__main__":
    unittest.main()
