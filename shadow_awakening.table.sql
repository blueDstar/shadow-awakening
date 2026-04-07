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