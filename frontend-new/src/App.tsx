import { Routes, Route, Navigate } from 'react-router-dom'
import { useEffect } from 'react'
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

function App() {
  const { isOnboarded, checkOnboardingStatus } = useUserStore()

  useEffect(() => {
    // checkOnboardingStatus now handles fetching real channel data internally
    checkOnboardingStatus()
  }, [checkOnboardingStatus])

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