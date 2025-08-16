<template>
  <div class="min-h-screen bg-background text-text-primary p-6 pt-32">
    <div class="max-w-6xl mx-auto space-y-12">
      <!-- Header -->
      <div class="text-center">
        <h1 class="text-4xl font-bold mb-4 bg-gradient-brand bg-clip-text text-transparent">
          Vidalytics Design System
        </h1>
        <p class="text-text-secondary text-lg">
          A comprehensive design system for consistent, beautiful interfaces
        </p>
      </div>

      <!-- Colors Section -->
      <section class="space-y-6">
        <h2 class="text-2xl font-bold">Color Palette</h2>
        
        <!-- Agent Colors -->
        <div class="card">
          <h3 class="text-lg font-semibold mb-4">Agent Colors</h3>
          <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div class="text-center">
              <div class="w-full h-16 bg-agent-1 rounded-lg mb-2"></div>
              <p class="text-sm font-medium">Agent 1</p>
              <p class="text-xs text-text-muted">Purple #9333ea</p>
            </div>
            <div class="text-center">
              <div class="w-full h-16 bg-agent-2 rounded-lg mb-2"></div>
              <p class="text-sm font-medium">Agent 2</p>
              <p class="text-xs text-text-muted">Blue #2563eb</p>
            </div>
            <div class="text-center">
              <div class="w-full h-16 bg-agent-3 rounded-lg mb-2"></div>
              <p class="text-sm font-medium">Agent 3</p>
              <p class="text-xs text-text-muted">Green #059669</p>
            </div>
            <div class="text-center">
              <div class="w-full h-16 bg-agent-4 rounded-lg mb-2"></div>
              <p class="text-sm font-medium">Agent 4</p>
              <p class="text-xs text-text-muted">Orange #ea580c</p>
            </div>
            <div class="text-center">
              <div class="w-full h-16 bg-agent-5 rounded-lg mb-2"></div>
              <p class="text-sm font-medium">Agent 5</p>
              <p class="text-xs text-text-muted">Pink #db2777</p>
            </div>
            <div class="text-center">
              <div class="w-full h-16 bg-agent-boss rounded-lg mb-2"></div>
              <p class="text-sm font-medium">Boss Agent</p>
              <p class="text-xs text-text-muted">Brown #7c2d12</p>
            </div>
          </div>
        </div>

        <!-- Agent Gradients -->
        <div class="card">
          <h3 class="text-lg font-semibold mb-4">Agent Gradients</h3>
          <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div class="text-center">
              <div class="w-full h-16 bg-gradient-agent-1 rounded-lg mb-2"></div>
              <p class="text-sm font-medium">Agent 1</p>
              <p class="text-xs text-text-muted">Purple Gradient</p>
            </div>
            <div class="text-center">
              <div class="w-full h-16 bg-gradient-agent-2 rounded-lg mb-2"></div>
              <p class="text-sm font-medium">Agent 2</p>
              <p class="text-xs text-text-muted">Blue Gradient</p>
            </div>
            <div class="text-center">
              <div class="w-full h-16 bg-gradient-agent-3 rounded-lg mb-2"></div>
              <p class="text-sm font-medium">Agent 3</p>
              <p class="text-xs text-text-muted">Green Gradient</p>
            </div>
            <div class="text-center">
              <div class="w-full h-16 bg-gradient-agent-4 rounded-lg mb-2"></div>
              <p class="text-sm font-medium">Agent 4</p>
              <p class="text-xs text-text-muted">Orange Gradient</p>
            </div>
            <div class="text-center">
              <div class="w-full h-16 bg-gradient-agent-5 rounded-lg mb-2"></div>
              <p class="text-sm font-medium">Agent 5</p>
              <p class="text-xs text-text-muted">Pink Gradient</p>
            </div>
            <div class="text-center">
              <div class="w-full h-16 bg-gradient-multi-agent rounded-lg mb-2"></div>
              <p class="text-sm font-medium">Multi-Agent</p>
              <p class="text-xs text-text-muted">All Agents</p>
            </div>
          </div>
        </div>

        <!-- Status Colors -->
        <div class="card">
          <h3 class="text-lg font-semibold mb-4">Status Colors</h3>
          <div class="grid grid-cols-3 gap-4">
            <div class="text-center">
              <div class="w-full h-16 bg-success rounded-lg mb-2"></div>
              <p class="text-sm font-medium">Success</p>
              <p class="text-xs text-text-muted">#10b981</p>
            </div>
            <div class="text-center">
              <div class="w-full h-16 bg-warning rounded-lg mb-2"></div>
              <p class="text-sm font-medium">Warning</p>
              <p class="text-xs text-text-muted">#f59e0b</p>
            </div>
            <div class="text-center">
              <div class="w-full h-16 bg-error rounded-lg mb-2"></div>
              <p class="text-sm font-medium">Error</p>
              <p class="text-xs text-text-muted">#ef4444</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Typography Section -->
      <section class="space-y-6">
        <h2 class="text-2xl font-bold">Typography</h2>
        
        <div class="card">
          <div class="space-y-4">
            <div>
              <h1 class="text-4xl font-bold">Heading 1</h1>
              <p class="text-text-muted text-sm">text-4xl font-bold</p>
            </div>
            <div>
              <h2 class="text-3xl font-bold">Heading 2</h2>
              <p class="text-text-muted text-sm">text-3xl font-bold</p>
            </div>
            <div>
              <h3 class="text-2xl font-semibold">Heading 3</h3>
              <p class="text-text-muted text-sm">text-2xl font-semibold</p>
            </div>
            <div>
              <p class="text-lg">Large paragraph text</p>
              <p class="text-text-muted text-sm">text-lg</p>
            </div>
            <div>
              <p class="text-base">Regular paragraph text</p>
              <p class="text-text-muted text-sm">text-base</p>
            </div>
            <div>
              <p class="text-sm text-text-secondary">Secondary text</p>
              <p class="text-text-muted text-sm">text-sm text-text-secondary</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Buttons Section -->
      <section class="space-y-6">
        <h2 class="text-2xl font-bold">Buttons</h2>
        
        <div class="card">
          <div class="space-y-6">
            <!-- Button Variants -->
            <div>
              <h3 class="text-lg font-semibold mb-4">Variants</h3>
              <div class="flex flex-wrap gap-4">
                <VButton variant="primary">Primary</VButton>
                <VButton variant="secondary">Secondary</VButton>
                <VButton variant="ghost">Ghost</VButton>
                <VButton variant="primary" disabled>Disabled</VButton>
              </div>
            </div>

            <!-- Button Sizes -->
            <div>
              <h3 class="text-lg font-semibold mb-4">Sizes</h3>
              <div class="flex flex-wrap items-center gap-4">
                <VButton variant="primary" size="sm">Small</VButton>
                <VButton variant="primary" size="md">Medium</VButton>
                <VButton variant="primary" size="lg">Large</VButton>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Cards Section -->
      <section class="space-y-6">
        <h2 class="text-2xl font-bold">Cards</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <VCard>
            <template #header>
              <h3 class="font-semibold">Default Card</h3>
            </template>
            <p class="text-text-secondary">This is a default card with header and content.</p>
            <template #footer>
              <VButton variant="primary" size="sm">Action</VButton>
            </template>
          </VCard>

          <VCard variant="glass">
            <template #header>
              <h3 class="font-semibold">Glass Card</h3>
            </template>
            <p class="text-text-secondary">This card uses glass morphism effect.</p>
          </VCard>

          <VCard variant="elevated" hoverable>
            <template #header>
              <h3 class="font-semibold">Elevated Card</h3>
            </template>
            <p class="text-text-secondary">This card is elevated and hoverable.</p>
          </VCard>
        </div>
      </section>

      <!-- Badges Section -->
      <section class="space-y-6">
        <h2 class="text-2xl font-bold">Badges</h2>
        
        <div class="card">
          <div class="space-y-4">
            <div>
              <h3 class="text-lg font-semibold mb-4">Variants</h3>
              <div class="flex flex-wrap gap-2">
                <VBadge variant="primary">Primary</VBadge>
                <VBadge variant="secondary">Secondary</VBadge>
                <VBadge variant="success">Success</VBadge>
                <VBadge variant="warning">Warning</VBadge>
                <VBadge variant="error">Error</VBadge>
              </div>
            </div>

            <div>
              <h3 class="text-lg font-semibold mb-4">Sizes</h3>
              <div class="flex flex-wrap items-center gap-2">
                <VBadge variant="primary" size="sm">Small</VBadge>
                <VBadge variant="primary" size="md">Medium</VBadge>
                <VBadge variant="primary" size="lg">Large</VBadge>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Inputs Section -->
      <section class="space-y-6">
        <h2 class="text-2xl font-bold">Form Inputs</h2>
        
        <div class="card">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <VInput 
              label="Default Input" 
              placeholder="Enter text..." 
              hint="This is a hint message"
            />
            <VInput 
              label="Required Input" 
              placeholder="Required field..." 
              required
            />
            <VInput 
              label="Error State" 
              placeholder="Invalid input..." 
              error="This field has an error"
            />
            <VInput 
              label="Disabled Input" 
              placeholder="Disabled..." 
              disabled
            />
          </div>
        </div>
      </section>

      <!-- Agent Cards Example -->
      <section class="space-y-6">
        <h2 class="text-2xl font-bold">Agent Cards Example</h2>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <!-- Agent 1 Card -->
          <div class="card bg-gradient-agent-1 text-white">
            <div class="flex items-center space-x-3 mb-4">
              <div class="w-12 h-12 bg-white bg-opacity-20 rounded-lg flex items-center justify-center">
                <span class="text-lg">🤖</span>
              </div>
              <div>
                <h3 class="font-semibold">Agent 1</h3>
                <p class="text-sm opacity-80">Content Creator</p>
              </div>
            </div>
            <p class="text-sm opacity-90">AI-powered content creation and optimization specialist.</p>
          </div>

          <!-- Agent 2 Card -->
          <div class="card bg-gradient-agent-2 text-white">
            <div class="flex items-center space-x-3 mb-4">
              <div class="w-12 h-12 bg-white bg-opacity-20 rounded-lg flex items-center justify-center">
                <span class="text-lg">📊</span>
              </div>
              <div>
                <h3 class="font-semibold">Agent 2</h3>
                <p class="text-sm opacity-80">Analytics Expert</p>
              </div>
            </div>
            <p class="text-sm opacity-90">Data analysis and performance insights specialist.</p>
          </div>

          <!-- Agent 3 Card -->
          <div class="card bg-gradient-agent-3 text-white">
            <div class="flex items-center space-x-3 mb-4">
              <div class="w-12 h-12 bg-white bg-opacity-20 rounded-lg flex items-center justify-center">
                <span class="text-lg">🎯</span>
              </div>
              <div>
                <h3 class="font-semibold">Agent 3</h3>
                <p class="text-sm opacity-80">Strategy Advisor</p>
              </div>
            </div>
            <p class="text-sm opacity-90">Strategic planning and growth optimization expert.</p>
          </div>
        </div>
      </section>

      <!-- Spacing Section -->
      <section class="space-y-6">
        <h2 class="text-2xl font-bold">Spacing Scale</h2>

        <div class="card">
          <div class="space-y-4">
            <div class="flex items-center gap-4">
              <div class="w-1 h-4 bg-agent-1"></div>
              <span class="text-sm font-mono">space-1 (4px)</span>
            </div>
            <div class="flex items-center gap-4">
              <div class="w-2 h-4 bg-agent-2"></div>
              <span class="text-sm font-mono">space-2 (8px)</span>
            </div>
            <div class="flex items-center gap-4">
              <div class="w-4 h-4 bg-agent-3"></div>
              <span class="text-sm font-mono">space-4 (16px)</span>
            </div>
            <div class="flex items-center gap-4">
              <div class="w-6 h-4 bg-agent-4"></div>
              <span class="text-sm font-mono">space-6 (24px)</span>
            </div>
            <div class="flex items-center gap-4">
              <div class="w-8 h-4 bg-agent-5"></div>
              <span class="text-sm font-mono">space-8 (32px)</span>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
// Set page title
useHead({
  title: 'Design System - Vidalytics'
})
</script>
