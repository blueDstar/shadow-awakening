-- ============================================================
-- EXPANDED SEED DATA - Additional Skills (To reach 20)
-- ============================================================
INSERT INTO skills (name_vi, name_en, description_vi, description_en, unlock_condition, icon) VALUES
('Hơi Thở Hư Không', 'Void Breath', 'Tăng 15% hiệu quả thiền định.', 'Increase meditation effectiveness by 15%.', '{"level": 8, "stat": {"focus": 50}}', '🌬️'),
('Bộ Pháp Bóng Tối', 'Shadow Step', 'Tăng 10% stamina khi chạy bộ.', 'Increase stamina from jogging by 10%.', '{"stat": {"stamina": 30}}', '👣'),
('Huyết Mạch Titan', 'Titan Blood', 'Giảm 50% thời gian hồi phục thể lực.', 'Reduce physical recovery time by 50%.', '{"level": 20, "stat": {"strength": 60}}', '🩸'),
('Tầm Nhìn U Minh', 'Nether Vision', 'Tỉ lệ 10% nhận x2 EXP cho bất kỳ quest nào.', '10% chance to get x2 EXP for any quest.', '{"level": 12}', '👁️'),
('Giáp Tâm Linh', 'Mental Armor', 'Giảm mất mát streak khi lỡ 1 ngày (dùng 1 lần/tuần).', 'Protect streak failure once per week.', '{"streak": 21}', '🛡️'),
('Khế Ước Tri Thức', 'Knowledge Pact', 'Tăng 25% stats từ việc đọc sách.', 'Increase stat gain from reading by 25%.', '{"stat": {"wisdom": 45}}', '📜'),
('Sát Thủ Tập Trung', 'Focus Assassin', 'Xóa bỏ mọi thông báo điện thoại khi bật chế độ focus.', 'No distractions during focus mode.', '{"stat": {"focus": 70}}', '🎯'),
('Dấu Ấn Kỷ Luật', 'Mark of Discipline', 'Tự động hoàn thành 1 side quest nếu hoàn thành 2 main quest.', 'Auto-complete 1 side quest after 2 main quests.', '{"stat": {"discipline": 60}}', '⚖️'),
('Linh Hồn Khám Phá', 'Explorer''s Soul', 'Nhận thêm 100 EXP khi tìm hiểu topic mới lạ.', 'Extra 100 EXP for exploration topics.', '{"exploration_quests": 10}', '🗺️'),
('Tiếng Gọi Chiến Binh', 'Warrior''s Call', 'Tăng 20% sức mạnh từ các bài tập bodyweight.', 'Increase strength gain from bodyweight exercises by 20%.', '{"stat": {"strength": 40}}', '📣'),
('Sự Tĩnh Lặng Của Rừng', 'Forest Silence', 'Tăng tốc độ hồi phục Focus Capacity.', 'Faster Focus Capacity recovery.', '{"meditation_hours": 10}', '🌲'),
('Bản Năng Sinh Tồn', 'Survival Instinct', 'Không bị trừ EXP khi fail quest penalty.', 'No EXP loss on penalty quest failure.', '{"level": 25}', '🐺');

-- ============================================================
-- EXPANDED SEED DATA - Additional Rewards (To reach 20)
-- ============================================================
INSERT INTO rewards (name_vi, name_en, reward_type, description_vi, description_en, unlock_condition, icon, rarity) VALUES
('Chúa Tể Bóng Tối', 'Shadow Lord', 'title', 'Danh hiệu dành cho bậc thầy bóng tối.', 'Title for the shadow master.', '{"level": 50}', '⚔️', 'legendary'),
('Thợ Săn Quái Vật', 'Monster Hunter', 'badge', 'Hoàn thành 500 quest tổng cộng.', 'Complete 500 total quests.', '{"total_quests": 500}', '🏹', 'epic'),
('Lửa Thiêng Vĩnh Cửu', 'Eternal Flame', 'aura', 'Duy trì 100 ngày streak.', 'Maintain a 100-day streak.', '{"streak": 100}', '💠', 'legendary'),
('Kiến Trúc Sư Cuộc Đời', 'Architect of Life', 'title', 'Hoàn thành 20 Challenge.', 'Complete 20 challenges.', '{"challenges_completed": 20}', '🏛️', 'epic'),
('Bàn Tay Thép', 'Iron Hand', 'badge', 'Đạt cấp 10 Discipline.', 'Reach Discipline level 10.', '{"stat": {"discipline": 100}}', '🫱', 'rare'),
('Trái Tim Rồng', 'Dragon Heart', 'aura', 'Đạt cấp 10 Stamina.', 'Reach Stamina level 10.', '{"stat": {"stamina": 100}}', '❤️', 'epic'),
('Đại Hiền Triết', 'Grand Sage', 'title', 'Đạt Wisdom & Knowledge cấp cao.', 'High Wisdom & Knowledge reached.', '{"stat": {"wisdom": 100, "knowledge": 100}}', '🧙', 'legendary'),
('Sát Thủ Tập Trung', 'Focus Master', 'badge', 'Hoàn thành 50 Deep Work sessions.', 'Complete 50 Deep Work sessions.', '{"focus_sessions": 50}', '🧘', 'rare'),
('Vương Miện Vinh Quang', 'Crown of Glory', 'aura', 'Hoàn thành mọi quest trong tuần.', 'Complete all quests in a week.', '{"weekly_completion": true}', '👑', 'epic'),
('Kẻ Phá Vỡ Giới Hạn', 'Limit Breaker', 'title', 'Hoàn thành Đột Phá Phase 5.', 'Complete Phase 5 Breakthrough.', '{"breakthrough_phase": 5}', '🌀', 'legendary');

-- ============================================================
-- EXPANDED SEED DATA - Additional Challenges (To reach 20)
-- ============================================================
INSERT INTO challenges (name_vi, name_en, description_vi, description_en, challenge_type, duration_days, requirements, rewards, min_level, category) VALUES
('10.000 Squats Marathon', '10,000 Squats', '10,000 squat trong 90 ngày.', '10,000 squats in 90 days.', 'long_term', 90, '{"total_squats": 10000}', '{"exp": 5000, "aura": "titan"}', 10, 'fitness'),
('Chiến Dịch Tỉnh Táo', 'Digital Detox', 'Không dùng mạng xã hội trong 7 ngày.', 'No social media for 7 days.', 'weekly', 7, '{"no_social_media": true}', '{"exp": 500, "stat": {"focus": 10}}', 5, 'focus'),
('Bậc Thầy Trí Tuệ', 'Master Mind', 'Đọc 5 cuốn sách trong 30 ngày.', 'Read 5 books in 30 days.', 'monthly', 30, '{"books_read": 5}', '{"exp": 2000, "title": "bibliophile"}', 1, 'wisdom'),
('Con Đường Samurai', 'Way of the Samurai', 'Ngủ trước 11h đêm trong 21 ngày liên tục.', 'Sleep before 11 PM for 21 days.', 'monthly', 21, '{"early_sleep_streak": 21}', '{"exp": 1500, "badge": "discipline_master"}', 1, 'discipline'),
('Tiếng Anh Thần Tốc', 'English Blitz', 'Học 500 từ vựng mới trong 30 ngày.', 'Learn 500 new words in 30 days.', 'monthly', 30, '{"new_words": 500}', '{"exp": 2500, "stat": {"wisdom": 10}}', 1, 'wisdom'),
('Chiến Binh Sáng Sớm', 'Early Bird Warrior', 'Thức dậy lúc 5h sáng trong 14 ngày.', 'Wake up at 5 AM for 14 days.', 'weekly', 14, '{"wakeup_5am_streak": 14}', '{"exp": 1000, "stat": {"discipline": 5}}', 5, 'discipline'),
('Tâm Trí Kim Cương', 'Diamond Mind', 'Thiền 20 phút mỗi ngày trong 30 ngày.', 'Meditate 20 min daily for 30 days.', 'monthly', 30, '{"meditation_daily": 20}', '{"exp": 2000, "aura": "inner_peace"}', 1, 'focus'),
('Hành Trình Khám Phá', 'Exploration Quest', 'Tìm hiểu 30 chủ đề mới trong 30 ngày.', 'Explore 30 new topics in 30 days.', 'monthly', 30, '{"new_topics": 30}', '{"exp": 2000, "stat": {"knowledge": 15}}', 1, 'exploration'),
('Vua Kỷ Luật', 'Discipline King', 'Không bỏ lỡ bất kỳ quest nào trong 14 ngày.', 'Zero failed quests for 14 days.', 'weekly', 14, '{"zero_fail_streak": 14}', '{"exp": 3000, "title": "unbroken"}', 10, 'discipline'),
('Tập Trung Tuyệt Đối', 'Total Focus', '50 giờ Deep Work trong 30 ngày.', '50 hours of Deep Work in 30 days.', 'monthly', 30, '{"deep_work_hours": 50}', '{"exp": 3500, "stat": {"focus": 20}}', 10, 'focus'),
('Giao Tiếp Bậc Thầy', 'Master Communicator', 'Nói chuyện với 15 người lạ trong 15 ngày.', 'Talk to 15 strangers in 15 days.', 'weekly', 15, '{"stranger_conversations": 15}', '{"exp": 1000, "stat": {"confidence": 15}}', 5, 'confidence'),
('Cơ Thể Thép', 'Iron Body', 'Chạy bộ 100km trong 30 ngày.', 'Run 100km in 30 days.', 'monthly', 30, '{"running_distance": 100}', '{"exp": 4000, "stat": {"stamina": 20}}', 1, 'fitness'),
('Tri Thức Vô Tận', 'Infinite Knowledge', 'Viết 20 bài blog/ghi chú nghiên cứu trong 20 ngày.', 'Write 20 study notes in 20 days.', 'monthly', 20, '{"study_notes": 20}', '{"exp": 2000, "stat": {"knowledge": 10}}', 1, 'wisdom'),
('Sự Thay Đổi Thầm Lặng', 'Silent Change', 'Dọn dẹp nhà cửa mỗi ngày trong 7 ngày.', 'Clean home daily for 7 days.', 'weekly', 7, '{"daily_cleaning": true}', '{"exp": 400, "stat": {"discipline": 5}}', 1, 'discipline');
