// Mock data for demo without backend

export const MOCK_USER = {
  id: 'demo-user-001',
  username: 'shadow_hunter',
  email: 'hunter@shadow.dev',
  is_active: true,
};

export const MOCK_TOKEN = 'mock-jwt-token-shadow-awakening';

export const MOCK_DASHBOARD = {
  character_name: 'Shadow Hunter',
  title: 'Kẻ Thức Tỉnh',
  level: 7,
  current_exp: 680,
  exp_to_next_level: 1540,
  total_exp: 4200,
  aura: 'shadow_basic',
  stats: [
    { stat_name: 'wisdom', current_value: 38, cap: 100 },
    { stat_name: 'confidence', current_value: 22, cap: 100 },
    { stat_name: 'strength', current_value: 45, cap: 100 },
    { stat_name: 'discipline', current_value: 52, cap: 100 },
    { stat_name: 'focus', current_value: 30, cap: 100 },
    { stat_name: 'stamina', current_value: 40, cap: 100 },
    { stat_name: 'knowledge', current_value: 28, cap: 100 },
    { stat_name: 'consistency', current_value: 35, cap: 100 },
    { stat_name: 'mental_resilience', current_value: 18, cap: 100 },
    { stat_name: 'social_courage', current_value: 12, cap: 100 },
  ],
  stat_cap: 100,
  phase: 1,
  breakthrough_available: false,
  today_quests_total: 6,
  today_quests_completed: 2,
  today_quests_failed: 0,
  day_completed: false,
  overall_streak: 5,
  best_streak: 12,
  streaks: [
    { streak_type: 'overall', current_streak: 5, best_streak: 12 },
    { streak_type: 'reading', current_streak: 3, best_streak: 8 },
    { streak_type: 'english', current_streak: 2, best_streak: 5 },
    { streak_type: 'fitness', current_streak: 5, best_streak: 10 },
    { streak_type: 'deep_work', current_streak: 1, best_streak: 4 },
    { streak_type: 'journal', current_streak: 4, best_streak: 7 },
    { streak_type: 'research', current_streak: 0, best_streak: 3 },
  ],
  reset_countdown_seconds: 46800,
  quote_vi: 'Kỷ luật là cầu nối giữa mục tiêu và thành tựu.',
  quote_en: 'Discipline is the bridge between goals and accomplishment.',
};

export const MOCK_QUESTS = {
  quests: [
    {
      id: 'q1', title_vi: 'Chống đẩy 20 cái', title_en: 'Do 20 push-ups',
      description_vi: 'Hoàn thành 20 cái chống đẩy. Có thể chia thành nhiều set.',
      description_en: 'Complete 20 push-ups. You can split into multiple sets.',
      quest_type: 'main', category: 'fitness', difficulty: 3, exp_reward: 42,
      stat_rewards: '{"strength": 2, "discipline": 1}', status: 'completed', quest_date: new Date().toISOString().slice(0, 10), completed_at: new Date().toISOString(),
    },
    {
      id: 'q2', title_vi: 'Đọc 15 trang sách', title_en: 'Read 15 pages',
      description_vi: 'Đọc 15 trang từ sách bạn đang đọc. Ghi chú 1-2 insight.',
      description_en: 'Read 15 pages from your current book. Note 1-2 insights.',
      quest_type: 'main', category: 'wisdom', difficulty: 3, exp_reward: 42,
      stat_rewards: '{"wisdom": 2, "focus": 1}', status: 'completed', quest_date: new Date().toISOString().slice(0, 10), completed_at: new Date().toISOString(),
    },
    {
      id: 'q3', title_vi: 'Deep work 3 Pomodoro (25 phút)', title_en: 'Deep work 3 Pomodoro (25 minutes)',
      description_vi: 'Làm việc tập trung sâu 3 session Pomodoro, mỗi session 25 phút.',
      description_en: 'Complete 3 deep work Pomodoro sessions, 25 minutes each.',
      quest_type: 'side', category: 'focus', difficulty: 3, exp_reward: 22,
      stat_rewards: '{"focus": 3, "discipline": 1}', status: 'pending', quest_date: new Date().toISOString().slice(0, 10), completed_at: null,
    },
    {
      id: 'q4', title_vi: 'Học 12 từ tiếng Anh mới', title_en: 'Learn 12 new English words',
      description_vi: 'Học 12 từ vựng mới và viết ít nhất 2 câu ví dụ.',
      description_en: 'Learn 12 new vocabulary words and write at least 2 example sentences.',
      quest_type: 'side', category: 'wisdom', difficulty: 3, exp_reward: 22,
      stat_rewards: '{"wisdom": 1, "confidence": 1, "knowledge": 1}', status: 'pending', quest_date: new Date().toISOString().slice(0, 10), completed_at: null,
    },
    {
      id: 'q5', title_vi: 'Uống đủ 8 ly nước hôm nay', title_en: 'Drink 8 glasses of water today',
      description_vi: 'Uống ít nhất 8 ly nước trong ngày để duy trì sức khỏe.',
      description_en: 'Drink at least 8 glasses of water to stay healthy.',
      quest_type: 'habit', category: 'fitness', difficulty: 3, exp_reward: 14,
      stat_rewards: '{"stamina": 1}', status: 'pending', quest_date: new Date().toISOString().slice(0, 10), completed_at: null,
    },
    {
      id: 'q6', title_vi: 'Ghi lại 3 điều biết ơn hôm nay', title_en: 'Write 3 things you\'re grateful for today',
      description_vi: 'Viết ra 3 điều bạn cảm thấy biết ơn ngày hôm nay.',
      description_en: 'Write down 3 things you feel grateful for today.',
      quest_type: 'habit', category: 'focus', difficulty: 3, exp_reward: 14,
      stat_rewards: '{"mental_resilience": 1}', status: 'pending', quest_date: new Date().toISOString().slice(0, 10), completed_at: null,
    },
  ],
  total: 6, completed: 2, failed: 0, day_completed: false, can_refresh: false,
  quest_date: new Date().toISOString().slice(0, 10),
};

export const MOCK_STATS = {
  stats: MOCK_DASHBOARD.stats,
  current_cap: 100,
  phase: 1,
  breakthrough_available: false,
};

export const MOCK_STREAKS = { streaks: MOCK_DASHBOARD.streaks };

export const MOCK_SETTINGS = {
  language: 'vi',
  timezone: 'Asia/Ho_Chi_Minh',
  difficulty_preference: 'moderate',
  notification_enabled: true,
  daily_reset_hour: 0,
};

export const MOCK_JOURNAL = [
  {
    id: 'j1', reflection_date: new Date(Date.now() - 86400000).toISOString().slice(0, 10),
    content: 'Hôm nay hoàn thành được 5/6 quest. Cảm thấy năng lượng tốt sau khi tập thể lực buổi sáng.',
    mood: 'good', insights: 'Tập buổi sáng giúp tập trung tốt hơn cả ngày.',
    success_reasons: 'Dậy sớm, có kế hoạch rõ ràng', fail_reasons: 'Chưa đọc đủ sách',
    created_at: new Date(Date.now() - 86400000).toISOString(),
  },
  {
    id: 'j2', reflection_date: new Date(Date.now() - 172800000).toISOString().slice(0, 10),
    content: 'Ngày hôm nay khá căng thẳng nhưng vẫn duy trì được kỷ luật.',
    mood: 'neutral', insights: 'Stress không phải lý do để bỏ cuộc.',
    success_reasons: 'Kiên trì dù mệt', fail_reasons: '',
    created_at: new Date(Date.now() - 172800000).toISOString(),
  },
];

export const MOCK_BREAKTHROUGH = {
  available: false, current_cap: 100, next_cap: 200, phase: 1, active_trial: null,
};
