export default defineNuxtRouteMiddleware((to, from) => {
  const { user, subscription } = useAuthStore()
  
  // Check if user is authenticated
  if (!user) {
    throw createError({
      statusCode: 401,
      statusMessage: 'Authentication required'
    })
  }

  // Check if user has premium access
  const hasPremiumAccess = checkPremiumAccess(subscription, 'research-workspace')
  
  if (!hasPremiumAccess) {
    // Redirect to upgrade page with context
    return navigateTo('/upgrade', {
      query: {
        feature: 'research-workspace',
        returnTo: to.fullPath
      }
    })
  }
})

function checkPremiumAccess(subscription: any, feature: string): boolean {
  if (!subscription) return false
  
  const premiumFeatures = {
    'research-workspace': ['growth', 'pro'],
    'specialized-agents': ['growth', 'pro'],
    'advanced-analytics': ['pro'],
    'competitor-tracking': ['growth', 'pro'],
    'trend-analysis': ['growth', 'pro']
  }
  
  const requiredPlans = premiumFeatures[feature] || []
  return requiredPlans.includes(subscription.plan)
}
