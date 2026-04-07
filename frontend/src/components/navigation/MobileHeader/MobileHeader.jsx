import { memo } from 'react';
import { useTranslation } from 'react-i18next';
import './MobileHeader.scss';

const MobileHeader = memo(({ onMenuClick }) => {
  const { t } = useTranslation();

  return (
    <header className="mobile-header">
      <div className="mobile-header__logo">
        <span className="mobile-header__logo-icon">🌑</span>
        <div className="mobile-header__logo-text">
          <span className="mobile-header__logo-title">Shadow</span>
          <span className="mobile-header__logo-subtitle">Awakening</span>
        </div>
      </div>
      
      <button 
        className="mobile-header__toggle" 
        onClick={onMenuClick}
        aria-label="Toggle Menu"
      >
        <span className="mobile-header__toggle-bar"></span>
        <span className="mobile-header__toggle-bar"></span>
        <span className="mobile-header__toggle-bar"></span>
      </button>
    </header>
  );
});

export default MobileHeader;
