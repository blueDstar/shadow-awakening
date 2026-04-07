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

  if (loading) return <div className="skills-loading">{t('common.loading')}</div>;

  return (
    <div className="skills-page">
      <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }}>{t('skills.title')}</motion.h1>
      <div className="skills-grid">
        {skills.map((skill, i) => {
          const name = i18n.language === 'en' ? skill.name_en : skill.name_vi;
          const description = i18n.language === 'en' ? skill.description_en : skill.description_vi;
          
          return (
            <motion.div
              key={skill.id}
              className={`skill-card ${skill.is_locked ? 'skill-card--locked' : ''}`}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
            >
              <div className="skill-card__icon">{skill.icon}</div>
              <h3 className="skill-card__name">{name}</h3>
              <p className="skill-card__desc">{description}</p>
              <p className="skill-card__condition">{skill.unlock_condition}</p>
              <span className={`skill-card__status ${skill.is_locked ? '' : 'unlocked'}`}>
                {skill.is_locked ? `🔒 ${t('skills.locked')}` : `✅ ${t('skills.unlocked')}`}
              </span>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
