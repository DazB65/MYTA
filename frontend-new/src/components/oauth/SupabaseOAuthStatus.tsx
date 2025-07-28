/**
 * Supabase OAuth Status Component
 * Displays current YouTube authentication status using Supabase Auth
 */

import { useSupabaseOAuthStore } from '../../store/supabaseOAuthStore';
import { CheckCircle, AlertCircle, Loader } from 'lucide-react';
import { useEffect } from 'react';

interface SupabaseOAuthStatusProps {
  showDetails?: boolean;
  className?: string;
  onClick?: () => void;
}

export default function SupabaseOAuthStatus({ 
  showDetails = false, 
  className = '', 
  onClick 
}: SupabaseOAuthStatusProps) {
  const {
    isAuthenticated,
    status,
    isLoading,
    error,
    checkStatus
  } = useSupabaseOAuthStore();

  // Check status on component mount and periodically
  useEffect(() => {
    checkStatus();
    
    // Refresh status every 5 minutes
    const interval = setInterval(() => {
      checkStatus();
    }, 5 * 60 * 1000);
    
    return () => clearInterval(interval);
  }, [checkStatus]);

  const getStatusText = () => {
    if (isLoading) return 'Checking...';
    if (error) return 'Connection Error';
    if (!isAuthenticated) return 'Not Connected';
    
    if (status?.expires_in_seconds) {
      const hours = Math.floor(status.expires_in_seconds / 3600);
      if (hours < 1) {
        return 'Expires Soon';
      }
      return showDetails ? `Connected (${hours}h)` : 'Connected';
    }
    
    return 'Connected';
  };

  const getStatusIcon = () => {
    if (isLoading) return <Loader className="w-4 h-4 animate-spin" />;
    if (error) return <AlertCircle className="w-4 h-4 text-red-400" />;
    if (!isAuthenticated) return <AlertCircle className="w-4 h-4 text-gray-400" />;
    
    if (status?.expires_in_seconds && status.expires_in_seconds < 3600) {
      return <AlertCircle className="w-4 h-4 text-yellow-400" />;
    }
    
    return <CheckCircle className="w-4 h-4 text-green-400" />;
  };

  const getStatusColor = () => {
    if (isLoading) return 'text-gray-400';
    if (error) return 'text-red-400';
    if (!isAuthenticated) return 'text-gray-400';
    
    if (status?.expires_in_seconds && status.expires_in_seconds < 3600) {
      return 'text-yellow-400';
    }
    
    return 'text-green-400';
  };

  return (
    <div 
      className={`flex items-center gap-2 cursor-pointer hover:opacity-80 transition-opacity ${className}`}
      onClick={onClick}
      title={showDetails ? getStatusText() : undefined}
    >
      {getStatusIcon()}
      <span className={`text-sm font-medium ${getStatusColor()}`}>
        {getStatusText()}
      </span>
      
      {showDetails && status?.email && (
        <span className="text-xs text-gray-400 ml-2">
          ({status.email})
        </span>
      )}
    </div>
  );
}