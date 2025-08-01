/**
 * OAuth Store for React State Management
 * Manages OAuth authentication state using Zustand
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { useEffect } from 'react';
import oauthService, { OAuthStatus, AuthenticatedChannelData } from '../services/oauth';
import { secureTokenStorage } from '../utils/secureStorage';

interface OAuthState {
  // Authentication state
  isAuthenticated: boolean;
  status: OAuthStatus | null;
  isLoading: boolean;
  error: string | null;
  
  // User info
  userId: string;
  
  // OAuth flow state
  isAuthenticating: boolean;
  
  // Authenticated data
  authenticatedChannelData: AuthenticatedChannelData | null;
  
  // Actions
  initialize: () => Promise<void>;
  setUserId: (userId: string) => Promise<void>;
  checkStatus: () => Promise<void>;
  initiateOAuth: (returnUrl?: string) => Promise<void>;
  handleCallback: () => { success: boolean; error?: string };
  refreshToken: () => Promise<boolean>;
  revokeToken: () => Promise<boolean>;
  getChannelData: (channelId: string) => Promise<AuthenticatedChannelData | null>;
  clearError: () => void;
  resetAuthentication: () => void;
}

export const useOAuthStore = create<OAuthState>()(
  persist(
    (set, get) => ({
      // Initial state
      isAuthenticated: false,
      status: null,
      isLoading: false,
      error: null,
      userId: 'default_user', // Will be updated in initialize()
      isAuthenticating: false,
      authenticatedChannelData: null,

      // Initialize store by loading user data from secure storage
      initialize: async () => {
        try {
          // First try to get user ID from localStorage (same as userStore)
          let userId = localStorage.getItem('Vidalytics_user_id');
          
          if (!userId) {
            // Generate and store a new user ID if none exists
            userId = 'user_' + Math.random().toString(36).substring(2, 15);
            localStorage.setItem('Vidalytics_user_id', userId);
          }
          
          set({ userId });
          
          // Also try secure storage (fallback)
          const userData = await secureTokenStorage.getUserData();
          if (userData?.userId && userData.userId !== userId) {
            console.log('🔄 OAuth: Using secure storage user ID:', userData.userId);
            set({ userId: userData.userId });
          }
        } catch (error) {
          console.warn('Failed to load user data from secure storage:', error);
        }
      },

      // Set user ID
      setUserId: async (userId: string) => {
        await secureTokenStorage.setUserData({ userId });
        set({ userId });
      },

      // Check OAuth status
      checkStatus: async () => {
        const { userId } = get();
        set({ isLoading: true, error: null });

        try {
          const status = await oauthService.checkOAuthStatus(userId);
          
          
          set({
            status,
            isAuthenticated: status.authenticated,
            isLoading: false,
            error: null
          });
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Failed to check OAuth status'
          });
        }
      },

      // Initiate OAuth flow
      initiateOAuth: async (returnUrl?: string) => {
        const { userId } = get();
        console.log('🎯 Store: Starting OAuth for user', userId, 'returnUrl:', returnUrl);
        set({ isAuthenticating: true, error: null });

        try {
          console.log('🎯 Store: Calling oauthService.initiateOAuth');
          const authUrl = await oauthService.initiateOAuth({
            user_id: userId,
            return_url: returnUrl
          });

          console.log('🎯 Store: Got authorization URL, redirecting...', authUrl);
          // Redirect to Google OAuth
          window.location.href = authUrl;
        } catch (error) {
          console.error('🎯 Store: OAuth initiation failed', error);
          set({
            isAuthenticating: false,
            error: error instanceof Error ? error.message : 'Failed to initiate OAuth'
          });
        }
      },

      // Handle OAuth callback
      handleCallback: () => {
        const result = oauthService.handleOAuthCallback();
        
        if (result.success) {
          set({ 
            isAuthenticating: false, 
            error: null 
          });
          
          // Check status after successful callback
          get().checkStatus();
          
          return { success: true, userId: result.userId };
        } else if (result.error) {
          set({ 
            isAuthenticating: false, 
            error: result.error 
          });
          
          return { success: false, error: result.error };
        }
        
        return { success: false };
      },

      // Refresh token
      refreshToken: async () => {
        const { userId } = get();
        set({ isLoading: true, error: null });

        try {
          const success = await oauthService.refreshToken(userId);
          
          if (success) {
            // Refresh status after token refresh
            await get().checkStatus();
            return true;
          } else {
            set({ 
              isLoading: false,
              error: 'Failed to refresh token'
            });
            return false;
          }
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Failed to refresh token'
          });
          return false;
        }
      },

      // Revoke token
      revokeToken: async () => {
        const { userId } = get();
        set({ isLoading: true, error: null });

        try {
          const success = await oauthService.revokeToken(userId);
          
          if (success) {
            set({
              isAuthenticated: false,
              status: null,
              authenticatedChannelData: null,
              isLoading: false,
              error: null
            });
            return true;
          } else {
            set({ 
              isLoading: false,
              error: 'Failed to revoke token'
            });
            return false;
          }
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Failed to revoke token'
          });
          return false;
        }
      },

      // Get authenticated channel data
      getChannelData: async (channelId: string) => {
        const { userId, isAuthenticated } = get();
        
        if (!isAuthenticated) {
          set({ error: 'Not authenticated. Please connect your YouTube account first.' });
          return null;
        }

        set({ isLoading: true, error: null });

        try {
          const data = await oauthService.getAuthenticatedChannelData(channelId, userId);
          set({
            authenticatedChannelData: data,
            isLoading: false,
            error: null
          });
          return data;
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Failed to get channel data'
          });
          return null;
        }
      },

      // Clear error
      clearError: () => {
        set({ error: null });
      },

      // Reset authentication state
      resetAuthentication: () => {
        oauthService.resetAuthenticationState();
        secureTokenStorage.clearAll(); // Clear all secure storage
        set({
          isAuthenticated: false,
          status: null,
          isAuthenticating: false,
          authenticatedChannelData: null,
          error: null,
          userId: 'default_user'
        });
      }
    }),
    {
      name: 'oauth-store',
      partialize: (state) => ({
        userId: state.userId,
        // Don't persist sensitive auth data - it will be refreshed on app load
      })
    }
  )
);

// Custom hook for OAuth status checking
export const useOAuthStatus = () => {
  const store = useOAuthStore();
  
  // Auto-check status on mount and periodically
  useEffect(() => {
    // Check status on mount
    store.checkStatus();
    
    // Set up periodic status checking (every 5 minutes)
    const interval = setInterval(() => {
      if (store.isAuthenticated) {
        store.checkStatus();
      }
    }, 5 * 60 * 1000);
    
    return () => clearInterval(interval);
  }, [store.checkStatus, store.isAuthenticated]);
  
  return store;
};

export default useOAuthStore;