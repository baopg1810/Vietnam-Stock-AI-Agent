import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# 1. Load biến môi trường từ file .env
load_dotenv()

# Kiểm tra API Key (để báo lỗi rõ ràng nếu quên)
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("Chưa tìm thấy GOOGLE_API_KEY. Vui lòng kiểm tra file .env")

# 2. Các Import quan trọng của LangChain & Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import StructuredTool 

# 3. Import các hàm chức năng từ file tools.py
from tools import (
    get_company_info,
    get_stock_history,
    calculate_technical_indicators,
    get_major_shareholders,
    get_company_officers,
    get_subsidiaries,
)

# --- CẤU HÌNH AGENT ---

# Định nghĩa Tools để Agent hiểu cách sử dụng
tools = [
    StructuredTool.from_function(
        func=get_company_info,
        name="get_company_info",
        description="Tra cứu thông tin hồ sơ, tổng quan về một công ty dựa trên mã chứng khoán (ticker)."
    ),
    StructuredTool.from_function(
        func=get_stock_history,
        name="get_stock_history",
        description="Lấy dữ liệu giá lịch sử (Open, High, Low, Close, Volume). Input ngày format YYYY-MM-DD. Mặc định lấy 90 ngày nếu không có input."
    ),
    StructuredTool.from_function(
        func=calculate_technical_indicators,
        name="calculate_technical_indicators",
        description="Tính toán chỉ số kỹ thuật SMA hoặc RSI theo ngày (daily timeframe). Ví dụ: symbol='HPG', indicator='RSI', window_size=14. Lưu ý: 1m = 1 tháng, 1w = 1 tuần, 1d = 1 ngày."
    ),
    StructuredTool.from_function(
        func=get_major_shareholders,
        name="get_major_shareholders",
        description="Lấy danh sách cổ đông lớn (major shareholders) của một công ty theo mã chứng khoán."
    ),
    StructuredTool.from_function(
        func=get_company_officers,
        name="get_company_officers",
        description="Lấy danh sách ban lãnh đạo (officers) đang làm việc của một công ty theo mã chứng khoán."
    ),
    StructuredTool.from_function(
        func=get_subsidiaries,
        name="get_subsidiaries",
        description="Lấy danh sách các công ty con (subsidiaries) của một công ty theo mã chứng khoán."
    ),
]

# Khởi tạo LLM (Gemini)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
)

# Tạo agent với system message
system_message = (
    "Bạn là một chuyên gia phân tích chứng khoán tại Việt Nam. "
    "Nhiệm vụ của bạn là trả lời câu hỏi của nhà đầu tư dựa trên dữ liệu từ các tools. "
    "Sau khi có dữ liệu, hãy tóm tắt câu trả lời ngắn gọn, xúc tích bằng tiếng Việt. "
    "Nếu không tìm thấy dữ liệu, hãy nói rõ."
)

agent = create_agent(llm, tools, system_prompt=system_message)

# --- CẤU HÌNH API (FastAPI) ---
app = FastAPI(title="Vietnam Stock AI Agent")

class QuestionRequest(BaseModel):
    question: str

@app.post("/api/chat")
async def chat_endpoint(request: QuestionRequest):
    """
    API nhận câu hỏi và trả về câu trả lời của AI.
    """
    try:
        # Gọi Agent xử lý
        result = agent.invoke({"messages": [HumanMessage(content=request.question)]})
        # Lấy message cuối cùng từ kết quả
        last_message = result["messages"][-1].content
        return {"answer": last_message}
    except Exception as e:
        # In lỗi ra terminal để dễ debug
        print(f"Lỗi xử lý: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Chạy server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)