import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../context/AuthContext';
import { motion } from 'framer-motion';
import './Register.scss';

export default function Register() {
  const { t } = useTranslation();
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: '', email: '', password: '', confirmPassword: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (form.password !== form.confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    setLoading(true);
    setError('');
    try {
      await register(form.username, form.email, form.password);
      navigate('/onboarding');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  const update = (field) => (e) => setForm({ ...form, [field]: e.target.value });

  return (
    <div className="register-page">
      <motion.div
        className="register-card"
        initial={{ opacity: 0, y: 40, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
      >
        <div className="register-card__header">
          <img src="/main_app_logo_1024.png" alt="Shadow Awakening" className="register-card__icon" style={{width: '80px', margin: '0 auto', display: 'block'}} />
          <h1 className="register-card__title">Shadow Awakening</h1>
          <p className="register-card__subtitle">{t('auth.registerTitle')}</p>
        </div>

        <form onSubmit={handleSubmit} className="register-card__form">
          {error && <div className="register-card__error">{error}</div>}
          
          <div className="register-card__field">
            <label>{t('auth.username')}</label>
            <input type="text" value={form.username} onChange={update('username')} placeholder={t('auth.username')} />
          </div>
          <div className="register-card__field">
            <label>{t('auth.email')}</label>
            <input type="email" value={form.email} onChange={update('email')} placeholder={t('auth.email')} />
          </div>
          <div className="register-card__field">
            <label>{t('auth.password')}</label>
            <input type="password" value={form.password} onChange={update('password')} placeholder={t('auth.password')} />
          </div>
          <div className="register-card__field">
            <label>{t('auth.confirmPassword')}</label>
            <input type="password" value={form.confirmPassword} onChange={update('confirmPassword')} placeholder={t('auth.confirmPassword')} />
          </div>

          <button type="submit" className="register-card__submit" disabled={loading}>
            {loading ? '⏳' : '⚔️'} {t('auth.register')}
          </button>
        </form>

        <div className="register-card__footer">
          <span>{t('auth.hasAccount')}</span>
          <Link to="/login">{t('auth.login')}</Link>
        </div>
      </motion.div>
    </div>
  );
}
