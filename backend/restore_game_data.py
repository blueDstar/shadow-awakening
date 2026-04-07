import os
import json
import uuid
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('DATABASE_URL_SYNC')
if not url:
    print("DATABASE_URL_SYNC not found in .env")
    exit(1)

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()

def restore():
    print("--- Restoring Skills ---")
    skills_data = [
        # Base (from shadow_awakening_seeddata.sql)
        ('Chế Độ Tập Trung', 'Focus Mode', 'Tăng 20% EXP cho quest focus khi active.', 'Increase focus quest EXP by 20% when active.', '{"level": 5, "stat": {"focus": 30}}', '🧠'),
        ('Chế Độ Nghiên Cứu', 'Research Mode', 'Mở rộng quest exploration mỗi ngày.', 'Expand daily exploration quests.', '{"level": 10, "stat": {"knowledge": 40}}', '🔬'),
        ('Chuỗi Bóng Tối', 'Shadow Streak', 'Nhận bonus x1.5 EXP khi đạt 7+ streak.', 'Get x1.5 EXP bonus at 7+ streak.', '{"streak": 7}', '🔥'),
        ('Chuỗi Tinh Nhuệ', 'Elite Chain', 'Nhận bonus x2 EXP khi đạt 14+ streak.', 'Get x2 EXP bonus at 14+ streak.', '{"streak": 14}', '⛓️'),
        ('Thử Thách Đột Phá', 'Breakthrough Trial', 'Cho phép mở trần chỉ số khi đạt max.', 'Allows stat cap expansion when maxed.', '{"all_core_stats_at_cap": true}', '💥'),
        ('Tầm Nhìn Tri Thức', 'Insight Vision', 'Hiển thị phân tích chi tiết chỉ số.', 'Show detailed stat analytics.', '{"level": 15, "stat": {"wisdom": 60}}', '👁️'),
        ('Khóa Kỷ Luật', 'Discipline Lock', 'Không thể bỏ quest khi active.', 'Cannot skip quests when active.', '{"stat": {"discipline": 50}}', '🔒'),
        ('Nghi Thức Phục Hồi', 'Recovery Protocol', 'Giảm penalty khi fail streak.', 'Reduce penalty on streak failure.', '{"penalty_quests_completed": 3}', '💚'),
        # Expanded (from expanded_content.sql)
        ('Hơi Thở Hư Không', 'Void Breath', 'Tăng 15% hiệu quả thiền định.', 'Increase meditation effectiveness by 15%.', '{"level": 8, "stat": {"focus": 50}}', '🌬️'),
        ('Bộ Pháp Bóng Tối', 'Shadow Step', 'Tăng 10% stamina khi chạy bộ.', 'Increase stamina from jogging by 10%.', '{"stat": {"stamina": 30}}', '👣'),
        ('Huyết Mạch Titan', 'Titan Blood', 'Giảm 50% thời gian hồi phục thể lực.', 'Reduce physical recovery time by 50%.', '{"level": 20, "stat": {"strength": 60}}', '🩸'),
        ('Tầm Nhìn U Minh', 'Nether Vision', 'Tỉ lệ 10% nhận x2 EXP cho bất kỳ quest nào.', '10% chance to get x2 EXP for any quest.', '{"level": 12}', '👁️'),
        ('Giáp Tâm Linh', 'Mental Armor', 'Giảm mất mát streak khi lỡ 1 ngày (dùng 1 lần/tuần).', 'Protect streak failure once per week.', '{"streak": 21}', '🛡️'),
        ('Khế Ước Tri Thức', 'Knowledge Pact', 'Tăng 25% stats từ việc đọc sách.', 'Increase stat gain from reading by 25%.', '{"stat": {"wisdom": 45}}', '📜'),
        ('Sát Thủ Tập Trung', 'Focus Assassin', 'Xóa bỏ mọi thông báo điện thoại khi bật chế độ focus.', 'No distractions during focus mode.', '{"stat": {"focus": 70}}', '🎯'),
        ('Dấu Ấn Kỷ Luật', 'Mark of Discipline', 'Tự động hoàn thành 1 side quest nếu hoàn thành 2 main quest.', 'Auto-complete 1 side quest after 2 main quests.', '{"stat": {"discipline": 60}}', '⚖️'),
        ('Linh Hồn Khám Phá', 'Explorer\'s Soul', 'Nhận thêm 100 EXP khi tìm hiểu topic mới lạ.', 'Extra 100 EXP for exploration topics.', '{"exploration_quests": 10}', '🗺️'),
        ('Tiếng Gọi Chiến Binh', 'Warrior\'s Call', 'Tăng 20% sức mạnh từ các bài tập bodyweight.', 'Increase strength gain from bodyweight exercises by 20%.', '{"stat": {"strength": 40}}', '📣'),
        ('Sự Tĩnh Lặng Của Rừng', 'Forest Silence', 'Tăng tốc độ hồi phục Focus Capacity.', 'Faster Focus Capacity recovery.', '{"meditation_hours": 10}', '🌲'),
        ('Bản Năng Sinh Tồn', 'Survival Instinct', 'Không bị trừ EXP khi fail quest penalty.', 'No EXP loss on penalty quest failure.', '{"level": 25}', '🐺')
    ]
    
    session.execute(text("TRUNCATE TABLE skills CASCADE")) # Ensure fresh start
    for s in skills_data:
        session.execute(
            text("INSERT INTO skills (id, name_vi, name_en, description_vi, description_en, unlock_condition, icon) VALUES (:id, :n_vi, :n_en, :d_vi, :d_en, :cond, :icon)"),
            {"id": str(uuid.uuid4()), "n_vi": s[0], "n_en": s[1], "d_vi": s[2], "d_en": s[3], "cond": s[4], "icon": s[5]}
        )
    print(f"Restored {len(skills_data)} skills.")

    print("--- Restoring Rewards ---")
    rewards_data = [
        # Base
        ('Kẻ Thức Tỉnh', 'The Awakened', 'title', 'Danh hiệu mặc định khi bắt đầu.', 'Default title when starting.', '{"auto": true}', '👑', 'common'),
        ('Ngày Đầu Tiên', 'First Day', 'badge', 'Hoàn thành ngày đầu tiên.', 'Complete the first day.', '{"days_completed": 1}', '🌅', 'common'),
        ('Chuỗi 7 Ngày', '7-Day Streak', 'badge', 'Duy trì chuỗi 7 ngày liên tục.', 'Maintain a 7-day streak.', '{"streak": 7}', '🔥', 'rare'),
        ('Chuỗi 30 Ngày', '30-Day Streak', 'badge', 'Duy trì chuỗi 30 ngày liên tục.', 'Maintain a 30-day streak.', '{"streak": 30}', '🔥', 'epic'),
        ('Bóng Tối Cấp 10', 'Shadow Level 10', 'aura', 'Đạt cấp 10.', 'Reach level 10.', '{"level": 10}', '🌑', 'epic'),
        ('Bóng Tối Cấp 25', 'Shadow Level 25', 'aura', 'Đạt cấp 25.', 'Reach level 25.', '{"level": 25}', '🌑', 'legendary'),
        ('Đột Phá Kỷ Luật', 'Discipline Breakthrough', 'badge', 'Hoàn thành đột phá stat cap lần đầu.', 'Complete first stat cap breakthrough.', '{"breakthrough_completed": 1}', '⚡', 'legendary'),
        ('Thiền Giả', 'The Meditator', 'badge', 'Thiền 30 ngày liên tục.', 'Meditate for 30 consecutive days.', '{"meditation_streak": 30}', '🧘', 'rare'),
        ('Chiến Binh Thể Lực', 'Fitness Warrior', 'badge', 'Hoàn thành 100 quest fitness.', 'Complete 100 fitness quests.', '{"fitness_quests": 100}', '💪', 'epic'),
        ('Nhà Hiền Triết', 'The Sage', 'title', 'Đạt wisdom ≥ 80.', 'Reach wisdom ≥ 80.', '{"stat": {"wisdom": 80}}', '📚', 'legendary'),
        # Expanded
        ('Chúa Tể Bóng Tối', 'Shadow Lord', 'title', 'Danh hiệu dành cho bậc thầy bóng tối.', 'Title for the shadow master.', '{"level": 50}', '⚔️', 'legendary'),
        ('Thợ Săn Quái Vật', 'Monster Hunter', 'badge', 'Hoàn thành 500 quest tổng cộng.', 'Complete 500 total quests.', '{"total_quests": 500}', '🏹', 'epic'),
        ('Lửa Thiêng Vĩnh Cửu', 'Eternal Flame', 'aura', 'Duy trì 100 ngày streak.', 'Maintain a 100-day streak.', '{"streak": 100}', '💠', 'legendary'),
        ('Kiến Trúc Sư Cuộc Đời', 'Architect of Life', 'title', 'Hoàn thành 20 Challenge.', 'Complete 20 challenges.', '{"challenges_completed": 20}', '🏛️', 'epic'),
        ('Bàn Tay Thép', 'Iron Hand', 'badge', 'Đạt cấp 10 Discipline.', 'Reach Discipline level 10.', '{"stat": {"discipline": 100}}', '🫱', 'rare'),
        ('Trái Tim Rồng', 'Dragon Heart', 'aura', 'Đạt cấp 10 Stamina.', 'Reach Stamina level 10.', '{"stat": {"stamina": 100}}', '❤️', 'epic'),
        ('Đại Hiền Triết', 'Grand Sage', 'title', 'Đạt Wisdom & Knowledge cấp cao.', 'High Wisdom & Knowledge reached.', '{"stat": {"wisdom": 100, "knowledge": 100}}', '🧙', 'legendary'),
        ('Sát Thủ Tập Trung', 'Focus Master', 'badge', 'Hoàn thành 50 Deep Work sessions.', 'Complete 50 Deep Work sessions.', '{"focus_sessions": 50}', '🧘', 'rare'),
        ('Vương Miện Vinh Quang', 'Crown of Glory', 'aura', 'Hoàn thành mọi quest trong tuần.', 'Complete all quests in a week.', '{"weekly_completion": true}', '👑', 'epic'),
        ('Kẻ Phá Vỡ Giới Hạn', 'Limit Breaker', 'title', 'Hoàn thành Đột Phá Phase 5.', 'Complete Phase 5 Breakthrough.', '{"breakthrough_phase": 5}', '🌀', 'legendary')
    ]
    
    session.execute(text("TRUNCATE TABLE rewards CASCADE"))
    for r in rewards_data:
        session.execute(
            text("INSERT INTO rewards (id, name_vi, name_en, reward_type, description_vi, description_en, unlock_condition, icon, rarity) VALUES (:id, :n_vi, :n_en, :type, :d_vi, :d_en, :cond, :icon, :rarity)"),
            {"id": str(uuid.uuid4()), "n_vi": r[0], "n_en": r[1], "type": r[2], "d_vi": r[3], "d_en": r[4], "cond": r[5], "icon": r[6], "rarity": r[7]}
        )
    print(f"Restored {len(rewards_data)} rewards.")

    print("--- Restoring Challenges ---")
    challenges_data = [
        # Base
        ('7 Ngày Đọc Sách', '7-Day Reading', 'Đọc sách mỗi ngày trong 7 ngày liên tục.', 'Read every day for 7 consecutive days.', 'weekly', 7, '{"daily_reading": true}', '{"exp": 200, "badge": "bookworm"}', 1, 'wisdom'),
        ('14 Ngày Tiếng Anh', '14-Day English', 'Học tiếng Anh mỗi ngày trong 14 ngày.', 'Study English daily for 14 days.', 'monthly', 14, '{"daily_english": true}', '{"exp": 500, "stat": {"wisdom": 5}}', 1, 'wisdom'),
        ('30 Ngày Thể Lực', '30-Day Fitness', 'Tập thể lực mỗi ngày trong 30 ngày.', 'Exercise daily for 30 days.', 'monthly', 30, '{"daily_fitness": true}', '{"exp": 1000, "badge": "iron_body"}', 1, 'fitness'),
        ('5 Ngày Deep Work', '5-Day Deep Work', 'Deep work mỗi ngày trong 5 ngày.', 'Deep work daily for 5 days.', 'weekly', 5, '{"daily_deep_work": true}', '{"exp": 150, "stat": {"focus": 3}}', 3, 'focus'),
        ('21 Ngày Kỷ Luật', '21-Day Discipline', 'Hoàn thành tất cả quest trong 21 ngày.', 'Complete all quests for 21 days.', 'monthly', 21, '{"all_quests_daily": true}', '{"exp": 800, "stat": {"discipline": 8}}', 5, 'discipline'),
        ('7 Ngày Nhật Ký', '7-Day Journal', 'Viết nhật ký mỗi ngày trong 7 ngày.', 'Write journal entries for 7 days.', 'weekly', 7, '{"daily_journal": true}', '{"exp": 150, "stat": {"mental_resilience": 3}}', 1, 'discipline'),
        # Expanded
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
        ('Sự Thay Đổi Thầm Lặng', 'Silent Change', 'Dọn dẹp nhà cửa mỗi ngày trong 7 ngày.', 'Clean home daily for 7 days.', 'weekly', 7, '{"daily_cleaning": true}', '{"exp": 400, "stat": {"discipline": 5}}', 1, 'discipline')
    ]
    
    session.execute(text("TRUNCATE TABLE challenges CASCADE"))
    for c in challenges_data:
        session.execute(
            text("INSERT INTO challenges (id, name_vi, name_en, description_vi, description_en, challenge_type, duration_days, requirements, rewards, min_level, category) VALUES (:id, :n_vi, :n_en, :d_vi, :d_en, :type, :dur, :req, :rew, :min_lvl, :cat)"),
            {"id": str(uuid.uuid4()), "n_vi": c[0], "n_en": c[1], "d_vi": c[2], "d_en": c[3], "type": c[4], "dur": c[5], "req": c[6], "rew": c[7], "min_lvl": c[8], "cat": c[9]}
        )
    print(f"Restored {len(challenges_data)} challenges.")

    session.commit()
    print("--- Restoration Complete ---")

if __name__ == "__main__":
    restore()
    session.close()
