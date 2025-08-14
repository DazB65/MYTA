import React, { useState } from 'react';
import { Box, Stack } from '@mui/material';
import { useSelector } from 'react-redux';
import { RootState } from '../../store';
import ChatSidebar from './ChatSidebar';
import ChatWindow from './ChatWindow';
import ChatInput from './ChatInput';

const ChatInterface: React.FC = () => {
  const { sessions, activeSessionId } = useSelector((state: RootState) => state.chat);
  const activeSession = activeSessionId ? sessions[activeSessionId] : null;
  const [message, setMessage] = useState('');

  return (
    <Box sx={{ height: 'calc(100vh - 200px)', display: 'flex' }}>
      <ChatSidebar />
      
      <Stack sx={{ flex: 1, minWidth: 0 }}>
        {activeSession ? (
          <>
            <ChatWindow session={activeSession} />
            <ChatInput 
              message={message}
              setMessage={setMessage}
              sessionId={activeSession.id}
            />
          </>
        ) : (
          <Box 
            sx={{ 
              flex: 1, 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              bgcolor: 'background.paper',
              borderRadius: 2,
              border: '1px solid',
              borderColor: 'divider',
            }}
          >
            <Stack spacing={2} sx={{ textAlign: 'center', p: 4 }}>
              <Box sx={{ fontSize: '4rem' }}>💬</Box>
              <Box>
                <h3>Select an Agent to Start Chatting</h3>
                <p style={{ color: 'var(--color-text-secondary)' }}>
                  Choose an AI agent from your dashboard to begin a conversation
                </p>
              </Box>
            </Stack>
          </Box>
        )}
      </Stack>
    </Box>
  );
};

export default ChatInterface;