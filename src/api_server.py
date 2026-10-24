"""
Free Fall 2.0 - HTTP Simulation API Bridge & Web Server
Author: Nguyen Quang Minh (Technical Developer)
Student ID: 2412380031
Subject: Technology Applications in Banking and Finance (NHA408E)

Provides a lightweight, zero-dependency HTTP REST API bridging the Python
Financial Engine with the Web Frontend (Week 5 Refinement & Week 6 Build Clinic).

Endpoints:
  GET  /api/state         -> Get current account metrics, balances, prices, and phase
  POST /api/init          -> Initialize/reset game with initial capital, margin tier, and house target
  POST /api/trade         -> Execute BUY or SELL order with margin toggle
  POST /api/savings       -> Deposit or withdraw cash into Bank Savings
  POST /api/advance       -> Advance market to next phase or tick
  GET  /                  -> Interactive Web Testing GUI for quick verification
"""

import http.server
import json
import math
import socketserver
import threading
import urllib.parse
from typing import Dict, Any, Optional
from src.game_controller import GameController
from src.simulation_engine import HouseType, MarginStatus

PORT = 8000
state_lock = threading.RLock()
controller = GameController(
    initial_capital=10000.0,
    target_house_type=HouseType.NORMAL_HOUSE,
    initial_margin_ratio=1.0,
)


MAX_BODY_SIZE = 1024 * 1024  # 1 MB limit (HIGH-15)


def parse_finite_float(val: Any, default: Optional[float] = None) -> Optional[float]:
    try:
        if val is None:
            return default
        f = float(val)
        if math.isnan(f) or math.isinf(f):
            return default
        return f
    except (TypeError, ValueError):
        return default


def parse_strict_bool(val: Any, default: bool = False) -> bool:
    """HIGH-12: Strictly parse boolean values so string 'false' or '0' evaluates to False."""
    if val is None:
        return default
    if val is True or val == 1:
        return True
    if val is False or val == 0:
        return False
    if isinstance(val, str):
        return val.strip().lower() in ("true", "1")
    return False


def serialize_metrics(m) -> Dict[str, Any]:
    return {
        "portfolio_value": m.portfolio_value,
        "bank_savings": m.bank_savings,
        "margin_debt": m.margin_debt,
        "cash": m.cash,
        "equity": m.equity,
        "leverage": 0.0 if m.leverage == float("inf") else round(m.leverage, 2),
        "margin_ratio": round(m.margin_ratio * 100, 2),
        "margin_status": m.margin_status.value,
        "target_progress": round(m.target_progress, 2),
        "is_solvent": m.is_solvent,
    }


def get_game_state_payload() -> Dict[str, Any]:
    with state_lock:
        metrics = controller.engine.evaluate(controller.current_prices)
        phase = controller.get_current_phase()
        current_second = (
            controller.price_ticks[controller.current_tick_index]["global_second"]
            if controller.price_ticks
            else 1
        )
        current_tick = ((current_second - 1) % 300) + 1
        return {
            "scenario_id": getattr(controller, "scenario_id", 1),
            "current_second": current_second,
            "current_tick": current_tick,
            "initial_margin_ratio": controller.engine.initial_margin_ratio,
            "maintenance_margin_ratio": controller.engine.maintenance_margin_ratio,
            "phase": {
                "id": phase.phase_id,
                "name": phase.name,
                "description": phase.description,
                "start_second": phase.start_second,
                "end_second": phase.end_second,
            },
            "target": {
                "house_type": controller.engine.target_house_type.value,
                "target_value": controller.engine.target_value,
                "initial_capital": controller.engine.initial_capital,
            },
            "bank": {
                "balance": round(controller.engine.state.bank_savings, 2),
                "emergency_reserve": round(controller.engine.state.emergency_reserve, 2),
                "available_transfer": round(max(0.0, controller.engine.state.bank_savings - controller.engine.state.emergency_reserve), 2),
            },
            "metrics": serialize_metrics(metrics),
            "account": {
                "cash": round(controller.engine.state.cash, 2),
                "bank_savings": round(controller.engine.state.bank_savings, 2),
                "margin_debt": round(controller.engine.state.margin_debt, 2),
                "equity": round(metrics.equity, 2),
                "portfolio_value": round(metrics.portfolio_value, 2),
            },
            # MOD-11: Return shallow copies to prevent external mutation of internal engine state
            "holdings": dict(controller.engine.state.holdings),
            "pending_shares": dict(controller.engine.state.pending_shares),
            "pending_queue": [
                {
                    "ticker": p.ticker,
                    "shares": p.shares,
                    "delivery_tick": p.delivery_tick,
                    "deliver_in_phase": p.deliver_in_phase,
                }
                for p in controller.engine.state.pending_queue
            ],
            "is_liquidated": controller.engine.state.is_liquidated,
            "prices": {t: round(p, 2) for t, p in controller.current_prices.items()},
        }


class SimulationRequestHandler(http.server.SimpleHTTPRequestHandler):
    def _send_json(self, data: Dict[str, Any], status: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/state":
            # HIGH-02: Compute payload inside lock, perform network I/O outside lock
            with state_lock:
                payload = get_game_state_payload()
            self._send_json(payload)
            return

        import os
        import mimetypes
        raw_unquoted = urllib.parse.unquote(parsed.path)
        req_path = raw_unquoted.lstrip("/")

        # CRIT-03: Sanitize path and block directory traversal / arbitrary file read
        if ".." in raw_unquoted or ".." in req_path or ":" in req_path or req_path.startswith(("/", "\\")):
            self.send_error(404, "File not found")
            return

        WEB_ROOT = os.path.abspath("web")
        DATA_ROOT = os.path.abspath("data")
        ASSETS_ROOT = os.path.abspath("assets")

        candidates = []
        if not req_path or req_path == "index.html":
            for root_index in [os.path.join("web", "index.html"), "index.html"]:
                if os.path.isfile(root_index):
                    candidates.append(root_index)
        else:
            rel_req = req_path[4:] if req_path.startswith("web/") else req_path
            candidate_paths = [
                os.path.join("web", rel_req),
                os.path.join("web", "assets", os.path.basename(rel_req)),
                os.path.join("assets", os.path.basename(rel_req)),
            ]
            if rel_req.startswith("data/"):
                candidate_paths.append(rel_req)

            allowed_roots = (WEB_ROOT + os.sep, DATA_ROOT + os.sep, ASSETS_ROOT + os.sep)
            for c in candidate_paths:
                abs_c = os.path.abspath(c)
                if abs_c.startswith(allowed_roots) and os.path.isfile(abs_c):
                    candidates.append(abs_c)

        file_path = candidates[0] if candidates else None

        if file_path:
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = "application/octet-stream"
            with open(file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", mime_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            try:
                self.wfile.write(content)
            except Exception:
                pass
        elif not req_path or req_path == "index.html":
            self._serve_gui()
        else:
            self.send_error(404, "File not found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        try:
            length = int(self.headers.get("Content-Length", 0))
        except (TypeError, ValueError):
            length = 0

        # HIGH-15: Enforce maximum request body size to prevent DoS memory exhaustion
        if length < 0 or length > MAX_BODY_SIZE:
            self.send_error(413, "Request body too large")
            return

        raw_body = self.rfile.read(length).decode("utf-8", errors="replace") if length > 0 else "{}"
        try:
            body = json.loads(raw_body)
            # HIGH-13: Guard against valid JSON payloads that are not dicts (e.g., list, int, str, null)
            if not isinstance(body, dict):
                body = {}
        except Exception:
            body = {}

        global controller
        resp_data: Optional[Dict[str, Any]] = None
        resp_status: int = 200
        not_found: bool = False

        # HIGH-02: Perform state transitions inside state_lock, then send HTTP response outside state_lock
        with state_lock:
            if parsed.path == "/api/init":
                capital = parse_finite_float(body.get("initial_capital"), 10000.0)
                if capital is None or capital <= 0:
                    resp_data = {"status": "error", "message": "Initial capital must be a positive finite number."}
                    resp_status = 400
                else:
                    house_str = body.get("target_house_type", "Normal House")
                    h_map = {
                        "Small House": HouseType.SMALL_HOUSE,
                        "Normal House": HouseType.NORMAL_HOUSE,
                        "ToLam Villa": HouseType.TOLAM_VILLA,
                    }
                    house = h_map.get(house_str, HouseType.NORMAL_HOUSE)
                    margin_ratio = parse_finite_float(body.get("initial_margin_ratio"), 1.0)
                    if margin_ratio is None or margin_ratio <= 0 or margin_ratio > 1.0:
                        resp_data = {"status": "error", "message": "Initial margin ratio must be a finite number in (0, 1.0]."}
                        resp_status = 400
                    else:
                        scen_val = body.get("scenario")
                        scen_id = int(scen_val) if (scen_val is not None and str(scen_val).isdigit() and int(scen_val) in [1, 2]) else None

                        controller = GameController(
                            scenario_id=scen_id,
                            initial_capital=capital,
                            target_house_type=house,
                            initial_margin_ratio=margin_ratio,
                        )
                        state_res = get_game_state_payload()
                        resp_data = {"status": "success", "message": f"Simulation initialized with Scenario {controller.scenario_id}", "state": state_res}

            elif parsed.path == "/api/trade":
                ticker = str(body.get("ticker", "Vintrumite")).strip()
                alias_map = {
                    "VNT": "Vintrumite",
                    "000660": "Vintrumite",
                    "SEC": "Samsung Electronics",
                    "005930": "Samsung Electronics",
                    "Samsung": "Samsung Electronics",
                    "KODEX": "KODEX Semiconductor",
                    "091160": "KODEX Semiconductor",
                    "KODEX2X": "KODEX Leverage",
                    "KODEX 2X": "KODEX Leverage",
                    "122630": "KODEX Leverage",
                    "TIGER": "TIGER Semiconductor TOP10",
                    "396500": "TIGER Semiconductor TOP10",
                    "HYUNDAI": "Hyundai Motor",
                    "005380": "Hyundai Motor",
                    "KIA": "Kia",
                    "000270": "Kia",
                    "POSCO-FM": "POSCO Future M",
                    "POSCO FM": "POSCO Future M",
                    "003670": "POSCO Future M",
                    "POSCO-HD": "POSCO Holdings",
                    "POSCO HD": "POSCO Holdings",
                    "005490": "POSCO Holdings",
                    "KZINC": "Korea Zinc",
                    "010130": "Korea Zinc",
                }
                code = body.get("code")
                # CRIT-05: Only resolve alias if ticker is not already a canonical key in current_prices
                if ticker not in controller.current_prices:
                    if ticker in alias_map:
                        ticker = alias_map[ticker]
                    elif code and code in alias_map:
                        ticker = alias_map[code]

                action = str(body.get("action", "BUY")).upper()
                if action not in ["BUY", "SELL"]:
                    resp_data = {"status": "error", "message": f"Invalid trade action: {action}"}
                    resp_status = 400
                else:
                    shares = parse_finite_float(body.get("shares"), None)
                    if shares is None or shares <= 0:
                        resp_data = {"status": "error", "message": "Shares must be a positive finite number."}
                        resp_status = 400
                    else:
                        # HIGH-12: Strict boolean parsing for use_margin
                        use_margin = parse_strict_bool(body.get("use_margin", False), False)

                        phase_tick = (controller.price_ticks[controller.current_tick_index]["global_second"] - 1) % 300 + 1 if controller.price_ticks else 1
                        current_phase = controller.get_current_phase().phase_id

                        try:
                            # C-1 Fix: Ignore client-provided price completely to prevent price spoofing.
                            price = controller.current_prices.get(ticker)
                            if (price is None or price <= 0.0) and code:
                                price = controller.current_prices.get(code)
                            if (price is None or price <= 0.0) and controller.price_ticks:
                                tick_prices = controller.price_ticks[controller.current_tick_index].get("prices", {})
                                price = tick_prices.get(ticker) or (tick_prices.get(code) if code else None)

                            if price is None or price <= 0.0 or math.isnan(price) or math.isinf(price):
                                resp_data = {"status": "error", "message": f"Unknown ticker or market price unavailable: {ticker}", "state": get_game_state_payload()}
                                resp_status = 400
                            else:
                                # HIGH-08: Do not mutate engine margin_multiplier per-order via /api/trade; use /api/margin
                                ok = controller.engine.execute_order(
                                    ticker=ticker,
                                    action=action,
                                    shares=shares,
                                    price=price,
                                    use_margin=use_margin,
                                    current_tick=phase_tick,
                                    current_phase=current_phase,
                                )
                                if ok:
                                    liq_info = controller.check_midphase_liquidation()
                                    payload = get_game_state_payload()
                                    if liq_info:
                                        payload["liquidation_info"] = liq_info
                                    resp_data = {"status": "success", "message": f"{action} order executed successfully", "state": payload}
                                else:
                                    is_settlement_locked = False
                                    if action == "SELL":
                                        active_shares = controller.engine.state.holdings.get(ticker, 0.0)
                                        pending_shares = controller.engine.state.pending_shares.get(ticker, 0.0)
                                        if shares > active_shares and (active_shares + pending_shares) >= shares:
                                            is_settlement_locked = True
                                    msg = "Order rejected: Shares locked in T+0.5 settlement holding pen" if is_settlement_locked else "Order rejected: Insufficient funds or invalid holdings"
                                    resp_data = {"status": "error", "is_settlement_locked": is_settlement_locked, "message": msg, "state": get_game_state_payload()}
                                    resp_status = 400
                        except Exception as e:
                            resp_data = {"status": "error", "message": str(e)}
                            resp_status = 400

            elif parsed.path == "/api/margin":
                mult_val = parse_finite_float(body.get("margin_multiplier"), 1.0)
                if mult_val is None or mult_val < 1.0 or mult_val > 4.0:
                    resp_data = {"status": "error", "message": "Margin multiplier must be a finite number between 1.0 and 4.0."}
                    resp_status = 400
                else:
                    mult = controller.engine.set_margin_multiplier(mult_val)
                    resp_data = {
                        "status": "success",
                        "margin_multiplier": mult,
                        "initial_margin_ratio": controller.engine.initial_margin_ratio,
                        "maintenance_margin_ratio": controller.engine.maintenance_margin_ratio,
                        "state": get_game_state_payload(),
                    }

            elif parsed.path == "/api/savings":
                action = body.get("action", "deposit")
                # HIGH-14: Strictly validate savings action
                if action not in ("deposit", "withdraw"):
                    resp_data = {"status": "error", "message": f"Invalid savings action: {action}"}
                    resp_status = 400
                else:
                    amount = parse_finite_float(body.get("amount"), None)
                    if amount is None or amount <= 0:
                        resp_data = {"status": "error", "message": "Amount must be a positive finite number."}
                        resp_status = 400
                    else:
                        if action == "deposit":
                            ok = controller.engine.deposit_to_savings(amount)
                        else:
                            ok = controller.engine.withdraw_from_savings(amount)

                        if ok:
                            # HIGH-11: Check if transferring cash to savings triggered a margin call
                            liq_info = controller.check_midphase_liquidation() if action == "deposit" else None
                            payload = get_game_state_payload()
                            if liq_info:
                                payload["liquidation_info"] = liq_info
                            resp_data = {"status": "success", "state": payload}
                        else:
                            resp_data = {"status": "error", "message": "Invalid savings transaction amount"}
                            resp_status = 400

            elif parsed.path == "/api/repay_debt":
                amount = parse_finite_float(body.get("amount"), None)
                if amount is None or amount <= 0:
                    resp_data = {"status": "error", "message": "Repay amount must be a positive finite number."}
                    resp_status = 400
                else:
                    source = body.get("source", "bank")
                    ok = controller.engine.repay_margin_debt(amount, from_source=source)
                    if ok:
                        resp_data = {"status": "success", "message": f"Repaid ${amount:,.2f} debt from {source}", "state": get_game_state_payload()}
                    else:
                        resp_data = {"status": "error", "message": "Repayment failed: check balance or debt amount", "state": get_game_state_payload()}
                        resp_status = 400

            elif parsed.path == "/api/emergency_reserve":
                amount = parse_finite_float(body.get("amount"), None)
                if amount is None or amount < 0:
                    resp_data = {"status": "error", "message": "Reserve amount must be a non-negative finite number."}
                    resp_status = 400
                else:
                    ok = controller.engine.set_emergency_reserve(amount)
                    if ok:
                        resp_data = {"status": "success", "message": f"Emergency reserve set to ${amount:,.2f}", "state": get_game_state_payload()}
                    else:
                        resp_data = {"status": "error", "message": "Cannot set reserve higher than bank balance", "state": get_game_state_payload()}
                        resp_status = 400

            elif parsed.path == "/api/transfer_to_trading":
                amount = parse_finite_float(body.get("amount"), None)
                if amount is None or amount <= 0:
                    resp_data = {"status": "error", "message": "Transfer amount must be a positive finite number."}
                    resp_status = 400
                else:
                    # MOD-12 & HIGH-12: Enforce emergency reserve lock on public transfer endpoint
                    ok = controller.engine.withdraw_from_savings(amount, ignore_reserve=False)
                    if ok:
                        resp_data = {"status": "success", "message": f"Transferred ${amount:,.2f} to Trading Cash", "state": get_game_state_payload()}
                    else:
                        resp_data = {"status": "error", "message": "Transfer failed: insufficient unlocked bank balance", "state": get_game_state_payload()}
                        resp_status = 400

            elif parsed.path == "/api/transfer_to_bank":
                amount = parse_finite_float(body.get("amount"), None)
                if amount is None or amount <= 0:
                    resp_data = {"status": "error", "message": "Transfer amount must be a positive finite number."}
                    resp_status = 400
                else:
                    ok = controller.engine.deposit_to_savings(amount)
                    if ok:
                        # HIGH-11: Check if transferring cash to bank triggered a margin call
                        liq_info = controller.check_midphase_liquidation()
                        payload = get_game_state_payload()
                        if liq_info:
                            payload["liquidation_info"] = liq_info
                        resp_data = {"status": "success", "message": f"Transferred ${amount:,.2f} to Safe Haven Bank", "state": payload}
                    else:
                        resp_data = {"status": "error", "message": "Transfer failed: insufficient trading cash", "state": get_game_state_payload()}
                        resp_status = 400

            elif parsed.path == "/api/advance":
                old_phase = controller.current_phase_index
                result = controller.advance_phase()
                # MOD-10: Accurately report whether phase actually advanced
                actually_advanced = result.get("phase_advanced", controller.current_phase_index != old_phase)
                resp_data = {
                    "status": "success",
                    "phase_advanced": actually_advanced,
                    "liquidation_info": result.get("liquidation_info"),
                    "state": get_game_state_payload(),
                }

            elif parsed.path == "/api/tick":
                second_val = parse_finite_float(body.get("global_second") or body.get("second"), 1)
                second = int(second_val) if (second_val is not None and second_val >= 1) else 1
                # HIGH-09: Prevent time travel backwards
                current_global = controller.price_ticks[controller.current_tick_index]["global_second"] if controller.price_ticks else 1
                if second < current_global:
                    resp_data = {"status": "error", "message": f"Cannot rewind time from {current_global} to {second}"}
                    resp_status = 400
                else:
                    controller.set_tick_by_global_second(second)
                    liq_info = controller.check_midphase_liquidation()
                    payload = get_game_state_payload()
                    resp_data = {
                        "status": "success",
                        "tick": second,
                        "state": payload,
                    }
                    if liq_info:
                        resp_data["liquidation_info"] = liq_info

            else:
                not_found = True

        # HIGH-02: Send response outside state_lock
        if not_found:
            self.send_error(404, "Endpoint not found")
        elif resp_data is not None:
            self._send_json(resp_data, status=resp_status)

    def _serve_gui(self):
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Free Fall 2.0 - Financial Simulation Engine Bridge</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
        .container { max-width: 1000px; margin: 0 auto; }
        h1 { color: #38bdf8; margin-bottom: 4px; }
        .subtitle { color: #94a3b8; font-size: 14px; margin-bottom: 20px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .card { background: #1e293b; border-radius: 8px; padding: 15px; border: 1px solid #334155; }
        .card-title { font-size: 12px; color: #94a3b8; text-transform: uppercase; margin-bottom: 6px; }
        .card-value { font-size: 20px; font-weight: bold; }
        .badge { display: inline-block; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
        .badge-healthy { background: #065f46; color: #34d399; }
        .badge-warning { background: #854d0e; color: #facc15; }
        .badge-call { background: #991b1b; color: #f87171; }
        .badge-liquidated { background: #450a0a; color: #fca5a5; }
        .controls { background: #1e293b; border-radius: 8px; padding: 15px; border: 1px solid #334155; margin-bottom: 20px; }
        button { background: #0284c7; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: bold; margin-right: 8px; }
        button:hover { background: #0369a1; }
        button.danger { background: #dc2626; }
        button.danger:hover { background: #b91c1c; }
        select, input { background: #0f172a; border: 1px solid #475569; color: white; padding: 8px; border-radius: 6px; margin-right: 8px; }
        pre { background: #020617; padding: 12px; border-radius: 6px; overflow-x: auto; color: #cbd5e1; font-size: 12px; }
    </style>
</head>
<body>
<div class="container">
    <h1>📉 Free Fall 2.0 - Core Engine Bridge</h1>
    <div class="subtitle">NHA408E Midterm - Week 5 Refinement Studio | Author: Nguyen Quang Minh (Technical Lead)</div>

    <div class="grid">
        <div class="card"><div class="card-title">Net Equity</div><div class="card-value" id="val-equity">$0.00</div></div>
        <div class="card"><div class="card-title">Cash / Savings</div><div class="card-value" id="val-cash">$0.00 / $0.00</div></div>
        <div class="card"><div class="card-title">Margin Debt</div><div class="card-value" id="val-debt">$0.00</div></div>
        <div class="card"><div class="card-title">Margin Ratio</div><div class="card-value" id="val-ratio">100.0%</div></div>
        <div class="card"><div class="card-title">Margin Health</div><div class="card-value" id="val-status">-</div></div>
        <div class="card"><div class="card-title">Target Progress</div><div class="card-value" id="val-progress">0.0%</div></div>
    </div>

    <div class="controls">
        <h3>🎮 Actions & Phase Advancement</h3>
        <div style="margin-bottom: 12px;">
            <label>Trade:</label>
            <select id="trade-ticker">
                <option value="Vintrumite">Vintrumite</option>
                <option value="Samsung Electronics">Samsung Electronics</option>
                <option value="POSCO Future M">POSCO Future M</option>
                <option value="Kakao">Kakao</option>
                <option value="KODEX KOSDAQ150 Leverage">KODEX KOSDAQ150 Leverage</option>
            </select>
            <input type="number" id="trade-shares" value="10" style="width: 80px;" placeholder="Shares">
            <label><input type="checkbox" id="trade-margin" checked> Use Margin (4x)</label>
            <button onclick="trade('BUY')">BUY</button>
            <button onclick="trade('SELL')">SELL</button>
        </div>
        <div>
            <button class="danger" onclick="advancePhase()">⏩ Advance to Next Phase</button>
            <button onclick="depositSavings()">🏦 Deposit $2,000 to Savings</button>
            <button onclick="refreshState()">🔄 Refresh State</button>
        </div>
    </div>

    <h3>📡 Live REST API State (JSON)</h3>
    <pre id="raw-state">Loading state...</pre>
</div>

<script>
async function refreshState() {
    const res = await fetch('/api/state');
    const data = await res.json();
    document.getElementById('raw-state').textContent = JSON.stringify(data, null, 2);

    const m = data.metrics;
    document.getElementById('val-equity').textContent = '$' + m.equity.toLocaleString();
    document.getElementById('val-cash').textContent = '$' + m.cash.toLocaleString() + ' / $' + m.bank_savings.toLocaleString();
    document.getElementById('val-debt').textContent = '$' + m.margin_debt.toLocaleString();
    document.getElementById('val-ratio').textContent = m.margin_ratio + '% (Lev: ' + m.leverage + 'x)';
    document.getElementById('val-progress').textContent = m.target_progress + '%';

    const statusEl = document.getElementById('val-status');
    statusEl.textContent = m.margin_status;
    statusEl.className = 'badge ' + (
        m.margin_status === 'HEALTHY' ? 'badge-healthy' :
        m.margin_status === 'WARNING' ? 'badge-warning' :
        m.margin_status === 'MARGIN_CALL' ? 'badge-call' : 'badge-liquidated'
    );
}

async function trade(action) {
    const ticker = document.getElementById('trade-ticker').value;
    const shares = parseFloat(document.getElementById('trade-shares').value);
    const useMargin = document.getElementById('trade-margin').checked;
    await fetch('/api/trade', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ticker, action, shares, use_margin: useMargin})
    });
    refreshState();
}

async function advancePhase() {
    await fetch('/api/advance', {method: 'POST'});
    refreshState();
}

async function depositSavings() {
    await fetch('/api/savings', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({action: 'deposit', amount: 2000.0})
    });
    refreshState();
}

refreshState();
</script>
</body>
</html>
"""
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

def run_server():
    with ThreadedTCPServer(("", PORT), SimulationRequestHandler) as httpd:
        print(f"Server started at http://localhost:{PORT}")
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()
