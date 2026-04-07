import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import { challengeService } from '../../services/apiServices';
import './Challenges.scss';

export default function Challenges() {
  const { t, i18n } = useTranslation();
  const [challenges, setChallenges] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchChallenges = async () => {
      try {
        const response = await challengeService.getAll();
        setChallenges(response.data);
      } catch (error) {
        console.error('Failed to fetch challenges:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchChallenges();
  }, []);

  if (loading) return <div className="challenges-loading">{t('common.loading')}</div>;

  return (
    <div className="challenges-page">
      <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }}>{t('challenges.title')}</motion.h1>
      <div className="challenge-list">
        {challenges.map((ch, i) => {
          const name = i18n.language === 'en' ? ch.name_en : ch.name_vi;
          const progressPercent = Math.min(100, (ch.days_completed / ch.duration_days) * 100);

          return (
            <motion.div 
              key={ch.id} 
              className={`challenge-item ${ch.is_active ? 'challenge-item--active' : ''}`}
              initial={{ opacity: 0, y: 20 }} 
              animate={{ opacity: 1, y: 0 }} 
              transition={{ delay: i * 0.05 }}
            >
              <span className="challenge-item__icon">{'🏆'}</span>
              <div className="challenge-item__info">
                <h3>{name}</h3>
                <div className="challenge-item__bar">
                  <div 
                    className="challenge-item__fill" 
                    style={{ width: `${progressPercent}%` }} 
                  />
                </div>
                <span className="challenge-item__progress">
                  {ch.days_completed} / {ch.duration_days} {t('common.days')}
                </span>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
