import React from 'react';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  IconButton, 
  Avatar, 
  Box, 
  Badge,
  Stack
} from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../../store';
import { toggleSidebar } from '../../store/slices/uiSlice';
import { logout } from '../../store/slices/authSlice';
import MenuIcon from '@mui/icons-material/Menu';
import NotificationsOutlinedIcon from '@mui/icons-material/NotificationsOutlined';
import LogoutIcon from '@mui/icons-material/Logout';

const Header: React.FC = () => {
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => state.auth);
  const { notifications, sidebarOpen } = useSelector((state: RootState) => state.ui);

  const handleMenuClick = () => {
    dispatch(toggleSidebar());
  };

  const handleLogout = () => {
    dispatch(logout());
  };

  return (
    <AppBar 
      position="sticky" 
      elevation={0}
      sx={{ 
        bgcolor: 'background.paper',
        borderBottom: '1px solid',
        borderColor: 'divider',
        color: 'text.primary'
      }}
    >
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        <Stack direction="row" alignItems="center" spacing={2}>
          <IconButton
            edge="start"
            color="inherit"
            onClick={handleMenuClick}
            sx={{ mr: 1 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" sx={{ fontWeight: 600 }}>
            Dashboard
          </Typography>
        </Stack>

        <Stack direction="row" alignItems="center" spacing={2}>
          <IconButton color="inherit">
            <Badge badgeContent={notifications.length} color="primary">
              <NotificationsOutlinedIcon />
            </Badge>
          </IconButton>
          
          <Stack direction="row" alignItems="center" spacing={2}>
            <Avatar 
              sx={{ 
                width: 32, 
                height: 32, 
                bgcolor: 'primary.main',
                fontSize: '0.875rem'
              }}
            >
              {user?.name?.charAt(0) || 'U'}
            </Avatar>
            <Box sx={{ display: { xs: 'none', sm: 'block' } }}>
              <Typography variant="body2" sx={{ fontWeight: 500 }}>
                {user?.name || 'User'}
              </Typography>
              <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                {user?.subscription_tier || 'Free'}
              </Typography>
            </Box>
          </Stack>

          <IconButton color="inherit" onClick={handleLogout}>
            <LogoutIcon />
          </IconButton>
        </Stack>
      </Toolbar>
    </AppBar>
  );
};

export default Header;