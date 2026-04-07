import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import MainLayout from './layouts/MainLayout/MainLayout';
import Login from './pages/Login/Login';
import Register from './pages/Register/Register';
import Dashboard from './pages/Dashboard/Dashboard';
import DailyQuests from './pages/DailyQuests/DailyQuests';
import CharacterStats from './pages/CharacterStats/CharacterStats';
import Skills from './pages/Skills/Skills';
import Challenges from './pages/Challenges/Challenges';
import Journal from './pages/Journal/Journal';
import Rewards from './pages/Rewards/Rewards';
import Settings from './pages/Settings/Settings';
import './i18n';
import './index.scss';

function ProtectedRoute({ children }) {
  const { token, loading } = useAuth();
  if (loading) {
    return (
      <div className="app-loading">
        <div className="app-loading__spinner" />
        <p>Shadow Awakening</p>
      </div>
    );
  }
  return token ? children : <Navigate to="/login" />;
}

function PublicRoute({ children }) {
  const { token, loading } = useAuth();
  if (loading) return null;
  return !token ? children : <Navigate to="/" />;
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
          <Route path="/register" element={<PublicRoute><Register /></PublicRoute>} />

          {/* Protected routes */}
          <Route path="/" element={<ProtectedRoute><MainLayout /></ProtectedRoute>}>
            <Route index element={<Dashboard />} />
            <Route path="quests" element={<DailyQuests />} />
            <Route path="stats" element={<CharacterStats />} />
            <Route path="skills" element={<Skills />} />
            <Route path="challenges" element={<Challenges />} />
            <Route path="journal" element={<Journal />} />
            <Route path="rewards" element={<Rewards />} />
            <Route path="settings" element={<Settings />} />
          </Route>

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
