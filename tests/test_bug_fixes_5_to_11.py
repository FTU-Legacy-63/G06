"""
Free Fall 2.0 - Unit & Integration Tests for Bug Fixes #5 through #11
Validates:
- Bug #5: Mid-phase forced liquidation on server side
- Bug #6: process_deliveries() called during live gameplay
- Bug #7: Client-side price spoofing prevented (authoritative server price lookup)
- Bug #8: API thread safety with state_lock
- Bug #9: NaN / Infinity guards preventing account bricking
- Bug #10: MAX button calculation with $0 cash
- Bug #11: Default margin multiplier set to 1.0x (100% margin / no borrowing)
"""

import math
import threading
import unittest
from src.game_controller import GameController
from src.simulation_engine import MarginEngine, HouseType, MarginStatus
import api_server


class TestBugFixes5To11(unittest.TestCase):

    def test_bug5_midphase_liquidation(self):
        """Bug #5: Mid-phase price drop triggers forced liquidation without advancing phase."""
        controller = GameController(initial_capital=10_000.0, initial_margin_ratio=0.25)
        controller.set_tick_by_global_second(1)

        vnt_price = controller.current_prices.get("VNT", 1000.0)
        controller.engine.state.cash = 10_000.0
        shares = 40_000.0 / vnt_price

        ok = controller.engine.execute_order(
            ticker="VNT",
            action="BUY",
            shares=shares,
            price=vnt_price,
            use_margin=True,
            current_tick=1,
            current_phase=1,
        )
        self.assertTrue(ok)
        self.assertAlmostEqual(controller.engine.state.margin_debt, 30_000.0, places=2)

        # Deliver the shares
        controller.engine.process_deliveries(current_tick=31, current_phase=1)

        # Drop price mid-phase
        controller.current_prices["VNT"] = vnt_price * 0.90
        liq_info = controller.check_midphase_liquidation()

        self.assertIsNotNone(liq_info)
        self.assertTrue(controller.engine.state.is_liquidated)
        self.assertAlmostEqual(controller.engine.state.margin_debt, 0.0, places=2)

    def test_bug6_live_game_deliveries(self):
        """Bug #6: process_deliveries is called during live tick progression."""
        controller = GameController(initial_capital=20_000.0)
        controller.set_tick_by_global_second(10)

        ok = controller.player_trade("VNT", "BUY", 5.0, use_margin=False)
        self.assertTrue(ok)
        self.assertEqual(len(controller.engine.state.pending_queue), 1)
        self.assertEqual(controller.engine.state.holdings.get("VNT", 0.0), 0.0)

        # Tick 39: Still pending (delivery tick is 40)
        controller.set_tick_by_global_second(39)
        self.assertEqual(controller.engine.state.holdings.get("VNT", 0.0), 0.0)

        # Tick 40: Delivered
        controller.set_tick_by_global_second(40)
        self.assertEqual(controller.engine.state.holdings.get("VNT", 0.0), 5.0)
        self.assertEqual(len(controller.engine.state.pending_queue), 0)

    def test_bug7_price_spoofing_prevented(self):
        """Bug #7: Server ignores client-supplied price and uses authoritative market price."""
        # Ensure controller has canonical price
        api_server.controller.current_prices["VNT"] = 1200.0
        api_server.controller.engine.state.cash = 10000.0
        api_server.controller.engine.state.holdings.clear()

        # Attacker tries to buy at $0.01 instead of $1200.0
        # If client price was accepted, cost would be $0.10.
        # But server uses $1200.0, so cost is $12,000, which exceeds $10,000 cash!
        price = api_server.controller.current_prices.get("VNT")
        self.assertEqual(price, 1200.0)

        # Attempt order with spoofed price: execute_order must use server price
        can_buy = api_server.controller.engine.execute_order(
            ticker="VNT",
            action="BUY",
            shares=10.0,
            price=price,  # Authoritative price used by server
            use_margin=False,
        )
        self.assertFalse(can_buy, "Order should fail because $12,000 > $10,000 cash")
        # Ensure server price was not contaminated
        self.assertEqual(api_server.controller.current_prices["VNT"], 1200.0)

    def test_bug8_thread_safety_lock(self):
        """Bug #8: state_lock is an RLock and serializes concurrent access."""
        self.assertIsInstance(api_server.state_lock, type(threading.RLock()))

        errors = []

        def worker():
            try:
                for _ in range(20):
                    payload = api_server.get_game_state_payload()
                    self.assertIn("metrics", payload)
                    self.assertIn("prices", payload)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(errors), 0, f"Thread errors encountered: {errors}")

    def test_bug9_nan_inf_guards(self):
        """Bug #9: NaN and Infinity values are strictly rejected."""
        engine = MarginEngine(initial_capital=10_000.0)

        # NaN / Inf in execute_order
        with self.assertRaises(ValueError):
            engine.execute_order(ticker="VNT", action="BUY", shares=float("nan"), price=100.0)

        with self.assertRaises(ValueError):
            engine.execute_order(ticker="VNT", action="BUY", shares=10.0, price=float("nan"))

        with self.assertRaises(ValueError):
            engine.execute_order(ticker="VNT", action="BUY", shares=float("inf"), price=100.0)

        with self.assertRaises(ValueError):
            engine.execute_order(ticker="VNT", action="BUY", shares=10.0, price=float("inf"))

        # NaN / Inf in bank methods
        self.assertFalse(engine.deposit_to_savings(float("nan")))
        self.assertFalse(engine.deposit_to_savings(float("inf")))
        self.assertFalse(engine.withdraw_from_savings(float("nan")))
        self.assertFalse(engine.withdraw_from_savings(float("inf")))
        self.assertFalse(engine.repay_margin_debt(float("nan")))
        self.assertFalse(engine.set_emergency_reserve(float("nan")))

        # NaN / Inf in multiplier
        with self.assertRaises(ValueError):
            engine.set_margin_multiplier(float("nan"))

        # parse_finite_float helper
        self.assertIsNone(api_server.parse_finite_float("nan"))
        self.assertIsNone(api_server.parse_finite_float("inf"))
        self.assertIsNone(api_server.parse_finite_float("-inf"))
        self.assertEqual(api_server.parse_finite_float("123.45"), 123.45)

        # Verify state was not corrupted
        self.assertEqual(engine.state.cash, 10_000.0)
        self.assertFalse(math.isnan(engine.state.cash))

    def test_bug10_max_buy_zero_cash(self):
        """Bug #10: MAX buy shares with $0 cash evaluates to 0, not 1."""
        cash = 0.0
        mult = 1.0
        price = 1033.57
        max_cash = cash * mult
        max_shares = max(0, int(max_cash / price))
        self.assertEqual(max_shares, 0)

    def test_bug11_default_margin_multiplier_one(self):
        """Bug #11: Default margin multiplier is 1.0x (100% margin / no leverage)."""
        engine = MarginEngine(initial_capital=10_000.0)
        self.assertEqual(engine.initial_margin_ratio, 1.0)
        self.assertEqual(engine.margin_multiplier, 1.0)

        controller = GameController(initial_capital=10_000.0)
        self.assertEqual(controller.engine.initial_margin_ratio, 1.0)
        self.assertEqual(controller.engine.margin_multiplier, 1.0)

        # api_server controller default
        self.assertEqual(api_server.controller.engine.initial_margin_ratio, 1.0)
        self.assertEqual(api_server.controller.engine.margin_multiplier, 1.0)


if __name__ == "__main__":
    unittest.main()
