import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { RootState } from './store';
import AppLayout from './components/layout/AppLayout';
import LoginForm from './components/auth/LoginForm';
import MultiAgentDashboard from './components/dashboard/MultiAgentDashboard';
import AnalyticsOverview from './components/analytics/AnalyticsOverview';
import ChatInterface from './components/chat/ChatInterface';
import ContentManagement from './components/content/ContentManagement';

const AppRouter: React.FC = () => {
  const { isAuthenticated } = useSelector((state: RootState) => state.auth);

  if (!isAuthenticated) {
    return <LoginForm />;
  }

  return (
    <Router>
      <AppLayout>
        <Routes>
          <Route path="/" element={<MultiAgentDashboard />} />
          <Route path="/agents" element={<MultiAgentDashboard />} />
          <Route path="/analytics" element={<AnalyticsOverview />} />
          <Route path="/chat" element={<ChatInterface />} />
          <Route path="/content" element={<ContentManagement />} />
          <Route path="/settings" element={<div>Settings Page (Coming Soon)</div>} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AppLayout>
    </Router>
  );
};

export default AppRouter;