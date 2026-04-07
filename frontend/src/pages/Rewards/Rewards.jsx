import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import { rewardService } from '../../services/apiServices';
import './Rewards.scss';

const RARITY_COLORS = { common: '#9d9bb0', rare: '#4a9eff', epic: '#b44aff', legendary: '#ffd700' };

export default function Rewards() {
  const { t, i18n } = useTranslation();
  const [rewards, setRewards] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRewards = async () => {
      try {
        const response = await rewardService.getAll();
        setRewards(response.data);
      } catch (error) {
        console.error('Failed to fetch rewards:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchRewards();
  }, []);

  if (loading) return <div className="rewards-loading">{t('common.loading')}</div>;

  return (
    <div className="rewards-page">
      <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }}>{t('nav.rewards')}</motion.h1>
      <div className="rewards-grid">
        {rewards.map((r, i) => {
          const name = i18n.language === 'en' ? r.name_en : r.name_vi;
          const description = i18n.language === 'en' ? r.description_en : r.description_vi;

          return (
            <motion.div
              key={r.id}
              className={`reward-card ${!r.is_unlocked ? 'reward-card--locked' : ''}`}
              style={{ '--rarity-color': RARITY_COLORS[r.rarity] }}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: i * 0.05 }}
            >
              <span className="reward-card__icon">{r.icon}</span>
              <h3>{name}</h3>
              <p className="reward-card__desc">{description}</p>
              <span className="reward-card__type">{r.reward_type}</span>
              <span className="reward-card__rarity" style={{ color: RARITY_COLORS[r.rarity] }}>
                {r.rarity.toUpperCase()}
              </span>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
