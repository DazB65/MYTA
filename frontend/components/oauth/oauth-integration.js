/**
 * OAuth Integration Component for CreatorMate
 * Handles YouTube OAuth 2.0 authentication flow
 */

class OAuthIntegration {
    constructor() {
        this.baseUrl = 'http://localhost:8888';
        this.userId = localStorage.getItem('creatormate_user_id') || 'default_user';
        this.isAuthenticating = false;
        this.oauthStatus = null;
        
        // Initialize OAuth status check
        this.checkOAuthStatus();
        
        // Listen for OAuth callback
        this.handleOAuthCallback();
    }

    /**
     * Check current OAuth authentication status
     */
    async checkOAuthStatus() {
        try {
            const response = await fetch(`${this.baseUrl}/auth/status/${this.userId}`);
            const data = await response.json();
            
            this.oauthStatus = data;
            this.updateUI();
            
            return data.authenticated;
        } catch (error) {
            console.error('Error checking OAuth status:', error);
            return false;
        }
    }

    /**
     * Initiate OAuth authorization flow
     */
    async initiateOAuth() {
        if (this.isAuthenticating) {
            return;
        }

        this.isAuthenticating = true;
        this.updateUI();

        try {
            const response = await fetch(`${this.baseUrl}/auth/initiate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: this.userId,
                    return_url: window.location.href
                })
            });

            const data = await response.json();

            if (response.ok && data.authorization_url) {
                // Store state for validation
                localStorage.setItem('oauth_state', data.state);
                localStorage.setItem('oauth_return_url', window.location.href);
                
                // Redirect to Google OAuth
                window.location.href = data.authorization_url;
            } else {
                throw new Error(data.detail || 'Failed to initiate OAuth');
            }
        } catch (error) {
            console.error('Error initiating OAuth:', error);
            this.showError('Failed to start YouTube authentication. Please try again.');
            this.isAuthenticating = false;
            this.updateUI();
        }
    }

    /**
     * Handle OAuth callback from Google
     */
    handleOAuthCallback() {
        const urlParams = new URLSearchParams(window.location.search);
        const oauthSuccess = urlParams.get('oauth_success');
        const oauthError = urlParams.get('oauth_error');
        const userId = urlParams.get('user_id');

        if (oauthSuccess === 'true') {
            this.handleOAuthSuccess(userId);
        } else if (oauthError) {
            this.handleOAuthError(oauthError);
        }
    }

    /**
     * Handle successful OAuth callback
     */
    async handleOAuthSuccess(userId) {
        this.showSuccess('YouTube authentication successful!');
        
        // Clean up URL parameters
        window.history.replaceState({}, document.title, window.location.pathname);
        
        // Update OAuth status
        await this.checkOAuthStatus();
        
        // Trigger custom event for other components
        window.dispatchEvent(new CustomEvent('oauth-success', {
            detail: { userId: userId }
        }));
    }

    /**
     * Handle OAuth error
     */
    handleOAuthError(error) {
        let errorMessage = 'YouTube authentication failed. ';
        
        switch (error) {
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
        
        this.showError(errorMessage);
        
        // Clean up URL parameters
        window.history.replaceState({}, document.title, window.location.pathname);
        
        this.isAuthenticating = false;
        this.updateUI();
    }

    /**
     * Refresh OAuth token
     */
    async refreshToken() {
        try {
            const response = await fetch(`${this.baseUrl}/auth/refresh/${this.userId}`, {
                method: 'POST'
            });

            const data = await response.json();

            if (response.ok) {
                this.showSuccess('Token refreshed successfully!');
                await this.checkOAuthStatus();
                return true;
            } else {
                throw new Error(data.detail || 'Failed to refresh token');
            }
        } catch (error) {
            console.error('Error refreshing token:', error);
            this.showError('Failed to refresh authentication token.');
            return false;
        }
    }

    /**
     * Revoke OAuth token
     */
    async revokeToken() {
        try {
            const response = await fetch(`${this.baseUrl}/auth/revoke/${this.userId}`, {
                method: 'DELETE'
            });

            const data = await response.json();

            if (response.ok) {
                this.showSuccess('YouTube access revoked successfully!');
                await this.checkOAuthStatus();
                return true;
            } else {
                throw new Error(data.detail || 'Failed to revoke token');
            }
        } catch (error) {
            console.error('Error revoking token:', error);
            this.showError('Failed to revoke YouTube access.');
            return false;
        }
    }

    /**
     * Get authenticated YouTube data
     */
    async getAuthenticatedChannelData(channelId) {
        try {
            const response = await fetch(`${this.baseUrl}/api/youtube/analytics/authenticated`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    channel_id: channelId,
                    user_id: this.userId,
                    include_videos: true,
                    video_count: 10,
                    analysis_type: 'comprehensive'
                })
            });

            const data = await response.json();

            if (response.ok) {
                return data;
            } else {
                throw new Error(data.detail || 'Failed to get authenticated data');
            }
        } catch (error) {
            console.error('Error getting authenticated data:', error);
            throw error;
        }
    }

    /**
     * Update UI based on OAuth status
     */
    updateUI() {
        // Update OAuth status indicator
        const statusElement = document.getElementById('oauth-status');
        if (statusElement) {
            if (this.oauthStatus?.authenticated) {
                statusElement.className = 'oauth-status text-xs flex items-center gap-1 px-2 py-1 rounded-full bg-green-500/20 text-green-200 border border-green-400/30';
                statusElement.innerHTML = `
                    <span class="status-icon">✓</span>
                    <span class="status-text">YouTube Connected</span>
                `;
            } else {
                statusElement.className = 'oauth-status text-xs flex items-center gap-1 px-2 py-1 rounded-full bg-red-500/20 text-red-200 border border-red-400/30';
                statusElement.innerHTML = `
                    <span class="status-icon">⚠</span>
                    <span class="status-text">YouTube Not Connected</span>
                `;
            }
        }

        // Update OAuth button
        const oauthButton = document.getElementById('oauth-connect-btn');
        if (oauthButton) {
            if (this.isAuthenticating) {
                oauthButton.disabled = true;
                oauthButton.textContent = 'Connecting...';
                oauthButton.className = 'w-full bg-gray-500 text-white text-sm font-medium py-2 px-4 rounded-lg cursor-not-allowed opacity-50';
            } else if (this.oauthStatus?.authenticated) {
                oauthButton.textContent = 'Disconnect YouTube';
                oauthButton.disabled = false;
                oauthButton.className = 'w-full bg-gradient-to-r from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white text-sm font-medium py-2 px-4 rounded-lg transition-all duration-200 shadow-lg hover:shadow-gray-500/25';
                oauthButton.onclick = () => this.revokeToken();
            } else {
                oauthButton.textContent = 'Connect YouTube';
                oauthButton.disabled = false;
                oauthButton.className = 'w-full bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white text-sm font-medium py-2 px-4 rounded-lg transition-all duration-200 shadow-lg hover:shadow-red-500/25';
                oauthButton.onclick = () => this.initiateOAuth();
            }
        }

        // Update token expiration info
        const tokenInfo = document.getElementById('oauth-token-info');
        if (tokenInfo) {
            if (this.oauthStatus?.authenticated) {
                const expiresIn = this.oauthStatus.expires_in_seconds;
                const needsRefresh = this.oauthStatus.needs_refresh;
                
                if (needsRefresh) {
                    tokenInfo.innerHTML = `
                        <span class="text-yellow-200">Token expired - refresh needed</span>
                    `;
                } else {
                    const hoursRemaining = Math.floor(expiresIn / 3600);
                    tokenInfo.innerHTML = `
                        <span class="text-green-200">Connected - expires in ${hoursRemaining}h</span>
                    `;
                }
            } else {
                tokenInfo.innerHTML = `
                    <span class="text-indigo-200">Connect your YouTube account for detailed analytics</span>
                `;
            }
        }
    }

    /**
     * Show success message
     */
    showSuccess(message) {
        this.showMessage(message, 'success');
    }

    /**
     * Show error message
     */
    showError(message) {
        this.showMessage(message, 'error');
    }

    /**
     * Show message to user
     */
    showMessage(message, type = 'info') {
        // Create message element
        const messageDiv = document.createElement('div');
        messageDiv.className = `oauth-message ${type}`;
        messageDiv.textContent = message;

        // Add to page
        const container = document.getElementById('oauth-messages') || document.body;
        container.appendChild(messageDiv);

        // Remove after 5 seconds
        setTimeout(() => {
            messageDiv.remove();
        }, 5000);

        // Also log to console
        console.log(`OAuth ${type}:`, message);
    }

    /**
     * Check if user is authenticated
     */
    isAuthenticated() {
        return this.oauthStatus?.authenticated || false;
    }

    /**
     * Get OAuth scopes
     */
    getScopes() {
        return this.oauthStatus?.scopes || [];
    }
}

// Initialize OAuth integration
const oauthIntegration = new OAuthIntegration();

// Export for use in other modules
window.oauthIntegration = oauthIntegration;