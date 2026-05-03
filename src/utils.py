"""
Shared helper functions for Network Intrusion Detection System
"""
from pathlib import Path
import joblib


def load_model(path):
    """Tải model từ file .pkl"""
    return joblib.load(Path(path))


def get_selected_features():
    """Trả về danh sách 18 đặc trưng được chọn để phát hiện xâm nhập"""
    return [
        'Destination Port', 'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets',
        'Total Length of Fwd Packets', 'Total Length of Bwd Packets', 'Fwd Packet Length Mean',
        'Bwd Packet Length Mean', 'Flow Bytes/s', 'Flow Packets/s',
        'Packet Length Mean', 'Packet Length Std', 'SYN Flag Count',
        'ACK Flag Count', 'FIN Flag Count', 'RST Flag Count',
        'PSH Flag Count', 'URG Flag Count'
    ]


def format_alert(attack_type, port):
    """Tạo chuỗi cảnh báo được định dạng"""
    return f"[ALERT] Suspicious traffic detected: {attack_type}. Destination Port: {port}."
