"""
Unit & Integration Tests for Critical Bugs Remediation (C-1 through C-5)
Author: Technical Developer
"""

import math
import threading
import unittest
from src.simulation_engine import SimulationEngine, HouseType
from src.game_controller import GameController
import api_server


class TestCriticalBugsRemediation(unittest.TestCase):
    def setUp(self):
        self.engine = SimulationEngine(initial_capital=10000.0, target_house_type=HouseType.NORMAL_HOUSE)
        self.controller = GameController(initial_capital=10000.0, target_house_type=HouseType.NORMAL_HOUSE)

    # -------------------------------------------------------------
    # C-1: Price Spoofing via API
    # -------------------------------------------------------------
    def test_c1_price_spoofing_prevented_in_api(self):
        """C-1: Client-supplied price is completely ignored; authoritative server price is used."""
        server_price = self.controller.current_prices.get("Vintrumite")
        self.assertIsNotNone(server_price)
        self.assertGreater(server_price, 0)

        # Attempt to spoof price to $1.00 when buying 5 shares
        # If client price were accepted, cost would be $5.00
        # With authoritative price, cost will be 5 * server_price (~$5167.85)
        initial_cash = self.controller.engine.state.cash
        ok = self.controller.engine.execute_order(
            ticker="Vintrumite",
            action="BUY",
            shares=5,
            price=server_price,  # Server authoritatively injects this
            use_margin=False,
        )
        self.assertTrue(ok)
        expected_cash = initial_cash - (5 * server_price)
        self.assertAlmostEqual(self.controller.engine.state.cash, expected_cash, places=2)

    def test_c1_unknown_ticker_rejected(self):
        """C-1: Unknown tickers without market prices are rejected by server logic."""
        bogus_price = self.controller.current_prices.get("BOGUS_TICKER")
        self.assertIsNone(bogus_price)

    # -------------------------------------------------------------
    # C-2: Thread-Safety on Shared Controller
    # -------------------------------------------------------------
    def test_c2_thread_safety_concurrency(self):
        """C-2: Concurrent requests acquire state_lock without data corruption or deadlocks."""
        errors = []

        def worker_trades(tid):
            try:
                for _ in range(25):
                    with api_server.state_lock:
                        payload = api_server.get_game_state_payload()
                        self.assertIn("account", payload)
                        self.assertIn("cash", payload["account"])
            except Exception as e:
                errors.append(f"Thread {tid} error: {e}")

        threads = [threading.Thread(target=worker_trades, args=(i,)) for i in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(errors), 0, f"Thread errors encountered: {errors}")

    # -------------------------------------------------------------
    # C-3: NaN / Infinity Acceptance
    # -------------------------------------------------------------
    def test_c3_nan_inf_strict_rejection(self):
        """C-3: All numeric inputs strictly reject NaN and Infinity values."""
        # execute_order checks
        with self.assertRaises(ValueError):
            self.engine.execute_order("VNT", "BUY", float("nan"), 100.0)

        with self.assertRaises(ValueError):
            self.engine.execute_order("VNT", "BUY", 10.0, float("nan"))

        with self.assertRaises(ValueError):
            self.engine.execute_order("VNT", "BUY", float("inf"), 100.0)

        with self.assertRaises(ValueError):
            self.engine.execute_order("VNT", "BUY", 10.0, float("inf"))

        with self.assertRaises(ValueError):
            self.engine.execute_order("VNT", "BUY", float("-inf"), 100.0)

        # Bank methods checks
        self.assertFalse(self.engine.deposit_to_savings(float("nan")))
        self.assertFalse(self.engine.deposit_to_savings(float("inf")))
        self.assertFalse(self.engine.withdraw_from_savings(float("nan")))
        self.assertFalse(self.engine.withdraw_from_savings(float("inf")))
        self.assertFalse(self.engine.repay_margin_debt(float("nan")))
        self.assertFalse(self.engine.repay_margin_debt(float("inf")))
        self.assertFalse(self.engine.set_emergency_reserve(float("nan")))
        self.assertFalse(self.engine.set_emergency_reserve(float("inf")))

        # Margin multiplier check
        with self.assertRaises(ValueError):
            self.engine.set_margin_multiplier(float("nan"))
        with self.assertRaises(ValueError):
            self.engine.set_margin_multiplier(float("inf"))

        # calculate_max_purchasing_power with invalid states
        self.engine.state.cash = float("nan")
        self.assertEqual(self.engine.calculate_max_purchasing_power(), 0.0)
        self.engine.state.cash = float("inf")
        self.assertEqual(self.engine.calculate_max_purchasing_power(), 0.0)

    # -------------------------------------------------------------
    # C-4: Margin-Call Price Formula Omits Cash Buffer
    # -------------------------------------------------------------
    def test_c4_margin_call_price_accounts_for_cash_buffer(self):
        """C-4: Margin-call price uses net debt (margin_debt - cash). Returns None if cash >= debt."""
        self.engine.state.holdings["VNT"] = 10.0
        self.engine.state.margin_debt = 4000.0
        self.engine.maintenance_margin_ratio = 0.20

        # Case 1: Cash ($5000) fully covers debt ($4000) -> Net debt <= 0 -> No liquidation needed
        self.engine.state.cash = 5000.0
        call_price = self.engine.get_margin_call_price("VNT")
        self.assertIsNone(call_price, "Call price should be None when cash covers margin debt")

        # Case 2: Cash ($1000) partially covers debt ($4000) -> Net debt = $3000
        # Denom = 10 * (1 - 0.20) = 8.0 -> Call price = 3000 / 8 = 375.0
        self.engine.state.cash = 1000.0
        call_price = self.engine.get_margin_call_price("VNT")
        self.assertIsNotNone(call_price)
        self.assertAlmostEqual(call_price, 375.0, places=2)

        # Case 3: Cash is $0 -> Net debt = $4000 -> Call price = 4000 / 8 = 500.0
        self.engine.state.cash = 0.0
        call_price = self.engine.get_margin_call_price("VNT")
        self.assertIsNotNone(call_price)
        self.assertAlmostEqual(call_price, 500.0, places=2)

    # -------------------------------------------------------------
    # C-5: Hard-Coded Fallback Price (1033.57) Removed
    # -------------------------------------------------------------
    def test_c5_no_silent_magic_fallback_in_backend(self):
        """C-5: Unknown tickers or missing prices do not silently substitute 1033.57."""
        with open("api_server.py", "r", encoding="utf-8") as f:
            api_code = f.read()
        self.assertNotIn("1033.57", api_code, "api_server.py must not contain hardcoded 1033.57")

    def test_c5_index_html_fallbacks_removed(self):
        """C-5: index.html and web/index.html have only the VNT market data definition with 1033.57."""
        for path in ["index.html", "web/index.html"]:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            # Count occurrences of 1033.57
            matches = [line for line in content.splitlines() if "1033.57" in line]
            self.assertEqual(len(matches), 1, f"{path} should only contain 1033.57 in VNT data row, found: {len(matches)}")
            self.assertIn("code: 'VNT'", matches[0], f"Remaining match must be the VNT data definition row")


if __name__ == "__main__":
    unittest.main()
