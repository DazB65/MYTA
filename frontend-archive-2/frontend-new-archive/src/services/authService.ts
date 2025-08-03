/**
 * Authentication Service
 * Handles JWT-based authentication with secure token storage
 */

import React from 'react';
import { secureTokenStorage } from '../utils/secureStorage';

interface LoginResponse {
  token: string;
  user_id: string;
  expires_in: number;
}

interface UserInfo {
  user_id: string;
  session_id: string;
  permissions: string[];
  expires_at: string;
}

interface AuthState {
  isAuthenticated: boolean;
  user: UserInfo | null;
  loading: boolean;
  error: string | null;
}

class AuthService {
  private baseUrl = '/api/auth';
  private authState: AuthState = {
    isAuthenticated: false,
    user: null,
    loading: false,
    error: null
  };
  private listeners: ((state: AuthState) => void)[] = [];

  constructor() {
    this.initialize();
  }

  private async initialize() {
    try {
      const token = await secureTokenStorage.getToken();
      if (token) {
        await this.validateToken();
      }
    } catch (error) {
      console.warn('Failed to initialize auth service:', error);
    }
  }

  private notifyListeners() {
    this.listeners.forEach(listener => listener(this.authState));
  }

  public subscribe(listener: (state: AuthState) => void) {
    this.listeners.push(listener);
    // Immediately call with current state
    listener(this.authState);
    
    // Return unsubscribe function
    return () => {
      const index = this.listeners.indexOf(listener);
      if (index > -1) {
        this.listeners.splice(index, 1);
      }
    };
  }

  private async makeAuthenticatedRequest(url: string, options: RequestInit = {}) {
    const token = await secureTokenStorage.getToken();
    
    const headers = new Headers(options.headers);
    if (token) {
      headers.set('Authorization', `Bearer ${token}`);
    }
    headers.set('Content-Type', 'application/json');

    // Add CSRF protection for POST requests
    if (options.method === 'POST' || options.method === 'PUT' || options.method === 'PATCH') {
      headers.set('X-Requested-With', 'XMLHttpRequest');
    }

    return fetch(url, {
      ...options,
      headers,
      credentials: 'same-origin' // Only send cookies to same origin
    });
  }

  public async login(userId: string): Promise<boolean> {
    try {
      this.authState.loading = true;
      this.authState.error = null;
      this.notifyListeners();

      const response = await fetch(`${this.baseUrl}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'same-origin',
        body: JSON.stringify({ user_id: userId })
      });

      if (!response.ok) {
        throw new Error(`Login failed: ${response.statusText}`);
      }

      const data: { data: LoginResponse } = await response.json();
      const { token, expires_in } = data.data;

      // Store token securely
      await secureTokenStorage.setToken(token, expires_in / 60); // Convert seconds to minutes

      // Get user info
      await this.getCurrentUser();

      this.authState.loading = false;
      this.notifyListeners();

      return true;
    } catch (error) {
      this.authState.loading = false;
      this.authState.error = error instanceof Error ? error.message : 'Login failed';
      this.authState.isAuthenticated = false;
      this.authState.user = null;
      this.notifyListeners();
      return false;
    }
  }

  public async logout(): Promise<void> {
    try {
      // Try to call logout endpoint
      await this.makeAuthenticatedRequest(`${this.baseUrl}/logout`, {
        method: 'POST'
      });
    } catch (error) {
      console.warn('Logout API call failed:', error);
    } finally {
      // Clear local storage regardless of API call success
      await secureTokenStorage.clearAll();
      
      this.authState.isAuthenticated = false;
      this.authState.user = null;
      this.authState.error = null;
      this.notifyListeners();
    }
  }

  public async getCurrentUser(): Promise<UserInfo | null> {
    try {
      const response = await this.makeAuthenticatedRequest(`${this.baseUrl}/me`);
      
      if (!response.ok) {
        if (response.status === 401) {
          await this.logout();
        }
        throw new Error(`Failed to get user info: ${response.statusText}`);
      }

      const data: { data: UserInfo } = await response.json();
      
      this.authState.isAuthenticated = true;
      this.authState.user = data.data;
      this.authState.error = null;
      this.notifyListeners();

      return data.data;
    } catch (error) {
      this.authState.isAuthenticated = false;
      this.authState.user = null;
      this.authState.error = error instanceof Error ? error.message : 'Failed to get user info';
      this.notifyListeners();
      return null;
    }
  }

  public async validateToken(): Promise<boolean> {
    const token = await secureTokenStorage.getToken();
    if (!token) {
      this.authState.isAuthenticated = false;
      this.authState.user = null;
      this.notifyListeners();
      return false;
    }

    try {
      const user = await this.getCurrentUser();
      return !!user;
    } catch (error) {
      await secureTokenStorage.clearToken();
      return false;
    }
  }

  public async makeApiRequest(url: string, options: RequestInit = {}) {
    const response = await this.makeAuthenticatedRequest(url, options);
    
    if (response.status === 401) {
      // Token expired or invalid
      await this.logout();
      throw new Error('Authentication required');
    }
    
    return response;
  }

  public getAuthState(): AuthState {
    return { ...this.authState };
  }

  public isAuthenticated(): boolean {
    return this.authState.isAuthenticated;
  }

  public getUser(): UserInfo | null {
    return this.authState.user;
  }

  public getUserId(): string | null {
    return this.authState.user?.user_id || null;
  }

  public hasPermission(permission: string): boolean {
    return this.authState.user?.permissions.includes(permission) || false;
  }

  // Legacy support for existing code
  public async getLegacyUserId(): Promise<string> {
    const user = this.getUser();
    if (user) {
      return user.user_id;
    }

    // Fallback to secure storage for backward compatibility
    const userData = await secureTokenStorage.getUserData();
    return userData?.userId || 'default_user';
  }
}

// Create singleton instance
export const authService = new AuthService();

// React hook for using auth state
export function useAuth() {
  const [authState, setAuthState] = React.useState<AuthState>(authService.getAuthState());

  React.useEffect(() => {
    const unsubscribe = authService.subscribe(setAuthState);
    return unsubscribe;
  }, []);

  return {
    ...authState,
    login: authService.login.bind(authService),
    logout: authService.logout.bind(authService),
    hasPermission: authService.hasPermission.bind(authService),
    getUserId: authService.getUserId.bind(authService)
  };
}

export default authService;