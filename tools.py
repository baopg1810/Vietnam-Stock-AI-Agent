import pandas as pd
from datetime import datetime, timedelta

def get_company_info(symbol: str):
    """
    Tra cứu thông tin cơ bản của doanh nghiệp dựa trên mã chứng khoán.
    """
    try:
        from vnstock import Vnstock
        stock = Vnstock().stock(symbol=symbol, source='VCI')
        profile = stock.company.profile(symbol=symbol)
        if profile is None or profile.empty:
            return f"Không tìm thấy thông tin cho mã {symbol}."
        return profile.to_string()
    except Exception as e:
        return f"Lỗi khi lấy thông tin công ty {symbol}: {str(e)}"

def get_stock_history(symbol: str, start_date: str = None, end_date: str = None, days_ago: int = 90):
    """
    Lấy dữ liệu giá lịch sử (Open, High, Low, Close, Volume).
    Mặc định lấy 90 ngày gần nhất nếu không nhập ngày.
    Date format: YYYY-MM-DD.
    """
    try:
        from vnstock import Vnstock
        stock = Vnstock().stock(symbol=symbol, source='VCI')
        
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if not start_date:
            start_date_obj = datetime.now() - timedelta(days=days_ago)
            start_date = start_date_obj.strftime("%Y-%m-%d")

        df = stock.quote.history(symbol=symbol, start=start_date, end=end_date)
        
        if df is None or df.empty:
            return f"Không có dữ liệu giá cho {symbol} từ {start_date} đến {end_date}."
        
        # Chỉ lấy các cột quan trọng để tiết kiệm token cho LLM
        return df[['time', 'open', 'high', 'low', 'close', 'volume']].to_string()
    except Exception as e:
        return f"Lỗi khi lấy lịch sử giá {symbol}: {str(e)}"

def calculate_technical_indicators(symbol: str, indicator: str, window_size: int = 14):
    """
    Tính toán chỉ số kỹ thuật SMA hoặc RSI.
    """
    try:
        from vnstock import Vnstock
        stock = Vnstock().stock(symbol=symbol, source='VCI')
        
        # Lấy dữ liệu đủ dài (180 ngày) để đảm bảo đủ window tính toán
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
        
        df = stock.quote.history(symbol=symbol, start=start_date, end=end_date)
        
        if df is None or df.empty:
            return "Không đủ dữ liệu để tính toán."

        df['close'] = pd.to_numeric(df['close'])
        
        if indicator.upper() == "SMA":
            sma = df['close'].rolling(window=window_size).mean()
            current_sma = sma.iloc[-1]
            return f"SMA({window_size}) hiện tại của {symbol} là: {current_sma:.2f}"
            
        elif indicator.upper() == "RSI":
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=window_size).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=window_size).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = rsi.iloc[-1]
            return f"RSI({window_size}) hiện tại của {symbol} là: {current_rsi:.2f}"
        
        return "Chỉ hỗ trợ SMA hoặc RSI."
    except Exception as e:
        return f"Lỗi tính toán: {str(e)}"

def get_major_shareholders(symbol: str):
    """
    Lấy danh sách cổ đông lớn của công ty.
    Trả về chuỗi (string) để agent dễ sử dụng.
    """
    try:
        from vnstock import Vnstock
        stock = Vnstock().stock(symbol=symbol, source='VCI')
        # vnstock API: company.shareholders(...) -> DataFrame
        shareholders = stock.company.shareholders(symbol=symbol)
        if shareholders is None or getattr(shareholders, 'empty', False):
            return f"Không tìm thấy thông tin cổ đông cho mã {symbol}."
        return shareholders.to_string()
    except Exception as e:
        return f"Lỗi khi lấy danh sách cổ đông {symbol}: {str(e)}"


def get_company_officers(symbol: str):
    """
    Lấy danh sách ban lãnh đạo đang làm việc của công ty.
    """
    try:
        from vnstock import Vnstock
        stock = Vnstock().stock(symbol=symbol, source='VCI')
        officers = stock.company.officers(symbol=symbol)
        if officers is None or getattr(officers, 'empty', False):
            return f"Không tìm thấy thông tin ban lãnh đạo cho mã {symbol}."
        return officers.to_string()
    except Exception as e:
        return f"Lỗi khi lấy danh sách ban lãnh đạo {symbol}: {str(e)}"


def get_subsidiaries(symbol: str):
    """
    Lấy danh sách các công ty con của công ty.
    """
    try:
        from vnstock import Vnstock
        stock = Vnstock().stock(symbol=symbol, source='VCI')
        subsidiaries = stock.company.subsidiaries(symbol=symbol)
        if subsidiaries is None or getattr(subsidiaries, 'empty', False):
            return f"Không tìm thấy thông tin công ty con cho mã {symbol}."
        return subsidiaries.to_string()
    except Exception as e:
        return f"Lỗi khi lấy danh sách công ty con {symbol}: {str(e)}"