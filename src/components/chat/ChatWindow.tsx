import React, { useEffect, useRef } from 'react';
import {
  Box,
  Stack,
  Typography,
  Avatar,
  Paper,
  Chip,
} from '@mui/material';
import { useSelector } from 'react-redux';
import { RootState } from '../../store';
import { ChatSession } from '../../types';

interface ChatWindowProps {
  session: ChatSession;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ session }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { agents } = useSelector((state: RootState) => state.agents);
  const { typingAgents } = useSelector((state: RootState) => state.chat);
  
  const agent = agents[session.agentId];
  const isAgentTyping = typingAgents.includes(session.agentId);

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

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [session.messages]);

  return (
    <Stack sx={{ flex: 1, minHeight: 0 }}>
      {/* Chat Header */}
      <Box
        sx={{
          p: 3,
          bgcolor: 'background.paper',
          borderBottom: '1px solid',
          borderColor: 'divider',
        }}
      >
        <Stack direction="row" alignItems="center" spacing={2}>
          <Avatar
            sx={{
              bgcolor: 'primary.main',
              width: 48,
              height: 48,
              fontSize: '1.5rem',
            }}
          >
            {getAgentIcon(session.agentId)}
          </Avatar>
          <Box>
            <Typography variant="h6" sx={{ fontWeight: 600 }}>
              {agent?.name || 'Unknown Agent'}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {agent?.description || 'AI Assistant'}
            </Typography>
          </Box>
        </Stack>
      </Box>

      {/* Messages */}
      <Box
        sx={{
          flex: 1,
          overflow: 'auto',
          p: 2,
          bgcolor: 'background.default',
        }}
      >
        <Stack spacing={2}>
          {session.messages.length === 0 ? (
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <Typography variant="body1" color="text.secondary">
                Start a conversation with {agent?.name}
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                Ask questions about your YouTube analytics, content strategy, or get insights
              </Typography>
            </Box>
          ) : (
            session.messages.map((message) => (
              <Box
                key={message.id}
                sx={{
                  display: 'flex',
                  justifyContent: message.isFromUser ? 'flex-end' : 'flex-start',
                }}
              >
                <Paper
                  sx={{
                    p: 2,
                    maxWidth: '70%',
                    bgcolor: message.isFromUser ? 'primary.main' : 'background.paper',
                    color: message.isFromUser ? 'primary.contrastText' : 'text.primary',
                    borderRadius: 2,
                    border: message.isFromUser ? 'none' : '1px solid',
                    borderColor: 'divider',
                  }}
                >
                  <Typography variant="body1" sx={{ mb: 1 }}>
                    {message.content}
                  </Typography>
                  
                  {message.type !== 'text' && (
                    <Chip
                      label={message.type.replace('_', ' ')}
                      size="small"
                      variant="outlined"
                      sx={{
                        fontSize: '0.75rem',
                        height: 20,
                        textTransform: 'capitalize',
                        borderColor: message.isFromUser ? 'primary.contrastText' : 'primary.main',
                        color: message.isFromUser ? 'primary.contrastText' : 'primary.main',
                      }}
                    />
                  )}
                  
                  <Typography
                    variant="caption"
                    sx={{
                      display: 'block',
                      mt: 1,
                      opacity: 0.7,
                      textAlign: 'right',
                    }}
                  >
                    {new Date(message.timestamp).toLocaleTimeString()}
                  </Typography>
                </Paper>
              </Box>
            ))
          )}

          {/* Typing Indicator */}
          {isAgentTyping && (
            <Box sx={{ display: 'flex', justifyContent: 'flex-start' }}>
              <Paper
                sx={{
                  p: 2,
                  bgcolor: 'background.paper',
                  border: '1px solid',
                  borderColor: 'divider',
                  borderRadius: 2,
                }}
              >
                <Typography variant="body2" color="text.secondary">
                  {agent?.name} is typing...
                </Typography>
              </Paper>
            </Box>
          )}

          <div ref={messagesEndRef} />
        </Stack>
      </Box>
    </Stack>
  );
};

export default ChatWindow;