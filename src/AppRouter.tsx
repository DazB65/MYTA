import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Box } from '@mui/material';
import Sidebar from './components/layout/Sidebar';
import Dashboard from './pages/Dashboard';
import Pillars from './pages/Pillars';
import Videos from './pages/Videos';
import ContentStudio from './pages/ContentStudio';
import AIAssistant from './pages/AIAssistant';
import CreateProfile from './pages/CreateProfile';
import Settings from './pages/Settings';
import { mockUserProfile } from './vidalyticsMockData';

const AppRouter: React.FC = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(true);

  const handleLogout = () => {
    setIsAuthenticated(false);
  };

  if (!isAuthenticated) {
    return <CreateProfile />;
  }

  return (
    <Router>
      <Box sx={{ display: 'flex' }}>
        <Sidebar user={mockUserProfile} onLogout={handleLogout} />
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/pillars" element={<Pillars />} />
          <Route path="/videos" element={<Videos />} />
          <Route path="/content-studio" element={<ContentStudio />} />
          <Route path="/ai-assistant" element={<AIAssistant />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </Box>
    </Router>
  );
};

export default AppRouter;