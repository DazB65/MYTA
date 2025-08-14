import React from 'react';
import {
  Box,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Typography,
  Avatar,
  Stack,
  Divider,
} from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../../store';
import { setActiveSession } from '../../store/slices/chatSlice';

const ChatSidebar: React.FC = () => {
  const dispatch = useDispatch();
  const { sessions, activeSessionId } = useSelector((state: RootState) => state.chat);
  const { agents } = useSelector((state: RootState) => state.agents);
  
  const sessionList = Object.values(sessions);

  const getAgentIcon = (agentId: string) => {
    const iconMap: Record<string, string> = {
      boss_agent: '👑',
      content_analysis: '📊',
      audience_insights: '👥',
      seo_discoverability: '🔍',
      monetization_strategy: '💰',
      competitive_analysis: '📈',
    };
    const agent = agents[agentId];
    return iconMap[agent?.type] || '🤖';
  };

  const handleSessionClick = (sessionId: string) => {
    dispatch(setActiveSession(sessionId));
  };

  return (
    <Box
      sx={{
        width: 300,
        bgcolor: 'background.paper',
        borderRight: '1px solid',
        borderColor: 'divider',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <Box sx={{ p: 3 }}>
        <Typography variant="h6" sx={{ fontWeight: 600 }}>
          Chat Sessions
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Active conversations with AI agents
        </Typography>
      </Box>

      <Divider />

      <List sx={{ flex: 1, overflow: 'auto', p: 1 }}>
        {sessionList.length === 0 ? (
          <Box sx={{ p: 3, textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              No active chat sessions
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Start a conversation from the dashboard
            </Typography>
          </Box>
        ) : (
          sessionList.map((session) => {
            const agent = agents[session.agentId];
            const isActive = session.id === activeSessionId;
            const lastMessage = session.messages[session.messages.length - 1];

            return (
              <ListItem key={session.id} disablePadding sx={{ mb: 0.5 }}>
                <ListItemButton
                  onClick={() => handleSessionClick(session.id)}
                  selected={isActive}
                  sx={{
                    borderRadius: 2,
                    '&.Mui-selected': {
                      bgcolor: 'primary.main',
                      color: 'primary.contrastText',
                      '&:hover': {
                        bgcolor: 'primary.dark',
                      },
                    },
                  }}
                >
                  <Stack direction="row" alignItems="center" spacing={2} sx={{ width: '100%' }}>
                    <Avatar
                      sx={{
                        width: 40,
                        height: 40,
                        bgcolor: isActive ? 'primary.contrastText' : 'primary.main',
                        color: isActive ? 'primary.main' : 'primary.contrastText',
                        fontSize: '1.2rem',
                      }}
                    >
                      {getAgentIcon(session.agentId)}
                    </Avatar>
                    <Box sx={{ flex: 1, minWidth: 0 }}>
                      <Typography
                        variant="subtitle2"
                        sx={{
                          fontWeight: 600,
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap',
                        }}
                      >
                        {agent?.name || 'Unknown Agent'}
                      </Typography>
                      <Typography
                        variant="caption"
                        sx={{
                          color: isActive ? 'inherit' : 'text.secondary',
                          opacity: 0.8,
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap',
                          display: 'block',
                        }}
                      >
                        {lastMessage?.content || 'No messages yet'}
                      </Typography>
                    </Box>
                  </Stack>
                </ListItemButton>
              </ListItem>
            );
          })
        )}
      </List>
    </Box>
  );
};

export default ChatSidebar;