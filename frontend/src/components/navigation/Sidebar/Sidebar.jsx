import { Link, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../../context/AuthContext';
import './Sidebar.scss';

export default function Sidebar({ isOpen, onClose }) {
  const { t } = useTranslation();
  const { logout } = useAuth();
  const location = useLocation();

  const navLinks = [
    { path: '/', icon: <img src="/main_app_logo_1024.png" alt="dashboard" style={{ width: '35px', height: '35px' }} />, label: t('nav.dashboard') },
    { path: '/quests', icon: <img src="/rewards_system_chest_512.png" alt="quests" style={{ width: '35px', height: '35px' }} />, label: t('nav.quests') },
    { path: '/stats', icon: <img src="/stats_shadow_hunter_512.png" alt="stats" style={{ width: '35px', height: '35px' }} />, label: t('nav.stats') },
    { path: '/skills', icon: <img src="/focus_eye_512.png" alt="skills" style={{ width: '35px', height: '35px' }} />, label: t('nav.skills') },
    { path: '/challenges', icon: <img src="/fitness_sword_512.png" alt="challenges" style={{ width: '35px', height: '35px' }} />, label: t('nav.challenges') },
    { path: '/rewards', icon: <img src="/confidence_soul_fire_512.png" alt="rewards" style={{ width: '35px', height: '35px' }} />, label: t('nav.rewards') },
    { path: '/journal', icon: <img src="/wisdom_spellbook_512.png" alt="journal" style={{ width: '35px', height: '35px' }} />, label: t('nav.journal') },
    { path: '/settings', icon: '⚙️', label: t('nav.settings') },
  ];

  return (
    <>
      <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar__logo">
          <img src="/main_app_logo_1024.png" alt="Logo" className="sidebar__logo-icon" style={{ width: '40px', height: '40px' }} />
          <div className="sidebar__logo-text">
            <span className="sidebar__logo-title">Shadow</span>
            <span className="sidebar__logo-subtitle">Awakening</span>
          </div>
        </div>

        <nav className="sidebar__nav">
          {navLinks.map((link) => (
            <Link
              key={link.path}
              to={link.path}
              className={`sidebar__link ${location.pathname === link.path ? 'sidebar__link--active' : ''}`}
              onClick={onClose}
            >
              <span className="sidebar__link-icon">{link.icon}</span>
              <span className="sidebar__link-text">{link.label}</span>
              <div className="sidebar__link-glow" />
            </Link>
          ))}
        </nav>

        <div className="sidebar__footer">
          <button className="sidebar__logout" onClick={logout}>
            <span className="sidebar__link-icon">🚪</span>
            <span>{t('auth.logout')}</span>
          </button>
        </div>
      </aside>

      {/* Mobile Overlay */}
      {isOpen && <div className="sidebar-overlay" onClick={onClose} />}
    </>
  );
}
