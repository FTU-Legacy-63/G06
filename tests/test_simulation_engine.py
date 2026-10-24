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
from src.game_controller import GameController


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

    def test_bank_savings_isolated_from_margin_collateral(self):
        """
        Validates Bug #1 fix: Bank savings are outside broker custody.
        They do NOT inflate the margin ratio or prevent liquidation.
        """
        engine = MarginEngine(
            initial_capital=20_000_000.0,
            initial_margin_ratio=0.25,
            maintenance_margin_ratio=0.20,
        )
        # Put 10,000,000 into Safe Haven Bank
        engine.deposit_to_savings(10_000_000.0)
        self.assertEqual(engine.state.cash, 10_000_000.0)
        self.assertEqual(engine.state.bank_savings, 10_000_000.0)

        # Buy 40,000,000 of stock on 4x leverage (requires 10m cash, borrows 30m debt)
        ok = engine.execute_order("VINTRUMITE", "BUY", 400.0, 100_000.0, use_margin=True)
        self.assertTrue(ok)
        self.assertEqual(engine.state.cash, 0.0)
        self.assertEqual(engine.state.margin_debt, 30_000_000.0)

        # Market shock: Stock drops to 90,000 (-10%) -> Stock value = 36,000,000
        # Trading Equity = 0 + 36m - 30m = 6,000,000
        # Margin Ratio = 6m / 36m = 16.67% (< 20% maintenance margin!)
        # Total Net Worth (including bank) = 0 + 36m + 10m - 30m = 16,000,000
        metrics = engine.evaluate({"VINTRUMITE": 90_000.0})
        self.assertAlmostEqual(metrics.margin_ratio, 6_000_000.0 / 36_000_000.0, places=4)
        self.assertEqual(metrics.margin_status, MarginStatus.MARGIN_CALL)
        self.assertEqual(metrics.bank_savings, 10_000_000.0)
        self.assertEqual(metrics.equity, 16_000_000.0)

        # When liquidation is triggered, Bank Savings remain 100% untouched
        liq = engine.trigger_forced_liquidation({"VINTRUMITE": 90_000.0})
        self.assertEqual(engine.state.bank_savings, 10_000_000.0)
        self.assertTrue(engine.state.is_liquidated)

    def test_bug3_and_bug4_phases_2_to_6_settlement_delay(self):
        """
        Validates Bug #3 and Bug #4 fixes:
        - Bug #3: Orders placed in Phases 2-6 do NOT bypass T+0.5 settlement.
        - Bug #4: Global seconds (> 300) are converted to phase-relative tick (< 150 check).
        """
        engine = MarginEngine(initial_capital=20_000_000.0)

        # In Phase 2, order at global tick 320 (which is phase-relative tick 20 < 150)
        # Should be scheduled for Phase 2, delivery_tick = 20 + 30 = 50
        engine.execute_order("VINTRUMITE", "BUY", 10.0, 100_000.0, current_tick=320, current_phase=2)
        self.assertIn("VINTRUMITE", engine.state.pending_shares)
        self.assertEqual(engine.state.holdings.get("VINTRUMITE", 0.0), 0.0)
        self.assertEqual(len(engine.state.pending_queue), 1)
        self.assertEqual(engine.state.pending_queue[0].deliver_in_phase, 2)
        self.assertEqual(engine.state.pending_queue[0].delivery_tick, 50)

        # Bug #3 check: Make sure it is NOT delivered immediately on tick 321
        engine.process_deliveries(current_tick=321, current_phase=2)
        self.assertEqual(engine.state.holdings.get("VINTRUMITE", 0.0), 0.0)

        # At tick 349 (phase_tick 49): still pending
        engine.process_deliveries(current_tick=349, current_phase=2)
        self.assertEqual(engine.state.holdings.get("VINTRUMITE", 0.0), 0.0)

        # At tick 350 (phase_tick 50): delivered!
        engine.process_deliveries(current_tick=350, current_phase=2)
        self.assertEqual(engine.state.holdings.get("VINTRUMITE", 0.0), 10.0)
        self.assertEqual(len(engine.state.pending_queue), 0)

        # Late order in Phase 2 at global tick 500 (phase-relative tick 200 > 150)
        # Should be scheduled for deliver_in_phase = 3, delivery_tick = 1
        engine.execute_order("SAMSUNG_ELEC", "BUY", 5.0, 50_000.0, current_tick=500, current_phase=2)
        self.assertEqual(len(engine.state.pending_queue), 1)
        self.assertEqual(engine.state.pending_queue[0].deliver_in_phase, 3)
        self.assertEqual(engine.state.pending_queue[0].delivery_tick, 1)

        # Tick 599 in Phase 2: still pending
        engine.process_deliveries(current_tick=599, current_phase=2)
        self.assertEqual(engine.state.holdings.get("SAMSUNG_ELEC", 0.0), 0.0)

        # Phase 3 transition: delivered!
        engine.process_deliveries(current_tick=601, current_phase=3)
        self.assertEqual(engine.state.holdings.get("SAMSUNG_ELEC", 0.0), 5.0)
        self.assertEqual(len(engine.state.pending_queue), 0)

    def test_bug5_midphase_forced_liquidation(self):
        """
        Validates Bug #5 fix:
        Mid-phase price drop triggers forced liquidation via GameController.check_midphase_liquidation()
        WITHOUT needing advance_phase().
        """
        controller = GameController(initial_capital=10_000.0, initial_margin_ratio=0.25)
        controller.set_tick_by_global_second(1)

        # Buy 4x margin position
        vnt_price = controller.current_prices.get("VNT", 1000.0)
        controller.engine.state.cash = 10_000.0
        # Buy $40,000 worth (requires $10,000 cash, creates $30,000 margin debt)
        shares_to_buy = 40_000.0 / vnt_price
        ok = controller.engine.execute_order(
            ticker="VNT",
            action="BUY",
            shares=shares_to_buy,
            price=vnt_price,
            use_margin=True,
            current_tick=1,
            current_phase=1,
        )
        self.assertTrue(ok)
        self.assertAlmostEqual(controller.engine.state.margin_debt, 30_000.0, places=2)

        # Deliver the shares immediately for testing liquidation
        controller.engine.process_deliveries(current_tick=31, current_phase=1)

        # Simulate mid-phase market crash (-10% drop) in current_prices
        # Stock value = $36,000, Debt = $30,000 -> Margin ratio = 6,000 / 36,000 = 16.67% (< 20%)
        controller.current_prices["VNT"] = vnt_price * 0.90

        # Check mid-phase liquidation
        liq_info = controller.check_midphase_liquidation()
        self.assertIsNotNone(liq_info)
        self.assertTrue(controller.engine.state.is_liquidated)
        self.assertAlmostEqual(controller.engine.state.margin_debt, 0.0, places=2)
        self.assertGreater(liq_info["penalty"], 0.0)

        # Subsequent checks return None (not double-liquidated)
        self.assertIsNone(controller.check_midphase_liquidation())

    def test_bug6_live_player_trade_and_tick_delivery(self):
        """
        Validates Bug #6 fix:
        GameController.player_trade() passes phase_tick & phase_id so orders route
        into the T+0.5 pending queue, and set_tick_by_global_second() processes deliveries.
        """
        controller = GameController(initial_capital=10_000.0)
        # Advance to Phase 2 tick 320 (phase_tick 20)
        controller.set_tick_by_global_second(320)
        self.assertEqual(controller.get_current_phase().phase_id, 2)

        vnt_price = controller.current_prices.get("VNT", 1000.0)
        controller.engine.state.cash = 50_000.0

        # Execute player trade
        ok = controller.player_trade("VNT", "BUY", 5.0, use_margin=False)
        self.assertTrue(ok)

        # Shares must be pending, NOT directly delivered yet
        self.assertIn("VNT", controller.engine.state.pending_shares)
        self.assertEqual(controller.engine.state.holdings.get("VNT", 0.0), 0.0)
        self.assertEqual(len(controller.engine.state.pending_queue), 1)
        self.assertEqual(controller.engine.state.pending_queue[0].deliver_in_phase, 2)
        self.assertEqual(controller.engine.state.pending_queue[0].delivery_tick, 50)

        # Live tick progression to tick 349 (phase tick 49)
        controller.set_tick_by_global_second(349)
        self.assertEqual(controller.engine.state.holdings.get("VNT", 0.0), 0.0)

        # Live tick progression to tick 350 (phase tick 50) -> Delivered!
        controller.set_tick_by_global_second(350)
        self.assertEqual(controller.engine.state.holdings.get("VNT", 0.0), 5.0)
        self.assertEqual(len(controller.engine.state.pending_queue), 0)


if __name__ == "__main__":
    unittest.main()
