# 🌑 Shadow Awakening — Hướng Dẫn Cài Đặt Database PostgreSQL

---

## BƯỚC 0: KIỂM TRA IP VÀ PORT CỦA POSTGRESQL

Mở **SQL Shell (psql)** hoặc **Command Prompt** và chạy:

```
-- Kiểm tra PostgreSQL đang lắng nghe ở đâu
SHOW listen_addresses;
SHOW port;
```

**Kết quả mặc định:**
- IP: `localhost` (hoặc `127.0.0.1`)
- Port: `5432`

**Nếu muốn kiểm tra chi tiết hơn**, mở **Command Prompt** (không phải psql) và gõ:

```
netstat -an | findstr 5432
```

Sẽ thấy dòng kiểu: `TCP 0.0.0.0:5432 ... LISTENING` → PostgreSQL đang chạy ở port 5432.

**Kiểm tra version:**
```
SELECT version();
```

---

## BƯỚC 1: ĐĂNG NHẬP VÀO SQL SHELL (psql)

Mở **SQL Shell (psql)** từ Start Menu. Nhập thông tin:

```
Server [localhost]: localhost
Database [postgres]: postgres
Port [5432]: 5432
Username [postgres]: postgres
Password: (nhập mật khẩu bạn đặt khi cài PostgreSQL)
```

> ⚠️ **Quan trọng:** Nhớ mật khẩu bạn nhập ở đây, sẽ dùng nó ở Bước 4.

---

## BƯỚC 2: TẠO DATABASE

Copy và dán lệnh này vào psql:

```sql
CREATE DATABASE shadow_awakening;
```

Kiểm tra đã tạo thành công:

```sql
\l
```

Sẽ thấy `shadow_awakening` trong danh sách.

---

## BƯỚC 3: KẾT NỐI VÀO DATABASE MỚI

```sql
\c shadow_awakening
```

Sẽ thấy: `You are now connected to database "shadow_awakening" as user "postgres".`

---

## BƯỚC 4: BẬT EXTENSION UUID

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

---

## BƯỚC 5: TẠO TẤT CẢ BẢNG

Copy **TOÀN BỘ** khối SQL dưới đây và dán vào psql:

```sql
-- ============================================================
-- SHADOW AWAKENING - DATABASE SCHEMA
-- ============================================================

-- 1. USERS
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- 2. USER PROFILES
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    long_term_goals TEXT DEFAULT '',
    short_term_goals TEXT DEFAULT '',
    development_areas TEXT DEFAULT '[]',
    daily_free_time_minutes VARCHAR(10) DEFAULT '120',
    fitness_level VARCHAR(20) DEFAULT 'beginner',
    focus_capacity VARCHAR(20) DEFAULT 'moderate',
    sleep_time VARCHAR(10) DEFAULT '23:00',
    wake_time VARCHAR(10) DEFAULT '07:00',
    current_habits TEXT DEFAULT '[]',
    exploration_interests TEXT DEFAULT '[]',
    discipline_level VARCHAR(20) DEFAULT 'moderate',
    onboarding_completed BOOLEAN DEFAULT FALSE
);

-- 3. CHARACTERS
CREATE TABLE characters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    title VARCHAR(100) DEFAULT 'Kẻ Thức Tỉnh',
    level INTEGER DEFAULT 1,
    current_exp BIGINT DEFAULT 0,
    total_exp BIGINT DEFAULT 0,
    aura VARCHAR(50) DEFAULT 'shadow_basic',
    avatar_type VARCHAR(50) DEFAULT 'default',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. STAT CAPS (trần chỉ số, mở rộng vô hạn)
CREATE TABLE stat_caps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    character_id UUID NOT NULL UNIQUE REFERENCES characters(id) ON DELETE CASCADE,
    current_cap INTEGER DEFAULT 100,
    phase INTEGER DEFAULT 1,
    breakthrough_available BOOLEAN DEFAULT FALSE
);

-- 5. USER STATS (10 chỉ số)
CREATE TABLE user_stats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    character_id UUID NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
    stat_name VARCHAR(50) NOT NULL,
    current_value FLOAT DEFAULT 0.0
);

-- 6. QUEST TEMPLATES
CREATE TABLE quests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title_vi VARCHAR(255) NOT NULL,
    title_en VARCHAR(255) NOT NULL,
    description_vi TEXT DEFAULT '',
    description_en TEXT DEFAULT '',
    quest_type VARCHAR(30) NOT NULL,
    category VARCHAR(30) NOT NULL,
    difficulty_min_level INTEGER DEFAULT 1,
    difficulty_max_level INTEGER DEFAULT 100,
    exp_reward INTEGER DEFAULT 10,
    stat_rewards TEXT DEFAULT '{}',
    base_requirements TEXT DEFAULT '{}',
    is_template BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. DAILY QUESTS (nhiệm vụ hàng ngày của user)
CREATE TABLE daily_quests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    quest_template_id UUID REFERENCES quests(id),
    quest_date DATE NOT NULL DEFAULT CURRENT_DATE,
    title_vi VARCHAR(255) NOT NULL,
    title_en VARCHAR(255) NOT NULL,
    description_vi TEXT DEFAULT '',
    description_en TEXT DEFAULT '',
    quest_type VARCHAR(30) NOT NULL,
    category VARCHAR(30) NOT NULL,
    difficulty INTEGER DEFAULT 1,
    exp_reward INTEGER DEFAULT 10,
    stat_rewards TEXT DEFAULT '{}',
    status VARCHAR(20) DEFAULT 'pending',
    completed_at TIMESTAMP,
    chain_parent_id UUID REFERENCES daily_quests(id),
    fail_reason VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_daily_quests_user_date ON daily_quests(user_id, quest_date);

-- 8. QUEST HISTORY (tổng kết mỗi ngày)
CREATE TABLE quest_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    quest_date DATE NOT NULL,
    total_quests INTEGER DEFAULT 0,
    completed_quests INTEGER DEFAULT 0,
    failed_quests INTEGER DEFAULT 0,
    exp_earned INTEGER DEFAULT 0,
    stats_gained TEXT DEFAULT '{}',
    day_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. STREAKS (chuỗi ngày)
CREATE TABLE streaks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    streak_type VARCHAR(30) NOT NULL,
    current_streak INTEGER DEFAULT 0,
    best_streak INTEGER DEFAULT 0,
    last_active_date DATE,
    started_at DATE DEFAULT CURRENT_DATE
);

-- 10. STREAK LOGS
CREATE TABLE streak_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    streak_type VARCHAR(30) NOT NULL,
    log_date DATE NOT NULL,
    streak_value INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 11. REWARDS (phần thưởng)
CREATE TABLE rewards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name_vi VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    reward_type VARCHAR(30) NOT NULL,
    description_vi TEXT DEFAULT '',
    description_en TEXT DEFAULT '',
    unlock_condition TEXT DEFAULT '{}',
    icon VARCHAR(50) DEFAULT '🏆',
    rarity VARCHAR(20) DEFAULT 'common',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 12. USER REWARDS
CREATE TABLE user_rewards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reward_id UUID NOT NULL REFERENCES rewards(id),
    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_equipped BOOLEAN DEFAULT FALSE
);

-- 13. SKILLS (kỹ năng)
CREATE TABLE skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name_vi VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    description_vi TEXT DEFAULT '',
    description_en TEXT DEFAULT '',
    unlock_condition TEXT DEFAULT '{}',
    icon VARCHAR(50) DEFAULT '⚡',
    effect TEXT DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 14. USER SKILLS
CREATE TABLE user_skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    skill_id UUID NOT NULL REFERENCES skills(id),
    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- 15. CHALLENGES (thử thách)
CREATE TABLE challenges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name_vi VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    description_vi TEXT DEFAULT '',
    description_en TEXT DEFAULT '',
    challenge_type VARCHAR(30) NOT NULL,
    duration_days INTEGER DEFAULT 7,
    requirements TEXT DEFAULT '{}',
    rewards TEXT DEFAULT '{}',
    min_level INTEGER DEFAULT 1,
    category VARCHAR(30) DEFAULT 'general',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 16. USER CHALLENGES
CREATE TABLE user_challenges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    challenge_id UUID NOT NULL REFERENCES challenges(id),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    progress TEXT DEFAULT '{}',
    days_completed INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',
    completed_at TIMESTAMP
);

-- 17. REFLECTIONS (nhật ký)
CREATE TABLE reflections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reflection_date DATE NOT NULL DEFAULT CURRENT_DATE,
    content TEXT DEFAULT '',
    mood VARCHAR(20) DEFAULT 'neutral',
    insights TEXT DEFAULT '',
    success_reasons TEXT DEFAULT '',
    fail_reasons TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 18. PLANNER BLOCKS (phân bổ thời gian)
CREATE TABLE planner_blocks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    block_date DATE NOT NULL DEFAULT CURRENT_DATE,
    start_time VARCHAR(10) NOT NULL,
    end_time VARCHAR(10) NOT NULL,
    activity VARCHAR(255) NOT NULL,
    category VARCHAR(30) DEFAULT 'general',
    completed BOOLEAN DEFAULT FALSE
);

-- 19. BREAKTHROUGH TRIALS (thử thách đột phá)
CREATE TABLE breakthrough_trials (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    phase INTEGER NOT NULL,
    from_cap INTEGER NOT NULL,
    to_cap INTEGER NOT NULL,
    requirements TEXT DEFAULT '{}',
    status VARCHAR(20) DEFAULT 'available',
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- 20. EXPERIENCE LOGS
CREATE TABLE experience_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    amount INTEGER NOT NULL,
    source VARCHAR(50) NOT NULL,
    source_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 21. USER SETTINGS
CREATE TABLE user_settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    language VARCHAR(5) DEFAULT 'vi',
    timezone VARCHAR(50) DEFAULT 'Asia/Ho_Chi_Minh',
    difficulty_preference VARCHAR(20) DEFAULT 'moderate',
    notification_enabled BOOLEAN DEFAULT TRUE,
    daily_reset_hour INTEGER DEFAULT 0
);
```

---

## BƯỚC 6: KIỂM TRA TẤT CẢ BẢNG ĐÃ TẠO

```sql
\dt
```

Phải thấy **21 bảng**:
```
breakthrough_trials | challenges      | characters
daily_quests        | experience_logs | planner_blocks
quest_history       | quests          | reflections
rewards             | skills          | stat_caps
streak_logs         | streaks         | user_challenges
user_profiles       | user_rewards    | user_settings
user_skills         | user_stats      | users
```

---

## BƯỚC 7: TẠO SEED DATA (dữ liệu mẫu)

Copy và dán:

```sql
-- ============================================================
-- SEED DATA - Skills
-- ============================================================
INSERT INTO skills (name_vi, name_en, description_vi, description_en, unlock_condition, icon) VALUES
('Chế Độ Tập Trung', 'Focus Mode', 'Tăng 20% EXP cho quest focus khi active.', 'Increase focus quest EXP by 20% when active.', '{"level": 5, "stat": {"focus": 30}}', '🧠'),
('Chế Độ Nghiên Cứu', 'Research Mode', 'Mở rộng quest exploration mỗi ngày.', 'Expand daily exploration quests.', '{"level": 10, "stat": {"knowledge": 40}}', '🔬'),
('Chuỗi Bóng Tối', 'Shadow Streak', 'Nhận bonus x1.5 EXP khi đạt 7+ streak.', 'Get x1.5 EXP bonus at 7+ streak.', '{"streak": 7}', '🔥'),
('Chuỗi Tinh Nhuệ', 'Elite Chain', 'Nhận bonus x2 EXP khi đạt 14+ streak.', 'Get x2 EXP bonus at 14+ streak.', '{"streak": 14}', '⛓️'),
('Thử Thách Đột Phá', 'Breakthrough Trial', 'Cho phép mở trần chỉ số khi đạt max.', 'Allows stat cap expansion when maxed.', '{"all_core_stats_at_cap": true}', '💥'),
('Tầm Nhìn Tri Thức', 'Insight Vision', 'Hiển thị phân tích chi tiết chỉ số.', 'Show detailed stat analytics.', '{"level": 15, "stat": {"wisdom": 60}}', '👁️'),
('Khóa Kỷ Luật', 'Discipline Lock', 'Không thể bỏ quest khi active.', 'Cannot skip quests when active.', '{"stat": {"discipline": 50}}', '🔒'),
('Nghi Thức Phục Hồi', 'Recovery Protocol', 'Giảm penalty khi fail streak.', 'Reduce penalty on streak failure.', '{"penalty_quests_completed": 3}', '💚');

-- ============================================================
-- SEED DATA - Rewards
-- ============================================================
INSERT INTO rewards (name_vi, name_en, reward_type, description_vi, description_en, unlock_condition, icon, rarity) VALUES
('Kẻ Thức Tỉnh', 'The Awakened', 'title', 'Danh hiệu mặc định khi bắt đầu.', 'Default title when starting.', '{"auto": true}', '👑', 'common'),
('Ngày Đầu Tiên', 'First Day', 'badge', 'Hoàn thành ngày đầu tiên.', 'Complete the first day.', '{"days_completed": 1}', '🌅', 'common'),
('Chuỗi 7 Ngày', '7-Day Streak', 'badge', 'Duy trì chuỗi 7 ngày liên tục.', 'Maintain a 7-day streak.', '{"streak": 7}', '🔥', 'rare'),
('Chuỗi 30 Ngày', '30-Day Streak', 'badge', 'Duy trì chuỗi 30 ngày liên tục.', 'Maintain a 30-day streak.', '{"streak": 30}', '🔥', 'epic'),
('Bóng Tối Cấp 10', 'Shadow Level 10', 'aura', 'Đạt cấp 10.', 'Reach level 10.', '{"level": 10}', '🌑', 'epic'),
('Bóng Tối Cấp 25', 'Shadow Level 25', 'aura', 'Đạt cấp 25.', 'Reach level 25.', '{"level": 25}', '🌑', 'legendary'),
('Đột Phá Kỷ Luật', 'Discipline Breakthrough', 'badge', 'Hoàn thành đột phá stat cap lần đầu.', 'Complete first stat cap breakthrough.', '{"breakthrough_completed": 1}', '⚡', 'legendary'),
('Thiền Giả', 'The Meditator', 'badge', 'Thiền 30 ngày liên tục.', 'Meditate for 30 consecutive days.', '{"meditation_streak": 30}', '🧘', 'rare'),
('Chiến Binh Thể Lực', 'Fitness Warrior', 'badge', 'Hoàn thành 100 quest fitness.', 'Complete 100 fitness quests.', '{"fitness_quests": 100}', '💪', 'epic'),
('Nhà Hiền Triết', 'The Sage', 'title', 'Đạt wisdom ≥ 80.', 'Reach wisdom ≥ 80.', '{"stat": {"wisdom": 80}}', '📚', 'legendary');

-- ============================================================
-- SEED DATA - Challenges
-- ============================================================
INSERT INTO challenges (name_vi, name_en, description_vi, description_en, challenge_type, duration_days, requirements, rewards, min_level, category) VALUES
('7 Ngày Đọc Sách', '7-Day Reading', 'Đọc sách mỗi ngày trong 7 ngày liên tục.', 'Read every day for 7 consecutive days.', 'weekly', 7, '{"daily_reading": true}', '{"exp": 200, "badge": "bookworm"}', 1, 'wisdom'),
('14 Ngày Tiếng Anh', '14-Day English', 'Học tiếng Anh mỗi ngày trong 14 ngày.', 'Study English daily for 14 days.', 'monthly', 14, '{"daily_english": true}', '{"exp": 500, "stat": {"wisdom": 5}}', 1, 'wisdom'),
('30 Ngày Thể Lực', '30-Day Fitness', 'Tập thể lực mỗi ngày trong 30 ngày.', 'Exercise daily for 30 days.', 'monthly', 30, '{"daily_fitness": true}', '{"exp": 1000, "badge": "iron_body"}', 1, 'fitness'),
('5 Ngày Deep Work', '5-Day Deep Work', 'Deep work mỗi ngày trong 5 ngày.', 'Deep work daily for 5 days.', 'weekly', 5, '{"daily_deep_work": true}', '{"exp": 150, "stat": {"focus": 3}}', 3, 'focus'),
('21 Ngày Kỷ Luật', '21-Day Discipline', 'Hoàn thành tất cả quest trong 21 ngày.', 'Complete all quests for 21 days.', 'monthly', 21, '{"all_quests_daily": true}', '{"exp": 800, "stat": {"discipline": 8}}', 5, 'discipline'),
('7 Ngày Nhật Ký', '7-Day Journal', 'Viết nhật ký mỗi ngày trong 7 ngày.', 'Write journal entries for 7 days.', 'weekly', 7, '{"daily_journal": true}', '{"exp": 150, "stat": {"mental_resilience": 3}}', 1, 'discipline');
```

---

## BƯỚC 8: KIỂM TRA DỮ LIỆU

```sql
SELECT COUNT(*) AS total_skills FROM skills;
SELECT COUNT(*) AS total_rewards FROM rewards;
SELECT COUNT(*) AS total_challenges FROM challenges;
```

Kết quả phải là: **8 skills, 10 rewards, 6 challenges**.

---

## BƯỚC 9: CẬP NHẬT FILE .env CỦA BACKEND

Mở file `f:\Shadow_awakening\backend\.env` và sửa **mật khẩu PostgreSQL** cho đúng:

```
DATABASE_URL=postgresql+asyncpg://postgres:MẬT_KHẨU_CỦA_BẠN@localhost:5432/shadow_awakening
DATABASE_URL_SYNC=postgresql://postgres:MẬT_KHẨU_CỦA_BẠN@localhost:5432/shadow_awakening
```

> ⚠️ Thay `MẬT_KHẨU_CỦA_BẠN` bằng mật khẩu PostgreSQL bạn nhập ở Bước 1.

**Ví dụ** nếu mật khẩu là `abc123`:
```
DATABASE_URL=postgresql+asyncpg://postgres:abc123@localhost:5432/shadow_awakening
DATABASE_URL_SYNC=postgresql://postgres:abc123@localhost:5432/shadow_awakening
```

---

## BƯỚC 10: CHẠY BACKEND

Mở terminal mới, chạy:

```bash
cd f:\Shadow_awakening\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Nếu thấy: `🌑 Shadow Awakening API is rising...` → **THÀNH CÔNG!**

Mở trình duyệt: http://localhost:8000/docs để xem API docs.

---

## BƯỚC 11: TẮT MOCK MODE Ở FRONTEND

Mở file `f:\Shadow_awakening\frontend\src\services\apiServices.js`

Đổi dòng:
```js
const USE_MOCK = true;
```
Thành:
```js
const USE_MOCK = false;
```

Refresh trang http://localhost:5173 → Giờ frontend sẽ kết nối **thật** với backend.

---

## 📋 TÓM TẮT KẾT NỐI

| Thành phần | URL |
|------------|-----|
| PostgreSQL | `localhost:5432` |
| Backend API | `http://localhost:8000` |
| API Docs | `http://localhost:8000/docs` |
| Frontend | `http://localhost:5173` |

| Giá trị cần nhớ | Mặc định |
|-----------------|----------|
| DB name | `shadow_awakening` |
| DB user | `postgres` |
| DB password | (bạn tự đặt) |
| DB port | `5432` |

---

## ❓ XỬ LÝ LỖI THƯỜNG GẶP

**Lỗi "password authentication failed":**
→ Sai mật khẩu trong `.env`. Kiểm tra lại.

**Lỗi "database does not exist":**
→ Chưa chạy `CREATE DATABASE shadow_awakening;` ở Bước 2.

**Lỗi "connection refused":**
→ PostgreSQL chưa chạy. Mở **Services** (services.msc) → tìm **postgresql** → Start.

**Lỗi "relation does not exist":**
→ Chưa tạo bảng. Quay lại Bước 5.
