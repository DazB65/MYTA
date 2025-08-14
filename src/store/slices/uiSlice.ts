import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Notification } from '../../types';

interface UIState {
  theme: 'light' | 'dark' | 'auto';
  notifications: Notification[];
  isMobile: boolean;
  sidebarOpen: boolean;
}

const initialState: UIState = {
  theme: 'dark',
  notifications: [],
  isMobile: false,
  sidebarOpen: true,
};

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    setTheme: (state, action: PayloadAction<'light' | 'dark' | 'auto'>) => {
      state.theme = action.payload;
    },
    addNotification: (state, action: PayloadAction<Notification>) => {
      state.notifications.push(action.payload);
    },
    removeNotification: (state, action: PayloadAction<string>) => {
      state.notifications = state.notifications.filter(n => n.id !== action.payload);
    },
    setMobile: (state, action: PayloadAction<boolean>) => {
      state.isMobile = action.payload;
    },
    toggleSidebar: (state) => {
      state.sidebarOpen = !state.sidebarOpen;
    },
    setSidebarOpen: (state, action: PayloadAction<boolean>) => {
      state.sidebarOpen = action.payload;
    },
  },
});

export const { 
  setTheme, 
  addNotification, 
  removeNotification, 
  setMobile, 
  toggleSidebar, 
  setSidebarOpen 
} = uiSlice.actions;
export default uiSlice.reducer;