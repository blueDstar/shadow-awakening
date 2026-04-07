import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import './Skills.scss';

const SKILLS = [
  { key: 'focusMode', icon: '🧠', condition: 'Level 5 + Focus ≥ 30', locked: true },
  { key: 'researchMode', icon: '🔬', condition: 'Level 10 + Knowledge ≥ 40', locked: true },
  { key: 'shadowStreak', icon: '🔥', condition: '7-day streak', locked: true },
  { key: 'eliteChain', icon: '⛓️', condition: '14-day streak', locked: true },
  { key: 'breakthroughTrial', icon: '💥', condition: 'All core stats ≥ cap', locked: true },
  { key: 'insightVision', icon: '👁️', condition: 'Level 15 + Wisdom ≥ 60', locked: true },
  { key: 'disciplineLock', icon: '🔒', condition: 'Discipline ≥ 50', locked: true },
  { key: 'recoveryProtocol', icon: '💚', condition: 'Complete 3 penalty quests', locked: true },
];

export default function Skills() {
  const { t } = useTranslation();

  return (
    <div className="skills-page">
      <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }}>{t('skills.title')}</motion.h1>
      <div className="skills-grid">
        {SKILLS.map((skill, i) => (
          <motion.div
            key={skill.key}
            className={`skill-card ${skill.locked ? 'skill-card--locked' : ''}`}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.08 }}
          >
            <div className="skill-card__icon">{skill.icon}</div>
            <h3 className="skill-card__name">{t(`skills.${skill.key}`)}</h3>
            <p className="skill-card__condition">{skill.condition}</p>
            <span className={`skill-card__status ${skill.locked ? '' : 'unlocked'}`}>
              {skill.locked ? `🔒 ${t('skills.locked')}` : `✅ ${t('skills.unlocked')}`}
            </span>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
