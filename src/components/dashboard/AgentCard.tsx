import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  Stack,
  IconButton,
  Avatar,
} from '@mui/material';
import { useDispatch } from 'react-redux';
import { Agent } from '../../types';
import { createSession } from '../../store/slices/chatSlice';
import ChatIcon from '@mui/icons-material/Chat';
import FiberManualRecordIcon from '@mui/icons-material/FiberManualRecord';
import { v4 as uuidv4 } from 'uuid';

interface AgentCardProps {
  agent: Agent;
}

const AgentCard: React.FC<AgentCardProps> = ({ agent }) => {
  const dispatch = useDispatch();

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online': return '#10b981';
      case 'busy': return '#f59e0b';
      case 'thinking': return '#6366f1';
      default: return '#6b7280';
    }
  };

  const getAgentIcon = (type: string) => {
    const iconMap: Record<string, string> = {
      boss_agent: '👑',
      content_analysis: '📊',
      audience_insights: '👥',
      seo_discoverability: '🔍',
      monetization_strategy: '💰',
      competitive_analysis: '📈',
    };
    return iconMap[type] || '🤖';
  };

  const handleChatClick = () => {
    const sessionId = uuidv4();
    const newSession = {
      id: sessionId,
      userId: 'demo-user',
      agentId: agent.id,
      title: `Chat with ${agent.name}`,
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
      isActive: true,
    };
    dispatch(createSession(newSession));
  };

  return (
    <Card
      sx={{
        height: '100%',
        transition: 'all 0.3s ease',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: 4,
        },
        border: '1px solid',
        borderColor: 'divider',
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Stack spacing={2}>
          <Box sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
            <Stack direction="row" alignItems="center" spacing={2}>
              <Avatar
                sx={{
                  bgcolor: 'primary.main',
                  width: 48,
                  height: 48,
                  fontSize: '1.5rem',
                }}
              >
                {getAgentIcon(agent.type)}
              </Avatar>
              <Box>
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 0.5 }}>
                  {agent.name}
                </Typography>
                <Stack direction="row" alignItems="center" spacing={1}>
                  <FiberManualRecordIcon
                    sx={{
                      fontSize: 12,
                      color: getStatusColor(agent.status),
                    }}
                  />
                  <Typography
                    variant="caption"
                    sx={{
                      color: getStatusColor(agent.status),
                      fontWeight: 500,
                      textTransform: 'capitalize',
                    }}
                  >
                    {agent.status}
                  </Typography>
                </Stack>
              </Box>
            </Stack>
            <IconButton
              size="small"
              onClick={handleChatClick}
              sx={{
                bgcolor: 'primary.main',
                color: 'primary.contrastText',
                '&:hover': {
                  bgcolor: 'primary.dark',
                },
              }}
            >
              <ChatIcon fontSize="small" />
            </IconButton>
          </Box>

          <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.5 }}>
            {agent.description}
          </Typography>

          <Box>
            <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
              Capabilities
            </Typography>
            <Stack direction="row" spacing={1} sx={{ flexWrap: 'wrap', gap: 1 }}>
              {agent.capabilities.slice(0, 3).map((capability) => (
                <Chip
                  key={capability}
                  label={capability.replace('_', ' ')}
                  size="small"
                  variant="outlined"
                  sx={{
                    fontSize: '0.75rem',
                    height: 24,
                    textTransform: 'capitalize',
                  }}
                />
              ))}
              {agent.capabilities.length > 3 && (
                <Chip
                  label={`+${agent.capabilities.length - 3} more`}
                  size="small"
                  variant="outlined"
                  sx={{
                    fontSize: '0.75rem',
                    height: 24,
                  }}
                />
              )}
            </Stack>
          </Box>

          {agent.lastActive && (
            <Typography variant="caption" color="text.secondary">
              Last active: {new Date(agent.lastActive).toLocaleTimeString()}
            </Typography>
          )}
        </Stack>
      </CardContent>
    </Card>
  );
};

export default AgentCard;