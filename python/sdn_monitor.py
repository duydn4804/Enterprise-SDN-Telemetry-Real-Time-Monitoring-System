import requests
import time
from requests.auth import HTTPBasicAuth

# --- CẤU HÌNH ODL CONTROLLER ---
ODL_IP = "127.0.0.1"
ODL_PORT = "8181"
AUTH = HTTPBasicAuth('admin', 'admin')
HEADERS = {'Accept': 'application/json'}

# --- CẤU HÌNH BOT TELEGRAM CỦA BẠN ---
TELEGRAM_TOKEN = "8622379403:AAHDwfwebHOQpEmeBYmnVFFk3O-QAtqlVlU"
TELEGRAM_CHAT_ID = "6051010150"

def send_telegram_alert(message):
    """Hàm bắn tin nhắn cảnh báo về Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print("[-] Lỗi không gửi được Telegram:", e)

def get_port_statistics(node_id, port_num):
    """Hàm lấy dữ liệu băng thông từ Core Switch"""
    port_id = f"{node_id}:{port_num}"
    url = f"http://{ODL_IP}:{ODL_PORT}/restconf/operational/opendaylight-inventory:nodes/node/{node_id}/node-connector/{port_id}"
    
    try:
        res = requests.get(url, headers=HEADERS, auth=AUTH)
        if res.status_code == 200:
            data = res.json()
            stats = data['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']
            return stats['bytes']['transmitted'], stats['bytes']['received']
    except Exception:
        pass
    return 0, 0

if __name__ == "__main__":
    print("🚀 Bắt đầu hệ thống SDN Telemetry & Telegram ChatOps...")
    
    MONITOR_LINKS = [
        {"node": "openflow:1", "port": "1", "name": "Core -> Aggr1 (Nhánh Trái)"},
        {"node": "openflow:1", "port": "2", "name": "Core -> Aggr2 (Nhánh Phải)"}
    ]
    
    prev_data = {}
    for link in MONITOR_LINKS:
        tx, rx = get_port_statistics(link["node"], link["port"])
        prev_data[link["name"]] = {"tx": tx, "rx": rx}
        
    print("📲 Đang gửi tin nhắn khởi động về Telegram...")
    send_telegram_alert("🟢 <b>SDN Telemetry</b>: Hệ thống giám sát mạng đã KHỞI ĐỘNG!")
        
    try:
        while True:
            time.sleep(3)
            print(f"\n🕒 Cập nhật lúc: {time.strftime('%H:%M:%S')} " + "-"*40)
            
            for link in MONITOR_LINKS:
                link_name = link["name"]
                curr_tx, curr_rx = get_port_statistics(link["node"], link["port"])
                
                tx_mbps = ((curr_tx - prev_data[link_name]["tx"]) * 8) / (1024 * 1024 * 3)
                rx_mbps = ((curr_rx - prev_data[link_name]["rx"]) * 8) / (1024 * 1024 * 3)
                
                # ĐÃ HẠ NGƯỠNG XUỐNG 5.0 Mbps
                if tx_mbps > 80.0 or rx_mbps > 80.0:
                    alert_msg = f"🚨 <b>CẢNH BÁO QUÁ TẢI MẠNG!</b>\n\n📍 <b>Vị trí:</b> {link_name}\n📤 <b>Gửi:</b> {tx_mbps:.2f} Mbps\n📥 <b>Nhận:</b> {rx_mbps:.2f} Mbps\n⚠️ <i>Vui lòng kiểm tra hệ thống ngay lập tức!</i>"
                    print(f"🔥 [QUÁ TẢI] {link_name:<25} | Gửi: {tx_mbps:>6.2f} Mbps | Nhận: {rx_mbps:>6.2f} Mbps")
                    send_telegram_alert(alert_msg)
                else:
                    print(f"✅ [ỔN ĐỊNH] {link_name:<25} | Gửi: {tx_mbps:>6.2f} Mbps | Nhận: {rx_mbps:>6.2f} Mbps")
                    
                prev_data[link_name] = {"tx": curr_tx, "rx": curr_rx}
                
    except KeyboardInterrupt:
        # Bắt sự kiện khi bạn bấm Ctrl + C để tắt tool
        print("\n🛑 Phát hiện lệnh tắt hệ thống (Ctrl+C).")
        print("📲 Đang gửi tin nhắn tắt hệ thống về Telegram...")
        send_telegram_alert("🔴 <b>SDN Telemetry</b>: Hệ thống giám sát mạng đã bị ĐÓNG!")
        print("👋 Đã tắt an toàn. Tạm biệt!")
