import { NavLink, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../../context/AuthContext';
import { motion } from 'framer-motion';
import './Sidebar.scss';

const navItems = [
  { path: '/', icon: '⚔️', key: 'dashboard' },
  { path: '/quests', icon: '📜', key: 'quests' },
  { path: '/stats', icon: '📊', key: 'stats' },
  { path: '/skills', icon: '⚡', key: 'skills' },
  { path: '/challenges', icon: '🏆', key: 'challenges' },
  { path: '/journal', icon: '📖', key: 'journal' },
  { path: '/rewards', icon: '💎', key: 'rewards' },
  { path: '/settings', icon: '⚙️', key: 'settings' },
];

export default function Sidebar() {
  const { t } = useTranslation();
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <motion.aside
      className="sidebar"
      initial={{ x: -280 }}
      animate={{ x: 0 }}
      transition={{ type: 'spring', stiffness: 120, damping: 20 }}
    >
      <div className="sidebar__logo">
        <div className="sidebar__logo-icon">🌑</div>
        <div className="sidebar__logo-text">
          <span className="sidebar__logo-title">Shadow</span>
          <span className="sidebar__logo-subtitle">Awakening</span>
        </div>
      </div>

      <nav className="sidebar__nav">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `sidebar__link ${isActive ? 'sidebar__link--active' : ''}`
            }
            end={item.path === '/'}
          >
            <span className="sidebar__link-icon">{item.icon}</span>
            <span className="sidebar__link-text">{t(`nav.${item.key}`)}</span>
            <div className="sidebar__link-glow" />
          </NavLink>
        ))}
      </nav>

      <div className="sidebar__footer">
        <button className="sidebar__logout" onClick={handleLogout}>
          <span>🚪</span>
          <span>{t('auth.logout')}</span>
        </button>
      </div>
    </motion.aside>
  );
}
