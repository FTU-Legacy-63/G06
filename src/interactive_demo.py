"""
Free Fall 2.0 - Interactive Simulation Engine Prototype
Author: Nguyen Quang Minh (Technical Developer)
Student ID: 2412380031
Subject: Technology Applications in Banking and Finance (NHA408E)

Integrated with real CSV market dataset: market scenario/market_scenario.csv
(1,800 ticks, 50 Korean equity tickers across 6 phases)
"""

import sys
from src.game_controller import GameController
from src.simulation_engine import HouseType, MarginStatus


def print_banner():
    print("=" * 75)
    print("      📉 FREE FALL 2.0 - MARGIN SIMULATION ENGINE (CSV DATASET INTEGRATED)")
    print("      Midterm Technical Verification: NHA408E - Group 6 (Minh Nguyen)")
    print("=" * 75)


def main():
    print_banner()
    print("Select Difficulty / House Target (Calibrated against benchmark backtest):")
    print("  1. Small House   (Goal: 3.0x Capital   - Normie Ending / Solvency)")
    print("  2. Normal House  (Goal: 20.0x Capital  - Balanced)")
    print("  3. ToLam Villa   (Goal: 100.0x Capital - Extreme / 4.0x Leverage Required)")

    choice = input("\nEnter choice (1-3, default 3): ").strip() or "3"
    target_map = {"1": HouseType.SMALL_HOUSE, "2": HouseType.NORMAL_HOUSE, "3": HouseType.TOLAM_VILLA}
    house = target_map.get(choice, HouseType.TOLAM_VILLA)

    print("\nSelect Margin Tier:")
    print("  1. Cash Only (1.0x - Buying Power 1.0x, Immune to Margin Calls)")
    print("  2. 2.0x Margin (50% Initial Margin Ratio)")
    print("  3. 4.0x Margin (25% Initial Margin Ratio - Extreme Fragility)")

    tier_choice = input("Enter margin tier (1-3, default 3): ").strip() or "3"
    margin_map = {"1": 1.0, "2": 0.50, "3": 0.25}
    initial_margin = margin_map.get(tier_choice, 0.25)

    controller = GameController(
        scenario_csv_path="market scenario/market_scenario.csv",
        initial_capital=10000.0,  # $10,000 USD
        target_house_type=house,
        initial_margin_ratio=initial_margin,
    )

    print(f"\n[INIT] Starting Capital: ${controller.engine.initial_capital:,.2f} USD")
    print(f"[INIT] House Target:     ${controller.engine.target_value:,.2f} USD ({house.value})")
    print(f"[INIT] Max Buying Power: ${controller.engine.calculate_max_purchasing_power():,.2f} USD")
    print(f"[INIT] Maintenance Margin Floor: {controller.engine.maintenance_margin_ratio * 100:.0f}%")
    print(f"[INIT] Loaded {len(controller.price_ticks)} market ticks across 50 asset tickers.")
    print("-" * 75)

    for step in range(len(controller.phases)):
        phase = controller.get_current_phase()
        print(f"\n>>> [Phase {phase.phase_id}: {phase.name}] (Global Seconds: {phase.start_second}-{phase.end_second})")
        print(f"Context: {phase.description}")

        featured_tickers = ["Vintrumite", "Samsung Electronics", "POSCO Future M", "Kakao", "KODEX KOSDAQ150 Leverage"]
        print("Featured Asset Prices (USD/KRW Equivalent):")
        for t in featured_tickers:
            price = controller.current_prices.get(t, 0.0)
            print(f"  - {t:28}: {price:,.2f}")

        metrics = controller.engine.evaluate(controller.current_prices)
        print(f"\nAccount Balance & Health:")
        print(f"  Cash: ${metrics.cash:,.2f} | Margin Debt: ${metrics.margin_debt:,.2f}")
        print(f"  Portfolio Value: ${metrics.portfolio_value:,.2f} | Net Equity: ${metrics.equity:,.2f}")
        print(f"  Effective Leverage: {metrics.leverage:.2f}x | Margin Ratio: {metrics.margin_ratio * 100:.2f}%")
        print(f"  Status: [{metrics.margin_status.value}] | Target Progress: {metrics.target_progress:.2f}%")

        if controller.engine.state.is_liquidated:
            print("\n🚨 [ALERT] Account has been LIQUIDATED. Terminating simulation.")
            break

        print("\nPlayer Action:")
        print("  1. Buy Asset (Leveraged or Cash)")
        print("  2. Sell Asset")
        print("  3. Hold / Advance to Next Phase")
        act = input("Select action (1/2/3, default 3): ").strip() or "3"

        if act == "1":
            ticker = input("Enter ticker name (default: Vintrumite): ").strip() or "Vintrumite"
            use_m = input("Use margin borrowing? (y/n, default: y): ").strip().lower() != "n"
            shares_str = input("Enter number of shares: ").strip() or "10"
            try:
                sh = float(shares_str)
                ok = controller.player_trade(ticker, "BUY", sh, use_margin=use_m)
                if ok:
                    print(f"[SUCCESS] Executed BUY {sh} shares of {ticker}.")
                else:
                    print("[REJECTED] Insufficient cash balance or exceeds maximum buying power.")
            except Exception as e:
                print(f"[ERROR] {e}")

        elif act == "2":
            ticker = input("Enter ticker to sell (default: Vintrumite): ").strip() or "Vintrumite"
            shares_str = input("Enter number of shares to sell: ").strip() or "10"
            try:
                sh = float(shares_str)
                ok = controller.player_trade(ticker, "SELL", sh)
                if ok:
                    print(f"[SUCCESS] Executed SELL {sh} shares of {ticker}.")
                else:
                    print("[REJECTED] Insufficient holdings to sell.")
            except Exception as e:
                print(f"[ERROR] {e}")

        if step + 1 < len(controller.phases):
            print("\nAdvancing market timeline across phase...")
            result = controller.advance_phase()
            if result.get("liquidation_info"):
                print("\n" + "!" * 75)
                print("🚨🚨 [CRITICAL ALERT] FORCED LIQUIDATION TRIGGERED BY CLEARINGHOUSE!")
                print("Your Margin Ratio breached the 20% maintenance margin threshold.")
                print(f"  Liquidation Proceeds: ${result['liquidation_info']['gross_proceeds']:,.2f}")
                print(f"  Settled Debt:         ${result['liquidation_info']['remaining_debt']:,.2f}")
                print(f"  Final Net Equity:     ${result['liquidation_info']['final_equity']:,.2f}")
                print("!" * 75)

    print("\n" + "=" * 75)
    print("                           FINAL PERFORMANCE DEBRIEF")
    print("=" * 75)
    summary = controller.get_summary()
    for k, v in summary.items():
        if isinstance(v, float):
            print(f"  {k:25}: {v:,.2f}")
        else:
            print(f"  {k:25}: {v}")
    print("=" * 75)


if __name__ == "__main__":
    main()
