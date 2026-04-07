import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import './Rewards.scss';

const DEMO_REWARDS = [
  { name_vi: 'Kẻ Thức Tỉnh', name_en: 'The Awakened', type: 'title', icon: '👑', rarity: 'common', unlocked: true },
  { name_vi: 'Ngày Đầu Tiên', name_en: 'First Day', type: 'badge', icon: '🌅', rarity: 'common', unlocked: true },
  { name_vi: 'Chuỗi 7 Ngày', name_en: '7-Day Streak', type: 'badge', icon: '🔥', rarity: 'rare', unlocked: false },
  { name_vi: 'Bóng Tối Cấp 10', name_en: 'Shadow Level 10', type: 'aura', icon: '🌑', rarity: 'epic', unlocked: false },
  { name_vi: 'Đột Phá Kỷ Luật', name_en: 'Discipline Breakthrough', type: 'badge', icon: '⚡', rarity: 'legendary', unlocked: false },
];

const RARITY_COLORS = { common: '#9d9bb0', rare: '#4a9eff', epic: '#b44aff', legendary: '#ffd700' };

export default function Rewards() {
  const { t, i18n } = useTranslation();
  const lang = i18n.language;

  return (
    <div className="rewards-page">
      <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }}>{t('nav.rewards')}</motion.h1>
      <div className="rewards-grid">
        {DEMO_REWARDS.map((r, i) => (
          <motion.div
            key={i}
            className={`reward-card ${!r.unlocked ? 'reward-card--locked' : ''}`}
            style={{ '--rarity-color': RARITY_COLORS[r.rarity] }}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: i * 0.08 }}
          >
            <span className="reward-card__icon">{r.icon}</span>
            <h3>{lang === 'vi' ? r.name_vi : r.name_en}</h3>
            <span className="reward-card__type">{r.type}</span>
            <span className="reward-card__rarity" style={{ color: RARITY_COLORS[r.rarity] }}>{r.rarity}</span>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
