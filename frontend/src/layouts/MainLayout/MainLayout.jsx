import { Outlet } from 'react-router-dom';
import Sidebar from '../../components/navigation/Sidebar/Sidebar';
import ParticleBackground from '../../components/effects/ParticleBackground/ParticleBackground';
import './MainLayout.scss';

export default function MainLayout() {
  return (
    <div className="main-layout">
      <ParticleBackground />
      <Sidebar />
      <main className="main-layout__content">
        <Outlet />
      </main>
    </div>
  );
}
