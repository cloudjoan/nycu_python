import flask
from flask import Flask, request, jsonify, render_template_string
import threading
import time
import requests
import logging

# --- 全域變數：儲存機器人的狀態 ---
# 警告：在真實的應用中，您需要一個更穩健的資料庫來儲存狀態
bot_status = {
    "running": False,
    "symbol": "BTCUSDT",
    "profit_percentage": 1.0,  # 預設獲利 1%
    "buy_price": None,
    "last_price": None,
}

# 儲存日誌訊息以顯示在網頁上
bot_logs = []

# 線程鎖，用於安全地存取全域變數
status_lock = threading.Lock()
log_lock = threading.Lock()

# Flask App
app = Flask(__name__)

# 關閉 Flask 的預設日誌，以便我們自訂
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# --- 機器人日誌功能 ---
def add_log(message):
    """安全地新增日誌訊息"""
    global bot_logs
    print(message)  # 同時在控制台顯示
    with log_lock:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        bot_logs.append(f"[{timestamp}] {message}")
        # 保持日誌列表只顯示最新的 100 條
        if len(bot_logs) > 100:
            bot_logs = bot_logs[-100:]

# --- 模擬交易邏輯 ---
def get_binance_price(symbol):
    """
    使用幣安的公共 API 獲取即時價格。
    這不需要 API Key。
    """
    try:
        url = "https://api.binance.com/api/v3/ticker/price"
        params = {"symbol": symbol}
        response = requests.get(url, params=params)
        response.raise_for_status()  # 如果請求失敗，則引發異常
        data = response.json()
        return float(data['price'])
    except requests.RequestException as e:
        add_log(f"錯誤：無法獲取 {symbol} 價格: {e}")
        return None

def trading_bot_logic():
    """
    這是機器人執行緒的主體。
    它會持續執行，直到 "running" 狀態變為 False。
    """
    global bot_status
    add_log("交易機器人執行緒已啟動...")

    while True:
        # 讀取當前狀態
        with status_lock:
            if not bot_status["running"]:
                break  # 如果 "running" 為 False，則跳出迴圈
            
            current_symbol = bot_status["symbol"]
            profit_target = bot_status["profit_percentage"]
            current_buy_price = bot_status["buy_price"]
        
        # 獲取即時價格
        price = get_binance_price(current_symbol)
        if price is None:
            time.sleep(5)  # 如果獲取價格失敗，稍後重試
            continue
            
        with status_lock:
            bot_status["last_price"] = price

        # --- 模擬交易決策 ---
        if current_buy_price is None:
            # 狀態：尚未買入 -> 執行 "模擬買入"
            with status_lock:
                bot_status["buy_price"] = price
            add_log(f"模擬買入：在 ${price:.2f} 買入 {current_symbol}")
        
        else:
            # 狀態：已買入 -> 檢查是否達到獲利目標
            target_sell_price = current_buy_price * (1 + profit_target / 100)
            
            if price >= target_sell_price:
                # 達到獲利目標 -> 執行 "模擬賣出"
                profit = (price - current_buy_price) * 1  # 假設數量為 1
                add_log(f"✨ 模擬賣出：在 ${price:.2f} 賣出 {current_symbol}，獲利 ${profit:.2f}!")
                with status_lock:
                    bot_status["buy_price"] = None  # 賣出後重置買入價格
            else:
                # 尚未達到目標
                add_log(f"監控中... | 目前價格: ${price:.2f} | 目標賣價: ${target_sell_price:.2f}")

        # 迴圈間隔
        time.sleep(5) # 幣安 API 限制，不要請求太頻繁

    add_log("交易機器人執行緒已停止。")

# --- Flask Web 介面與 API ---

# 我們將 HTML, CSS, JS 寫在同一個 Python 字串中
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Binance 模擬交易機器人</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { font-family: 'Inter', 'Noto Sans TC', sans-serif; }
    </style>
</head>
<body class="bg-gray-900 text-gray-100 min-h-screen p-8">
    <div class="max-w-3xl mx-auto bg-gray-800 rounded-lg shadow-xl p-8">
        <h1 class="text-3xl font-bold mb-6 text-yellow-400">Binance 模擬交易機器人</h1>
        
        <!-- 狀態顯示 -->
        <div class="mb-6 p-4 bg-gray-700 rounded-lg">
            <h2 class="text-xl font-semibold mb-3">即時狀態</h2>
            <div class="grid grid-cols-2 gap-4">
                <div>狀態: 
                    <span id="status-running" class="font-bold text-lg px-3 py-1 rounded">--</span>
                </div>
                <div>交易對: <span id="status-symbol" class="font-bold text-lg">--</span></div>
                <div>目前價格: <span id="status-price" class="font-bold text-lg">--</span></div>
                <div>買入價格: <span id="status-buy-price" class="font-bold text-lg">--</span></div>
            </div>
        </div>

        <!-- 控制面板 -->
        <div class="mb-6">
            <h2 class="text-xl font-semibold mb-3">控制面板</h2>
            <div class="flex flex-col sm:flex-row gap-4">
                <div class="flex-1">
                    <label for="profit-percent" class="block text-sm font-medium text-gray-300">獲利百分比 (%)</label>
                    <input type="number" id="profit-percent" value="1.0" step="0.1" 
                           class="w-full mt-1 bg-gray-700 border-gray-600 rounded-md p-2 text-white focus:ring-yellow-500 focus:border-yellow-500">
                </div>
                <button id="btn-start" onclick="startBot()" class="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 rounded-lg self-end">
                    啟動機器人
                </button>
                <button id="btn-stop" onclick="stopBot()" class="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-6 rounded-lg self-end">
                    停止機器人
                </button>
            </div>
        </div>

        <!-- 日誌輸出 -->
        <div>
            <h2 class="text-xl font-semibold mb-3">日誌輸出</h2>
            <pre id="log-output" class="bg-gray-900 text-sm text-gray-300 p-4 rounded-md h-64 overflow-y-auto font-mono">
等待機器人啟動...
            </pre>
        </div>
    </div>

    <script>
        // 啟動機器人
        async function startBot() {
            const profitPercentage = document.getElementById('profit-percent').value;
            if (!profitPercentage || parseFloat(profitPercentage) <= 0) {
                alert('請輸入一個有效的獲利百分比 ( > 0 )');
                return;
            }
            
            try {
                const response = await fetch('/api/start', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ profit_percentage: parseFloat(profitPercentage) })
                });
                const data = await response.json();
                alert(data.message);
                updateStatus();
            } catch (error) {
                console.error('啟動失敗:', error);
                alert('啟動機器人失敗');
            }
        }

        // 停止機器人
        async function stopBot() {
            try {
                const response = await fetch('/api/stop', { method: 'POST' });
                const data = await response.json();
                alert(data.message);
                updateStatus();
            } catch (error) {
                console.error('停止失敗:', error);
                alert('停止機器人失敗');
            }
        }

        // 更新狀態顯示
        async function updateStatus() {
            try {
                const response = await fetch('/api/status');
                const status = await response.json();

                const statusEl = document.getElementById('status-running');
                if (status.running) {
                    statusEl.textContent = '運行中';
                    statusEl.className = 'font-bold text-lg px-3 py-1 rounded bg-green-600';
                } else {
                    statusEl.textContent = '已停止';
                    statusEl.className = 'font-bold text-lg px-3 py-1 rounded bg-red-600';
                }
                
                document.getElementById('status-symbol').textContent = status.symbol;
                document.getElementById('profit-percent').value = status.profit_percentage;
                
                document.getElementById('status-price').textContent = status.last_price ? `$${status.last_price.toFixed(2)}` : '--';
                document.getElementById('status-buy-price').textContent = status.buy_price ? `$${status.buy_price.toFixed(2)}` : 'N/A';

            } catch (error) {
                console.error('更新狀態失敗:', error);
            }
        }

        // 更新日誌
        async function updateLogs() {
            try {
                const response = await fetch('/api/logs');
                const data = await response.json();
                const logBox = document.getElementById('log-output');
                logBox.textContent = data.logs.join('\\n');
                logBox.scrollTop = logBox.scrollHeight; // 自動捲動到底部
            } catch (error) {
                console.error('更新日誌失敗:', error);
            }
        }

        // 頁面載入時和之後定期更新
        document.addEventListener('DOMContentLoaded', () => {
            updateStatus();
            updateLogs();
            setInterval(updateStatus, 3000); // 每 3 秒更新一次狀態
            setInterval(updateLogs, 2000);   // 每 2 秒更新一次日誌
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """提供網頁介面"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/start', methods=['POST'])
def api_start_bot():
    """API: 啟動機器人"""
    global bot_status
    data = request.json
    
    with status_lock:
        if bot_status["running"]:
            return jsonify({"message": "機器人已經在運行中"}), 400
        
        # 設定新的獲利百分比
        bot_status["profit_percentage"] = data.get('profit_percentage', 1.0)
        bot_status["running"] = True
        bot_status["buy_price"] = None # 重置買入價
        
        # 啟動機器人執行緒
        # 使用 daemon=True 讓執行緒在主程式結束時自動結束
        bot_thread = threading.Thread(target=trading_bot_logic, daemon=True)
        bot_thread.start()
        
        add_log(f"機器人已啟動，目標獲利: {bot_status['profit_percentage']}%")
        
    return jsonify({"message": "機器人已成功啟動"})

@app.route('/api/stop', methods=['POST'])
def api_stop_bot():
    """API: 停止機器人"""
    global bot_status
    
    with status_lock:
        if not bot_status["running"]:
            return jsonify({"message": "機器人尚未啟動"}), 400
            
        bot_status["running"] = False # 觸發執行緒停止
        
    add_log("正在停止機器人...")
    return jsonify({"message": "機器人已成功停止"})

@app.route('/api/status')
def api_status():
    """API: 獲取機器人當前狀態"""
    with status_lock:
        # 建立一個安全的副本以傳送
        safe_status = bot_status.copy()
        
    return jsonify(safe_status)

@app.route('/api/logs')
def api_logs():
    """API: G獲取日誌"""
    with log_lock:
        # 建立一個安全的副本
        logs_copy = list(bot_logs)
        
    return jsonify({"logs": logs_copy})


# --- 程式主入口 ---
if __name__ == '__main__':
    print("======================================================")
    print("  Binance 模擬交易機器人已啟動")
    print("  請在瀏覽器中開啟: http://127.0.0.1:5000")
    print("  警告：本程式僅為模擬，請勿用於真實交易。")
    print("======================================================")
    app.run(host='127.0.0.1', port=5000)
