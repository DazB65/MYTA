/**
 * OAuth Connection Component
 * Handles YouTube OAuth connection/disconnection
 */

import { useState, useEffect } from 'react';
import { useOAuthStore } from '../../store/oauthStore';
import { Youtube, RefreshCw, LogOut, AlertCircle, CheckCircle, Loader } from 'lucide-react';
import Button from '../common/Button';
import oauthService from '../../services/oauth';

interface OAuthConnectionProps {
  variant?: 'sidebar' | 'full' | 'compact';
  showBenefits?: boolean;
  onSuccess?: () => void;
  onError?: (error: string) => void;
}

export default function OAuthConnection({ 
  variant = 'full',
  showBenefits = false,
  onSuccess,
  onError 
}: OAuthConnectionProps) {
  const {
    isAuthenticated,
    status,
    isLoading,
    isAuthenticating,
    error,
    initiateOAuth,
    refreshToken,
    revokeToken,
    handleCallback,
    clearError,
    checkStatus
  } = useOAuthStore();

  const [showSuccess, setShowSuccess] = useState(false);
  const [directStatus, setDirectStatus] = useState<any>(null);

  // Check OAuth status on component mount
  useEffect(() => {
    checkStatus();
    
    // Also get direct status as fallback
    const getDirectStatus = async () => {
      try {
        const result = await oauthService.checkOAuthStatus('default_user');
        setDirectStatus(result);
      } catch (err) {
        console.error('Direct OAuth call failed:', err);
      }
    };
    
    getDirectStatus();
  }, [checkStatus]);

  // Handle OAuth callback on component mount
  useEffect(() => {
    const result = handleCallback();
    if (result.success) {
      setShowSuccess(true);
      onSuccess?.();
      setTimeout(() => setShowSuccess(false), 5000);
    } else if (result.error) {
      onError?.(result.error);
    }
  }, [handleCallback, onSuccess, onError]);

  const handleConnect = async () => {
    try {
      clearError();
      await initiateOAuth(window.location.href);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to connect to YouTube';
      onError?.(errorMessage);
    }
  };

  const handleRefresh = async () => {
    try {
      clearError();
      const success = await refreshToken();
      if (success) {
        setShowSuccess(true);
        setTimeout(() => setShowSuccess(false), 3000);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to refresh token';
      onError?.(errorMessage);
    }
  };

  const handleDisconnect = async () => {
    if (!confirm('Are you sure you want to disconnect your YouTube account? You will lose access to detailed analytics.')) {
      return;
    }

    try {
      clearError();
      const success = await revokeToken();
      if (success) {
        setShowSuccess(true);
        setTimeout(() => setShowSuccess(false), 3000);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to disconnect YouTube account';
      onError?.(errorMessage);
    }
  };

  // Compact variant for sidebar
  if (variant === 'compact') {
    return (
      <div className="space-y-2">
        {showSuccess && (
          <div className="flex items-center gap-2 text-xs text-green-600 bg-green-50 px-2 py-1 rounded">
            <CheckCircle className="w-3 h-3" />
            Operation successful!
          </div>
        )}

        {error && (
          <div className="flex items-center gap-2 text-xs text-red-600 bg-red-50 px-2 py-1 rounded">
            <AlertCircle className="w-3 h-3" />
            {error}
          </div>
        )}

        {isAuthenticated ? (
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-xs text-green-600">
              <CheckCircle className="w-3 h-3" />
              Connected
            </div>
            <div className="flex gap-1">
              <Button
                onClick={handleRefresh}
                disabled={isLoading}
                variant="secondary"
                size="sm"
                className="text-xs px-2 py-1 h-6"
              >
                {isLoading ? <Loader className="w-3 h-3 animate-spin" /> : <RefreshCw className="w-3 h-3" />}
              </Button>
              <Button
                onClick={handleDisconnect}
                disabled={isLoading}
                variant="secondary"
                size="sm"
                className="text-xs px-2 py-1 h-6 text-red-600 hover:bg-red-50"
              >
                <LogOut className="w-3 h-3" />
              </Button>
            </div>
          </div>
        ) : (
          <Button
            onClick={handleConnect}
            disabled={isLoading || isAuthenticating}
            variant="primary"
            size="sm"
            className="w-full text-xs bg-red-600 hover:bg-red-700"
          >
            {isAuthenticating ? (
              <>
                <Loader className="w-3 h-3 animate-spin mr-1" />
                Connecting...
              </>
            ) : (
              <>
                <Youtube className="w-3 h-3 mr-1" />
                Connect
              </>
            )}
          </Button>
        )}
      </div>
    );
  }

  // Sidebar variant
  if (variant === 'sidebar') {
    return (
      <div className="bg-white/10 backdrop-blur-sm border border-indigo-400/20 rounded-lg p-4 shadow-lg">
        <div className="flex items-center justify-between mb-3">
          <h4 className="font-medium text-white flex items-center gap-2">
            <Youtube className="w-4 h-4 text-red-500" />
            YouTube Connection
          </h4>
        </div>

        {showSuccess && (
          <div className="flex items-center gap-2 text-xs text-green-200 bg-green-500/20 px-2 py-1 rounded mb-3">
            <CheckCircle className="w-3 h-3" />
            Success!
          </div>
        )}

        {error && (
          <div className="flex items-center gap-2 text-xs text-red-200 bg-red-500/20 px-2 py-1 rounded mb-3">
            <AlertCircle className="w-3 h-3" />
            {error}
          </div>
        )}

        <div className="text-sm mb-3">
          {isAuthenticated ? (
            status?.needs_refresh ? (
              <span className="text-yellow-200 font-medium">⚠ Token expired - refresh needed</span>
            ) : (
              <div className="space-y-1">
                <span className="text-green-200 font-medium">✅ Connected - access to detailed analytics</span>
                {((status?.expires_in_seconds !== undefined) || (directStatus?.expires_in_seconds !== undefined)) && (
                  <div 
                    className="text-white font-bold bg-black/40 px-3 py-2 rounded-lg border border-white/20"
                    style={{ 
                      fontSize: '14px', 
                      color: '#ffffff', 
                      backgroundColor: 'rgba(0, 0, 0, 0.6)',
                      border: '1px solid rgba(255, 255, 255, 0.3)'
                    }}
                  >
                    {(() => {
                      // TEMPORARY: Always use direct status since store is not working properly
                      const effectiveStatus = directStatus || status;
                      const hours = Math.floor((effectiveStatus?.expires_in_seconds || 0) / 3600);
                      return `⏰ Expires in ${hours} hours`;
                    })()}
                  </div>
                )}
              </div>
            )
          ) : (
            <span className="text-indigo-200">Connect your YouTube account for detailed analytics</span>
          )}
        </div>

        {isAuthenticated ? (
          <div className="space-y-2">
            <Button
              onClick={handleRefresh}
              disabled={isLoading}
              variant="secondary"
              size="sm"
              className="w-full text-sm"
            >
              {isLoading ? (
                <>
                  <Loader className="w-4 h-4 animate-spin mr-2" />
                  Refreshing...
                </>
              ) : (
                <>
                  <RefreshCw className="w-4 h-4 mr-2" />
                  Refresh Token
                </>
              )}
            </Button>
            <Button
              onClick={handleDisconnect}
              disabled={isLoading}
              variant="secondary"
              size="sm"
              className="w-full text-sm text-red-300 hover:bg-red-500/20"
            >
              <LogOut className="w-4 h-4 mr-2" />
              Disconnect
            </Button>
          </div>
        ) : (
          <Button
            onClick={handleConnect}
            disabled={isLoading || isAuthenticating}
            variant="primary"
            size="sm"
            className="w-full bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white text-sm font-medium shadow-lg hover:shadow-red-500/25"
          >
            {isAuthenticating ? (
              <>
                <Loader className="w-4 h-4 animate-spin mr-2" />
                Connecting...
              </>
            ) : (
              <>
                <Youtube className="w-4 h-4 mr-2" />
                Connect YouTube
              </>
            )}
          </Button>
        )}
      </div>
    );
  }

  // Full variant for settings/dedicated pages
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
          <Youtube className="w-6 h-6 text-red-600" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-gray-900">YouTube Account Connection</h3>
          <p className="text-sm text-gray-600">Connect your YouTube account to access detailed analytics and channel data</p>
        </div>
      </div>

      {showSuccess && (
        <div className="flex items-center gap-2 text-sm text-green-700 bg-green-50 px-3 py-2 rounded-lg mb-4">
          <CheckCircle className="w-4 h-4" />
          Operation completed successfully!
        </div>
      )}

      {error && (
        <div className="flex items-center gap-2 text-sm text-red-700 bg-red-50 px-3 py-2 rounded-lg mb-4">
          <AlertCircle className="w-4 h-4" />
          {error}
        </div>
      )}

      <div className="space-y-4">
        {isAuthenticated ? (
          <div className="space-y-4">
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <CheckCircle className="w-5 h-5 text-green-600" />
                <span className="font-medium text-green-800">Connected to YouTube</span>
              </div>
              
              {status && (
                <div className="space-y-1 text-sm">
                  {status.needs_refresh ? (
                    <p className="text-orange-700 font-medium">⚠ Token expired - refresh needed</p>
                  ) : (
                    <p 
                      className="text-gray-900 font-bold text-lg bg-gray-100 px-3 py-2 rounded-lg border"
                      style={{ 
                        fontSize: '18px', 
                        color: '#111827', 
                        backgroundColor: '#f3f4f6',
                        border: '2px solid #e5e7eb',
                        fontWeight: 'bold'
                      }}
                    >
                      ⏰ Access expires in {Math.floor((status.expires_in_seconds || 0) / 3600)} hours
                    </p>
                  )}
                  <p className="text-gray-600">Permissions: {status.scopes?.join(', ') || 'YouTube Analytics, Read-only'}</p>
                </div>
              )}
            </div>

            <div className="flex gap-3">
              <Button
                onClick={handleRefresh}
                disabled={isLoading}
                variant="secondary"
                className="flex-1"
              >
                {isLoading ? (
                  <>
                    <Loader className="w-4 h-4 animate-spin mr-2" />
                    Refreshing...
                  </>
                ) : (
                  <>
                    <RefreshCw className="w-4 h-4 mr-2" />
                    Refresh Token
                  </>
                )}
              </Button>
              
              <Button
                onClick={handleDisconnect}
                disabled={isLoading}
                variant="secondary"
                className="flex-1 text-red-600 hover:bg-red-50"
              >
                <LogOut className="w-4 h-4 mr-2" />
                Disconnect
              </Button>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <Button
              onClick={handleConnect}
              disabled={isLoading || isAuthenticating}
              variant="primary"
              size="lg"
              className="w-full bg-red-600 hover:bg-red-700"
            >
              {isAuthenticating ? (
                <>
                  <Loader className="w-5 h-5 animate-spin mr-2" />
                  Connecting to YouTube...
                </>
              ) : (
                <>
                  <Youtube className="w-5 h-5 mr-2" />
                  Connect YouTube Account
                </>
              )}
            </Button>

            {showBenefits && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h4 className="font-medium text-blue-900 mb-2">Benefits of connecting your YouTube account:</h4>
                <ul className="text-sm text-blue-800 space-y-1">
                  <li>• Access to detailed YouTube Analytics data</li>
                  <li>• Real-time subscriber and view counts</li>
                  <li>• Revenue and monetization insights</li>
                  <li>• Audience demographics and engagement metrics</li>
                  <li>• Video performance analytics</li>
                </ul>
                
                <div className="mt-3 p-2 bg-blue-100 rounded text-xs text-blue-700">
                  🔒 We only request read-only access to your YouTube data. We cannot make changes to your channel or upload videos.
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}