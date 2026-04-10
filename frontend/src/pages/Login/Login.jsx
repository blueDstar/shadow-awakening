import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../context/AuthContext';
import { motion } from 'framer-motion';
import './Login.scss';

export default function Login() {
  const { t } = useTranslation();
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username || !password) return;
    
    setLoading(true);
    setError('');
    try {
      await login(username, password);
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-page__particles" />
      <motion.div
        className="login-card"
        initial={{ opacity: 0, y: 40, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
      >
        <div className="login-card__header">
          <img src="/main_app_logo_1024.png" alt="Shadow Awakening" className="login-card__icon" style={{width: '80px', margin: '0 auto', display: 'block'}} />
          <h1 className="login-card__title">Shadow Awakening</h1>
          <p className="login-card__subtitle">{t('auth.loginTitle')}</p>
        </div>

        <form onSubmit={handleSubmit} className="login-card__form">
          {error && <div className="login-card__error">{error}</div>}
          
          <div className="login-card__field">
            <label>{t('auth.username')}</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder={t('auth.username')}
              autoComplete="username"
            />
          </div>

          <div className="login-card__field">
            <label>{t('auth.password')}</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder={t('auth.password')}
              autoComplete="current-password"
            />
          </div>

          <button
            type="submit"
            className="login-card__submit"
            disabled={loading || !username || !password}
          >
            {loading ? '⏳' : '⚔️'} {t('auth.login')}
          </button>
        </form>

        <div className="login-card__footer">
          <span>{t('auth.noAccount')}</span>
          <Link to="/register">{t('auth.register')}</Link>
        </div>
      </motion.div>
    </div>
  );
}
