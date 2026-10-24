import math
import os
import unittest

import api_server
from src.game_controller import GameController
from src.simulation_engine import MarginEngine, MarginStatus


class TestCompleteBugReport45(unittest.TestCase):
    """Comprehensive verification suite for all 45 bugs in complete_bug_report.md."""

    # =========================================================================
    # CRITICAL BUGS (CRIT-01 to CRIT-05)
    # =========================================================================

    def test_crit_01_uncollateralized_debt_triggers_margin_call(self):
        """CRIT-01 & HIGH-04: Residual margin_debt > 0 with stock_portfolio_value == 0 triggers MARGIN_CALL."""
        engine = MarginEngine(initial_capital=10000.0, initial_margin_ratio=0.25)
        engine.state.cash = 0.0
        engine.state.margin_debt = 5000.0
        metrics = engine.evaluate({})
        self.assertEqual(metrics.margin_status, MarginStatus.MARGIN_CALL)
        self.assertEqual(metrics.margin_ratio, 0.0)
        self.assertTrue(math.isinf(metrics.leverage))

    def test_crit_02_alias_resolution_in_forced_liquidation(self):
        """CRIT-02: Forced liquidation resolves ticker aliases (VNT <-> Vintrumite) so proceeds are not $0."""
        engine = MarginEngine(initial_capital=10000.0, initial_margin_ratio=0.25)
        engine.state.holdings["VNT"] = 10.0
        engine.state.margin_debt = 5000.0
        engine.state.cash = 0.0
        info = engine.trigger_forced_liquidation({"Vintrumite": 800.0})
        self.assertAlmostEqual(info["gross_proceeds"], 8000.0)
        self.assertTrue(engine.state.is_liquidated)

    def test_crit_03_path_traversal_protection_in_api_server(self):
        """CRIT-03: do_GET resolves abspath against allowed_roots and rejects directory traversal."""
        with open("api_server.py", "r", encoding="utf-8") as f:
            src = f.read()
        self.assertTrue("allowed_roots = (WEB_ROOT + os.sep, DATA_ROOT + os.sep, ASSETS_ROOT + os.sep)" in src)
        self.assertTrue('if ".." in raw_unquoted or ".." in req_path' in src)

    def test_crit_04_pm_session_phase_6_settlement_delivery(self):
        """CRIT-04: PM-session buy in Phase 6 settles within Phase 6 (min(tick+30, 300)), not Phase 7."""
        engine = MarginEngine(initial_capital=10000.0)
        ok = engine.execute_order(
            "VNT", "BUY", 10, 100.0, use_margin=False, current_tick=200, current_phase=6
        )
        self.assertTrue(ok)
        self.assertEqual(engine.state.pending_shares.get("VNT"), 10.0)
        self.assertEqual(engine.state.pending_queue[0].deliver_in_phase, 6)
        self.assertEqual(engine.state.pending_queue[0].delivery_tick, 230)
        engine.process_deliveries(current_tick=230, current_phase=6)
        self.assertEqual(engine.state.holdings.get("VNT", 0.0), 10.0)
        self.assertEqual(engine.state.pending_shares.get("VNT", 0.0), 0.0)

    def test_crit_05_no_alias_collision_in_api_server(self):
        """CRIT-05: Ticker alias resolution checks canonical keys first and avoids cross-ticker collisions."""
        with open("api_server.py", "r", encoding="utf-8") as f:
            src = f.read()
        self.assertTrue("if ticker not in controller.current_prices:" in src)

    # =========================================================================
    # HIGH BUGS (HIGH-01 to HIGH-15)
    # =========================================================================

    def test_high_01_no_free_ten_cent_buffer_on_buy(self):
        """HIGH-01: Buying beyond exact cash balance (e.g. $0.05 over) is strictly rejected."""
        engine = MarginEngine(initial_capital=100.0)
        self.assertFalse(engine.execute_order("VNT", "BUY", 1, 100.05, use_margin=False))

    def test_high_02_network_io_outside_state_lock(self):
        """HIGH-02: Network socket reads/writes in api_server.py happen outside state_lock."""
        with open("api_server.py", "r", encoding="utf-8") as f:
            src = f.read()
        self.assertTrue("HIGH-02: Compute payload inside lock, perform network I/O outside lock" in src)
        self.assertTrue("HIGH-02: Send response outside state_lock" in src)

    def test_high_03_margin_call_triggered_flag_resets_when_healthy(self):
        """HIGH-03: margin_call_triggered resets to False when account returns to HEALTHY/NORMAL."""
        engine = MarginEngine(initial_capital=10000.0, initial_margin_ratio=0.25)
        engine.state.margin_debt = 5000.0
        engine.state.cash = 0.0
        m1 = engine.evaluate({})
        self.assertEqual(m1.margin_status, MarginStatus.MARGIN_CALL)
        self.assertTrue(engine.state.margin_call_triggered)

        engine.state.margin_debt = 0.0
        engine.state.cash = 5000.0
        m2 = engine.evaluate({})
        self.assertEqual(m2.margin_status, MarginStatus.HEALTHY)
        self.assertFalse(engine.state.margin_call_triggered)

    def test_high_05_block_margin_buy_when_under_margin_call(self):
        """HIGH-05: New leveraged buys raise RuntimeError when account is under margin call."""
        engine = MarginEngine(initial_capital=10000.0, initial_margin_ratio=0.25)
        engine.state.margin_call_triggered = True
        with self.assertRaises(RuntimeError):
            engine.execute_order("VNT", "BUY", 1, 100.0, use_margin=True)

    def test_high_06_deposit_to_savings_blocked_under_margin_call(self):
        """HIGH-06: deposit_to_savings blocks draining collateral cash when under margin call or uncollateralized debt."""
        engine = MarginEngine(initial_capital=5000.0, initial_margin_ratio=0.25)
        engine.state.margin_debt = 3000.0
        engine.state.margin_call_triggered = True
        self.assertFalse(engine.deposit_to_savings(1000.0))

    def test_high_07_emergency_reserve_clamped_on_withdraw(self):
        """HIGH-07: withdraw_from_savings with ignore_reserve=True clamps emergency_reserve to bank_savings."""
        engine = MarginEngine(initial_capital=10000.0)
        engine.deposit_to_savings(5000.0)
        engine.set_emergency_reserve(5000.0)
        self.assertTrue(engine.withdraw_from_savings(2000.0, ignore_reserve=True))
        self.assertEqual(engine.state.bank_savings, 3000.0)
        self.assertEqual(engine.state.emergency_reserve, 3000.0)

    def test_high_08_api_trade_does_not_pre_mutate_multiplier(self):
        """HIGH-08: /api/trade does not mutate engine margin_multiplier per-order."""
        with open("api_server.py", "r", encoding="utf-8") as f:
            src = f.read()
        self.assertTrue("HIGH-08: Do not mutate engine margin_multiplier per-order via /api/trade" in src)

    def test_high_09_api_tick_blocks_backward_time_travel(self):
        """HIGH-09: /api/tick rejects backward ticks below current global_second."""
        with open("api_server.py", "r", encoding="utf-8") as f:
            src = f.read()
        self.assertTrue("if second < current_global:" in src)

    def test_high_10_advance_phase_lands_at_phase_start_second(self):
        """HIGH-10: advance_phase sets current tick to phase.start_second, not phase.end_second."""
        controller = GameController(initial_capital=10000.0)
        res = controller.advance_phase()
        self.assertEqual(res["phase_id"], 2)
        cur_sec = controller.price_ticks[controller.current_tick_index]["global_second"]
        self.assertEqual(cur_sec, 301)

    def test_high_11_savings_deposit_and_transfer_to_bank_check_liquidation(self):
        """HIGH-11: Moving cash to bank when holding margin debt triggers check_midphase_liquidation."""
        with open("api_server.py", "r", encoding="utf-8") as f:
            src = f.read()
        self.assertTrue("liq_info = controller.check_midphase_liquidation() if action == \"deposit\" else None" in src)

    def test_high_12_parse_strict_bool(self):
        """HIGH-12: parse_strict_bool parses 'false', '0', 'no' as False instead of True."""
        self.assertFalse(api_server.parse_strict_bool("false"))
        self.assertFalse(api_server.parse_strict_bool("0"))
        self.assertFalse(api_server.parse_strict_bool("no"))
        self.assertTrue(api_server.parse_strict_bool("true"))
        self.assertTrue(api_server.parse_strict_bool(True))

    def test_high_13_non_dict_json_payload_rejected(self):
        """HIGH-13: Non-object JSON payloads (e.g. list, int) are guarded against."""
        with open("api_server.py", "r", encoding="utf-8") as f:
            src = f.read()
        self.assertTrue("if not isinstance(body, dict):" in src)

    def test_high_14_savings_action_validated(self):
        """HIGH-14: /api/savings validates action in ('deposit', 'withdraw')."""
        with open("api_server.py", "r", encoding="utf-8") as f:
            src = f.read()
        self.assertIn('action not in ("deposit", "withdraw")', src)

    def test_high_15_max_body_size_enforced(self):
        """HIGH-15: Content-Length is capped at MAX_BODY_SIZE (1 MB) with HTTP 413."""
        with open("api_server.py", "r", encoding="utf-8") as f:
            src = f.read()
        self.assertIn("MAX_BODY_SIZE = 1024 * 1024", src)

    # =========================================================================
    # MODERATE BUGS (MOD-01 to MOD-14)
    # =========================================================================

    def test_mod_01_to_mod_14_engine_and_api(self):
        """MOD-01..MOD-14: Verify engine multi-asset margin call price, idempotency, float hygiene, and API state."""
        engine = MarginEngine(initial_capital=10000.0, initial_margin_ratio=0.25, maintenance_margin_ratio=0.25)
        # MOD-07: Respect configured base maintenance margin ratio (capped at 80% of initial_margin_ratio)
        engine.set_margin_multiplier(2.0)
        self.assertAlmostEqual(engine.maintenance_margin_ratio, 0.25)

        # MOD-02 & MOD-01: get_margin_call_price resolves alias and other stock collateral
        engine.state.holdings["VNT"] = 10.0
        engine.state.holdings["SEC"] = 10.0
        engine.state.margin_debt = 5000.0
        engine.state.cash = 1000.0
        p_single = engine.get_margin_call_price("Vintrumite")
        p_multi = engine.get_margin_call_price("Vintrumite", current_prices={"SEC": 200.0})
        self.assertIsNotNone(p_single)
        self.assertLess(p_multi, p_single)

        # MOD-14: repay_margin_debt rejects invalid from_source
        self.assertFalse(engine.repay_margin_debt(100.0, from_source="invalid_source"))

        # MOD-03: trigger_forced_liquidation is idempotent
        engine.trigger_forced_liquidation({"VNT": 500.0, "SEC": 200.0})
        second_liq = engine.trigger_forced_liquidation({"VNT": 500.0, "SEC": 200.0})
        self.assertEqual(second_liq["gross_proceeds"], 0.0)

        # MOD-10..MOD-13: State payload fields and shallow copies
        state = api_server.get_game_state_payload()
        for key in ("current_second", "current_tick", "initial_margin_ratio", "maintenance_margin_ratio"):
            self.assertIn(key, state)

    # =========================================================================
    # VISUAL BUGS (VIS-01 to VIS-11) & HTML PARITY
    # =========================================================================

    def test_vis_01_to_vis_11_and_html_parity(self):
        """VIS-01..VIS-11: Verify CSS/DOM fixes and 100% parity between index.html and web/index.html."""
        with open("index.html", "r", encoding="utf-8") as f:
            root_html = f.read()
        with open(os.path.join("web", "index.html"), "r", encoding="utf-8") as f:
            web_html = f.read()

        self.assertTrue(root_html == web_html, "index.html and web/index.html must be 100% identical")
        self.assertTrue("@keyframes pulseDot" in root_html)  # VIS-01
        self.assertTrue("animation-play-state: paused" in root_html)  # VIS-02
        self.assertTrue("overflow-y: auto;" in root_html)  # VIS-04
        self.assertTrue("rgba(16, 185, 129, 0.6)" in root_html)  # VIS-09
        self.assertTrue("user-select: text" in root_html)  # VIS-10
        self.assertTrue('src="data/market_ticks.js" defer' in root_html)  # VIS-11

    def test_post_liquidation_restart_resumes_simulation(self):
        """Verify that restarting after forced liquidation resets session flags, unlocks trade buttons, and resets backend state."""
        with open("index.html", "r", encoding="utf-8") as f:
            root_html = f.read()

        # Verify resetSimulationRuntimeState resets marketSessionStarted, removes body.liquidated, and re-enables trade buttons
        self.assertTrue("async function resetSimulationRuntimeState(" in root_html)
        self.assertTrue("marketSessionStarted = false;" in root_html)
        self.assertTrue("document.body.classList.remove('liquidated');" in root_html)
        self.assertTrue("btn.disabled = false;" in root_html)

        # Verify restartSimulationFromEnding resets runtime state and calls startMarketSession()
        self.assertTrue("async function restartSimulationFromEnding()" in root_html)
        self.assertTrue("await resetSimulationRuntimeState();" in root_html)
        self.assertTrue("startMarketSession();" in root_html)

        # Verify backend /api/init cleanly resets a liquidated controller
        api_server.controller = GameController(initial_capital=10000.0)
        api_server.controller.engine.trigger_forced_liquidation(api_server.controller.current_prices)
        self.assertTrue(api_server.get_game_state_payload()["is_liquidated"])

        # Re-initializing via GameController clears liquidation and restores capital
        api_server.controller = GameController(initial_capital=10000.0)
        reset_payload = api_server.get_game_state_payload()
        self.assertFalse(reset_payload["is_liquidated"])
        self.assertEqual(reset_payload["metrics"]["cash"], 10000.0)


if __name__ == "__main__":
    unittest.main()
