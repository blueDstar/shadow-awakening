import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../../components/navigation/Sidebar/Sidebar';
import MobileHeader from '../../components/navigation/MobileHeader/MobileHeader';
import ParticleBackground from '../../components/effects/ParticleBackground/ParticleBackground';
import './MainLayout.scss';

export default function MainLayout() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen);
  const closeSidebar = () => setIsSidebarOpen(false);

  return (
    <div className="main-layout">
      <ParticleBackground />
      <MobileHeader onMenuClick={toggleSidebar} />
      <Sidebar isOpen={isSidebarOpen} onClose={closeSidebar} />
      <main className="main-layout__content">
        <Outlet />
      </main>
    </div>
  );
}
