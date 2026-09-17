#!/bin/bash
# ==============================================================================
# Script khởi chạy toàn bộ hệ thống SaleAI (Backend Django + Frontend React)
# ==============================================================================

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "⚡ Đang khởi động hệ thống SaleAI..."

# 1. Khởi động Backend Django
echo "🚀 Đang chạy Backend Django trên cổng 8000..."
cd "$PROJECT_DIR/backend"
if [ ! -d "venv" ]; then
    echo "Tạo venv và cài đặt thư viện..."
    python3 -m venv venv
    ./venv/bin/pip install -r requirements.txt
    ./venv/bin/python manage.py migrate
    ./venv/bin/python manage.py seed_products
fi

./venv/bin/python manage.py runserver 0.0.0.0:8000 &
BACKEND_PID=$!

# Đợi backend sẵn sàng
sleep 2

# 2. Khởi động Frontend React
echo "🌐 Đang chạy Frontend React trên cổng 5173..."
cd "$PROJECT_DIR/frontend"
npm run dev -- --port 5173 &
FRONTEND_PID=$!

# Đợi frontend sẵn sàng
sleep 2

# 3. Mở trình duyệt
echo "✨ Mở trình duyệt đến http://localhost:5173..."
open http://localhost:5173 2>/dev/null || true

echo ""
echo "=========================================================="
echo "🎉 HỆ THỐNG SALEAI ĐÃ SẴN SÀNG!"
echo "👉 Giao diện Khách Hàng & Quản Trị: http://localhost:5173"
echo "👉 Backend Django API:              http://localhost:8000/api/"
echo "👉 Django Admin:                    http://localhost:8000/admin/"
echo "=========================================================="
echo "Nhấn Ctrl+C để dừng cả 2 máy chủ."

# Dọn dẹp tiến trình khi nhấn Ctrl+C
trap "echo 'Đang tắt các dịch vụ...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" SIGINT SIGTERM
wait
