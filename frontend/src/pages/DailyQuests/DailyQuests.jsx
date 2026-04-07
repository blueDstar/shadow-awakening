import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { motion, AnimatePresence } from 'framer-motion';
import { questService } from '../../services/apiServices';
import './DailyQuests.scss';

const QUEST_TYPE_COLORS = {
  main: '#b44aff', side: '#4a9eff', habit: '#4aff9f',
  challenge: '#ffd700', penalty: '#ff4a6a', special: '#ff4a8d',
  breakthrough: '#b44aff',
};

const QUEST_TYPE_ICONS = {
  main: '⚔️', side: '🗡️', habit: '🔄', challenge: '🏆',
  penalty: '⚠️', special: '✨', breakthrough: '💥',
};

export default function DailyQuests() {
  const { t, i18n } = useTranslation();
  const lang = i18n.language;
  const [questData, setQuestData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [completing, setCompleting] = useState(null);
  const [levelUp, setLevelUp] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => { loadQuests(); }, []);

  const loadQuests = async () => {
    try {
      const res = await questService.getToday();
      setQuestData(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    try {
      const res = await questService.refresh();
      setQuestData(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setRefreshing(false);
    }
  };

  const handleComplete = async (questId) => {
    setCompleting(questId);
    try {
      const res = await questService.complete(questId);
      if (res.data.leveled_up) {
        setLevelUp(res.data.new_level);
        setTimeout(() => setLevelUp(null), 3000);
      }
      await loadQuests();
    } catch (err) {
      console.error(err);
    } finally {
      setCompleting(null);
    }
  };

  const handleFail = async (questId) => {
    try {
      await questService.fail(questId, 'forgot');
      await loadQuests();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="quests-loading">
        <div className="quests-loading__spinner" />
        <p>{t('common.loading')}</p>
      </div>
    );
  }

  const quests = questData?.quests || [];
  const grouped = {};
  quests.forEach(q => {
    if (!grouped[q.quest_type]) grouped[q.quest_type] = [];
    grouped[q.quest_type].push(q);
  });

  return (
    <div className="daily-quests">
      {/* Level Up Animation */}
      <AnimatePresence>
        {levelUp && (
          <motion.div
            className="level-up-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <motion.div
              className="level-up-overlay__content"
              initial={{ scale: 0.5, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 1.5, opacity: 0 }}
              transition={{ type: 'spring', stiffness: 200 }}
            >
              <div className="level-up-overlay__icon">⚡</div>
              <h2>{t('levelUp.title')}</h2>
              <p>{t('levelUp.message', { level: levelUp })}</p>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      <motion.div
        className="daily-quests__header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1>{t('quests.title')}</h1>
        <div className="daily-quests__progress">
          <div className="daily-quests__progress-bar">
            <motion.div
              className="daily-quests__progress-fill"
              initial={{ width: 0 }}
              animate={{ width: `${questData?.total > 0 ? (questData.completed / questData.total) * 100 : 0}%` }}
            />
          </div>
          <span>{questData?.completed || 0} / {questData?.total || 0}</span>
        </div>
      </motion.div>

      {questData?.can_refresh && (
        <motion.div
          className="day-completed-banner"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          <div className="day-completed-banner__info">
            <span className="day-completed-banner__icon">🔥</span>
            <span>{questData?.day_completed ? t('quests.allCompleted') : t('quests.readyForMore')}</span>
          </div>
          
          <button 
            className="day-completed-banner__refresh-btn"
            onClick={handleRefresh}
            disabled={refreshing}
          >
            {refreshing ? '⌛' : '🔄'} {t('quests.refreshQuests')}
          </button>
        </motion.div>
      )}

      <div className="quest-groups">
        {Object.entries(grouped).map(([type, typeQuests]) => (
          <motion.div
            key={type}
            className="quest-group"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className="quest-group__header" style={{ borderLeftColor: QUEST_TYPE_COLORS[type] }}>
              <span className="quest-group__icon">{QUEST_TYPE_ICONS[type]}</span>
              <span className="quest-group__title">{t(`quests.${type}`)}</span>
              <span className="quest-group__count">{typeQuests.length}</span>
            </div>

            <div className="quest-group__list">
              {typeQuests.map((quest, i) => {
                const statRewards = JSON.parse(quest.stat_rewards || '{}');
                return (
                  <motion.div
                    key={quest.id}
                    className={`quest-card quest-card--${quest.status}`}
                    style={{ '--quest-color': QUEST_TYPE_COLORS[type] }}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.05 }}
                  >
                    <div className="quest-card__content">
                      <h4 className="quest-card__title">
                        {lang === 'vi' ? quest.title_vi : quest.title_en}
                      </h4>
                      <p className="quest-card__desc">
                        {lang === 'vi' ? quest.description_vi : quest.description_en}
                      </p>
                      <div className="quest-card__meta">
                        <span className="quest-card__exp">+{quest.exp_reward} EXP</span>
                        <span className="quest-card__difficulty">
                          {t('quests.difficulty')}: {'⭐'.repeat(Math.min(quest.difficulty, 5))}
                        </span>
                        {Object.entries(statRewards).map(([stat, val]) => (
                          <span key={stat} className="quest-card__stat-reward">
                            +{val} {t(`stats.${stat}`)}
                          </span>
                        ))}
                      </div>
                    </div>

                    <div className="quest-card__actions">
                      {quest.status === 'pending' && (
                        <>
                          <button
                            className="quest-card__complete-btn"
                            onClick={() => handleComplete(quest.id)}
                            disabled={completing === quest.id}
                          >
                            {completing === quest.id ? '⏳' : '✅'} {t('quests.markComplete')}
                          </button>
                          <button
                            className="quest-card__fail-btn"
                            onClick={() => handleFail(quest.id)}
                          >
                            ❌
                          </button>
                        </>
                      )}
                      {quest.status === 'completed' && (
                        <span className="quest-card__status quest-card__status--completed">
                          ✅ {t('quests.complete')}
                        </span>
                      )}
                      {quest.status === 'failed' && (
                        <span className="quest-card__status quest-card__status--failed">
                          ❌ {t('quests.failed')}
                        </span>
                      )}
                    </div>
                  </motion.div>
                );
              })}
            </div>
          </motion.div>
        ))}
      </div>

      {quests.length === 0 && (
        <div className="no-quests">
          <span className="no-quests__icon">📜</span>
          <p>{t('quests.noQuests')}</p>
        </div>
      )}
    </div>
  );
}
