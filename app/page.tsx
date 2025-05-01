'use client';

import { useState, useEffect } from 'react';
import LandingPage from './components/LandingPage';
import ChatInterface from './components/ChatInterface';

export default function Home() {
  const [showLanding, setShowLanding] = useState(true);

  useEffect(() => {
    const hasVisited = localStorage.getItem('hasVisited');
    if (hasVisited) {
      setShowLanding(false);
    }
  }, []);

  const handleGetStarted = () => {
    localStorage.setItem('hasVisited', 'true');
    setShowLanding(false);
  };

  return (
    <main className="min-h-screen bg-[#f6f8fa]">
      {showLanding ? (
        <LandingPage onGetStarted={handleGetStarted} />
      ) : (
        <ChatInterface />
      )}
    </main>
  );
} 