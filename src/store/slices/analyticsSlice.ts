import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { AnalyticsData } from '../../types';

interface AnalyticsState {
  data: AnalyticsData;
  loading: boolean;
  error: string | null;
  isConnected: boolean;
}

const initialState: AnalyticsState = {
  data: {
    totalViews: 125000,
    totalSubscribers: 5420,
    totalVideos: 87,
    healthScore: 75,
    revenueMetrics: {
      total: 1250,
      rpm: 3.2,
      cpm: 1.8,
    },
    subscriberGrowth: {
      net: 150,
      rate: 2.5,
    },
  },
  loading: false,
  error: null,
  isConnected: true,
};

const analyticsSlice = createSlice({
  name: 'analytics',
  initialState,
  reducers: {
    setAnalyticsData: (state, action: PayloadAction<AnalyticsData>) => {
      state.data = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    setConnected: (state, action: PayloadAction<boolean>) => {
      state.isConnected = action.payload;
    },
  },
});

export const { setAnalyticsData, setLoading, setError, setConnected } = analyticsSlice.actions;
export default analyticsSlice.reducer;