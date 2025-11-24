import requests
import json
import csv
from datetime import datetime

# URL của API
API_URL = "http://localhost:8000/api/chat"

# Danh sách câu hỏi test
test_questions = [
    "Lấy dữ liệu OHLCV 10 ngày gần nhất HPG?",
    "Lấy giá đóng của của mã VCB từ đầu tháng 11 năm nay theo khung 1d?",
    "Trong các mã BID, TCB và VCB mã nào có giá mở cửa thấp nhất trong 10 ngày qua",
    "Tổng khối lượng giao dịch (volume) của mã VIC trong vòng 10 ngày gần đây",
    "So sánh khối lượng giao dịch của VIC với HPG trong 2 tuần gần đây",
    "Danh sách ban lãnh đạo đang làm việc của VCB",
    "Tính cho tôi SMA9 của mã VIC với timeframe 1d",
    "Tính SMA9 và SMA20 của mã TCB"

]

def run_tests():
    print(f"--- Bắt đầu kiểm thử Agent tại {API_URL} ---")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"test_results_{timestamp}.csv"
    
    with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['question', 'answer'])  
        
        for i, question in enumerate(test_questions):
            print(f"\n[Test Case {i+1}]")
            print(f"Câu hỏi: {question}")
            
            try:
                payload = {"question": question}
                response = requests.post(API_URL, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get('answer', '')
                    print(f"Trả lời: {answer}")
                    print("-> Trạng thái: Thành công (200 OK)")
                    
                    writer.writerow([question, answer])
                else:
                    error_msg = f"Lỗi: {response.status_code} - {response.text}"
                    print(f"-> {error_msg}")
                    writer.writerow([question, error_msg])
                    
            except Exception as e:
                error_msg = f"Exception: {str(e)}"
                print(f"-> {error_msg}")
                writer.writerow([question, error_msg])
    
    print(f"\n--- Kết quả đã được lưu vào file: {csv_filename} ---")

if __name__ == "__main__":

    run_tests()


