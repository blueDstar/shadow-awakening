import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { settingsService } from '../../services/apiServices';
import { useAuth } from '../../context/AuthContext';
import './Settings.scss';

export default function Settings() {
  const { t, i18n } = useTranslation();
  const { user, logout } = useAuth();
  const [settings, setSettings] = useState({ language: 'vi', timezone: 'Asia/Ho_Chi_Minh' });

  useEffect(() => {
    settingsService.get().then(res => setSettings(res.data)).catch(console.error);
  }, []);

  const handleLanguageChange = async (lang) => {
    try {
      await settingsService.updateLanguage(lang);
      i18n.changeLanguage(lang);
      localStorage.setItem('sa_language', lang);
      setSettings({ ...settings, language: lang });
    } catch (err) { console.error(err); }
  };

  return (
    <div className="settings-page">
      <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }}>{t('settings.title')}</motion.h1>

      <motion.div className="settings-section" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        <h3>{t('settings.language')}</h3>
        <div className="language-selector">
          <button
            className={`lang-btn ${settings.language === 'vi' ? 'lang-btn--active' : ''}`}
            onClick={() => handleLanguageChange('vi')}
          >
            🇻🇳 Tiếng Việt
          </button>
          <button
            className={`lang-btn ${settings.language === 'en' ? 'lang-btn--active' : ''}`}
            onClick={() => handleLanguageChange('en')}
          >
            🇬🇧 English
          </button>
        </div>
      </motion.div>

      <motion.div className="settings-section" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
        <h3>{t('settings.account')}</h3>
        <div className="account-info">
          <p><strong>{t('auth.username')}:</strong> {user?.username}</p>
          <p><strong>{t('auth.email')}:</strong> {user?.email}</p>
        </div>
        <button className="logout-btn" onClick={logout}>
          🚪 {t('auth.logout')}
        </button>
      </motion.div>
    </div>
  );
}
