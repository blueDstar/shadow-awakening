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

  const [expandedId, setExpandedId] = useState(null);
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);

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

    const handleResize = () => setIsMobile(window.innerWidth <= 768);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const handleEquip = async (e, id, name) => {
    e.stopPropagation(); // Prevents card collapse
    try {
      await rewardService.equip(id);
      alert(t('rewards.equipped', { defaultValue: `Đã trang bị ${name}!` }));
    } catch (error) {
      console.error('Failed to equip reward', error);
    }
  };

  if (loading) return <div className="rewards-loading">{t('common.loading')}</div>;

  const toggleExpand = (id) => {
    if (isMobile) {
      setExpandedId(expandedId === id ? null : id);
    }
  };

  return (
    <div className="rewards-page">
      <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }}>{t('nav.rewards')}</motion.h1>
      <div className="rewards-grid">
        {rewards.map((r, i) => {
          const name = i18n.language === 'en' ? r.name_en : r.name_vi;
          const description = i18n.language === 'en' ? r.description_en : r.description_vi;
          const isExpanded = !isMobile || expandedId === r.id;

          return (
            <motion.div
              key={r.id}
              className={`reward-card ${!r.is_unlocked ? 'reward-card--locked' : ''} ${isExpanded ? 'reward-card--expanded' : 'reward-card--collapsed'}`}
              style={{ '--rarity-color': RARITY_COLORS[r.rarity] }}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: i * 0.05 }}
              onClick={() => toggleExpand(r.id)}
            >
              <div className="reward-card__header">
                <span className="reward-card__icon">{r.icon}</span>
                <div className="reward-card__title-group">
                  <h3>{name}</h3>
                  <span className="reward-card__rarity" style={{ color: RARITY_COLORS[r.rarity] }}>
                    {r.rarity.toUpperCase()}
                  </span>
                </div>
                {isMobile && (
                  <span className={`reward-card__arrow ${isExpanded ? 'up' : 'down'}`}>
                    {isExpanded ? '▲' : '▼'}
                  </span>
                )}
              </div>

              {isExpanded && (
                <motion.div 
                  className="reward-card__details"
                  initial={isMobile ? { height: 0, opacity: 0 } : false}
                  animate={{ height: 'auto', opacity: 1 }}
                >
                  <p className="reward-card__desc">{description}</p>
                  <div className="reward-card__meta">
                    <span className="reward-card__type">{r.reward_type}</span>
                    {r.is_unlocked && (
                      <button 
                        className="reward-card__equip-btn" 
                        onClick={(e) => handleEquip(e, r.id, name)}
                      >
                        {t('rewards.equip', { defaultValue: 'Trang bị' })}
                      </button>
                    )}
                  </div>
                </motion.div>
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
