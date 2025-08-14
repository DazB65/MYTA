import React from 'react';
import {
  Box,
  TextField,
  IconButton,
  Stack,
} from '@mui/material';
import { useDispatch } from 'react-redux';
import { addMessage, setAgentTyping } from '../../store/slices/chatSlice';
import { ChatMessage } from '../../types';
import SendIcon from '@mui/icons-material/Send';
import { v4 as uuidv4 } from 'uuid';

interface ChatInputProps {
  message: string;
  setMessage: (message: string) => void;
  sessionId: string;
}

const ChatInput: React.FC<ChatInputProps> = ({ message, setMessage, sessionId }) => {
  const dispatch = useDispatch();

  const handleSend = async () => {
    if (!message.trim()) return;

    // Add user message
    const userMessage: ChatMessage = {
      id: uuidv4(),
      agentId: sessionId,
      userId: 'demo-user',
      content: message,
      type: 'text',
      timestamp: new Date(),
      isFromUser: true,
    };

    dispatch(addMessage({ sessionId, message: userMessage }));
    setMessage('');

    // Simulate agent typing
    dispatch(setAgentTyping({ agentId: sessionId, typing: true }));

    // Simulate agent response after delay
    setTimeout(() => {
      dispatch(setAgentTyping({ agentId: sessionId, typing: false }));
      
      const agentResponse: ChatMessage = {
        id: uuidv4(),
        agentId: sessionId,
        userId: 'demo-user',
        content: generateMockResponse(message),
        type: 'text',
        timestamp: new Date(),
        isFromUser: false,
      };

      dispatch(addMessage({ sessionId, message: agentResponse }));
    }, 2000);
  };

  const generateMockResponse = (userMessage: string): string => {
    const responses = [
      "I've analyzed your request and here's what I found based on your YouTube data...",
      "That's an interesting question! Let me provide some insights based on current trends...",
      "Based on your channel's performance metrics, I recommend the following strategies...",
      "I can help you with that! Here are some data-driven suggestions...",
      "Great question! Let me break down the analytics for you...",
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Box
      sx={{
        p: 2,
        bgcolor: 'background.paper',
        borderTop: '1px solid',
        borderColor: 'divider',
      }}
    >
      <Stack direction="row" spacing={2} alignItems="flex-end">
        <TextField
          fullWidth
          multiline
          maxRows={4}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message..."
          variant="outlined"
          sx={{
            '& .MuiOutlinedInput-root': {
              borderRadius: 3,
            },
          }}
        />
        <IconButton
          onClick={handleSend}
          disabled={!message.trim()}
          sx={{
            bgcolor: 'primary.main',
            color: 'primary.contrastText',
            '&:hover': {
              bgcolor: 'primary.dark',
            },
            '&:disabled': {
              bgcolor: 'action.disabledBackground',
              color: 'action.disabled',
            },
          }}
        >
          <SendIcon />
        </IconButton>
      </Stack>
    </Box>
  );
};

export default ChatInput;