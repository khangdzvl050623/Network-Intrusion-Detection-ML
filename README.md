# Network Intrusion Detection System (IDS) — ML-Based

> Phát hiện xâm nhập mạng sử dụng Machine Learning trên bộ dữ liệu CIC-IDS2017

## Thông tin nhóm

| Thành viên | Vai trò | Nhiệm vụ |
|---|---|---|
| **Nhóm trưởng** | Project Lead | Git setup, real-time deployment (`src/deploy.py`) |
| **Khang** | Data Analyst | EDA & Data Preprocessing (`notebooks/01_eda.ipynb`) |
| **Khánh** | ML Engineer | Preprocessing Pipeline (`notebooks/02_preprocessing.ipynb`) |
| **Kiệt** | ML Engineer | Model Training (`notebooks/03_models.ipynb`) |
| **Long** | Evaluator | Evaluation & Analysis (`notebooks/04_evaluation.ipynb`) |

---

## Cấu trúc dự án

```
Network-Intrusion-Detection-ML/
├── data/
│   ├── raw/                    # Đặt 8 file CSV của CIC-IDS2017 tại đây
│   └── processed/              # File đã xử lý (tự động tạo khi chạy notebook)
├── notebooks/
│   ├── 01_eda.ipynb            # [KHANG] EDA & Data Preprocessing
│   ├── 02_preprocessing.ipynb  # [KHANH] Handling Class Imbalance & Feature Selection
│   ├── 03_models.ipynb         # [KIỆT] Model Implementation & Comparison
│   └── 04_evaluation.ipynb     # [LONG] Model Evaluation & Best Model Selection
├── src/
│   ├── deploy.py               # [NHÓM TRƯỞNG] Real-time Alert Generation
│   └── utils.py                # Shared helper functions
├── models/                     # Saved .pkl model files
├── alerts.log                  # Alert log file
├── requirements.txt
└── README.md
```

---

## Dataset

Sử dụng bộ dữ liệu **CIC-IDS2017** (Canadian Institute for Cybersecurity).

**Tải dữ liệu tại:** https://www.unb.ca/cic/datasets/ids-2017.html

Đặt 8 file CSV vào thư mục `data/raw/`:
- `Monday-WorkingHours.pcap_ISCX.csv`
- `Tuesday-WorkingHours.pcap_ISCX.csv`
- `Wednesday-workingHours.pcap_ISCX.csv`
- `Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv`
- `Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv`
- `Friday-WorkingHours-Morning.pcap_ISCX.csv`
- `Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv`
- `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv`

---

## Cài đặt

```bash
# Tạo môi trường ảo
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Cài thư viện
pip install -r requirements.txt

# Khởi động Jupyter
jupyter notebook
```

---

## Quy trình chạy

Chạy các notebook theo thứ tự:

1. `notebooks/01_eda.ipynb` — Phân tích và làm sạch dữ liệu
2. `notebooks/02_preprocessing.ipynb` — Xử lý mất cân bằng, chọn đặc trưng
3. `notebooks/03_models.ipynb` — Huấn luyện 5 mô hình ML
4. `notebooks/04_evaluation.ipynb` — Đánh giá và lựa chọn mô hình tốt nhất

Sau khi huấn luyện xong, chạy hệ thống phát hiện xâm nhập real-time:

```bash
python src/deploy.py
```

---

## Các mô hình được sử dụng

| Mô hình | Thư viện |
|---|---|
| Logistic Regression | scikit-learn |
| Support Vector Machine | scikit-learn |
| Naive Bayes | scikit-learn |
| K-Nearest Neighbors | scikit-learn |
| Random Forest | scikit-learn |

---

## Kết quả kỳ vọng

- **Mô hình tốt nhất:** Random Forest
- **Đặc trưng được sử dụng:** 18 đặc trưng lưu lượng mạng chính
- **Hệ thống cảnh báo:** Real-time với ghi log vào `alerts.log`

---

## Giấy phép

Dự án học thuật — Môn An toàn Mạng / Machine Learning

---

*Built with scikit-learn, pandas, and CIC-IDS2017 dataset*
