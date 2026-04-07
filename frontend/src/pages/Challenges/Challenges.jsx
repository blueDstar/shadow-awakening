import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import './Challenges.scss';

export default function Challenges() {
  const { t } = useTranslation();
  const demoChallenges = [
    { name_vi: '7 ngày đọc sách liên tục', name_en: '7-day reading streak', type: 'weekly', days: 7, progress: 3, icon: '📚' },
    { name_vi: '14 ngày luyện tiếng Anh', name_en: '14-day English practice', type: 'monthly', days: 14, progress: 5, icon: '🗣️' },
    { name_vi: '30 ngày tăng thể lực nền', name_en: '30-day fitness foundation', type: 'monthly', days: 30, progress: 8, icon: '💪' },
    { name_vi: '5 ngày deep work', name_en: '5-day deep work challenge', type: 'weekly', days: 5, progress: 2, icon: '🧠' },
  ];

  return (
    <div className="challenges-page">
      <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }}>{t('challenges.title')}</motion.h1>
      <div className="challenge-list">
        {demoChallenges.map((ch, i) => (
          <motion.div key={i} className="challenge-item" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }}>
            <span className="challenge-item__icon">{ch.icon}</span>
            <div className="challenge-item__info">
              <h3>{ch.name_vi}</h3>
              <div className="challenge-item__bar"><div className="challenge-item__fill" style={{ width: `${(ch.progress / ch.days) * 100}%` }} /></div>
              <span className="challenge-item__progress">{ch.progress} / {ch.days} ngày</span>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
