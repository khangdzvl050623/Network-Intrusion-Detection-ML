"""
[NHÓM TRƯỞNG] Real-time Alert Generation
Hệ thống phát hiện xâm nhập mạng real-time sử dụng Random Forest
"""
import sys
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from utils import load_model, get_selected_features, format_alert

MODELS_DIR = ROOT / "models"
ALERTS_LOG = ROOT / "alerts.log"


def _load_artifacts():
    rf = load_model(MODELS_DIR / "random_forest.pkl")
    scaler = load_model(MODELS_DIR / "scaler.pkl")
    le = load_model(MODELS_DIR / "label_encoder.pkl")
    return rf, scaler, le


def simulate_realtime_flow(flow_dict, model=None, scaler=None, label_encoder=None):
    """
    Phân loại một luồng mạng và phát cảnh báo nếu phát hiện tấn công.
    flow_dict: dict với 18 đặc trưng + 'Destination Port' (tùy chọn)
    """
    if model is None or scaler is None or label_encoder is None:
        model, scaler, label_encoder = _load_artifacts()

    features = get_selected_features()
    port = flow_dict.get("Destination Port", "N/A")

    row = {f: flow_dict.get(f, 0) for f in features}
    df = pd.DataFrame([row])[features]

    df_scaled = scaler.transform(df)
    pred_idx = model.predict(df_scaled)[0]
    pred_label = label_encoder.inverse_transform([pred_idx])[0]

    if pred_label != "BENIGN":
        alert_msg = format_alert(pred_label, port)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] {alert_msg}"
        print(log_line)
        with open(ALERTS_LOG, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")
    else:
        print(f"[INFO] Traffic classified as: BENIGN. No action taken.")

    return pred_label


if __name__ == "__main__":
    print("=" * 60)
    print("[NHÓM TRƯỞNG] Network IDS — Real-time Demo")
    print("=" * 60)

    # Tải artifacts một lần để tái sử dụng
    model, scaler, label_encoder = _load_artifacts()

    # Luồng 1: BENIGN — lưu lượng bình thường
    flow_benign = {
        "Destination Port": 443,
        "Flow Duration": 50000,
        "Total Fwd Packets": 5,
        "Total Backward Packets": 4,
        "Total Length of Fwd Packets": 500,
        "Total Length of Bwd Packets": 400,
        "Fwd Packet Length Mean": 100.0,
        "Bwd Packet Length Mean": 100.0,
        "Flow Bytes/s": 180.0,
        "Flow Packets/s": 1.8,
        "Packet Length Mean": 100.0,
        "Packet Length Std": 5.0,
        "SYN Flag Count": 1,
        "ACK Flag Count": 8,
        "FIN Flag Count": 1,
        "RST Flag Count": 0,
        "PSH Flag Count": 3,
        "URG Flag Count": 0,
    }

    # Luồng 2: DDoS-like — lưu lượng có đặc trưng tấn công DDoS
    flow_ddos = {
        "Destination Port": 80,
        "Flow Duration": 1000,
        "Total Fwd Packets": 5000,
        "Total Backward Packets": 0,
        "Total Length of Fwd Packets": 370000,
        "Total Length of Bwd Packets": 0,
        "Fwd Packet Length Mean": 74.0,
        "Bwd Packet Length Mean": 0.0,
        "Flow Bytes/s": 370000000.0,
        "Flow Packets/s": 5000000.0,
        "Packet Length Mean": 74.0,
        "Packet Length Std": 0.0,
        "SYN Flag Count": 0,
        "ACK Flag Count": 0,
        "FIN Flag Count": 0,
        "RST Flag Count": 0,
        "PSH Flag Count": 0,
        "URG Flag Count": 0,
    }

    # Luồng 3: PortScan-like — quét cổng
    flow_portscan = {
        "Destination Port": 22,
        "Flow Duration": 0,
        "Total Fwd Packets": 1,
        "Total Backward Packets": 0,
        "Total Length of Fwd Packets": 0,
        "Total Length of Bwd Packets": 0,
        "Fwd Packet Length Mean": 0.0,
        "Bwd Packet Length Mean": 0.0,
        "Flow Bytes/s": 0.0,
        "Flow Packets/s": 0.0,
        "Packet Length Mean": 0.0,
        "Packet Length Std": 0.0,
        "SYN Flag Count": 1,
        "ACK Flag Count": 0,
        "FIN Flag Count": 0,
        "RST Flag Count": 1,
        "PSH Flag Count": 0,
        "URG Flag Count": 0,
    }

    sample_flows = [
        ("BENIGN flow", flow_benign),
        ("DDoS-like flow", flow_ddos),
        ("PortScan-like flow", flow_portscan),
    ]

    alert_count = 0
    print()
    for name, flow in sample_flows:
        print(f"--- Testing: {name} ---")
        result = simulate_realtime_flow(flow, model, scaler, label_encoder)
        if result != "BENIGN":
            alert_count += 1
        print()

    print("=" * 60)
    print(f"Demo complete. Alerts generated: {alert_count}/{len(sample_flows)}")
    print(f"Alert log: {ALERTS_LOG}")
    print("=" * 60)
