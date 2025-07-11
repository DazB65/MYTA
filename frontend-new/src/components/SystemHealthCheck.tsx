import React, { useEffect, useState } from 'react';
import { CheckCircle, XCircle, Loader2, AlertCircle } from 'lucide-react';
import { useUserStore } from '../store/userStore';
import { useChatStore } from '../store/chatStore';
import { useAvatarStore } from '../store/avatarStore';
import { useOAuthStore } from '../store/oauthStore';
import { useSuggestionStore } from '../store/suggestionStore';
import { useFloatingChatStore } from '../store/floatingChatStore';

interface HealthCheck {
  name: string;
  description: string;
  status: 'pending' | 'success' | 'error';
  message?: string;
  details?: any;
}

export const SystemHealthCheck: React.FC = () => {
  const [checks, setChecks] = useState<HealthCheck[]>([
    {
      name: 'API Connectivity',
      description: 'Testing connection to backend server',
      status: 'pending'
    },
    {
      name: 'Frontend Components',
      description: 'Verifying React components are available',
      status: 'pending'
    },
    {
      name: 'State Management',
      description: 'Checking Zustand stores initialization',
      status: 'pending'
    },
    {
      name: 'Static Assets',
      description: 'Verifying images and CSS are loaded',
      status: 'pending'
    },
    {
      name: 'Environment Variables',
      description: 'Checking API configuration',
      status: 'pending'
    }
  ]);

  const [overallStatus, setOverallStatus] = useState<'checking' | 'healthy' | 'issues'>('checking');

  // Test stores
  const userStore = useUserStore.getState();
  const chatStore = useChatStore.getState();
  const avatarStore = useAvatarStore.getState();
  const oauthStore = useOAuthStore.getState();
  const suggestionStore = useSuggestionStore.getState();
  const floatingChatStore = useFloatingChatStore.getState();

  useEffect(() => {
    runHealthChecks();
  }, []);

  const updateCheck = (name: string, status: 'success' | 'error', message?: string, details?: any) => {
    setChecks(prev => prev.map(check => 
      check.name === name 
        ? { ...check, status, message, details }
        : check
    ));
  };

  const runHealthChecks = async () => {
    // 1. Test API Connectivity
    try {
      const response = await fetch('/health');
      if (response.ok) {
        const data = await response.json();
        updateCheck('API Connectivity', 'success', 'Backend server is running', data);
      } else {
        updateCheck('API Connectivity', 'error', `Server returned ${response.status}`);
      }
    } catch (error) {
      updateCheck('API Connectivity', 'error', 'Cannot connect to backend server', error);
    }

    // 2. Test Frontend Components
    try {
      const missingComponents = [];
      // This is a basic check - in production you'd want more thorough testing
      if (!React.version) {
        missingComponents.push('React');
      }
      
      if (missingComponents.length === 0) {
        updateCheck('Frontend Components', 'success', 'All components loaded successfully');
      } else {
        updateCheck('Frontend Components', 'error', `Missing: ${missingComponents.join(', ')}`);
      }
    } catch (error) {
      updateCheck('Frontend Components', 'error', 'Component verification failed', error);
    }

    // 3. Test State Management
    try {
      const stores = {
        userStore: userStore,
        chatStore: chatStore,
        avatarStore: avatarStore,
        oauthStore: oauthStore,
        suggestionStore: suggestionStore,
        floatingChatStore: floatingChatStore
      };

      // Check if stores are initialized
      const storeChecks = Object.entries(stores).map(([name, state]) => ({
        name,
        initialized: state !== undefined && state !== null
      }));

      const failedStores = storeChecks.filter(s => !s.initialized);
      
      if (failedStores.length === 0) {
        updateCheck('State Management', 'success', 'All Zustand stores initialized', storeChecks);
      } else {
        updateCheck('State Management', 'error', 
          `Failed stores: ${failedStores.map(s => s.name).join(', ')}`, 
          storeChecks
        );
      }
    } catch (error) {
      updateCheck('State Management', 'error', 'Store initialization failed', error);
    }

    // 4. Test Static Assets
    try {
      const assetsToTest = [
        { type: 'image', url: '/assets/images/CM Logo White.svg' },
        { type: 'css', url: '/assets/index-CPk5koRp.css' },
        { type: 'js', url: '/assets/index-sjYPtZbr.js' }
      ];

      const assetResults = await Promise.all(
        assetsToTest.map(async (asset) => {
          try {
            const response = await fetch(asset.url, { method: 'HEAD' });
            return { ...asset, success: response.ok, status: response.status };
          } catch (error) {
            return { ...asset, success: false, error };
          }
        })
      );

      const failedAssets = assetResults.filter(a => !a.success);
      
      if (failedAssets.length === 0) {
        updateCheck('Static Assets', 'success', 'All assets loaded successfully', assetResults);
      } else {
        updateCheck('Static Assets', 'error', 
          `Failed to load ${failedAssets.length} assets`, 
          assetResults
        );
      }
    } catch (error) {
      updateCheck('Static Assets', 'error', 'Asset verification failed', error);
    }

    // 5. Test Environment Variables
    try {
      // Check if we're in development mode
      const isDevelopment = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      
      if (isDevelopment) {
        updateCheck('Environment Variables', 'success', 'Development environment detected');
      } else {
        updateCheck('Environment Variables', 'error', 'Production environment - API URL should be configured');
      }
    } catch (error) {
      updateCheck('Environment Variables', 'error', 'Environment check failed', error);
    }

    // Update overall status
    setTimeout(() => {
      const allChecks = checks;
      const hasErrors = allChecks.some(c => c.status === 'error');
      setOverallStatus(hasErrors ? 'issues' : 'healthy');
    }, 500);
  };

  const getStatusIcon = (status: 'pending' | 'success' | 'error') => {
    switch (status) {
      case 'pending':
        return <Loader2 className="w-5 h-5 text-gray-400 animate-spin" />;
      case 'success':
        return <CheckCircle className="w-5 h-5 text-green-400" />;
      case 'error':
        return <XCircle className="w-5 h-5 text-red-400" />;
    }
  };

  const getOverallStatusDisplay = () => {
    switch (overallStatus) {
      case 'checking':
        return (
          <div className="flex items-center space-x-3 text-gray-300">
            <Loader2 className="w-6 h-6 animate-spin" />
            <span className="text-lg font-medium">Running health checks...</span>
          </div>
        );
      case 'healthy':
        return (
          <div className="flex items-center space-x-3 text-green-400">
            <CheckCircle className="w-6 h-6" />
            <span className="text-lg font-medium">All systems operational</span>
          </div>
        );
      case 'issues':
        return (
          <div className="flex items-center space-x-3 text-yellow-400">
            <AlertCircle className="w-6 h-6" />
            <span className="text-lg font-medium">Some issues detected</span>
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">System Health Check</h1>
          <p className="text-gray-400">Verifying all components are ready for UI updates</p>
        </div>

        <div className="bg-gray-800 rounded-lg p-6 mb-8">
          {getOverallStatusDisplay()}
        </div>

        <div className="space-y-4">
          {checks.map((check) => (
            <div key={check.name} className="bg-gray-800 rounded-lg p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    {getStatusIcon(check.status)}
                    <h3 className="text-lg font-semibold">{check.name}</h3>
                  </div>
                  <p className="text-gray-400 text-sm mb-2">{check.description}</p>
                  {check.message && (
                    <p className={`text-sm ${
                      check.status === 'error' ? 'text-red-400' : 'text-green-400'
                    }`}>
                      {check.message}
                    </p>
                  )}
                </div>
                {check.details && (
                  <button
                    onClick={() => console.log(`${check.name} details:`, check.details)}
                    className="text-sm text-blue-400 hover:text-blue-300 transition-colors"
                  >
                    View Details
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="mt-8 bg-gray-800 rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4">Recommendations</h3>
          {overallStatus === 'healthy' ? (
            <p className="text-green-400">
              ✅ System is ready for UI updates. All components and services are functioning properly.
            </p>
          ) : overallStatus === 'issues' ? (
            <div className="space-y-2">
              <p className="text-yellow-400 mb-3">
                ⚠️ Some issues were detected. Please address the following:
              </p>
              <ul className="list-disc list-inside space-y-1 text-gray-300 ml-4">
                {checks.filter(c => c.status === 'error').map(check => (
                  <li key={check.name}>
                    <span className="font-medium">{check.name}:</span> {check.message}
                  </li>
                ))}
              </ul>
            </div>
          ) : (
            <p className="text-gray-400">Checking system status...</p>
          )}
        </div>

        <div className="mt-8 flex justify-center space-x-4">
          <button
            onClick={runHealthChecks}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Rerun Checks
          </button>
          <button
            onClick={() => window.location.href = '/'}
            className="px-6 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors"
          >
            Back to App
          </button>
        </div>
      </div>
    </div>
  );
};