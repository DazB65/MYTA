/**
 * OAuth Status Component
 * Displays current YouTube authentication status
 */

import { useOAuthStore } from '../../store/oauthStore';
import { CheckCircle, AlertCircle, Loader } from 'lucide-react';
import { useEffect, useState } from 'react';
import oauthService from '../../services/oauth';

interface OAuthStatusProps {
  showDetails?: boolean;
  className?: string;
  onClick?: () => void;
}

export default function OAuthStatus({ showDetails = false, className = '', onClick }: OAuthStatusProps) {
  const {
    isAuthenticated,
    status,
    isLoading,
    error,
    checkStatus
  } = useOAuthStore();
  
  const [directStatus, setDirectStatus] = useState<any>(null);

  // Check status on component mount and periodically
  useEffect(() => {
    checkStatus();
    
    // Get direct status as fallback
    const getDirectStatus = async () => {
      try {
        const directResult = await oauthService.checkOAuthStatus('default_user');
        setDirectStatus(directResult);
      } catch (err) {
        console.error('Direct OAuth call failed:', err);
      }
    };
    
    getDirectStatus();
    
    // Check every 30 seconds
    const interval = setInterval(() => {
      checkStatus();
      getDirectStatus();
    }, 30000);
    
    return () => clearInterval(interval);
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

  if (isAuthenticated && (status || directStatus)) {
    // TEMPORARY: Always use direct status since store is not working properly
    const effectiveStatus = directStatus || status;
    const expiresIn = effectiveStatus?.expires_in_seconds;
    const needsRefresh = effectiveStatus?.needs_refresh || status?.needs_refresh;
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
              <div 
                className="text-sm font-bold text-white bg-black/60 px-2 py-1 rounded border"
                style={{ 
                  fontSize: '13px', 
                  color: '#ffffff', 
                  backgroundColor: 'rgba(0, 0, 0, 0.7)',
                  border: '1px solid rgba(255, 255, 255, 0.4)',
                  fontWeight: 'bold'
                }}
              >
                ⏰ Expires in {hoursRemaining}h 
                <div style={{fontSize: '10px', color: '#ccc'}}>
                  DEBUG: expires={expiresIn}, direct={directStatus?.expires_in_seconds}, store={status?.expires_in_seconds}
                </div>
              </div>
            )}
            
            {(status?.scopes || effectiveStatus?.scopes) && (
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
    <div className={`flex items-center gap-2 ${className}`} onClick={onClick}>
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