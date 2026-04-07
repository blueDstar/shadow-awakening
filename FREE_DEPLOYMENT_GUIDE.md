# 🌑 Hướng Dẫn Deploy Miễn Phí (Vercel + Render + Neon)

Vì Railway đã hết hạn, đây là cách kết hợp 3 dịch vụ miễn phí tốt nhất để hệ thống **Shadow Awakening** của bạn chạy 24/7.

---

## 💎 Bước 1: Tạo Database PostgreSQL trên [Neon.tech](https://neon.tech/)
Neon là dịch vụ chuyên về Database PostgreSQL, miễn phí và rất mạnh mẽ.

1. Đăng ký tài khoản Neon.tech.
2. Tạo project mới (ví dụ: `shadow-db`).
3. Copy link **Connection String** (Dạng `postgresql://user:password@endpoint/dbname`).
4. **Lưu ý:** Để dùng với FastAPI (async), hãy đổi đầu link thành `postgresql+asyncpg://`.

---

## 🐍 Bước 2: Deploy Backend FastAPI lên [Render.com](https://render.com/)
Render là nơi chạy code Python (Backend) của bạn.

1. Đăng nhập Render bằng GitHub.
2. Chọn **New** -> **Web Service**.
3. Kết nối với repo `shadow-awakening`.
4. Cấu hình:
    - **Name:** `shadow-awakening-api`
    - **Root Directory:** `backend`
    - **Runtime:** `Python 3`
    - **Build Command:** `pip install -r requirements.txt`
    - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Thêm **Environment Variables** (Nút Advanced):
    - `DATABASE_URL`: (Dán link từ Neon vào).
    - `SECRET_KEY`: (Chuỗi bí mật của bạn).
    - `CORS_ORIGINS`: `*`
6. Đợi Render deploy xong, bạn sẽ có link Backend (vd: `https://shadow-api.onrender.com`).

---

## ⚛️ Bước 3: Deploy Frontend React lên [Vercel.com](https://vercel.com/)
Vercel là nơi tốt nhất để chạy giao diện web.

1. Đăng nhập Vercel bằng GitHub.
2. Chọn **Add New** -> **Project**.
3. Cấu hình:
    - **Framework Preset:** `Vite`
    - **Root Directory:** `frontend`
    - **Environment Variables:**
        - `VITE_API_URL`: (Dán link Backend từ Render vào).
4. Nhấn **Deploy**. Sau 1 phút bạn sẽ có link web chính thức!

---

## 🛠️ Quy trình cập nhật Code
Mỗi khi bạn sửa code và `git push` lên GitHub:
1. **Vercel** sẽ tự động thấy và cập nhật lại Frontend.
2. **Render** sẽ tự động thấy và cập nhật lại Backend.
3. Mọi thứ hoàn toàn tự động!

---

### ⚠️ Lưu ý về Render (Free Tier):
Render bản miễn phí sẽ tự tắt nếu không có ai truy cập trong 15 phút. Khi bạn mở web lên lại, có thể sẽ mất 30-40 giây chờ đợi để nó "tỉnh dậy". Đây là đánh đổi để có dịch vụ miễn phí hoàn toàn.
