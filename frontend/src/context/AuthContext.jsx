import { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/apiServices';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('sa_token'));

  useEffect(() => {
    if (token) {
      authService.getMe()
        .then(res => {
          setUser(res.data);
          setLoading(false);
        })
        .catch(() => {
          localStorage.removeItem('sa_token');
          setToken(null);
          setUser(null);
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, [token]);

  const login = async (username, password) => {
    const res = await authService.login({ username, password });
    const { access_token, user_id } = res.data;
    localStorage.setItem('sa_token', access_token);
    localStorage.setItem('sa_user_id', user_id);
    setToken(access_token);
    const meRes = await authService.getMe();
    setUser(meRes.data);
    return res.data;
  };

  const register = async (username, email, password) => {
    const res = await authService.register({ username, email, password });
    const { access_token, user_id } = res.data;
    localStorage.setItem('sa_token', access_token);
    localStorage.setItem('sa_user_id', user_id);
    setToken(access_token);
    const meRes = await authService.getMe();
    setUser(meRes.data);
    return res.data;
  };

  const logout = () => {
    localStorage.removeItem('sa_token');
    localStorage.removeItem('sa_user_id');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
