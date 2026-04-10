import { useState, useEffect, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { settingsService, profileService } from '../../services/apiServices';
import { useAuth } from '../../context/AuthContext';
import './Settings.scss';

export default function Settings() {
  const { t, i18n } = useTranslation();
  const { user, logout } = useAuth();
  const [settings, setSettings] = useState({ language: 'vi', timezone: 'Asia/Ho_Chi_Minh' });
  const [profile, setProfile] = useState(null);
  const [uploading, setUploading] = useState(null);

  const avatarInput = useRef();
  const coverInput = useRef();
  const bgInput = useRef();

  useEffect(() => {
    settingsService.get().then(res => setSettings(res.data)).catch(console.error);
    profileService.getProfile().then(res => setProfile(res.data)).catch(console.error);
  }, []);

  const handleLanguageChange = async (lang) => {
    try {
      await settingsService.updateLanguage(lang);
      i18n.changeLanguage(lang);
      localStorage.setItem('sa_language', lang);
      setSettings({ ...settings, language: lang });
    } catch (err) { console.error(err); }
  };

  const handleFileUpload = async (e, type) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(type);
    try {
      const res = await profileService.uploadImage(type, file);
      setProfile({ ...profile, [`${type}_url`]: res.data.url });
      // Reload page or update context if needed
      window.location.reload(); // Quickest way to sync globally for now
    } catch (err) {
      console.error(`Upload ${type} failed:`, err);
      alert(t('common.error') || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="settings-page">
      <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }}>{t('settings.title')}</motion.h1>

      {/* Profile Section */}
      <motion.div className="settings-section" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        <h3>{t('settings.profile') || 'Tùy chỉnh hồ sơ'}</h3>
        <div className="profile-edit-grid">
          {/* Avatar */}
          <div className="profile-edit-item">
            <label>{t('profile.avatar') || 'Ảnh đại diện'}</label>
            <div className="preview-box avatar-preview">
              <img src={profile?.avatar_url || '/main_app_logo_1024.png'} alt="Avatar" />
              <button onClick={() => avatarInput.current.click()} disabled={uploading === 'avatar'}>
                {uploading === 'avatar' ? '...' : (t('common.change') || 'Thay đổi')}
              </button>
            </div>
            <input type="file" ref={avatarInput} onChange={(e) => handleFileUpload(e, 'avatar')} hidden accept="image/*" />
          </div>

          {/* Cover */}
          <div className="profile-edit-item">
            <label>{t('profile.cover') || 'Ảnh bìa'}</label>
            <div className="preview-box cover-preview" style={{ backgroundImage: `url(${profile?.cover_url})` }}>
              <button onClick={() => coverInput.current.click()} disabled={uploading === 'cover'}>
                {uploading === 'cover' ? '...' : (t('common.change') || 'Thay đổi')}
              </button>
            </div>
            <input type="file" ref={coverInput} onChange={(e) => handleFileUpload(e, 'cover')} hidden accept="image/*" />
          </div>

          {/* Background */}
          <div className="profile-edit-item">
            <label>{t('profile.background') || 'Hình nền'}</label>
            <div className="preview-box bg-preview" style={{ backgroundImage: `url(${profile?.background_url})` }}>
              <button onClick={() => bgInput.current.click()} disabled={uploading === 'background'}>
                {uploading === 'background' ? '...' : (t('common.change') || 'Thay đổi')}
              </button>
            </div>
            <input type="file" ref={bgInput} onChange={(e) => handleFileUpload(e, 'background')} hidden accept="image/*" />
          </div>
        </div>
      </motion.div>

      <motion.div className="settings-section" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
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

      <motion.div className="settings-section" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
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
