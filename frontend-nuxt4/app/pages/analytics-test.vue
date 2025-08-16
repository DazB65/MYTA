<template>
  <div class="min-h-screen bg-gray-900 text-white p-8">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold mb-8">MYTA Analytics Connection Test</h1>
      
      <!-- Connection Status -->
      <div class="bg-gray-800 rounded-xl p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">Connection Status</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="bg-gray-700 rounded-lg p-4">
            <div class="text-sm text-gray-400">Backend Connection</div>
            <div :class="backendStatus.connected ? 'text-green-400' : 'text-red-400'" class="font-semibold">
              {{ backendStatus.connected ? 'Connected' : 'Disconnected' }}
            </div>
            <div class="text-xs text-gray-500">{{ backendStatus.message }}</div>
          </div>
          
          <div class="bg-gray-700 rounded-lg p-4">
            <div class="text-sm text-gray-400">YouTube OAuth</div>
            <div :class="oauthStatus.authenticated ? 'text-green-400' : 'text-yellow-400'" class="font-semibold">
              {{ oauthStatus.authenticated ? 'Authenticated' : 'Not Connected' }}
            </div>
            <div class="text-xs text-gray-500">{{ oauthStatus.message }}</div>
          </div>
          
          <div class="bg-gray-700 rounded-lg p-4">
            <div class="text-sm text-gray-400">Analytics Available</div>
            <div :class="analyticsStatus.available ? 'text-green-400' : 'text-gray-400'" class="font-semibold">
              {{ analyticsStatus.available ? 'Available' : 'Unavailable' }}
            </div>
            <div class="text-xs text-gray-500">{{ analyticsStatus.message }}</div>
          </div>
        </div>
      </div>

      <!-- Test Actions -->
      <div class="bg-gray-800 rounded-xl p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">Test Actions</h2>
        <div class="flex flex-wrap gap-4">
          <button 
            @click="testBackendConnection" 
            :disabled="testing"
            class="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 px-4 py-2 rounded-lg transition-colors"
          >
            {{ testing ? 'Testing...' : 'Test Backend' }}
          </button>
          
          <button 
            @click="testOAuthStatus" 
            :disabled="testing"
            class="bg-purple-600 hover:bg-purple-700 disabled:opacity-50 px-4 py-2 rounded-lg transition-colors"
          >
            Check OAuth Status
          </button>
          
          <button 
            @click="testAnalyticsData" 
            :disabled="testing"
            class="bg-green-600 hover:bg-green-700 disabled:opacity-50 px-4 py-2 rounded-lg transition-colors"
          >
            Test Analytics
          </button>
          
          <button 
            @click="connectYouTube" 
            :disabled="testing"
            class="bg-red-600 hover:bg-red-700 disabled:opacity-50 px-4 py-2 rounded-lg transition-colors"
          >
            Connect YouTube
          </button>
        </div>
      </div>

      <!-- Test Results -->
      <div class="bg-gray-800 rounded-xl p-6">
        <h2 class="text-xl font-semibold mb-4">Test Results</h2>
        <div class="bg-gray-900 rounded-lg p-4 max-h-96 overflow-y-auto">
          <pre class="text-sm text-gray-300 whitespace-pre-wrap">{{ testResults }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useAnalytics } from '../../composables/useAnalytics'

// Page setup
useHead({
  title: 'Analytics Test - MYTA'
})

// State
const testing = ref(false)
const testResults = ref('Ready to test...\n')

const backendStatus = ref({
  connected: false,
  message: 'Not tested'
})

const oauthStatus = ref({
  authenticated: false,
  message: 'Not checked'
})

const analyticsStatus = ref({
  available: false,
  message: 'Not tested'
})

// Analytics composable
const { 
  connectYouTube: connectYT, 
  checkOAuthStatus, 
  fetchStatus,
  fetchOverview 
} = useAnalytics()

// Helper to add test results
const addResult = (message) => {
  const timestamp = new Date().toLocaleTimeString()
  testResults.value += `[${timestamp}] ${message}\n`
}

// Test backend connection
const testBackendConnection = async () => {
  testing.value = true
  addResult('Testing backend connection...')
  
  try {
    const response = await fetch('http://localhost:8000/health')
    if (response.ok) {
      const data = await response.json()
      backendStatus.value = {
        connected: true,
        message: 'Backend is running'
      }
      addResult('✅ Backend connection successful')
      addResult(`Backend response: ${JSON.stringify(data, null, 2)}`)
    } else {
      throw new Error(`HTTP ${response.status}`)
    }
  } catch (error) {
    backendStatus.value = {
      connected: false,
      message: error.message
    }
    addResult(`❌ Backend connection failed: ${error.message}`)
    addResult('💡 Falling back to mock data for frontend development')
  } finally {
    testing.value = false
  }
}

// Test OAuth status
const testOAuthStatus = async () => {
  testing.value = true
  addResult('Checking OAuth status...')
  
  try {
    const result = await checkOAuthStatus('default_user')
    oauthStatus.value = {
      authenticated: result.authenticated || false,
      message: result.message || 'Status checked'
    }
    addResult('✅ OAuth status check completed')
    addResult(`OAuth result: ${JSON.stringify(result, null, 2)}`)
  } catch (error) {
    oauthStatus.value = {
      authenticated: false,
      message: error.message
    }
    addResult(`❌ OAuth status check failed: ${error.message}`)
  } finally {
    testing.value = false
  }
}

// Test analytics data
const testAnalyticsData = async () => {
  testing.value = true
  addResult('Testing analytics data fetch...')
  
  try {
    const statusResult = await fetchStatus('default_user')
    analyticsStatus.value = {
      available: statusResult.analytics_available || false,
      message: statusResult.analytics_available ? 'Analytics ready' : 'YouTube not connected'
    }
    addResult('✅ Analytics status check completed')
    addResult(`Analytics status: ${JSON.stringify(statusResult, null, 2)}`)
    
    if (statusResult.analytics_available) {
      addResult('Fetching analytics overview...')
      const overviewResult = await fetchOverview('default_user', 30)
      addResult('✅ Analytics overview fetched')
      addResult(`Overview data: ${JSON.stringify(overviewResult, null, 2)}`)
    }
  } catch (error) {
    analyticsStatus.value = {
      available: false,
      message: error.message
    }
    addResult(`❌ Analytics test failed: ${error.message}`)
  } finally {
    testing.value = false
  }
}

// Connect YouTube
const connectYouTube = async () => {
  testing.value = true
  addResult('Initiating YouTube connection...')
  
  try {
    await connectYT('default_user')
    addResult('✅ YouTube connection initiated - redirecting to OAuth...')
  } catch (error) {
    addResult(`❌ YouTube connection failed: ${error.message}`)
    testing.value = false
  }
}

// Auto-test on mount
onMounted(() => {
  addResult('Page loaded - ready for testing')
  // Auto-test backend connection
  testBackendConnection()
})
</script>
