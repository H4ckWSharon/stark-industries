import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './store/authStore';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { Login } from './pages/Login';
import { Dashboard } from './pages/Dashboard';
import { Challenges } from './pages/Challenges';
import { ChallengePage } from './pages/ChallengePage';
import { Leaderboard } from './pages/Leaderboard';
import { Progress } from './pages/Progress';
import { LearningPath } from './pages/LearningPath';
import { Profile } from './pages/Profile';

export const App: React.FC = () => {
  const { isAuthenticated, fetchMe } = useAuthStore();

  useEffect(() => {
    if (isAuthenticated) {
      fetchMe();
    }
  }, [isAuthenticated, fetchMe]);

  if (!isAuthenticated) {
    return <Login />;
  }

  return (
    <Router>
      <div className="min-h-screen bg-[#0a0a0f] flex flex-col font-mono text-[#e6edf3]">
        <Navbar />

        <div className="flex flex-1">
          <Sidebar />

          <main className="flex-1 bg-[#0a0a0f] overflow-y-auto min-h-[calc(100vh-4rem)]">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/challenges" element={<Challenges />} />
              <Route path="/challenge/:id" element={<ChallengePage />} />
              <Route path="/leaderboard" element={<Leaderboard />} />
              <Route path="/progress" element={<Progress />} />
              <Route path="/path" element={<LearningPath />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
};

export default App;
