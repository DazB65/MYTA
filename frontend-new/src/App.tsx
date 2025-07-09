import { Routes, Route, Navigate } from 'react-router-dom'
import { useEffect } from 'react'
import Layout from './components/layout/Layout'
import Onboarding from './pages/Onboarding'
import Channel from './pages/Channel'
import Pillars from './pages/Pillars'
import Videos from './pages/Videos'
import Tools from './pages/Tools'
import Settings from './pages/Settings'
import { useUserStore } from './store/userStore'

function App() {
  const { isOnboarded, checkOnboardingStatus } = useUserStore()

  useEffect(() => {
    checkOnboardingStatus()
  }, [checkOnboardingStatus])

  // Show onboarding if user hasn't completed it
  if (!isOnboarded) {
    return <Onboarding />
  }

  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/channel" replace />} />
        <Route path="/channel" element={<Channel />} />
        <Route path="/pillars" element={<Pillars />} />
        <Route path="/videos" element={<Videos />} />
        <Route path="/tools" element={<Tools />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="*" element={<Navigate to="/channel" replace />} />
      </Routes>
    </Layout>
  )
}

export default App