import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Box,
  Stack,
  Typography,
  Button,
  Avatar,
  Divider,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import { styled } from '@mui/material/styles';
import DashboardIcon from '@mui/icons-material/Dashboard';
import ViewColumnIcon from '@mui/icons-material/ViewColumn';
import VideoLibraryIcon from '@mui/icons-material/VideoLibrary';
import EditIcon from '@mui/icons-material/Edit';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import SettingsIcon from '@mui/icons-material/Settings';
import LogoutIcon from '@mui/icons-material/Logout';
import { UserProfileProps } from '../../types';

const SidebarContainer = styled(Box)(({ theme }) => ({
  width: 288,
  height: '100vh',
  backgroundColor: theme.palette.grey[800],
  display: 'flex',
  flexDirection: 'column',
  position: 'fixed',
  left: 0,
  top: 0,
  zIndex: 1200
}));

const LogoSection = styled(Box)(({ theme }) => ({
  padding: theme.spacing(3),
  borderBottom: `1px solid ${theme.palette.grey[700]}`
}));

const LogoIcon = styled(Box)(({ theme }) => ({
  width: 32,
  height: 32,
  backgroundColor: theme.palette.primary.main,
  borderRadius: theme.spacing(1),
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  fontSize: '14px'
}));

const MenuSection = styled(Box)(({ theme }) => ({
  padding: theme.spacing(2),
  flex: 1
}));

const SectionTitle = styled(Typography)(({ theme }) => ({
  fontSize: '0.75rem',
  fontWeight: 500,
  color: theme.palette.grey[400],
  marginBottom: theme.spacing(2),
  textTransform: 'uppercase'
}));

const UserSection = styled(Box)(({ theme }) => ({
  padding: theme.spacing(3),
  borderTop: `1px solid ${theme.palette.grey[700]}`
}));

interface SidebarProps {
  user: UserProfileProps;
  onLogout: () => void;
}

const menuItems = [
  { path: '/dashboard', label: 'Dashboard', icon: DashboardIcon },
  { path: '/pillars', label: 'Pillars', icon: ViewColumnIcon },
  { path: '/videos', label: 'Videos', icon: VideoLibraryIcon },
  { path: '/content-studio', label: 'Content Studio', icon: EditIcon },
  { path: '/ai-assistant', label: 'AI Assistant', icon: SmartToyIcon }
];

const generalItems = [
  { path: '/settings', label: 'Settings', icon: SettingsIcon }
];

const Sidebar: React.FC<SidebarProps> = ({ user, onLogout }) => {
  const location = useLocation();
  const navigate = useNavigate();

  const handleNavigation = (path: string) => {
    navigate(path);
  };

  return (
    <SidebarContainer>
      <LogoSection>
        <Stack direction="row" spacing={1} alignItems="center">
          <LogoIcon>
            ✨
          </LogoIcon>
          <Typography variant="h6" color="white" fontWeight="bold">
            Vidalytics
          </Typography>
        </Stack>
        <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5 }}>
          Your AI Agent for Content and Growth
        </Typography>
      </LogoSection>

      <MenuSection>
        <SectionTitle>Main Menu</SectionTitle>
        <List disablePadding>
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            
            return (
              <ListItem key={item.path} disablePadding sx={{ mb: 0.5 }}>
                <ListItemButton
                  onClick={() => handleNavigation(item.path)}
                  sx={{
                    borderRadius: 1,
                    backgroundColor: isActive ? 'primary.main' : 'transparent',
                    color: isActive ? 'white' : 'grey.300',
                    '&:hover': {
                      backgroundColor: isActive ? 'primary.main' : 'grey.700',
                      color: 'white'
                    }
                  }}
                >
                  <ListItemIcon sx={{ color: 'inherit', minWidth: 40 }}>
                    <Icon fontSize="small" />
                  </ListItemIcon>
                  <ListItemText primary={item.label} />
                </ListItemButton>
              </ListItem>
            );
          })}
        </List>

        <SectionTitle sx={{ mt: 4 }}>General</SectionTitle>
        <List disablePadding>
          {generalItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            
            return (
              <ListItem key={item.path} disablePadding>
                <ListItemButton
                  onClick={() => handleNavigation(item.path)}
                  sx={{
                    borderRadius: 1,
                    backgroundColor: isActive ? 'primary.main' : 'transparent',
                    color: isActive ? 'white' : 'grey.300',
                    '&:hover': {
                      backgroundColor: isActive ? 'primary.main' : 'grey.700',
                      color: 'white'
                    }
                  }}
                >
                  <ListItemIcon sx={{ color: 'inherit', minWidth: 40 }}>
                    <Icon fontSize="small" />
                  </ListItemIcon>
                  <ListItemText primary={item.label} />
                </ListItemButton>
              </ListItem>
            );
          })}
        </List>
      </MenuSection>

      <UserSection>
        <Stack direction="row" spacing={1.5} alignItems="center" sx={{ mb: 2 }}>
          <Avatar
            sx={{
              width: 40,
              height: 40,
              backgroundColor: 'primary.main',
              fontSize: '1rem',
              fontWeight: 'bold'
            }}
          >
            {user.initial}
          </Avatar>
          <Box flex={1}>
            <Typography variant="body2" color="white">
              {user.greeting}
            </Typography>
            <Typography variant="body2" color="white" fontWeight="bold">
              {user.name}!
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Let's see your current task work today
            </Typography>
          </Box>
        </Stack>
        
        <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 1 }}>
          <Typography variant="caption" color="text.secondary">
            📅 {user.currentDate}
          </Typography>
          <Button
            size="small"
            sx={{ color: 'grey.400', minWidth: 'auto', p: 0.5 }}
          >
            <LogoutIcon fontSize="small" />
          </Button>
        </Stack>
        
        <Button
          onClick={onLogout}
          size="small"
          startIcon={<LogoutIcon fontSize="small" />}
          sx={{
            color: 'grey.400',
            fontSize: '0.75rem',
            textTransform: 'none',
            p: 0,
            justifyContent: 'flex-start',
            '&:hover': {
              color: 'white',
              backgroundColor: 'transparent'
            }
          }}
        >
          Log Out
        </Button>
      </UserSection>
    </SidebarContainer>
  );
};

export default Sidebar;