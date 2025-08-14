import React from 'react';
import { Box, Stack } from '@mui/material';
import { useSelector } from 'react-redux';
import { RootState } from '../../store';
import Sidebar from './Sidebar';
import Header from './Header';
import NotificationSystem from '../common/NotificationSystem';

interface AppLayoutProps {
  children: React.ReactNode;
}

const AppLayout: React.FC<AppLayoutProps> = ({ children }) => {
  const { sidebarOpen, isMobile } = useSelector((state: RootState) => state.ui);

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
      <Sidebar />
      <Stack sx={{ flex: 1, overflow: 'hidden' }}>
        <Header />
        <Box 
          component="main" 
          sx={{ 
            flex: 1, 
            p: 3, 
            overflow: 'auto',
            ml: sidebarOpen && !isMobile ? '280px' : 0,
            transition: 'margin-left 0.3s ease'
          }}
        >
          {children}
        </Box>
      </Stack>
      <NotificationSystem />
    </Box>
  );
};

export default AppLayout;