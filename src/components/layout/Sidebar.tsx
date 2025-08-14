import React from 'react';
import { 
  Drawer, 
  List, 
  ListItem, 
  ListItemButton, 
  ListItemIcon, 
  ListItemText, 
  Typography, 
  Box, 
  Divider,
  Stack
} from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../../store';
import { setSidebarOpen } from '../../store/slices/uiSlice';
import DashboardIcon from '@mui/icons-material/Dashboard';
import ChatIcon from '@mui/icons-material/Chat';
import BarChartIcon from '@mui/icons-material/BarChart';
import SettingsIcon from '@mui/icons-material/Settings';
import PeopleIcon from '@mui/icons-material/People';
import ContentPasteIcon from '@mui/icons-material/ContentPaste';

const Sidebar: React.FC = () => {
  const dispatch = useDispatch();
  const { sidebarOpen, isMobile } = useSelector((state: RootState) => state.ui);

  const menuItems = [
    { icon: <DashboardIcon />, text: 'Dashboard', path: '/' },
    { icon: <PeopleIcon />, text: 'Agents', path: '/agents' },
    { icon: <ChatIcon />, text: 'Chat', path: '/chat' },
    { icon: <BarChartIcon />, text: 'Analytics', path: '/analytics' },
    { icon: <ContentPasteIcon />, text: 'Content', path: '/content' },
    { icon: <SettingsIcon />, text: 'Settings', path: '/settings' },
  ];

  const handleClose = () => {
    if (isMobile) {
      dispatch(setSidebarOpen(false));
    }
  };

  return (
    <Drawer
      variant={isMobile ? 'temporary' : 'persistent'}
      open={sidebarOpen}
      onClose={handleClose}
      sx={{
        width: 280,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: 280,
          boxSizing: 'border-box',
          bgcolor: 'background.paper',
          borderRight: '1px solid',
          borderColor: 'divider',
        },
      }}
    >
      <Box sx={{ p: 3 }}>
        <Typography variant="h5" sx={{ fontWeight: 700, color: 'primary.main' }}>
          Vidalytics
        </Typography>
        <Typography variant="body2" sx={{ color: 'text.secondary', mt: 0.5 }}>
          AI-Powered YouTube Analytics
        </Typography>
      </Box>
      
      <Divider />
      
      <List sx={{ px: 2, py: 1 }}>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding sx={{ mb: 0.5 }}>
            <ListItemButton
              sx={{
                borderRadius: 2,
                '&:hover': {
                  bgcolor: 'action.hover',
                },
                '&.Mui-selected': {
                  bgcolor: 'primary.main',
                  color: 'primary.contrastText',
                  '&:hover': {
                    bgcolor: 'primary.dark',
                  },
                },
              }}
            >
              <ListItemIcon sx={{ color: 'inherit', minWidth: 40 }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText 
                primary={item.text}
                primaryTypographyProps={{
                  fontSize: '0.9rem',
                  fontWeight: 500,
                }}
              />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
};

export default Sidebar;