import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { dashboardService, questService } from '../../services/apiServices';
import './Dashboard.scss';

const STAT_COLORS = {
  wisdom: '#a78bfa', confidence: '#f59e0b', strength: '#ef4444',
  discipline: '#3b82f6', focus: '#06b6d4', stamina: '#22c55e',
  knowledge: '#8b5cf6', consistency: '#14b8a6', mental_resilience: '#ec4899',
  social_courage: '#f97316',
};

const STAT_ICONS = {
  wisdom: '📚', confidence: '💪', strength: '⚔️',
  discipline: '🎯', focus: '🧠', stamina: '🏃',
  knowledge: '🔬', consistency: '🔁', mental_resilience: '🛡️',
  social_courage: '🗣️',
};

export default function Dashboard() {
  const { t } = useTranslation();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [countdown, setCountdown] = useState(0);

  useEffect(() => {
    loadDashboard();
  }, []);

  useEffect(() => {
    if (countdown <= 0) return;
    const timer = setInterval(() => {
      setCountdown((c) => Math.max(0, c - 1));
    }, 1000);
    return () => clearInterval(timer);
  }, [countdown]);

  const loadDashboard = async () => {
    try {
      const res = await dashboardService.getSummary();
      setData(res.data);
      setCountdown(res.data.reset_countdown_seconds);
    } catch (err) {
      console.error('Dashboard load failed:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatCountdown = (seconds) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
  };

  const expPercent = data ? Math.min((data.current_exp / data.exp_to_next_level) * 100, 100) : 0;
  const coreStats = data?.stats?.filter(s => ['wisdom', 'confidence', 'strength', 'discipline', 'focus'].includes(s.stat_name)) || [];

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="dashboard-loading__spinner" />
        <p>{t('common.loading')}</p>
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="dashboard">
      {/* Header */}
      <motion.div
        className="dashboard__header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="dashboard__welcome">
          <h1 className="dashboard__title">{t('dashboard.welcomeBack')}, <span className="glow-text">{data.character_name}</span></h1>
          <p className="dashboard__quote">"{data.quote_vi}"</p>
        </div>
        <div className="dashboard__countdown">
          <span className="dashboard__countdown-label">{t('dashboard.resetCountdown')}</span>
          <span className="dashboard__countdown-time">{formatCountdown(countdown)}</span>
        </div>
      </motion.div>

      {/* Character Card */}
      <motion.div
        className="dashboard__character-card"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <div className="shadow-fire-bg" />
        <div className="character-info">
          <div className="character-info__avatar">
            <div className="character-info__avatar-glow" />
            <span className="character-info__avatar-icon">🌑</span>
          </div>
          <div className="character-info__details">
            <h2 className="character-info__name">{data.character_name}</h2>
            <p className="character-info__title">{data.title}</p>
            <div className="character-info__meta">
              <span className="character-info__level">{t('dashboard.level')} {data.level}</span>
              <span className="character-info__phase">{t('dashboard.phase')} {data.phase}</span>
              <span className="character-info__cap">{t('dashboard.statCap')}: {data.stat_cap}</span>
            </div>
          </div>
        </div>

        {/* EXP Bar */}
        <div className="exp-section">
          <div className="exp-section__header">
            <span>{t('common.exp')}</span>
            <span>{data.current_exp} / {data.exp_to_next_level}</span>
          </div>
          <div className="exp-bar">
            <motion.div
              className="exp-bar__fill"
              initial={{ width: 0 }}
              animate={{ width: `${expPercent}%` }}
              transition={{ duration: 1, ease: 'easeOut', delay: 0.3 }}
            />
          </div>
        </div>
      </motion.div>

      {/* Stats + Today + Streaks Grid */}
      <div className="dashboard__grid">
        {/* Today's Status */}
        <motion.div
          className={`dashboard__today-card ${data.day_completed ? 'dashboard__today-card--completed' : ''}`}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <h3>{t('dashboard.todayStatus')}</h3>
          {data.day_completed && (
            <div className="today-conquered">
              <span className="today-conquered__icon">🔥</span>
              <span className="today-conquered__text">{t('dashboard.dayConquered')}</span>
            </div>
          )}
          <div className="today-progress">
            <div className="today-progress__bar">
              <motion.div
                className="today-progress__fill"
                initial={{ width: 0 }}
                animate={{ width: `${data.today_quests_total > 0 ? (data.today_quests_completed / data.today_quests_total) * 100 : 0}%` }}
                transition={{ duration: 0.8, delay: 0.4 }}
              />
            </div>
            <span className="today-progress__text">
              {data.today_quests_completed} / {data.today_quests_total} {t('dashboard.questsCompleted')}
            </span>
          </div>
        </motion.div>

        {/* Streak Card */}
        <motion.div
          className="dashboard__streak-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <h3>{t('streak.title')}</h3>
          <div className="streak-display">
            <div className="streak-display__main">
              <span className={`streak-display__flame ${data.overall_streak > 0 ? 'active' : ''}`}>🔥</span>
              <span className="streak-display__number">{data.overall_streak}</span>
              <span className="streak-display__label">{t('streak.days')}</span>
            </div>
            <div className="streak-display__best">
              <span>{t('streak.best')}: {data.best_streak} {t('streak.days')}</span>
            </div>
          </div>
          <div className="streak-list">
            {data.streaks?.filter(s => s.streak_type !== 'overall').map((s) => (
              <div key={s.streak_type} className="streak-item">
                <span className="streak-item__label">{t(`streak.${s.streak_type}`)}</span>
                <span className="streak-item__value">{s.current_streak}</span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Core Stats */}
        <motion.div
          className="dashboard__stats-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <h3>{t('stats.title')}</h3>
          {data.breakthrough_available && (
            <div className="breakthrough-alert">⚡ {t('stats.breakthroughAvailable')}</div>
          )}
          <div className="stats-grid">
            {coreStats.map((stat, i) => (
              <motion.div
                key={stat.stat_name}
                className="stat-item"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + i * 0.1 }}
              >
                <div className="stat-item__header">
                  <span className="stat-item__icon">{STAT_ICONS[stat.stat_name]}</span>
                  <span className="stat-item__name">{t(`stats.${stat.stat_name}`)}</span>
                  <span className="stat-item__value" style={{ color: STAT_COLORS[stat.stat_name] }}>
                    {Math.floor(stat.current_value)}/{stat.cap}
                  </span>
                </div>
                <div className="stat-item__bar">
                  <motion.div
                    className="stat-item__fill"
                    style={{ background: STAT_COLORS[stat.stat_name] }}
                    initial={{ width: 0 }}
                    animate={{ width: `${Math.min((stat.current_value / stat.cap) * 100, 100)}%` }}
                    transition={{ duration: 0.8, delay: 0.6 + i * 0.1 }}
                  />
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
