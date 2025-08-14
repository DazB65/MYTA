import { configureStore } from '@reduxjs/toolkit';
import authSlice from './slices/authSlice';
import agentsSlice from './slices/agentsSlice';
import chatSlice from './slices/chatSlice';
import analyticsSlice from './slices/analyticsSlice';
import uiSlice from './slices/uiSlice';

export const store = configureStore({
  reducer: {
    auth: authSlice,
    agents: agentsSlice,
    chat: chatSlice,
    analytics: analyticsSlice,
    ui: uiSlice,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;