import { useEffect, useRef } from 'react';
import './ParticleBackground.scss';

export default function ParticleBackground() {
  const containerRef = useRef(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const createParticle = () => {
      const particle = document.createElement('div');
      particle.className = 'particle';
      
      const size = Math.random() * 4 + 1;
      const x = Math.random() * 100;
      const duration = Math.random() * 15 + 10;
      const delay = Math.random() * 10;
      const opacity = Math.random() * 0.5 + 0.1;

      particle.style.cssText = `
        width: ${size}px;
        height: ${size}px;
        left: ${x}%;
        animation-duration: ${duration}s;
        animation-delay: ${delay}s;
        opacity: ${opacity};
      `;

      container.appendChild(particle);

      setTimeout(() => {
        if (particle.parentNode) particle.parentNode.removeChild(particle);
      }, (duration + delay) * 1000);
    };

    // Create initial particles
    for (let i = 0; i < 30; i++) {
      createParticle();
    }

    // Continuously create particles
    const interval = setInterval(createParticle, 1500);

    return () => {
      clearInterval(interval);
      if (container) container.innerHTML = '';
    };
  }, []);

  return <div className="particle-background" ref={containerRef} />;
}
