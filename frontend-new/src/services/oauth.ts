/**
 * OAuth Service for YouTube Authentication
 * Handles OAuth 2.0 flow integration with React
 */

export interface OAuthStatus {
  authenticated: boolean;
  user_id: string;
  expires_at?: string;
  expires_in_seconds?: number;
  scopes?: string[];
  needs_refresh?: boolean;
  message?: string;
}

export interface OAuthInitRequest {
  user_id: string;
  return_url?: string;
}

export interface OAuthInitResponse {
  authorization_url: string;
  state: string;
  user_id: string;
  return_url?: string;
  message: string;
}

export interface AuthenticatedChannelData {
  channel_data: {
    basic_info: {
      channel_id: string;
      title: string;
      subscriber_count: number;
      video_count: number;
      view_count: number;
      upload_frequency: string;
    };
    engagement_metrics: {
      avg_views_last_30: number;
      avg_engagement_last_30: number;
      growth_rate: number;
    };
    recent_videos: Array<{
      video_id: string;
      title: string;
      view_count: number;
      like_count: number;
      comment_count: number;
      published_at: string;
      engagement_rate: number;
    }>;
  };
  analytics_data: any;
  oauth_authenticated: boolean;
  status: string;
}

class OAuthService {
  private baseUrl = ''; // Use relative URLs to avoid CORS and routing issues
  private isAuthenticating = false;

  /**
   * Check current OAuth authentication status
   */
  async checkOAuthStatus(userId: string): Promise<OAuthStatus> {
    try {
      const response = await fetch(`${this.baseUrl}/auth/status/${userId}`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      const data = await response.json();
      
      // Transform backend response to match frontend interface
      const transformedStatus = {
        authenticated: data.authenticated,
        user_id: data.user_id,
        expires_at: data.expires_at,
        expires_in_seconds: data.expires_in_seconds,
        scopes: data.scopes,
        needs_refresh: data.needs_refresh,
        message: data.message
      };
      
      
      return transformedStatus;
    } catch (error) {
      console.error('Error checking OAuth status:', error);
      return {
        authenticated: false,
        user_id: userId,
        message: 'Failed to check authentication status'
      };
    }
  }

  /**
   * Initiate OAuth authorization flow
   */
  async initiateOAuth(request: OAuthInitRequest): Promise<string> {
    console.log('🚀 OAuth: Initiating OAuth flow...', request);
    
    if (this.isAuthenticating) {
      console.log('⚠️ OAuth: Already authenticating, aborting');
      throw new Error('OAuth flow already in progress');
    }

    this.isAuthenticating = true;

    try {
      console.log('📡 OAuth: Making request to /auth/initiate');
      const response = await fetch(`${this.baseUrl}/auth/initiate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: request.user_id,
          return_url: request.return_url || window.location.href
        })
      });

      console.log('📡 OAuth: Response received', response.status, response.statusText);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('❌ OAuth: Request failed', response.status, errorText);
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data: OAuthInitResponse = await response.json();
      console.log('✅ OAuth: Response data', data);

      if (data.authorization_url) {
        // Store state for validation
        localStorage.setItem('oauth_state', data.state);
        localStorage.setItem('oauth_return_url', request.return_url || window.location.href);
        
        console.log('🔄 OAuth: About to redirect to', data.authorization_url);
        return data.authorization_url;
      } else {
        console.error('❌ OAuth: No authorization URL in response');
        throw new Error(data.message || 'Failed to initiate OAuth');
      }
    } catch (error) {
      console.error('💥 OAuth: Error in initiateOAuth', error);
      this.isAuthenticating = false;
      throw error;
    }
  }

  /**
   * Handle OAuth callback parameters
   */
  handleOAuthCallback(): { success: boolean; error?: string; userId?: string } {
    console.log('🔍 OAuth: Current URL:', window.location.href);
    console.log('🔍 OAuth: URL search params:', window.location.search);
    
    const urlParams = new URLSearchParams(window.location.search);
    const oauthSuccess = urlParams.get('oauth_success');
    const oauthError = urlParams.get('oauth_error');
    const userId = urlParams.get('user_id');
    
    console.log('🔍 OAuth: Parsed params - success:', oauthSuccess, 'error:', oauthError, 'userId:', userId);

    if (oauthSuccess === 'true') {
      // Clean up URL parameters
      window.history.replaceState({}, document.title, window.location.pathname);
      this.isAuthenticating = false;
      return { success: true, userId: userId || undefined };
    } else if (oauthError) {
      // Clean up URL parameters
      window.history.replaceState({}, document.title, window.location.pathname);
      this.isAuthenticating = false;
      
      let errorMessage = 'YouTube authentication failed. ';
      
      switch (oauthError) {
        case 'access_denied':
          errorMessage += 'Access was denied by user.';
          break;
        case 'invalid_request':
          errorMessage += 'Invalid request parameters.';
          break;
        case 'server_error':
          errorMessage += 'Server error occurred.';
          break;
        case 'callback_failed':
          errorMessage += 'Authentication callback failed.';
          break;
        case 'missing_parameters':
          errorMessage += 'Missing required parameters.';
          break;
        default:
          errorMessage += 'Please try again.';
      }
      
      return { success: false, error: errorMessage };
    }

    return { success: false };
  }

  /**
   * Refresh OAuth token
   */
  async refreshToken(userId: string): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/auth/refresh/${userId}`, {
        method: 'POST'
      });

      if (response.ok) {
        return true;
      } else {
        const data = await response.json().catch(() => ({}));
        throw new Error(data.detail || data.message || 'Failed to refresh token');
      }
    } catch (error) {
      console.error('Error refreshing token:', error);
      return false;
    }
  }

  /**
   * Revoke OAuth token
   */
  async revokeToken(userId: string): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/auth/revoke/${userId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        return true;
      } else {
        const data = await response.json().catch(() => ({}));
        throw new Error(data.detail || data.message || 'Failed to revoke token');
      }
    } catch (error) {
      console.error('Error revoking token:', error);
      return false;
    }
  }

  /**
   * Get authenticated YouTube channel data
   */
  async getAuthenticatedChannelData(channelId: string, userId: string): Promise<AuthenticatedChannelData> {
    try {
      const response = await fetch(`${this.baseUrl}/api/youtube/analytics/authenticated`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          channel_id: channelId,
          user_id: userId,
          include_videos: true,
          video_count: 10,
          analysis_type: 'comprehensive'
        })
      });

      if (response.ok) {
        return await response.json();
      } else {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to get authenticated channel data');
      }
    } catch (error) {
      console.error('Error getting authenticated channel data:', error);
      throw error;
    }
  }

  /**
   * Check OAuth system health
   */
  async checkOAuthHealth(): Promise<any> {
    try {
      const response = await fetch(`${this.baseUrl}/auth/health`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error checking OAuth health:', error);
      return { status: 'unhealthy', error: error instanceof Error ? error.message : 'Unknown error' };
    }
  }

  /**
   * Check if currently authenticating
   */
  getIsAuthenticating(): boolean {
    return this.isAuthenticating;
  }

  /**
   * Reset authentication state
   */
  resetAuthenticationState(): void {
    this.isAuthenticating = false;
  }
}

// Export singleton instance
export const oauthService = new OAuthService();
export default oauthService;