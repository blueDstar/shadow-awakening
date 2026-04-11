import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import { breakthroughService } from '../../../services/apiServices';
import './BreakthroughModal.scss';

export default function BreakthroughModal({ isOpen, onClose, onComplete }) {
  const { t, i18n } = useTranslation();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (isOpen) {
      loadStatus();
    }
  }, [isOpen]);

  const loadStatus = async () => {
    setLoading(true);
    try {
      const res = await breakthroughService.getStatus();
      setData(res.data);
    } catch (err) {
      console.error('Failed to load breakthrough status:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleStart = async () => {
    try {
      await breakthroughService.start();
      loadStatus();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to start ritual');
    }
  };

  const handleSelectOption = async (optionId) => {
    try {
      await breakthroughService.selectOption(optionId);
      loadStatus();
    } catch (err) {
      alert('Failed to select option');
    }
  };

  const handleComplete = async () => {
    setSubmitting(true);
    try {
      const res = await breakthroughService.complete();
      onComplete(res.data);
      onClose();
    } catch (err) {
      alert(err.response?.data?.detail || 'Ritual requirements not met yet');
    } finally {
      setSubmitting(false);
    }
  };

  if (!isOpen) return null;

  const ritual = data?.ritual_template;
  const trial = data?.active_trial;
  const isAvailable = data?.available && !trial;
  const isVi = i18n.language === 'vi';

  return (
    <AnimatePresence>
      <div className="breakthrough-overlay" onClick={onClose}>
        <motion.div 
          className="breakthrough-modal"
          initial={{ scale: 0.9, opacity: 0, y: 20 }}
          animate={{ scale: 1, opacity: 1, y: 0 }}
          exit={{ scale: 0.9, opacity: 0, y: 20 }}
          onClick={(e) => e.stopPropagation()}
        >
          <button className="breakthrough-modal__close-btn" onClick={onClose}>&times;</button>
          
          <div className="breakthrough-modal__body">
            {loading ? (
              <div className="loading-spinner" />
            ) : isAvailable ? (
              <div className="start-phase">
                <div className="ritual-preview">
                  <img src="/breakthrough_gate_512.png" alt="Gate" className="ritual-gate-img" />
                  <h3>{isVi ? ritual?.title_vi : ritual?.title_en}</h3>
                  <div className="unlock-label">
                    {t('breakthrough.performToUnlock')}: {data.next_phase}
                  </div>
                  <p>{t('breakthrough.evolutionWarning')}</p>
                </div>
                <button className="start-btn" onClick={handleStart}>
                  {t('breakthrough.start')}
                </button>
              </div>
            ) : trial && ritual ? (
              <div className="ritual-progress">
                {/* Foundation */}
                <section className="ritual-section">
                  <h4><span className="icon">🛡️</span> {t('breakthrough.foundation')}</h4>
                  <div className="requirement-item">
                    <span>{t(`breakthrough.req.${ritual.foundation?.type || 'streak'}`)}: {ritual.foundation?.target || 0} {t('streak.days')}</span>
                    <span className="status">{(trial.progress?.streak || 0) >= (ritual.foundation?.target || 0) ? '✅' : '⏳'}</span>
                  </div>
                </section>

                {/* Mandatory */}
                <section className="ritual-section">
                  <h4><span className="icon">⚔️</span> {t('breakthrough.mandatory')}</h4>
                  {ritual.mandatory?.map((req, i) => (
                    <div key={i} className="requirement-item">
                      <span>{t(`breakthrough.req.${req.type}`)}: {trial.progress?.[req.type] || 0}/{req.target}</span>
                      <span className="status">{(trial.progress?.[req.type] || 0) >= req.target ? '✅' : '⏳'}</span>
                    </div>
                  ))}
                  <div className="requirement-item">
                    <span>{t('breakthrough.reflectionAtJournal')}</span>
                    <span className="status">{trial.progress?.reflection_done ? '✅' : '📝'}</span>
                  </div>
                </section>

                {/* Optional Paths */}
                <section className="ritual-section">
                  <h4><span className="icon">🌟</span> {t('breakthrough.optionalPaths')}</h4>
                  <div className="options-grid">
                    {ritual.options?.map((opt) => (
                      <div 
                        key={opt.id} 
                        className={`option-card ${trial.selected_option_id === opt.id ? 'active' : ''}`}
                        onClick={() => !trial.selected_option_id && handleSelectOption(opt.id)}
                      >
                        <h5>{isVi ? opt.label_vi : opt.label_en}</h5>
                        <p>{t(`breakthrough.req.${opt.req?.type}`)}: {opt.req?.target}</p>
                        {trial.selected_option_id === opt.id && <div className="selected-mark">{t('breakthrough.selected')}</div>}
                      </div>
                    ))}
                  </div>
                </section>

                <button 
                  className="complete-btn" 
                  disabled={submitting}
                  onClick={handleComplete}
                >
                  {submitting ? t('breakthrough.selecting') : t('breakthrough.complete')}
                </button>
              </div>
            ) : trial && !ritual ? (
              <div className="loading-ritual-data">
                <div className="loading-spinner" />
                <p>Đang chuẩn bị nghi thức...</p>
              </div>
            ) : (
              <div className="not-available">
                <p>Bạn chưa đạt đến giới hạn chỉ số của giai đoạn này. Hãy tiếp tục rèn luyện!</p>
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
