# Vietnam Stock AI Agent

Ứng dụng AI Agent phân tích chứng khoán Việt Nam sử dụng LangChain, Google Gemini và vnstock.

## Tính năng

- 🔍 Tra cứu thông tin công ty (hồ sơ, ban lãnh đạo, cổ đông, công ty con)
- 📊 Lấy dữ liệu giá lịch sử (OHLCV - Open, High, Low, Close, Volume)
- 📈 Tính toán chỉ số kỹ thuật (SMA, RSI)
- 🤖 Trả lời câu hỏi bằng tiếng Việt tự nhiên
- 🚀 API RESTful với FastAPI

## Yêu cầu hệ thống

- Python 3.8+
- Google API Key (Gemini)

## Cài đặt

### 1. Clone hoặc tải project về máy

### 2. Tạo virtual environment

```powershell
python -m venv venv_stock
```

### 3. Kích hoạt virtual environment

```powershell
.\venv_stock\Scripts\Activate.ps1
```

### 4. Cài đặt các thư viện

```powershell
pip install -r requirements.txt
```

### 5. Tạo file .env

Tạo file `.env` trong thư mục gốc với nội dung:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

Lấy API key tại: https://aistudio.google.com/app/apikey

## Cấu trúc project

```
Agent stock LLM/
├── main.py                 # Server FastAPI và cấu hình Agent
├── tools.py               # Các hàm công cụ (tools) cho Agent
├── test_agent.py          # Script kiểm thử Agent
├── requirements.txt       # Danh sách thư viện
├── .env                   # API keys 
├── README.md              # File hướng dẫn
└── venv_stock/            # Virtual environment
```

## Chạy ứng dụng

### Khởi động server

```powershell
python main.py
```

Server sẽ chạy tại: `http://localhost:8000`

### Kiểm thử Agent

```powershell
python test_agent.py
```

Kết quả test sẽ được lưu vào file CSV với format: `test_results_YYYYMMDD_HHMMSS.csv`


## Các câu hỏi mẫu

1. "Lấy dữ liệu OHLCV 10 ngày gần nhất HPG?"
2. "Lấy giá đóng của mã VCB từ đầu tháng 11 theo khung 1d?"
3. "Trong các mã BID, TCB và VCB mã nào có giá mở cửa thấp nhất trong 10 ngày qua?"
4. "Tổng khối lượng giao dịch (volume) của mã VIC trong vòng 1 tuần gần đây"
5. "So sánh khối lượng giao dịch của VIC với HPG trong 2 tuần gần đây"
7. "Danh sách ban lãnh đạo đang làm việc của VCB"
9. "Tính cho tôi SMA9 của mã VIC trong 2 tuần với timeframe 1d"
10. "Tính cho tôi RSI14 của TCB trong 1 tuần với timeframe 1m"

## Công nghệ sử dụng

- **LangChain**: Framework xây dựng AI Agent
- **LangGraph**: Quản lý workflow của Agent
- **Google Gemini 2.0**: Large Language Model
- **vnstock**: Thư viện lấy dữ liệu chứng khoán Việt Nam
- **FastAPI**: Web framework cho API
- **Uvicorn**: ASGI server



