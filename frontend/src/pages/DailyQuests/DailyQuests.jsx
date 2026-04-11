import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { motion, AnimatePresence } from 'framer-motion';
import { questService } from '../../services/apiServices';
import BreakthroughModal from '../../components/modals/BreakthroughModal/BreakthroughModal';
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
  const [showHistory, setShowHistory] = useState(false);
  const [isBreakthroughOpen, setIsBreakthroughOpen] = useState(false);

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

  const handleReroll = async (questId) => {
    try {
      await questService.reroll(questId);
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

  const allQuests = questData?.quests || [];

  // Split into pending vs done
  const pendingQuests = allQuests.filter(q => q.status === 'pending');
  const doneQuests = allQuests.filter(q => q.status === 'completed' || q.status === 'failed');

  // Group pending by type
  const groupedPending = {};
  pendingQuests.forEach(q => {
    if (!groupedPending[q.quest_type]) groupedPending[q.quest_type] = [];
    groupedPending[q.quest_type].push(q);
  });

  // Group done by type
  const groupedDone = {};
  doneQuests.forEach(q => {
    if (!groupedDone[q.quest_type]) groupedDone[q.quest_type] = [];
    groupedDone[q.quest_type].push(q);
  });

  const renderQuestCard = (quest, i) => {
    const type = quest.quest_type;
    let statRewards = {};
    try { statRewards = JSON.parse(quest.stat_rewards || '{}'); } catch { }
    return (
      <motion.div
        key={quest.id}
        className={`quest-card quest-card--${quest.status}`}
        style={{ '--quest-color': QUEST_TYPE_COLORS[type] }}
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: 20 }}
        transition={{ delay: i * 0.04 }}
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
              {t('quests.difficulty')}: {'⭐'.repeat(Math.min(Math.ceil(quest.difficulty / 5), 10))}
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
                {completing === quest.id ? '⏳' : <img src="/sucess_quest_512.png" alt="complete" style={{ width: '35px', height: '35px' }} />} {t('quests.markComplete')}
              </button>
              {!quest.is_rerolled && (
                <button
                  className="quest-card__reroll-btn"
                  onClick={() => handleReroll(quest.id)}
                  title="Xoay nhiệm vụ (1 lần/ngày)"
                >
                  <img src="/roll_quest_512.png" alt="reroll" style={{ width: '35px', height: '35px' }} />
                </button>
              )}
              <button
                className="quest-card__fail-btn"
                onClick={() => handleFail(quest.id)}
              >
                <img src="/fail_quest_512.png" alt="fail" style={{ width: '35px', height: '35px' }} />
              </button>
            </>
          )}
          {quest.status === 'completed' && (
            <span className="quest-card__status quest-card__status--completed">
              <img src="/sucess_quest_512.png" alt="complete" style={{ width: '35px', height: '35px' }} /> {t('quests.complete')}
            </span>
          )}
          {quest.status === 'failed' && (
            <span className="quest-card__status quest-card__status--failed">
              <img src="/fail_quest_512.png" alt="fail" style={{ width: '35px', height: '35px' }} /> {t('quests.failed')}
            </span>
          )}
        </div>
      </motion.div>
    );
  };

  const renderQuestGroup = (grouped, quests) => {
    return Object.entries(grouped).map(([type, typeQuests]) => (
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
          <AnimatePresence>
            {typeQuests.map((quest, i) => renderQuestCard(quest, i))}
          </AnimatePresence>
        </div>
      </motion.div>
    ));
  };

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

      {questData?.breakthrough_available && (
        <motion.div
          className="bt-alert-banner"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          onClick={() => setIsBreakthroughOpen(true)}
        >
          <div className="bt-alert-banner__content">
            <span className="bt-alert-banner__icon">⚡</span>
            <span className="bt-alert-banner__text">{t('stats.breakthroughAvailable')}</span>
          </div>
          <span className="bt-alert-banner__action">{t('common.next')} ➔</span>
        </motion.div>
      )}


      {(questData?.can_refresh || questData?.day_completed) && (
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
            {refreshing ? '⌛' : <img src="/roll_quest_512.png" alt="reroll" style={{ width: '35px', height: '35px' }} />} {t('quests.refreshQuests')}
          </button>
        </motion.div>
      )}

      {/* Active (Pending) Quests */}
      <div className="quest-groups">
        {pendingQuests.length > 0
          ? renderQuestGroup(groupedPending, pendingQuests)
          : (
            <div className="no-quests no-quests--pending">
              <span className="no-quests__icon">
                <img
                  src="/complete_quest512.png"
                  alt="complete"
                  style={{
                    width: '100px',
                    height: '100px',
                    display: 'block',
                    margin: '0 auto'
                  }}
                />
              </span>
              <p>{doneQuests.length > 0 ? t('quests.allDoneForNow') : t('quests.noQuests')}</p>
            </div>
          )
        }
      </div>

      {/* History Toggle */}
      {doneQuests.length > 0 && (
        <div className="quest-history-section">
          <button
            className="quest-history-toggle"
            onClick={() => setShowHistory(v => !v)}
          >
            <span className="quest-history-toggle__icon">{showHistory ? '🔼' : '🔽'}</span>
            <span>
              {showHistory ? t('quests.hideHistory') : t('quests.showHistory')}
              {' '}({doneQuests.length})
            </span>
          </button>

          <AnimatePresence>
            {showHistory && (
              <motion.div
                className="quest-history-list"
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
              >
                {renderQuestGroup(groupedDone, doneQuests)}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      )}

      <BreakthroughModal
        isOpen={isBreakthroughOpen}
        onClose={() => setIsBreakthroughOpen(false)}
        onComplete={() => {
          setLoading(true);
          loadQuests();
        }}
      />
    </div>
  );
}
