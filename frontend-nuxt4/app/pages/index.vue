<template>
  <div style="min-height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; font-family: Arial, sans-serif;">
    <div style="max-width: 800px; margin: 0 auto; background: white; border-radius: 10px; padding: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
      
      <!-- Header -->
      <header style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #333; font-size: 2.5rem; margin-bottom: 0.5rem;">🚀 Welcome to Nuxt 4!</h1>
        <p style="color: #666; font-size: 1.1rem;">Your migration from Next.js is working perfectly</p>
      </header>

      <!-- Status Cards -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
        
        <div style="background: #10b981; color: white; padding: 1.5rem; border-radius: 8px; text-align: center;">
          <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">✅ Nuxt 4</h3>
          <p style="margin: 0; opacity: 0.9;">Running Successfully</p>
        </div>

        <div style="background: #3b82f6; color: white; padding: 1.5rem; border-radius: 8px; text-align: center;">
          <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">🔄 Migration</h3>
          <p style="margin: 0; opacity: 0.9;">Ready to Begin</p>
        </div>

        <div style="background: #f59e0b; color: white; padding: 1.5rem; border-radius: 8px; text-align: center;">
          <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">⚡ Performance</h3>
          <p style="margin: 0; opacity: 0.9;">Optimized & Fast</p>
        </div>

      </div>

      <!-- Next Steps -->
      <div style="background: #f8fafc; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #667eea;">
        <h2 style="color: #333; margin: 0 0 1rem 0;">🎯 Next Steps</h2>
        <ul style="color: #555; line-height: 1.6; margin: 0; padding-left: 1.5rem;">
          <li>Add Tailwind CSS for better styling</li>
          <li>Create navigation between pages</li>
          <li>Migrate your first React component to Vue</li>
          <li>Set up your dashboard page</li>
        </ul>
      </div>

    </div>
  </div>
</template>