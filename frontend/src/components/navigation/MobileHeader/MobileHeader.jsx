import { memo } from 'react';
import { useTranslation } from 'react-i18next';
import './MobileHeader.scss';

const MobileHeader = memo(({ onMenuClick }) => {
  const { t } = useTranslation();

  return (
    <header className="mobile-header">
      <div className="mobile-header__logo">
        <img src="/main_app_logo_1024.png" alt="Logo" className="mobile-header__logo-icon" style={{width: '32px', height: '32px'}} />
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
