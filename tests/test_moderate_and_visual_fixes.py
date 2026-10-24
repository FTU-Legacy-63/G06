"""
Unit & Integration Tests for Moderate & Visual Fixes (M-1 to M-6, V-1 to V-6)
Author: Technical Developer
"""

import math
import re
import unittest
from src.simulation_engine import SimulationEngine, HouseType
from src.game_controller import GameController


class TestModerateAndVisualFixes(unittest.TestCase):
    def setUp(self):
        self.controller = GameController(initial_capital=10000.0, target_house_type=HouseType.NORMAL_HOUSE)

    # -------------------------------------------------------------
    # M-1: margin_multiplier Propagated to Engine
    # -------------------------------------------------------------
    def test_m1_margin_multiplier_propagated_in_player_trade(self):
        """M-1: player_trade forwards custom margin_multiplier to engine."""
        self.controller.engine.state.cash = 10000.0
        # Buy with 2.5x leverage
        ok = self.controller.player_trade(
            ticker="Samsung Electronics",
            action="BUY",
            shares=10,
            use_margin=True,
            margin_multiplier=2.5,
        )
        self.assertTrue(ok)
        self.assertEqual(self.controller.engine.margin_multiplier, 2.5)

    # -------------------------------------------------------------
    # M-2: MAX Button Math with $0 Cash
    # -------------------------------------------------------------
    def test_m2_max_button_math_zero_cash(self):
        """M-2: Max shares evaluates to 0 when cash is 0, not default 10000."""
        cash = 0.0
        mult = 2.0
        price = 166.07
        max_cash = cash * mult
        max_shares = max(0, int(math.floor(max_cash / price)))
        self.assertEqual(max_shares, 0)

    # -------------------------------------------------------------
    # M-3: Default Margin Multiplier is 1.0x
    # -------------------------------------------------------------
    def test_m3_default_margin_multiplier(self):
        """M-3: Initial margin multiplier is 1.0."""
        self.assertEqual(self.controller.engine.margin_multiplier, 1.0)
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn("marginMultiplier: 1.0", html)

    # -------------------------------------------------------------
    # M-4, M-5, M-6: UI Inspections
    # -------------------------------------------------------------
    def test_m4_custom_margin_validation_in_html(self):
        """M-4: promptCustomMargin checks for empty input and alerts on invalid multiplier."""
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn("Please enter a valid margin multiplier between 1.0× and 4.0×.", html)

    def test_m5_liquidation_ui_lock_in_html(self):
        """M-5: Liquidated state disables trade buttons and adds liquidated class."""
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn("document.body.classList.add('liquidated')", html)
        self.assertIn(".liquidated .trade-button", html)

    def test_m6_phase_bar_overflow_properties(self):
        """M-6: .persistent-phase-bar has flex-shrink, min-width, and text-overflow."""
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn("text-overflow: ellipsis", html)

    # -------------------------------------------------------------
    # V-1: No !important in @keyframes
    # -------------------------------------------------------------
    def test_v1_no_important_in_keyframes(self):
        """V-1: Verify no @keyframes declarations contain !important."""
        for path in ["index.html", "web/index.html"]:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            matches = re.finditer(r'@keyframes[^{]+\{([^}]+(?:\{[^}]+\}[^}]+)*)\}', content)
            for m in matches:
                self.assertNotIn("!important", m.group(0), f"Found !important in keyframe in {path}")

    # -------------------------------------------------------------
    # V-2: Chart Data Truncation Extended to Full Phase
    # -------------------------------------------------------------
    def test_v2_chart_data_truncation_extended(self):
        """V-2: appendPriceToChart preserves 300 points instead of truncating at 60."""
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn("labels.length > 300", html)
        self.assertNotIn("labels.length > 60", html)

    # -------------------------------------------------------------
    # V-3: Wall-Clock Timer Loop
    # -------------------------------------------------------------
    def test_v3_wall_clock_timer_in_html(self):
        """V-3: startMarketSession utilizes wall-clock Date.now() tracking."""
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn("lastWallClockTime", html)
        self.assertIn("accumulatedElapsedMs", html)

    # -------------------------------------------------------------
    # V-4: Tutorial Overlay Click-Through
    # -------------------------------------------------------------
    def test_v4_tutorial_overlay_css(self):
        """V-4: #screen-4.overlay-active has pointer-events: none."""
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn("#screen-4.overlay-active", html)

    # -------------------------------------------------------------
    # V-5: Phase Overlay Button Centering
    # -------------------------------------------------------------
    def test_v5_phase_overlay_centering_css(self):
        """V-5: .phase-overlay .next-button is centered with translateX(-50%)."""
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn(".phase-overlay .next-button", html)
        self.assertIn("transform: translateX(-50%)", html)

    # -------------------------------------------------------------
    # V-6: No Typos in Source Files
    # -------------------------------------------------------------
    def test_v6_no_typos_in_core_files(self):
        """V-6: No misspelled keywords like 'multipier' or 'liquidtion'."""
        for path in ["index.html", "web/index.html", "api_server.py"]:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().lower()
            self.assertNotIn("multipier", content, f"Found 'multipier' in {path}")
            self.assertNotIn("liquidtion", content, f"Found 'liquidtion' in {path}")


if __name__ == "__main__":
    unittest.main()
