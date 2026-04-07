# 🚀 Hướng Dẫn Đẩy Code Lên GitHub và Deploy Lên Railway

Tài liệu này hướng dẫn bạn từng bước cách đưa dự án **Shadow Awakening** từ máy cá nhân lên GitHub và triển khai (deploy) lên Railway để có link truy cập công khai.

---

## 🛠️ Giai Đoạn 1: Chuẩn Bị và Đẩy Code Lên GitHub

### 1. Tạo File `.gitignore` (Rất Quan Trọng)
Bạn cần ngăn không cho Git tải các thư mục rác hoặc file chứa mật khẩu lên GitHub.

**Tại thư mục gốc (`Shadow_awakening/`), tạo file `.gitignore`:**
```text
# Python
backend/venv/
backend/__pycache__/
backend/*.pyc
backend/.env

# Node.js
frontend/node_modules/
frontend/dist/
frontend/.env
frontend/.env.local

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

### 2. Đẩy Code Lên GitHub
1. Truy cập [github.com](https://github.com/) và tạo một repository mới (ví dụ: `shadow-awakening`).
2. Mở Terminal (PowerShell/CMD) tại thư mục `Shadow_awakening/`:
```bash
# Khởi tạo Git
git init

# Thêm tất cả file
git add .

# Commit lần đầu
git commit -m "Initial commit: Shadow Awakening Dark Fantasy App"

# Kết nối với GitHub (thay URL bằng link repo của bạn)
git remote add origin https://github.com/TEN_USER_CUA_BAN/shadow-awakening.git

# Đẩy code lên
git branch -M main
git push -u origin main
```

---

## 🚂 Giai Đoạn 2: Triển Khai Lên Railway

### 1. Tạo Project và Database
1. Đăng nhập [railway.app](https://railway.app/).
2. Chọn **New Project** -> **Provision PostgreSQL**.
3. Sau khi tạo xong Database, chọn **New** -> **GitHub Repo** -> Chọn repo `shadow-awakening`.
4. Railway sẽ hỏi bạn muốn deploy thư mục nào? Vì chúng ta có 2 phần (Backend & Frontend), chúng ta sẽ tạo **2 Service**.

### 2. Cấu Hình Backend (FastAPI)
1. Trong Project trên Railway, nhấn vào Service vừa tạo từ GitHub.
2. Tại tab **Settings**:
    - **Root Directory**: Đổi thành `backend`.
3. Tại tab **Variables**, thêm các biến sau:
    - `DATABASE_URL`: (Railway thường tự điền, nếu không hãy lấy từ service PostgreSQL của Railway).
      *Lưu ý: Đổi `postgresql://` thành `postgresql+asyncpg://` nếu dùng async.*
    - `SECRET_KEY`: Nhập một chuỗi ký tự ngẫu nhiên (vd: `dark_fantasy_secret_2024`).
    - `ALGORITHM`: `HS256`.
    - `CORS_ORIGINS`: `*` (Hoặc link frontend của bạn sau khi deploy).
    - `PORT`: `8000`.

### 3. Cấu Hình Frontend (React/Vite)
1. Nhấn **New** -> **GitHub Repo** -> Chọn lại repo `shadow-awakening` một lần nữa (để tạo service thứ 2).
2. Tại tab **Settings**:
    - **Service Name**: Đổi thành `frontend`.
    - **Root Directory**: Đổi thành `frontend`.
3. Tại tab **Variables**, thêm:
    - `VITE_API_BASE_URL`: Nhập URL Public của Backend (Lấy ở tab *Networking* của Service Backend). *Ví dụ: `https://backend-production-xyz.up.railway.app`*

---

## 🔗 Các Bước Kiểm Tra Sau Khi Deploy

### 1. Kiểm Tra Database
- Bạn có thể dùng tab **Data** trong service PostgreSQL trên Railway để xem các bảng đã được tạo chưa. 
- Nếu chưa có bảng, bạn có thể chạy lệnh `alembic upgrade head` trên Railway (qua tab Deployment -> Custom Command) hoặc import file SQL trực tiếp.

### 2. Cấp Quyền CORS
- Đảm bảo Backend có biến `CORS_ORIGINS` chứa link URL của Frontend để Frontend có thể gửi yêu cầu API.

### 3. Truy Cập Link
- Link Backend: `https://your-backend.up.railway.app/docs` (Để kiểm tra API).
- Link Frontend: `https://your-frontend.up.railway.app` (Để chơi game).

---

## 🔥 Lưu Ý Về Chi Phí (Railway)
- Railway cung cấp gói dùng thử miễn phí hoặc gói Hobby $5/tháng. 
- Nếu chỉ chạy chơi, gói miễn phí là đủ. Nếu dùng lâu dài, hãy theo dõi mức độ tiêu thụ RAM của PostgreSQL.
