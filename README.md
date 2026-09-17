# SaleAI • Trợ Lý Bán Hàng & Chốt Đơn Tự Động Bằng Google Gemini AI

Hệ thống AI Sales Rep thông minh tích hợp **Google Gemini**, hỗ trợ đa ngôn ngữ (**Tiếng Việt 🇻🇳 & Tiếng Lào 🇱🇦 - ພາສາລາວ**), tự động tư vấn bán hàng chuyên sâu theo tâm lý khách hàng, xử lý từ chối, tự động kích hoạt chốt đơn qua Function Calling và gửi email thông báo chi tiết đến chủ shop ngay lập tức.

---

## 🏗️ Kiến Trúc Hệ Thống (Architecture)

- **Backend**: Python 3.12, Django 5.x, Django REST Framework, CORS Headers, Gunicorn.
- **AI Core**: Google Gemini (`google-genai` SDK), Function Calling (`create_order`, `get_product_details`), Context Memory đa lượt, Smart Sales Fallback Engine.
- **Frontend**: React, Vite, Lucide Icons, Glassmorphism UI, Responsive Mobile/Desktop, Bảng điều khiển nạp dữ liệu sản phẩm và quản lý đơn hàng.
- **DevOps & Deployment**: Docker, Docker Compose, Nginx Reverse Proxy, GitHub Actions CI/CD.

---

## 🚀 Khởi Chạy Nhanh (Quick Start)

### Cách 1: Chạy Bằng Docker Compose (Khuyên Dùng)

```bash
# 1. Clone repository
git clone https://github.com/meodiemvuong1609/sale-ai.git
cd sale-ai

# 2. Cấu hình file môi trường
cp backend/.env.example backend/.env
# Thêm GEMINI_API_KEY vào file backend/.env (nếu có)

# 3. Khởi chạy toàn bộ hệ thống bằng Docker
docker compose up -d --build
```

- 🌐 **Frontend (Giao diện người dùng & quản trị)**: [http://localhost:3000](http://localhost:3000)
- 🚀 **Backend API**: [http://localhost:8000/api/](http://localhost:8000/api/)
- ⚙️ **Django Admin**: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

### Cách 2: Chạy Trực Tiếp Trên Máy (Local Machine)

Hệ thống đã có sẵn script khởi động 1-click:

```bash
./run.sh
```

- Frontend Vite: [http://localhost:5173](http://localhost:5173)
- Backend Django: [http://localhost:8000/api/](http://localhost:8000/api/)

---

## 🌟 Tính Năng Nổi Bật

1. **Giao Tiếp Bán Hàng Đời Thực**:
   - Xưng hô "Em" - "Anh/Chị" tự nhiên, câu ngắn 2-4 câu súc tích như nhân viên tư vấn trên Zalo/Messenger.
   - Tập trung trực diện vào câu hỏi khách hàng (độ ồn, diện tích, vật nuôi, em bé, giá cả...).
2. **Hỗ Trợ Song Ngữ Việt - Lào**:
   - Chuyển đổi ngôn ngữ tức thì giữa 🇻🇳 Tiếng Việt và 🇱🇦 ພາສາລາວ trên giao diện.
   - Gemini giao tiếp tiếng Lào tự nhiên, nhận diện địa chỉ tại Lào và chốt đơn tự động.
3. **Nạp Dữ Liệu Sản Phẩm & USP**:
   - Giao diện thêm/sửa/xóa sản phẩm, điểm bán hàng USP và FAQ để AI học và chốt đơn.
4. **Tự Động Gửi Email Thông Báo**:
   - Render HTML email chuyên nghiệp gửi ngay cho chủ shop kèm nút gọi điện thoại nhanh khi có đơn hàng mới.

---

## 🔄 Quy Trình CI/CD (GitHub Actions)

Mỗi lần push code hoặc tạo Pull Request lên nhánh `master`:
1. **Backend Checks**: Kiểm tra cú pháp, migrations và dữ liệu seed mẫu.
2. **Frontend Checks**: Cài đặt dependencies và kiểm tra build bundle Vite.
3. **Docker Build Check**: Kiểm tra build các Docker Images của Backend & Frontend.

---

## 📄 Bản Quyền & Giấy Phép
Dự án được phát triển phục vụ mục đích thương mại điện tử hội thoại và ứng dụng AI trong bán hàng.
