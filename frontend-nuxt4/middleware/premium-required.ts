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
    'research-workspace': ['solo_pro', 'teams'],
    'specialized-agents': ['solo_pro', 'teams'],
    'advanced-analytics': ['solo_pro', 'teams'],
    'competitor-tracking': ['solo_pro', 'teams'],
    'trend-analysis': ['solo_pro', 'teams'],
    'team-collaboration': ['teams'],
    'unlimited-content': ['solo_pro', 'teams'],
    'unlimited-goals': ['solo_pro', 'teams']
  }

  const requiredPlans = premiumFeatures[feature] || []
  return requiredPlans.includes(subscription.plan)
}
