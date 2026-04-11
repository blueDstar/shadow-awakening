import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { journalService, breakthroughService } from '../../services/apiServices';
import './Journal.scss';

const MOODS = ['great', 'good', 'neutral', 'bad', 'terrible'];
const MOOD_ICONS = { great: '🔥', good: '😊', neutral: '😐', bad: '😕', terrible: '😞' };

export default function Journal() {
  const { t } = useTranslation();
  const [entries, setEntries] = useState([]);
  const [form, setForm] = useState({ content: '', mood: 'neutral', insights: '', success_reasons: '', fail_reasons: '' });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [activeRitual, setActiveRitual] = useState(null);

  useEffect(() => { 
    loadEntries(); 
    checkBreakthrough();
  }, []);

  const checkBreakthrough = async () => {
    try {
      const res = await breakthroughService.getStatus();
      if (res.data?.active_trial) {
        setActiveRitual(res.data);
      }
    } catch (err) { console.error(err); }
  };

  const loadEntries = async () => {
    try {
      const res = await journalService.getAll(14);
      setEntries(res.data);
    } catch (err) { console.error(err); }
    finally { setLoading(false); }
  };

  const handleSave = async () => {
    if (!form.content.trim()) return;
    setSaving(true);
    try {
      const payload = {
        ...form,
        breakthrough_trial_id: activeRitual?.active_trial?.id
      };
      await journalService.create(payload);
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
      setForm({ content: '', mood: 'neutral', insights: '', success_reasons: '', fail_reasons: '' });
      await loadEntries();
    } catch (err) { console.error(err); }
    finally { setSaving(false); }
  };

  return (
    <div className="journal-page">
      <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }}>{t('journal.title')}</motion.h1>

      {activeRitual && (
        <motion.div 
          className="journal-ritual-alert"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
        >
          <span className="icon">✨</span>
          <div className="text">
            <strong>{activeRitual.ritual_template.title_vi}</strong>
            <p>Hãy viết bài tổng kết tối thiểu {activeRitual.ritual_template.min_reflection} từ để hoàn tất nghi thức.</p>
          </div>
        </motion.div>
      )}

      <motion.div className="journal-form" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        <div className="journal-form__mood">
          <label>{t('journal.mood')}</label>
          <div className="mood-selector">
            {MOODS.map(m => (
              <button
                key={m}
                className={`mood-btn ${form.mood === m ? 'mood-btn--active' : ''}`}
                onClick={() => setForm({ ...form, mood: m })}
              >
                <span className="mood-btn__icon">{MOOD_ICONS[m]}</span>
                <span className="mood-btn__label">{t(`journal.moods.${m}`)}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="journal-form__field">
          <label>{t('journal.content')}</label>
          <textarea
            value={form.content}
            onChange={(e) => setForm({ ...form, content: e.target.value })}
            placeholder={t('journal.placeholder')}
            rows={6}
          />
        </div>

        <div className="journal-form__field">
          <label>{t('journal.insights')}</label>
          <textarea
            value={form.insights}
            onChange={(e) => setForm({ ...form, insights: e.target.value })}
            rows={3}
          />
        </div>

        <div className="journal-form__row">
          <div className="journal-form__field">
            <label>{t('journal.successReasons')}</label>
            <textarea
              value={form.success_reasons}
              onChange={(e) => setForm({ ...form, success_reasons: e.target.value })}
              rows={2}
            />
          </div>
          <div className="journal-form__field">
            <label>{t('journal.failReasons')}</label>
            <textarea
              value={form.fail_reasons}
              onChange={(e) => setForm({ ...form, fail_reasons: e.target.value })}
              rows={2}
            />
          </div>
        </div>

        <button className="journal-form__save" onClick={handleSave} disabled={saving || !form.content.trim()}>
          {saving ? '⏳' : saved ? '✅' : '💾'} {t('journal.save')}
        </button>
      </motion.div>

      <div className="journal-entries">
        {entries.map((entry, i) => (
          <motion.div
            key={entry.id}
            className="journal-entry"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
          >
            <div className="journal-entry__header">
              <span className="journal-entry__mood">{MOOD_ICONS[entry.mood]}</span>
              <span className="journal-entry__date">{entry.reflection_date}</span>
            </div>
            <p className="journal-entry__content">{entry.content}</p>
            {entry.insights && <p className="journal-entry__insights">💡 {entry.insights}</p>}
          </motion.div>
        ))}
      </div>
    </div>
  );
}
