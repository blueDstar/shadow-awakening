import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import { skillService } from '../../services/apiServices';
import './Skills.scss';

export default function Skills() {
  const { t, i18n } = useTranslation();
  const [skills, setSkills] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSkills = async () => {
      try {
        const response = await skillService.getAll();
        setSkills(response.data);
      } catch (error) {
        console.error('Failed to fetch skills:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchSkills();
  }, []);

  const [expandedId, setExpandedId] = useState(null);
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);

  useEffect(() => {
    const handleResize = () => setIsMobile(window.innerWidth <= 768);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  if (loading) return <div className="skills-loading">{t('common.loading')}</div>;

  const toggleExpand = (id) => {
    if (isMobile) {
      setExpandedId(expandedId === id ? null : id);
    }
  };

  const formatCondition = (conditionStr) => {
    if (!conditionStr) return t('skills.none');
    try {
      const parsed = JSON.parse(conditionStr);
      let parts = [];
      if (parsed.level) parts.push(`${t('dashboard.level')} ${parsed.level}`);
      if (parsed.stat) {
        Object.entries(parsed.stat).forEach(([k, v]) => {
          parts.push(`${t(`stats.${k}`)}: ${v}`);
        });
      }
      return parts.length > 0 ? parts.join(', ') : conditionStr;
    } catch {
      return conditionStr;
    }
  };

  return (
    <div className="skills-page">
      <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }}>{t('skills.title')}</motion.h1>
      <div className="skills-grid">
        {skills.map((skill, i) => {
          const name = i18n.language === 'en' ? skill.name_en : skill.name_vi;
          const description = i18n.language === 'en' ? skill.description_en : skill.description_vi;
          const isExpanded = !isMobile || expandedId === skill.id;
          
          return (
            <motion.div
              key={skill.id}
              className={`skill-card ${skill.is_locked ? 'skill-card--locked' : ''} ${isExpanded ? 'skill-card--expanded' : 'skill-card--collapsed'}`}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              onClick={() => toggleExpand(skill.id)}
            >
              <div className="skill-card__header">
                <div className="skill-card__icon">{skill.icon}</div>
                <div className="skill-card__title-group">
                  <h3 className="skill-card__name">{name}</h3>
                  <span className={`skill-card__status ${skill.is_locked ? '' : 'unlocked'}`}>
                    {skill.is_locked ? `🔒 ${t('skills.locked')}` : `✅ ${t('skills.unlocked')}`}
                  </span>
                </div>
                {isMobile && (
                  <span className={`skill-card__arrow ${isExpanded ? 'up' : 'down'}`}>
                    {isExpanded ? '▲' : '▼'}
                  </span>
                )}
              </div>

              {(isExpanded) && (
                <motion.div 
                  className="skill-card__details"
                  initial={isMobile ? { height: 0, opacity: 0 } : false}
                  animate={{ height: 'auto', opacity: 1 }}
                >
                  <p className="skill-card__desc">{description}</p>
                  <p className="skill-card__condition">
                    <strong>{t('skills.unlockCondition') || 'Yêu cầu'}: </strong> 
                    {formatCondition(skill.unlock_condition)}
                  </p>
                </motion.div>
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
