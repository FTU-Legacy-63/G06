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
import socketserver
import urllib.parse
from typing import Dict, Any
from src.game_controller import GameController
from src.simulation_engine import HouseType, MarginStatus

PORT = 8000
controller = GameController(
    scenario_csv_path="market scenario/market_scenario.csv",
    initial_capital=10000.0,
    target_house_type=HouseType.NORMAL_HOUSE,
    initial_margin_ratio=0.25,
)


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
    metrics = controller.engine.evaluate(controller.current_prices)
    phase = controller.get_current_phase()
    return {
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
        "holdings": controller.engine.state.holdings,
        "pending_shares": controller.engine.state.pending_shares,
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
            self._send_json(get_game_state_payload())
            return
        
        import os
        import mimetypes
        req_path = parsed.path.lstrip("/")
        if not req_path or req_path == "index.html":
            file_path = os.path.join("web", "index.html")
        else:
            file_path = os.path.join("web", req_path)

        if os.path.isfile(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = "application/octet-stream"
            with open(file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", mime_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content)
        else:
            self._serve_gui()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            body = json.loads(raw_body)
        except Exception:
            body = {}

        global controller

        if parsed.path == "/api/init":
            capital = float(body.get("initial_capital", 10000.0))
            house_str = body.get("target_house_type", "Normal House")
            h_map = {
                "Small House": HouseType.SMALL_HOUSE,
                "Normal House": HouseType.NORMAL_HOUSE,
                "ToLam Villa": HouseType.TOLAM_VILLA,
            }
            house = h_map.get(house_str, HouseType.NORMAL_HOUSE)
            margin_ratio = float(body.get("initial_margin_ratio", 0.25))

            controller = GameController(
                scenario_csv_path="market scenario/market_scenario.csv",
                initial_capital=capital,
                target_house_type=house,
                initial_margin_ratio=margin_ratio,
            )
            self._send_json({"status": "success", "message": "Simulation initialized", "state": get_game_state_payload()})

        elif parsed.path == "/api/trade":
            ticker = body.get("ticker", "Vintrumite")
            alias_map = {
                "VNT": "Vintrumite",
                "005930": "Samsung Electronics",
                "091160": "KODEX Semiconductor",
                "122630": "KODEX Leverage",
                "396500": "TIGER Semiconductor TOP10",
                "005380": "Hyundai Motor",
                "000270": "Kia",
                "003670": "POSCO Future M",
                "005490": "POSCO Holdings",
                "010130": "Korea Zinc",
            }
            if ticker in alias_map:
                ticker = alias_map[ticker]
            action = body.get("action", "BUY").upper()
            shares = float(body.get("shares", 1.0))
            use_margin = bool(body.get("use_margin", False))

            current_tick = controller.price_ticks[controller.current_tick_index]["global_second"] if controller.price_ticks else 1
            current_phase = controller.get_current_phase().phase_id

            try:
                client_price = float(body.get("price", 0.0))
                price = client_price if client_price > 0.0 else controller.current_prices.get(ticker, 0.0)
                if price <= 0.0:
                    price = controller.current_prices.get("Vintrumite", 144.70)
                ok = controller.engine.execute_order(
                    ticker=ticker,
                    action=action,
                    shares=shares,
                    price=price,
                    use_margin=use_margin,
                    current_tick=current_tick,
                    current_phase=current_phase,
                )
                if ok:
                    self._send_json({"status": "success", "message": f"{action} order executed successfully", "state": get_game_state_payload()})
                else:
                    self._send_json({"status": "error", "message": "Order rejected: Insufficient funds or invalid holdings", "state": get_game_state_payload()}, status=400)
            except Exception as e:
                self._send_json({"status": "error", "message": str(e)}, status=400)

        elif parsed.path == "/api/savings":
            action = body.get("action", "deposit")
            amount = float(body.get("amount", 0.0))
            if action == "deposit":
                ok = controller.engine.deposit_to_savings(amount)
            else:
                ok = controller.engine.withdraw_from_savings(amount)

            if ok:
                self._send_json({"status": "success", "state": get_game_state_payload()})
            else:
                self._send_json({"status": "error", "message": "Invalid savings transaction amount"}, status=400)

        elif parsed.path == "/api/repay_debt":
            amount = float(body.get("amount", 0.0))
            source = body.get("source", "bank")
            ok = controller.engine.repay_margin_debt(amount, from_source=source)
            if ok:
                self._send_json({"status": "success", "message": f"Repaid ${amount:,.2f} debt from {source}", "state": get_game_state_payload()})
            else:
                self._send_json({"status": "error", "message": "Repayment failed: check balance or debt amount", "state": get_game_state_payload()}, status=400)

        elif parsed.path == "/api/emergency_reserve":
            amount = float(body.get("amount", 0.0))
            ok = controller.engine.set_emergency_reserve(amount)
            if ok:
                self._send_json({"status": "success", "message": f"Emergency reserve set to ${amount:,.2f}", "state": get_game_state_payload()})
            else:
                self._send_json({"status": "error", "message": "Cannot set reserve higher than bank balance", "state": get_game_state_payload()}, status=400)

        elif parsed.path == "/api/transfer_to_trading":
            amount = float(body.get("amount", 0.0))
            ignore_reserve = bool(body.get("ignore_reserve", False))
            ok = controller.engine.withdraw_from_savings(amount, ignore_reserve=ignore_reserve)
            if ok:
                self._send_json({"status": "success", "message": f"Transferred ${amount:,.2f} to Trading Cash", "state": get_game_state_payload()})
            else:
                self._send_json({"status": "error", "message": "Transfer failed: insufficient unlocked bank balance", "state": get_game_state_payload()}, status=400)

        elif parsed.path == "/api/transfer_to_bank":
            amount = float(body.get("amount", 0.0))
            ok = controller.engine.deposit_to_savings(amount)
            if ok:
                self._send_json({"status": "success", "message": f"Transferred ${amount:,.2f} to Safe Haven Bank", "state": get_game_state_payload()})
            else:
                self._send_json({"status": "error", "message": "Transfer failed: insufficient trading cash", "state": get_game_state_payload()}, status=400)

        elif parsed.path == "/api/advance":
            result = controller.advance_phase()
            self._send_json({
                "status": "success",
                "phase_advanced": True,
                "liquidation_info": result.get("liquidation_info"),
                "state": get_game_state_payload(),
            })

        else:
            self.send_error(404, "Endpoint not found")

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


def run_server():
    with socketserver.TCPServer(("", PORT), SimulationRequestHandler) as httpd:
        print(f"Server started at http://localhost:{PORT}")
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()
