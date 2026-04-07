import api from './api';
import {
  MOCK_USER, MOCK_TOKEN, MOCK_DASHBOARD, MOCK_QUESTS,
  MOCK_STATS, MOCK_STREAKS, MOCK_SETTINGS, MOCK_JOURNAL, MOCK_BREAKTHROUGH,
} from './mockData';

// Set to true to use mock data (no backend needed)
const USE_MOCK = false;

function mockRes(data) {
  return Promise.resolve({ data });
}

export const authService = USE_MOCK ? {
  register: () => mockRes({ access_token: MOCK_TOKEN, token_type: 'bearer', user_id: MOCK_USER.id }),
  login: () => mockRes({ access_token: MOCK_TOKEN, token_type: 'bearer', user_id: MOCK_USER.id }),
  getMe: () => mockRes(MOCK_USER),
  onboarding: () => mockRes({ status: 'ok' }),
} : {
  register: (data) => api.post('/api/auth/register', data),
  login: (data) => api.post('/api/auth/login', data),
  getMe: () => api.get('/api/auth/me'),
  onboarding: (data) => api.post('/api/auth/onboarding', data),
};

export const dashboardService = USE_MOCK ? {
  getSummary: () => mockRes(MOCK_DASHBOARD),
  getResetCountdown: () => mockRes({ reset_countdown_seconds: 46800 }),
} : {
  getSummary: () => api.get('/api/dashboard/summary'),
  getResetCountdown: () => api.get('/api/dashboard/reset-countdown'),
};

export const questService = USE_MOCK ? {
  getToday: () => mockRes(MOCK_QUESTS),
  complete: (questId) => {
    const q = MOCK_QUESTS.quests.find(x => x.id === questId);
    if (q) { q.status = 'completed'; q.completed_at = new Date().toISOString(); MOCK_QUESTS.completed++; }
    return mockRes({ status: 'completed', exp_earned: 42, stat_rewards: {}, leveled_up: false, new_level: 7, day_completed: false });
  },
  fail: (questId) => {
    const q = MOCK_QUESTS.quests.find(x => x.id === questId);
    if (q) { q.status = 'failed'; MOCK_QUESTS.failed++; }
    return mockRes({ status: 'failed' });
  },
  getHistory: () => mockRes([]),
} : {
  getToday: () => api.get('/api/quests/today'),
  complete: (questId) => api.post(`/api/quests/${questId}/complete`),
  fail: (questId, reason) => api.post(`/api/quests/${questId}/fail`, null, { params: { fail_reason: reason } }),
  getHistory: (limit = 30) => api.get('/api/quests/history', { params: { limit } }),
};

export const statsService = USE_MOCK ? {
  getAll: () => mockRes(MOCK_STATS),
} : {
  getAll: () => api.get('/api/stats'),
};

export const streakService = USE_MOCK ? {
  getAll: () => mockRes(MOCK_STREAKS),
} : {
  getAll: () => api.get('/api/streaks'),
};

export const breakthroughService = USE_MOCK ? {
  getStatus: () => mockRes(MOCK_BREAKTHROUGH),
  start: () => mockRes({ trial_id: 'demo', from_cap: 100, to_cap: 200, phase: 2 }),
  complete: () => mockRes({ new_cap: 200, new_phase: 2 }),
} : {
  getStatus: () => api.get('/api/breakthrough/status'),
  start: () => api.post('/api/breakthrough/start'),
  complete: () => api.post('/api/breakthrough/complete'),
};

export const journalService = USE_MOCK ? {
  getAll: () => mockRes(MOCK_JOURNAL),
  create: (data) => { MOCK_JOURNAL.unshift({ ...data, id: 'j' + Date.now(), reflection_date: new Date().toISOString().slice(0, 10), created_at: new Date().toISOString() }); return mockRes({ id: 'new', status: 'created' }); },
  getByDate: () => mockRes(null),
} : {
  getAll: (limit = 30) => api.get('/api/journal', { params: { limit } }),
  create: (data) => api.post('/api/journal', data),
  getByDate: (date) => api.get(`/api/journal/${date}`),
};

export const settingsService = USE_MOCK ? {
  get: () => mockRes(MOCK_SETTINGS),
  updateLanguage: (lang) => { MOCK_SETTINGS.language = lang; return mockRes({ language: lang }); },
  updateTimezone: (tz) => mockRes({ timezone: tz }),
} : {
  get: () => api.get('/api/settings'),
  updateLanguage: (language) => api.put('/api/settings/language', null, { params: { language } }),
  updateTimezone: (tz) => api.put('/api/settings/timezone', null, { params: { tz } }),
};
