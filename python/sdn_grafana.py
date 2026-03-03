import requests
import time
from requests.auth import HTTPBasicAuth
from prometheus_client import start_http_server, Gauge

# --- CẤU HÌNH ODL CONTROLLER ---
ODL_IP = "127.0.0.1"
ODL_PORT = "8181"
AUTH = HTTPBasicAuth('admin', 'admin')
HEADERS = {'Accept': 'application/json'}

# --- KHỞI TẠO BIỂU ĐỒ PROMETHEUS (METRICS) ---
# Biến Gauge dùng để đo lường các giá trị có thể tăng/giảm (như tốc độ mạng)
TX_GAUGE = Gauge('sdn_tx_bandwidth_mbps', 'Tốc độ gửi của Switch (Mbps)', ['link_name'])
RX_GAUGE = Gauge('sdn_rx_bandwidth_mbps', 'Tốc độ nhận của Switch (Mbps)', ['link_name'])

def get_port_statistics(node_id, port_num):
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
    print("🚀 Khởi động máy chủ trạm phát Prometheus Exporter...")
    
    # Mở cổng 8000 để Prometheus gọi đến lấy số liệu
    start_http_server(8000) 
    print("✅ Đã mở cổng 8000. Đang liên tục đẩy dữ liệu lên Grafana...")
    
    # Đặt tên link không có dấu cách để Grafana dễ đọc
    MONITOR_LINKS = [
        {"node": "openflow:1", "port": "1", "name": "Core_to_Aggr1"},
        {"node": "openflow:1", "port": "2", "name": "Core_to_Aggr2"}
    ]
    
    prev_data = {}
    for link in MONITOR_LINKS:
        tx, rx = get_port_statistics(link["node"], link["port"])
        prev_data[link["name"]] = {"tx": tx, "rx": rx}
            
    while True:
        time.sleep(3)
        for link in MONITOR_LINKS:
            link_name = link["name"]
            curr_tx, curr_rx = get_port_statistics(link["node"], link["port"])
            
            # Tính toán Mbps
            tx_mbps = ((curr_tx - prev_data[link_name]["tx"]) * 8) / (1024 * 1024 * 3)
            rx_mbps = ((curr_rx - prev_data[link_name]["rx"]) * 8) / (1024 * 1024 * 3)
            
            # 🌟 ĐIỂM ĂN TIỀN LÀ ĐÂY: Cập nhật số liệu vào biến Prometheus
            TX_GAUGE.labels(link_name=link_name).set(tx_mbps)
            RX_GAUGE.labels(link_name=link_name).set(rx_mbps)
            
            print(f"[{link_name}] Đã đẩy -> Gửi: {tx_mbps:.2f} Mbps | Nhận: {rx_mbps:.2f} Mbps")
            
            prev_data[link_name] = {"tx": curr_tx, "rx": curr_rx}
