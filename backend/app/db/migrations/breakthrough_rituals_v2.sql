-- 1. Create breakthrough_rituals table to store phase templates
CREATE TABLE breakthrough_rituals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phase INTEGER NOT NULL UNIQUE,
    title_vi VARCHAR(100) NOT NULL,
    title_en VARCHAR(100) NOT NULL,
    aura_name VARCHAR(50) NOT NULL,
    foundation_req TEXT NOT NULL, -- JSON: {type: 'streak', target: 7}
    mandatory_reqs TEXT NOT NULL, -- JSON List: [{type: 'habit_count', target: 10}, ...]
    optional_paths TEXT NOT NULL, -- JSON List of 3 paths: [{id: 1, type: 'wisdom', req: {...}}, ...]
    min_reflection_words INTEGER DEFAULT 300,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Update breakthrough_trials to track ritual-specific progress
ALTER TABLE breakthrough_trials ADD COLUMN IF NOT EXISTS selected_option_id UUID;
ALTER TABLE breakthrough_trials ADD COLUMN IF NOT EXISTS current_progress TEXT DEFAULT '{}';
ALTER TABLE breakthrough_trials ADD COLUMN IF NOT EXISTS ritual_id UUID REFERENCES breakthrough_rituals(id);

-- 3. Link reflections to breakthrough trials
ALTER TABLE reflections ADD COLUMN IF NOT EXISTS breakthrough_trial_id UUID REFERENCES breakthrough_trials(id);

-- 4. Seed Data for 12 Rituals
INSERT INTO breakthrough_rituals (phase, title_vi, title_en, aura_name, foundation_req, mandatory_reqs, optional_paths, min_reflection_words) VALUES
(1, 'Nghi thức Thức Tỉnh', 'Awakening Ritual', 'blue_glow', 
  '{"type": "streak", "target": 7}', 
  '[{"type": "habit_count", "target": 10}, {"type": "confidence_count", "target": 1}, {"type": "reflection_count", "target": 1}]',
  '[{"id": "opt1", "label_vi": "Trí Tuệ", "tag": "wisdom", "req": {"type": "wisdom_count", "target": 5}}, {"id": "opt2", "label_vi": "Thể Lực", "tag": "fitness", "req": {"type": "fitness_count", "target": 5}}, {"id": "opt3", "label_vi": "Tập Trung", "tag": "focus", "req": {"type": "deep_work_hours", "target": 2}}]',
  300),
(2, 'Phá Xiềng Trì Hoãn', 'Breaking Procrastination', 'dark_fire', 
  '{"type": "streak", "target": 7}', 
  '[{"type": "deep_work_hours", "target": 7}, {"type": "delayed_tasks_resolved", "target": 3}, {"type": "early_wake_days", "target": 5}]',
  '[{"id": "opt1", "label_vi": "Kỷ Luật Sáng", "tag": "discipline", "req": {"type": "no_social_morning", "target": 5}}, {"id": "opt2", "label_vi": "Bền Bỉ", "tag": "fitness", "req": {"type": "stamina_count", "target": 10}}, {"id": "opt3", "label_vi": "Sáng Suốt", "tag": "wisdom", "req": {"type": "wisdom_count", "target": 5}}]',
  300),
(3, 'Thử Lửa Can Đảm', 'Social Courage Trial', 'golden_aura', 
  '{"type": "streak", "target": 7}', 
  '[{"type": "new_conversations", "target": 10}, {"type": "public_questions", "target": 3}, {"type": "direct_feedback_requests", "target": 2}]',
  '[{"id": "opt1", "label_vi": "Kết Nối", "tag": "social", "req": {"type": "coffee_invitation", "target": 1}}, {"id": "opt2", "label_vi": "Lan Tỏa", "tag": "confidence", "req": {"type": "sincere_compliments", "target": 5}}, {"id": "opt3", "label_vi": "Dẫn Dắt", "tag": "wisdom", "req": {"type": "group_discussion", "target": 1}}]',
  300),
(4, 'Bách Luyện Trí Tuệ', 'Wisdom Refinement', 'purple_mystic', 
  '{"type": "streak", "target": 7}', 
  '[{"type": "book_completed", "target": 1}, {"type": "skill_module_completed", "target": 1}, {"type": "wisdom_focus_count", "target": 10}]',
  '[{"id": "opt1", "label_vi": "Tổng Hợp", "tag": "wisdom", "req": {"type": "knowledge_note_500w", "target": 1}}, {"id": "opt2", "label_vi": "Ngôn Ngữ", "tag": "wisdom", "req": {"type": "new_vocab_count", "target": 200}}, {"id": "opt3", "label_vi": "Ứng Dụng", "tag": "discipline", "req": {"type": "productivity_system_setup", "target": 1}}]',
  500),
(5, 'Luyện Thân - Luyện Tâm', 'Body & Mind Tempering', 'green_vitality', 
  '{"type": "streak", "target": 7}', 
  '[{"type": "workout_sessions", "target": 12}, {"type": "meditation_minutes", "target": 120}, {"type": "no_skip_workout_2d", "target": 1}]',
  '[{"id": "opt1", "label_vi": "Sức Mạnh", "tag": "fitness", "req": {"type": "pushups_daily_100", "target": 1}}, {"id": "opt2", "label_vi": "Bền Bỉ", "tag": "fitness", "req": {"type": "walking_15km_week", "target": 1}}, {"id": "opt3", "label_vi": "Linh Hoạt", "tag": "fitness", "req": {"type": "squats_daily_300", "target": 1}}]',
  400),
(6, 'Vực Sâu Tập Trung', 'Focus Abyss', 'cyan_crystal', 
  '{"type": "streak", "target": 10}', 
  '[{"type": "deep_work_hours", "target": 20}, {"type": "hard_task_3d_duration", "target": 1}, {"type": "no_fail_focus_7d", "target": 1}]',
  '[{"id": "opt1", "label_vi": "Phân Tích", "tag": "wisdom", "req": {"type": "distraction_report", "target": 1}}, {"id": "opt2", "label_vi": "Sáng Tạo", "tag": "focus", "req": {"type": "creative_sprint_10h", "target": 1}}, {"id": "opt3", "label_vi": "Trầm Tĩnh", "tag": "focus", "req": {"type": "silence_challenge_2h", "target": 1}}]',
  500),
(7, 'Vòng Tròn Ảnh Hưởng', 'Circle of Influence', 'orange_flare', 
  '{"type": "streak", "target": 10}', 
  '[{"type": "group_learning_lead", "target": 1}, {"type": "help_others_count", "target": 3}, {"type": "goal_oriented_convos", "target": 5}]',
  '[{"id": "opt1", "label_vi": "Phản Hồi", "tag": "social", "req": {"type": "positive_feedback_count", "target": 3}}, {"id": "opt2", "label_vi": "Chia Sẻ", "tag": "wisdom", "req": {"type": "public_resource_share", "target": 1}}, {"id": "opt3", "label_vi": "Kết Nối Sâu", "tag": "social", "req": {"type": "one_on_one_mentoring", "target": 1}}]',
  400),
(8, 'Nghi thức Dẫn Đường', 'Pathfinder Ritual', 'white_radiance', 
  '{"type": "streak", "target": 14}', 
  '[{"type": "mentoring_sessions", "target": 3}, {"type": "useful_resource_created", "target": 1}, {"type": "social_courage_challenge", "target": 1}]',
  '[{"id": "opt1", "label_vi": "Template", "tag": "wisdom", "req": {"type": "useful_template_creation", "target": 1}}, {"id": "opt2", "label_vi": "Hướng Dẫn", "tag": "wisdom", "req": {"type": "tutorial_video_short", "target": 1}}, {"id": "opt3", "label_vi": "Văn Bản", "tag": "wisdom", "req": {"type": "comprehensive_checklist", "target": 1}}]',
  500),
(9, 'Kiến Trúc Sư Kỷ Luật', 'Discipline Architect', 'red_obsidian', 
  '{"type": "streak", "target": 21}', 
  '[{"type": "self_system_design_30d", "target": 1}, {"type": "weekly_review_streak", "target": 4}, {"type": "core_habit_no_fail_21d", "target": 1}]',
  '[{"id": "opt1", "label_vi": "Toàn Diện", "tag": "discipline", "req": {"type": "progress_in_4_groups", "target": 1}}, {"id": "opt2", "label_vi": "Thử Thách", "tag": "focus", "req": {"type": "deep_work_30h_month", "target": 1}}, {"id": "opt3", "label_vi": "Tối Giản", "tag": "discipline", "req": {"type": "bad_habit_elimination", "target": 1}}]',
  500),
(10, 'Lãnh Đạo Bản Thân', 'Self Leadership', 'silver_knight', 
  '{"type": "streak", "target": 30}', 
  '[{"type": "deep_work_hours", "target": 30}, {"type": "major_goal_completed", "target": 1}, {"type": "public_presentation", "target": 1}]',
  '[{"id": "opt1", "label_vi": "Từ Bỏ", "tag": "discipline", "req": {"type": "major_bad_habit_cut", "target": 1}}, {"id": "opt2", "label_vi": "Tiên Phong", "tag": "confidence", "req": {"type": "lead_public_project", "target": 1}}, {"id": "opt3", "label_vi": "Trí Tuệ", "tag": "wisdom", "req": {"type": "personal_philosophy_essay", "target": 1}}]',
  600),
(11, 'Hành Trình Quân Vương', 'Sovereign Path', 'rainbow_divine', 
  '{"type": "streak", "target": 45}', 
  '[{"type": "major_knowledge_achievements", "target": 2}, {"type": "physical_milestone_major", "target": 1}, {"type": "valuable_public_contribution", "target": 1}]',
  '[{"id": "opt1", "label_vi": "Nội Tâm", "tag": "focus", "req": {"type": "deep_reflection_5_essays", "target": 1}}, {"id": "opt2", "label_vi": "Trí Tuệ", "tag": "wisdom", "req": {"type": "study_2_books_and_project", "target": 1}}, {"id": "opt3", "label_vi": "Cống Hiến", "tag": "social", "req": {"type": "foundation_support_action", "target": 1}}]',
  800),
(12, 'Nghi thức Siêu Việt', 'Transcendence Ritual', 'cosmic_void', 
  '{"type": "streak", "target": 60}', 
  '[{"type": "deep_work_hours", "target": 50}, {"type": "personal_project_result", "target": 1}, {"type": "clear_social_impact", "target": 1}]',
  '[{"id": "opt1", "label_vi": "Truyền Lửa", "tag": "social", "req": {"type": "teach_group_community", "target": 1}}, {"id": "opt2", "label_vi": "Tuyên Ngôn", "tag": "wisdom", "req": {"type": "self_dev_manifesto_v2", "target": 1}}, {"id": "opt3", "label_vi": "Vô Biến", "tag": "discipline", "req": {"type": "no_system_failure_60d", "target": 1}}]',
  1000);
