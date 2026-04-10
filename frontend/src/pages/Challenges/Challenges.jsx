import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import { challengeService } from '../../services/apiServices';
import './Challenges.scss';

export default function Challenges() {
  const { t, i18n } = useTranslation();
  const [challenges, setChallenges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedId, setExpandedId] = useState(null);
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);

  useEffect(() => {
    const handleResize = () => setIsMobile(window.innerWidth <= 768);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

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

  const toggleExpand = (id) => {
    if (isMobile) {
      setExpandedId(expandedId === id ? null : id);
    }
  };

  return (
    <div className="challenges-page">
      <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }}>{t('challenges.title')}</motion.h1>
      <div className="challenge-list">
        {challenges.map((ch, i) => {
          const name = i18n.language === 'en' ? ch.name_en : ch.name_vi;
          const description = i18n.language === 'en' ? ch.description_en : ch.description_vi;
          const progressPercent = Math.min(100, (ch.days_completed / ch.duration_days) * 100);
          const isExpanded = !isMobile || expandedId === ch.id;

          return (
            <motion.div 
              key={ch.id} 
              className={`challenge-item ${ch.is_active ? 'challenge-item--active' : ''} ${isExpanded ? 'challenge-item--expanded' : 'challenge-item--collapsed'}`}
              initial={{ opacity: 0, y: 20 }} 
              animate={{ opacity: 1, y: 0 }} 
              transition={{ delay: i * 0.05 }}
              onClick={() => toggleExpand(ch.id)}
              style={{ cursor: isMobile ? 'pointer' : 'default' }}
            >
              <div className="challenge-item__header">
                <span className="challenge-item__icon">{'🏆'}</span>
                <div className="challenge-item__title-group">
                  <h3>{name}</h3>
                  <div className="challenge-item__bar-container">
                    <div className="challenge-item__bar">
                      <div 
                        className="challenge-item__fill" 
                        style={{ width: `${progressPercent}%` }} 
                      />
                    </div>
                    <span className="challenge-item__progress">
                      {ch.days_completed}/{ch.duration_days} {t('common.days')}
                    </span>
                  </div>
                </div>
                {isMobile && (
                  <span className={`challenge-item__arrow ${isExpanded ? 'up' : 'down'}`}>
                    {isExpanded ? '▲' : '▼'}
                  </span>
                )}
              </div>

              {isExpanded && (
                <motion.div 
                  className="challenge-item__details"
                  initial={isMobile ? { height: 0, opacity: 0 } : false}
                  animate={{ height: 'auto', opacity: 1 }}
                >
                  <p className="challenge-item__desc">{description}</p>
                </motion.div>
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
