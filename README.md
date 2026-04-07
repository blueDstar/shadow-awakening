# 🌑 Shadow Awakening — Bóng Tối Thức Tỉnh

> *"Mỗi ngày là một trận chiến. Mỗi nhiệm vụ là một bước tiến hóa."*

App gamification phát triển bản thân theo phong cách dark fantasy — biến cuộc sống thường ngày thành hành trình thăng cấp.

**🌐 Link trải nghiệm (Demo):** [https://shadow-awakening-sepia.vercel.app/](https://shadow-awakening-sepia.vercel.app/)

## 🛠️ Tech Stack

| Layer | Công nghệ |
|-------|-----------|
| Frontend | React 18 + Vite + SCSS + Framer Motion |
| Backend | FastAPI + SQLAlchemy 2.0 + Alembic |
| Database | PostgreSQL |
| Auth | JWT (python-jose) + bcrypt |
| i18n | react-i18next (Việt / Anh) |

## 🚀 Chạy Localhost

### 1. Cài PostgreSQL
- Tải PostgreSQL: https://www.postgresql.org/download/
- Cài đặt và tạo database:
```sql
CREATE DATABASE shadow_awakening;
```

### 2. Backend
```bash
cd backend

# Tạo virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Cài dependencies
pip install -r requirements.txt

# Copy .env
cp .env.example .env
# Sửa DATABASE_URL trong .env cho phù hợp

# Chạy server
uvicorn app.main:app --reload --port 8000
```

Backend sẽ chạy ở: http://localhost:8000
API docs: http://localhost:8000/docs

### 3. Frontend
```bash
cd frontend

# Cài dependencies
npm install

# Chạy dev server
npm run dev
```

Frontend sẽ chạy ở: http://localhost:5173

### 4. Sử dụng
1. Mở http://localhost:5173
2. Đăng ký tài khoản mới
3. Hệ thống sẽ tự tạo nhân vật + chỉ số + quest cho bạn
4. Dashboard → Quests → hoàn thành quest → nhận EXP → level up!

## 📁 Cấu Trúc Thư Mục

```
Shadow_awakening/
├── backend/
│   ├── app/
│   │   ├── main.py         # FastAPI entry point
│   │   ├── core/            # Config, Security, Dependencies
│   │   ├── db/              # Database engine
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── routes/          # API routes
│   │   ├── services/        # Business logic
│   │   └── utils/           # Helpers
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── layouts/         # Layout wrappers
│   │   ├── services/        # API service layer
│   │   ├── context/         # React Context
│   │   ├── i18n/            # Translations
│   │   ├── styles/          # SCSS design system
│   │   ├── App.jsx
│   │   └── index.scss
│   ├── package.json
│   └── .env
└── README.md
```

## 🌐 Deploy Production

### Frontend → Vercel / Netlify
```bash
cd frontend
npm run build
# Upload dist/ folder hoặc connect GitHub repo
```

### Backend → Render / Railway
1. Push code lên GitHub
2. Tạo project trên Render (render.com)
3. Tạo PostgreSQL database trên Render
4. Connect GitHub repo → Auto deploy
5. Set environment variables (DATABASE_URL, SECRET_KEY)

### Lưu ý quan trọng
- GitHub chỉ dùng để lưu mã nguồn, KHÔNG chạy backend
- Frontend (React) → deploy miễn phí trên Vercel/Netlify
- Backend (FastAPI + PostgreSQL) → cần Render/Railway/Fly.io/VPS
- Cần có DATABASE_URL PostgreSQL trên cloud cho production

## 📜 API Docs

Sau khi chạy backend, Swagger docs tại: http://localhost:8000/docs

## 🎮 Tính Năng

- ⚔️ Quest system với 7 loại: Main/Side/Habit/Challenge/Penalty/Special/Breakthrough
- 📊 10 loại chỉ số: Wisdom, Confidence, Strength, Discipline, Focus, + 5 extended
- 🔥 Streak tracking theo 7 nhóm
- 💥 Breakthrough system: mở trần chỉ số vô hạn (100→200→300→...)
- 📖 Journal/Reflection
- 🌐 Song ngữ Việt-Anh
- 🎨 Dark fantasy UI với particle effects

## License

MIT
