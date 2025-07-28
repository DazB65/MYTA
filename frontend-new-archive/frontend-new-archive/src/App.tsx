import { Routes, Route, Navigate } from 'react-router-dom'
import { useEffect, useCallback } from 'react'
import Layout from './components/layout/Layout'
import Onboarding from './pages/Onboarding'
import Dashboard from './pages/Dashboard'
import Channel from './pages/Channel'
import Pillars from './pages/Pillars'
import Videos from './pages/Videos'
import Settings from './pages/Settings'
import EnhancedAnalytics from './pages/EnhancedAnalytics'
import ContentStudio from './pages/ContentStudio'
import { SystemHealthCheck } from './components/SystemHealthCheck'
import { useUserStore } from './store/userStore'
import { useOAuthStore } from './store/oauthStore'
import { logger } from './utils/logger'
import { errorHandler } from './utils/errorHandler'

function App() {
  const { isOnboarded, checkOnboardingStatus } = useUserStore()
  const { handleCallback } = useOAuthStore()

  const initializeApp = useCallback(async () => {
    try {
      // Handle OAuth callback first (before any routing)
      logger.debug('Initializing app and checking OAuth callback parameters', {}, 'App');
      
      const result = handleCallback();
      if (result.success) {
        logger.oauth('OAuth callback processed successfully');
      } else if (result.error) {
        errorHandler.handleOAuthError(result.error, { action: 'callback' });
      }

      // Check onboarding status and load user data
      await checkOnboardingStatus();
      
      logger.info('App initialization completed', {}, 'App');
    } catch (error) {
      errorHandler.handle(error as Error, { component: 'App', action: 'initialization' });
    }
  }, [checkOnboardingStatus, handleCallback]);

  useEffect(() => {
    initializeApp();
  }, [initializeApp])

  // Show onboarding if user hasn't completed it
  if (!isOnboarded) {
    return <Onboarding />
  }

  return (
    <>
      <Routes>
        <Route path="/health" element={<SystemHealthCheck />} />
        <Route path="/*" element={
          <Layout>
            <Routes>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/channel" element={<Channel />} />
              <Route path="/pillars" element={<Pillars />} />
              <Route path="/videos" element={<Videos />} />
              <Route path="/content-studio" element={<ContentStudio />} />
              <Route path="/analytics" element={<EnhancedAnalytics />} />
              <Route path="/settings" element={<Settings />} />
              <Route path="*" element={<Navigate to="/dashboard" replace />} />
            </Routes>
          </Layout>
        } />
      </Routes>
    </>
  )
}

export default App