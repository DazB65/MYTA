import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { ChatSession, ChatMessage } from '../../types';

interface ChatState {
  sessions: Record<string, ChatSession>;
  activeSessionId: string | null;
  loading: boolean;
  error: string | null;
  typingAgents: string[];
}

const initialState: ChatState = {
  sessions: {},
  activeSessionId: null,
  loading: false,
  error: null,
  typingAgents: [],
};

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    createSession: (state, action: PayloadAction<ChatSession>) => {
      const session = action.payload;
      state.sessions[session.id] = session;
      state.activeSessionId = session.id;
    },
    setActiveSession: (state, action: PayloadAction<string>) => {
      state.activeSessionId = action.payload;
    },
    addMessage: (state, action: PayloadAction<{ sessionId: string; message: ChatMessage }>) => {
      const { sessionId, message } = action.payload;
      if (state.sessions[sessionId]) {
        state.sessions[sessionId].messages.push(message);
        state.sessions[sessionId].updatedAt = new Date();
      }
    },
    setAgentTyping: (state, action: PayloadAction<{ agentId: string; typing: boolean }>) => {
      const { agentId, typing } = action.payload;
      if (typing && !state.typingAgents.includes(agentId)) {
        state.typingAgents.push(agentId);
      } else if (!typing) {
        state.typingAgents = state.typingAgents.filter(id => id !== agentId);
      }
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
  },
});

export const { 
  createSession, 
  setActiveSession, 
  addMessage, 
  setAgentTyping, 
  setLoading, 
  setError 
} = chatSlice.actions;
export default chatSlice.reducer;