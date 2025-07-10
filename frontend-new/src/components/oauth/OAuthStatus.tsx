/**
 * OAuth Status Component
 * Displays current YouTube authentication status
 */

import { useOAuthStore } from '../../store/oauthStore';
import { CheckCircle, AlertCircle, Loader } from 'lucide-react';
import { useEffect } from 'react';

interface OAuthStatusProps {
  showDetails?: boolean;
  className?: string;
}

export default function OAuthStatus({ showDetails = false, className = '' }: OAuthStatusProps) {
  const {
    isAuthenticated,
    status,
    isLoading,
    error,
    checkStatus
  } = useOAuthStore();

  // Check status on component mount
  useEffect(() => {
    checkStatus();
  }, [checkStatus]);

  if (isLoading) {
    return (
      <div className={`flex items-center gap-2 ${className}`}>
        <Loader className="w-4 h-4 animate-spin text-blue-500" />
        <span className="text-sm text-gray-600">Checking connection...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`flex items-center gap-2 ${className}`}>
        <AlertCircle className="w-4 h-4 text-red-500" />
        <span className="text-sm text-red-600">Connection Error</span>
      </div>
    );
  }

  if (isAuthenticated && status) {
    const expiresIn = status.expires_in_seconds;
    const needsRefresh = status.needs_refresh;
    const hoursRemaining = expiresIn ? Math.floor(expiresIn / 3600) : 0;

    return (
      <div className={`${className}`}>
        <div className="flex items-center gap-2">
          <CheckCircle className="w-4 h-4 text-green-500" />
          <span className="text-sm text-green-600 font-medium">YouTube Connected</span>
        </div>
        
        {showDetails && (
          <div className="mt-2 space-y-1">
            {needsRefresh ? (
              <div className="text-xs text-yellow-600 bg-yellow-50 px-2 py-1 rounded">
                ⚠ Token expired - refresh needed
              </div>
            ) : (
              <div className="text-xs text-gray-600">
                Expires in {hoursRemaining}h
              </div>
            )}
            
            {status.scopes && (
              <div className="text-xs text-gray-500">
                Permissions: YouTube Analytics, Read-only
              </div>
            )}
          </div>
        )}
      </div>
    );
  }

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <AlertCircle className="w-4 h-4 text-red-500" />
      <span className="text-sm text-red-600">YouTube Not Connected</span>
      {showDetails && (
        <div className="text-xs text-gray-500 mt-1">
          Connect to access detailed analytics
        </div>
      )}
    </div>
  );
}