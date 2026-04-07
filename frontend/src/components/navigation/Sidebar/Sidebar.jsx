import { Link, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../../context/AuthContext';
import './Sidebar.scss';

export default function Sidebar({ isOpen, onClose }) {
  const { t } = useTranslation();
  const { logout } = useAuth();
  const location = useLocation();

  const navLinks = [
    { path: '/', icon: '🏰', label: t('nav.dashboard') },
    { path: '/quests', icon: '📜', label: t('nav.quests') },
    { path: '/stats', icon: '📊', label: t('nav.stats') },
    { path: '/skills', icon: '✨', label: t('nav.skills') },
    { path: '/challenges', icon: '⚔️', label: t('nav.challenges') },
    { path: '/rewards', icon: '🏆', label: t('nav.rewards') },
    { path: '/journal', icon: '📔', label: t('nav.journal') },
    { path: '/settings', icon: '⚙️', label: t('nav.settings') },
  ];

  return (
    <>
      <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar__logo">
          <span className="sidebar__logo-icon">🌑</span>
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
