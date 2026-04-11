import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { statsService } from '../../services/apiServices';
import BreakthroughModal from '../../components/modals/BreakthroughModal/BreakthroughModal';
import './CharacterStats.scss';

const STAT_COLORS = {
  wisdom: '#a78bfa', confidence: '#f59e0b', strength: '#ef4444',
  discipline: '#3b82f6', focus: '#06b6d4', stamina: '#22c55e',
  knowledge: '#8b5cf6', consistency: '#14b8a6', mental_resilience: '#ec4899',
  social_courage: '#f97316',
};
const STAT_ICONS = {
  wisdom: <img src="/wisdom_spellbook_512.png" alt="wisdom" style={{width: '24px', height: '24px', verticalAlign: 'middle', objectFit: 'contain'}} />,
  confidence: <img src="/confidence_soul_fire_512.png" alt="confidence" style={{width: '24px', height: '24px', verticalAlign: 'middle', objectFit: 'contain'}} />,
  strength: <img src="/fitness_sword_512.png" alt="strength" style={{width: '24px', height: '24px', verticalAlign: 'middle', objectFit: 'contain'}} />,
  discipline: '🎯',
  focus: <img src="/focus_eye_512.png" alt="focus" style={{width: '24px', height: '24px', verticalAlign: 'middle', objectFit: 'contain'}} />,
  stamina: <img src="/fitness_sword_512.png" alt="stamina" style={{width: '24px', height: '24px', verticalAlign: 'middle', objectFit: 'contain'}} />,
  knowledge: '🔬', 
  consistency: '🔁', 
  mental_resilience: '🛡️', 
  social_courage: '🗣️',
};

export default function CharacterStats() {
  const { t } = useTranslation();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isBreakthroughOpen, setIsBreakthroughOpen] = useState(false);

  useEffect(() => {
    statsService.getAll()
      .then(res => setData(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="stats-loading"><div className="spinner" /><p>{t('common.loading')}</p></div>;

  const stats = data?.stats || [];
  const core = stats.filter(s => ['wisdom','confidence','strength','discipline','focus'].includes(s.stat_name));
  const extended = stats.filter(s => !['wisdom','confidence','strength','discipline','focus'].includes(s.stat_name));

  return (
    <div className="character-stats">
      <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }}>{t('stats.title')}</motion.h1>

      {data?.breakthrough_available && (
        <motion.div 
          className="bt-alert clickable" 
          initial={{ scale: 0.9 }} 
          animate={{ scale: 1 }}
          onClick={() => setIsBreakthroughOpen(true)}
        >
          ⚡ {t('stats.breakthroughAvailable')}
        </motion.div>
      )}

      <div className="stats-info">
        <span>{t('dashboard.phase')}: {data?.phase}</span>
        <span>{t('stats.cap')}: {data?.current_cap}</span>
      </div>

      <h2>Core Stats</h2>
      <div className="stats-list">
        {core.map((stat, i) => (
          <motion.div key={stat.stat_name} className="stat-row" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.08 }}>
            <div className="stat-row__info">
              <span className="stat-row__icon">{STAT_ICONS[stat.stat_name]}</span>
              <span className="stat-row__name">{t(`stats.${stat.stat_name}`)}</span>
              <span className="stat-row__value" style={{ color: STAT_COLORS[stat.stat_name] }}>{Math.floor(stat.current_value)} / {stat.cap}</span>
            </div>
            <div className="stat-row__bar-bg">
              <motion.div className="stat-row__bar-fill" style={{ background: STAT_COLORS[stat.stat_name] }} initial={{ width: 0 }} animate={{ width: `${(stat.current_value / stat.cap) * 100}%` }} transition={{ duration: 0.8, delay: 0.2 + i * 0.08 }} />
            </div>
          </motion.div>
        ))}
      </div>

      <h2>Extended Stats</h2>
      <div className="stats-list">
        {extended.map((stat, i) => (
          <motion.div key={stat.stat_name} className="stat-row" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.5 + i * 0.08 }}>
            <div className="stat-row__info">
              <span className="stat-row__icon">{STAT_ICONS[stat.stat_name] || '🔹'}</span>
              <span className="stat-row__name">{t(`stats.${stat.stat_name}`)}</span>
              <span className="stat-row__value" style={{ color: STAT_COLORS[stat.stat_name] || '#888' }}>{Math.floor(stat.current_value)} / {stat.cap}</span>
            </div>
            <div className="stat-row__bar-bg">
              <motion.div className="stat-row__bar-fill" style={{ background: STAT_COLORS[stat.stat_name] || '#888' }} initial={{ width: 0 }} animate={{ width: `${(stat.current_value / stat.cap) * 100}%` }} transition={{ duration: 0.8, delay: 0.7 + i * 0.08 }} />
            </div>
          </motion.div>
        ))}
      </div>
      
      <BreakthroughModal 
        isOpen={isBreakthroughOpen}
        onClose={() => setIsBreakthroughOpen(false)}
        onComplete={() => {
          setLoading(true);
          statsService.getAll()
            .then(res => setData(res.data))
            .finally(() => setLoading(false));
        }}
      />
    </div>
  );
}
