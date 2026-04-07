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