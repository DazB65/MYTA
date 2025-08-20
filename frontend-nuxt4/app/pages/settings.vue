<template>
  <div class="min-h-screen bg-forest-900 text-white">
    <!-- Settings Content -->
    <div class="p-6 pt-24">
      <!-- Page Header -->
      <div class="mb-4 flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <h1 class="text-2xl font-bold text-white">Settings</h1>
          <span class="text-gray-400">•</span>
          <p class="text-gray-400">Manage your account and application preferences</p>
        </div>
        <div class="flex items-center space-x-4">
          <!-- Future: Add settings actions here -->
        </div>
      </div>

      <!-- Settings Tabs -->
      <div class="mb-6 rounded-xl bg-forest-800 p-6">
        <div class="border-b border-forest-600">
          <nav class="flex space-x-8">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                'flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors',
                activeTab === tab.id
                  ? 'border-orange-500 text-orange-500'
                  : 'border-transparent text-gray-400 hover:text-gray-300 hover:border-gray-300'
              ]"
            >
              <span>{{ tab.icon }}</span>
              <span>{{ tab.name }}</span>
            </button>
          </nav>
        </div>
      </div>

      <!-- Tab Content -->
      <div>
        <!-- Agent Customization Tab -->
        <div v-if="activeTab === 'agent'" class="mb-6 rounded-xl bg-forest-800 p-6">
          <div class="mb-6 flex items-center space-x-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-orange-500">
              <svg class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path
                  d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"
                />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-white">AI Agent Customization</h3>
              <p class="text-sm text-gray-400">Personalize your AI assistant experience</p>
            </div>
          </div>

          <div class="grid grid-cols-1 gap-8 lg:grid-cols-2">
            <!-- Agent Name -->
            <div>
              <label class="mb-2 block text-sm font-medium text-white">Agent Name</label>
              <input
                v-model="agentName"
                type="text"
                placeholder="Enter your agent's name"
                class="w-full rounded-lg border border-forest-600 bg-forest-700 px-4 py-3 text-white placeholder-gray-400 focus:border-orange-500 focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
              <p class="mt-1 text-xs text-gray-400">
                This name will appear in the agent modal header
              </p>
            </div>

            <!-- Agent Selection -->
            <div>
              <label class="mb-2 block text-sm font-medium text-white">Choose Your Agent</label>
              <div class="grid grid-cols-5 gap-3">
                <div
                  v-for="agent in agents"
                  :key="agent.id"
                  class="relative cursor-pointer rounded-lg border-2 p-4 transition-all hover:shadow-md"
                  :class="selectedAgentId === agent.id ? '' : 'border-forest-600 hover:border-forest-500'"
                  :style="selectedAgentId === agent.id ? {
                    borderColor: agent.color,
                    backgroundColor: agent.color + '20'
                  } : {}"
                  @click="setSelectedAgent(agent.id)"
                >
                  <div class="text-center">
                    <div class="mx-auto mb-2 h-16 w-16 overflow-hidden rounded-full bg-forest-700">
                      <img
                        :src="agent.image"
                        :alt="agent.name"
                        class="h-full w-full object-cover"
                      />
                    </div>
                    <div class="text-xs font-medium text-white">{{ agent.name }}</div>
                    <div class="mt-1 text-xs text-gray-400">{{ agent.personality }}</div>
                  </div>

                  <!-- Selected indicator -->
                  <div
                    v-if="selectedAgentId === agent.id"
                    class="absolute -right-2 -top-2 flex h-6 w-6 items-center justify-center rounded-full"
                    :style="{ backgroundColor: agent.color }"
                  >
                    <svg class="h-4 w-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fill-rule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </div>
                </div>
              </div>
              <p class="mt-2 text-xs text-gray-400">
                Select from 5 different AI agent personalities
              </p>
            </div>
          </div>

          <!-- Preview Section -->
          <div class="mt-8 rounded-lg bg-forest-700 p-4">
            <h4 class="mb-3 text-sm font-medium text-white">Preview</h4>
            <div class="flex items-center space-x-3">
              <div class="h-12 w-12 overflow-hidden rounded-lg bg-forest-600">
                <img
                  :src="selectedAgent.image"
                  :alt="selectedAgent.name"
                  class="h-full w-full object-cover"
                />
              </div>
              <div>
                <div class="text-xl font-bold text-white">
                  {{ agentName || 'Professional Assistant' }}
                </div>
                <div class="text-sm font-medium text-orange-400">MYTA</div>
              </div>
            </div>
          </div>

          <!-- Save Button -->
          <div class="mt-6 flex justify-end">
            <button
              class="rounded-lg px-6 py-3 font-medium text-white transition-colors hover:opacity-90"
              :style="{ backgroundColor: selectedAgent.color }"
              @click="handleSaveSettings"
            >
              Save Changes
            </button>
          </div>
        </div>

        <!-- General Settings Tab -->
        <div v-if="activeTab === 'general'" class="rounded-xl bg-forest-800 p-6">
          <div class="mb-6 flex items-center space-x-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-forest-700">
              <svg class="h-6 w-6 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z"
                  clip-rule="evenodd"
                />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-white">General Settings</h3>
              <p class="text-sm text-gray-400">Additional settings coming soon</p>
            </div>
          </div>

          <div class="py-8 text-center">
            <p class="mb-4 text-gray-400">More settings will be available in future updates</p>
            <button
              class="rounded-lg bg-forest-700 px-4 py-2 text-gray-300 transition-colors hover:bg-forest-600"
            >
              Request Features
            </button>
          </div>
        </div>

        <!-- Subscription Tab -->
        <div v-if="activeTab === 'subscription'" class="space-y-6">
          <!-- Current Plan -->
          <div class="rounded-xl bg-forest-800 p-6">
            <div class="mb-6 flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-orange-500">
                  <svg class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4z"/>
                    <path fill-rule="evenodd" d="M18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM4 13a1 1 0 011-1h1a1 1 0 110 2H5a1 1 0 01-1-1zm5-1a1 1 0 100 2h1a1 1 0 100-2H9z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <div>
                  <h3 class="text-lg font-semibold text-white">Current Plan</h3>
                  <p class="text-sm text-gray-400">Manage your MYTA subscription</p>
                </div>
              </div>
              <div class="text-right">
                <div class="text-2xl font-bold text-orange-500">{{ currentPlan.name }}</div>
                <div class="text-sm text-gray-400">{{ currentPlan.billing }}</div>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <!-- Plan Details -->
              <div class="md:col-span-2">
                <div class="rounded-lg bg-forest-700 p-4">
                  <h4 class="font-medium text-white mb-3">Plan Features</h4>
                  <div class="space-y-2">
                    <div v-for="feature in currentPlan.features" :key="feature" class="flex items-center space-x-2">
                      <svg class="h-4 w-4 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                      </svg>
                      <span class="text-sm text-gray-300">{{ feature }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Usage Stats -->
              <div>
                <div class="rounded-lg bg-forest-700 p-4">
                  <h4 class="font-medium text-white mb-3">Usage This Month</h4>
                  <div class="space-y-3">
                    <div>
                      <div class="flex justify-between text-sm mb-1">
                        <span class="text-gray-400">AI Conversations</span>
                        <span class="text-white">{{ usage.aiConversations }}/{{ currentPlan.limits.aiConversations }}</span>
                      </div>
                      <div class="w-full bg-forest-600 rounded-full h-2">
                        <div class="bg-orange-500 h-2 rounded-full" :style="{ width: (usage.aiConversations / currentPlan.limits.aiConversations * 100) + '%' }"></div>
                      </div>
                    </div>
                    <div>
                      <div class="flex justify-between text-sm mb-1">
                        <span class="text-gray-400">Content Pillars</span>
                        <span class="text-white">{{ usage.contentPillars }}/{{ currentPlan.limits.contentPillars }}</span>
                      </div>
                      <div class="w-full bg-forest-600 rounded-full h-2">
                        <div class="bg-blue-500 h-2 rounded-full" :style="{ width: (usage.contentPillars / currentPlan.limits.contentPillars * 100) + '%' }"></div>
                      </div>
                    </div>
                    <div>
                      <div class="flex justify-between text-sm mb-1">
                        <span class="text-gray-400">Goals</span>
                        <span class="text-white">{{ usage.goals }}/{{ currentPlan.limits.goals }}</span>
                      </div>
                      <div class="w-full bg-forest-600 rounded-full h-2">
                        <div class="bg-green-500 h-2 rounded-full" :style="{ width: (usage.goals / currentPlan.limits.goals * 100) + '%' }"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="mt-6 flex items-center justify-between">
              <div class="text-sm text-gray-400">
                Next billing date: {{ formatDate(nextBillingDate) }}
              </div>
              <div class="flex space-x-3">
                <button
                  v-if="currentPlan.id !== 'growth'"
                  class="px-4 py-2 text-sm text-gray-400 hover:text-white transition-colors"
                  @click="showCancelModal = true"
                >
                  Cancel Plan
                </button>
                <button
                  class="px-6 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
                  @click="showPlansModal = true"
                >
                  Change Plan
                </button>
              </div>
            </div>
          </div>

          <!-- Payment Method -->
          <div class="rounded-xl bg-forest-800 p-6">
            <div class="mb-6 flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-forest-700">
                  <svg class="h-6 w-6 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4z"/>
                    <path fill-rule="evenodd" d="M18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM4 13a1 1 0 011-1h1a1 1 0 110 2H5a1 1 0 01-1-1zm5-1a1 1 0 100 2h1a1 1 0 100-2H9z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <div>
                  <h3 class="text-lg font-semibold text-white">Payment Method</h3>
                  <p class="text-sm text-gray-400">Manage your payment information</p>
                </div>
              </div>
              <button
                class="px-4 py-2 bg-forest-700 text-white rounded-lg hover:bg-forest-600 transition-colors"
                @click="showPaymentModal = true"
              >
                {{ paymentMethod ? 'Update' : 'Add' }} Payment Method
              </button>
            </div>

            <div v-if="paymentMethod" class="rounded-lg bg-forest-700 p-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-3">
                  <div class="w-12 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded flex items-center justify-center">
                    <span class="text-white text-xs font-bold">{{ paymentMethod.brand.toUpperCase() }}</span>
                  </div>
                  <div>
                    <div class="text-white font-medium">•••• •••• •••• {{ paymentMethod.last4 }}</div>
                    <div class="text-sm text-gray-400">Expires {{ paymentMethod.expiry }}</div>
                  </div>
                </div>
                <button
                  class="text-gray-400 hover:text-red-400 transition-colors"
                  @click="removePaymentMethod"
                >
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
                  </svg>
                </button>
              </div>
            </div>

            <div v-else class="text-center py-8">
              <div class="text-gray-400 mb-4">
                <svg class="h-12 w-12 mx-auto" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4z"/>
                  <path fill-rule="evenodd" d="M18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM4 13a1 1 0 011-1h1a1 1 0 110 2H5a1 1 0 01-1-1zm5-1a1 1 0 100 2h1a1 1 0 100-2H9z" clip-rule="evenodd"/>
                </svg>
              </div>
              <p class="text-gray-400 mb-4">No payment method added</p>
              <button
                class="px-6 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
                @click="showPaymentModal = true"
              >
                Add Payment Method
              </button>
            </div>
          </div>

          <!-- Billing History -->
          <div class="rounded-xl bg-forest-800 p-6">
            <div class="mb-6 flex items-center space-x-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-forest-700">
                <svg class="h-6 w-6 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"/>
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-white">Billing History</h3>
                <p class="text-sm text-gray-400">View and download your invoices</p>
              </div>
            </div>

            <div class="space-y-3">
              <div v-for="invoice in billingHistory" :key="invoice.id" class="flex items-center justify-between p-4 rounded-lg bg-forest-700 hover:bg-forest-600 transition-colors">
                <div class="flex items-center space-x-4">
                  <div class="w-10 h-10 rounded-lg bg-forest-600 flex items-center justify-center">
                    <svg class="h-5 w-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                  <div>
                    <div class="font-medium text-white">{{ invoice.description }}</div>
                    <div class="text-sm text-gray-400">{{ formatDate(invoice.date) }}</div>
                  </div>
                </div>
                <div class="flex items-center space-x-4">
                  <div class="text-right">
                    <div class="font-medium text-white">${{ invoice.amount }}</div>
                    <div class="text-sm" :class="invoice.status === 'paid' ? 'text-green-400' : 'text-yellow-400'">
                      {{ invoice.status.charAt(0).toUpperCase() + invoice.status.slice(1) }}
                    </div>
                  </div>
                  <button
                    class="p-2 text-gray-400 hover:text-white transition-colors"
                    @click="downloadInvoice(invoice.id)"
                  >
                    <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <div v-if="billingHistory.length === 0" class="text-center py-8">
              <div class="text-gray-400 mb-2">
                <span class="text-3xl">📄</span>
              </div>
              <p class="text-gray-400">No billing history yet</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Plans Modal -->
    <div v-if="showPlansModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-forest-800 rounded-xl p-6 max-w-6xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h2 class="text-2xl font-bold text-white">Choose Your Plan</h2>
            <p class="text-gray-400">Select the perfect plan for your YouTube growth journey</p>
          </div>
          <button @click="showPlansModal = false" class="text-gray-400 hover:text-white">
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <!-- Billing Toggle -->
        <div class="flex items-center justify-center mb-8">
          <div class="bg-forest-700 rounded-lg p-1 flex">
            <button
              :class="[
                'px-4 py-2 rounded-md text-sm font-medium transition-colors',
                billingCycle === 'monthly' ? 'bg-orange-500 text-white' : 'text-gray-400 hover:text-white'
              ]"
              @click="billingCycle = 'monthly'"
            >
              Monthly
            </button>
            <button
              :class="[
                'px-4 py-2 rounded-md text-sm font-medium transition-colors',
                billingCycle === 'yearly' ? 'bg-orange-500 text-white' : 'text-gray-400 hover:text-white'
              ]"
              @click="billingCycle = 'yearly'"
            >
              Yearly
              <span class="ml-1 text-xs bg-green-500 text-white px-1.5 py-0.5 rounded">Save 17%</span>
            </button>
          </div>
        </div>

        <!-- Plans Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div
            v-for="plan in availablePlans"
            :key="plan.id"
            :class="[
              'relative rounded-xl p-6 border-2 transition-all',
              plan.popular
                ? 'border-orange-500 bg-gradient-to-b from-orange-500/10 to-transparent'
                : 'border-forest-600 bg-forest-700 hover:border-forest-500',
              currentPlan.id === plan.id ? 'ring-2 ring-orange-500' : ''
            ]"
          >
            <!-- Popular Badge -->
            <div v-if="plan.popular" class="absolute -top-3 left-1/2 transform -translate-x-1/2">
              <span class="bg-orange-500 text-white px-3 py-1 rounded-full text-xs font-medium">
                Most Popular
              </span>
            </div>

            <!-- Current Plan Badge -->
            <div v-if="currentPlan.id === plan.id" class="absolute -top-3 right-4">
              <span class="bg-green-500 text-white px-3 py-1 rounded-full text-xs font-medium">
                Current Plan
              </span>
            </div>

            <div class="text-center mb-6">
              <h3 class="text-xl font-bold text-white mb-2">{{ plan.name }}</h3>
              <p class="text-gray-400 text-sm mb-4">{{ plan.description }}</p>
              <div class="mb-4">
                <span class="text-3xl font-bold text-white">
                  ${{ billingCycle === 'monthly' ? plan.price.monthly : plan.price.yearly }}
                </span>
                <span class="text-gray-400">
                  /{{ billingCycle === 'yearly' ? 'year' : 'month' }}
                </span>
              </div>
              <div v-if="billingCycle === 'yearly'" class="text-sm text-green-400">
                Save ${{ (plan.price.monthly * 12) - plan.price.yearly }} per year
              </div>
            </div>

            <!-- Features -->
            <div class="space-y-3 mb-6">
              <div
                v-for="feature in plan.features.slice(0, 6)"
                :key="feature"
                class="flex items-start space-x-2"
              >
                <svg class="h-4 w-4 text-green-400 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                </svg>
                <span class="text-sm text-gray-300">{{ feature }}</span>
              </div>
              <div v-if="plan.features.length > 6" class="text-xs text-gray-400">
                +{{ plan.features.length - 6 }} more features
              </div>
            </div>

            <!-- Action Button -->
            <button
              v-if="currentPlan.id !== plan.id"
              class="w-full py-3 px-4 rounded-lg font-medium transition-colors"
              :class="plan.popular
                ? 'bg-orange-500 text-white hover:bg-orange-600'
                : 'bg-forest-600 text-white hover:bg-forest-500'"
              @click="selectPlan(plan.id)"
            >
              {{ currentPlan.id === 'growth' ? 'Upgrade' : 'Select Plan' }}
            </button>
            <div v-else class="w-full py-3 px-4 rounded-lg bg-green-500 text-white text-center font-medium">
              Current Plan
            </div>
          </div>
        </div>

        <!-- Trial Notice -->
        <div class="mt-8 p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg">
          <div class="flex items-center space-x-2">
            <svg class="h-5 w-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
            </svg>
            <div>
              <p class="text-blue-400 font-medium">5-Day Free Trial</p>
              <p class="text-blue-300 text-sm">Experience the full power of MYTA with all Pro features unlocked. No credit card required.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAgentSettings } from '../../composables/useAgentSettings'

// Protect this route with authentication
definePageMeta({
  middleware: 'auth'
})

// Agent settings
const { agentName, selectedAgentId, selectedAgent, allAgents, setSelectedAgent, setAgentName, saveSettings } = useAgentSettings()

// Use agents from composable
const agents = allAgents

// Toast notifications
const { success, error } = useToast()

// Tab management
const activeTab = ref('agent')

const tabs = [
  { id: 'agent', name: 'Agent Settings', icon: '🤖' },
  { id: 'subscription', name: 'Subscription', icon: '💳' },
  { id: 'general', name: 'General', icon: '⚙️' }
]

// Subscription data
const currentPlan = ref({
  id: 'growth',
  name: 'Growth',
  billing: '$9/month',
  features: [
    '3 AI Agents (Alex + choice of 2 others)',
    '50 AI conversations/month',
    'Enhanced analytics with engagement metrics',
    '10 content pillars',
    'Advanced task management (up to 50 tasks)',
    'Basic goal tracking (3 goals)',
    'Weekly trending alerts',
    'Email support (48-72h response)',
    'Basic competitive insights (1 competitor)'
  ],
  limits: {
    aiConversations: 50,
    agentsCount: 3,
    contentPillars: 10,
    goals: 3,
    competitors: 1
  }
})

const usage = ref({
  aiConversations: 23,
  agentsCount: 3,
  contentPillars: 7,
  goals: 2,
  competitors: 1
})

// Available plans for upgrade modal
const availablePlans = ref([
  {
    id: 'growth',
    name: 'Growth',
    description: 'Essential tools for serious creators',
    price: { monthly: 9, yearly: 90 },
    popular: false,
    features: [
      '3 AI Agents (Alex + choice of 2 others)',
      '50 AI conversations/month',
      'Enhanced analytics with engagement metrics',
      '10 content pillars',
      'Advanced task management (up to 50 tasks)',
      'Basic goal tracking (3 goals)',
      'Weekly trending alerts',
      'Email support (48-72h response)',
      'Basic competitive insights (1 competitor)'
    ]
  },
  {
    id: 'creator',
    name: 'Creator',
    description: 'For creators ready to scale',
    price: { monthly: 19, yearly: 190 },
    popular: true,
    features: [
      'All 5 AI Agents with full personalities',
      '150 AI conversations/month',
      'Real-time analytics with live data',
      'Advanced charts & insights (retention, CTR, revenue)',
      'Unlimited content pillars',
      'Smart task management with AI suggestions',
      'Advanced competitive analysis (3 competitors)',
      'Unlimited goal tracking',
      'Priority email support (24-48h response)',
      'Daily trending alerts'
    ]
  },
  {
    id: 'pro',
    name: 'Pro',
    description: 'For established creators maximizing growth',
    price: { monthly: 49, yearly: 490 },
    popular: false,
    features: [
      'Unlimited AI conversations',
      'Advanced competitive analysis (unlimited competitors)',
      'AI-powered content strategy with personalized recommendations',
      'Custom agent training on your channel data',
      'Priority support (4-12h response)',
      'Advanced automation & scheduled reports',
      'Team collaboration (3 members)',
      'Custom dashboard layouts',
      'API access for integrations'
    ]
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    description: 'For agencies and top-tier creators',
    price: { monthly: 149, yearly: 1490 },
    popular: false,
    features: [
      'White-label options',
      'Unlimited team members',
      'Multi-channel management (up to 10 channels)',
      'Dedicated account manager',
      'Custom AI agent development',
      '24/7 phone & chat support',
      'Custom reporting & analytics'
    ]
  }
])

const billingCycle = ref('monthly')

const nextBillingDate = ref(new Date('2024-02-15'))

const paymentMethod = ref(null)
// Example payment method:
// const paymentMethod = ref({
//   brand: 'visa',
//   last4: '4242',
//   expiry: '12/25'
// })

const billingHistory = ref([
  {
    id: '1',
    description: 'MYTA Pro Plan - January 2024',
    date: new Date('2024-01-15'),
    amount: '29.99',
    status: 'paid'
  },
  {
    id: '2',
    description: 'MYTA Pro Plan - December 2023',
    date: new Date('2023-12-15'),
    amount: '29.99',
    status: 'paid'
  }
])

// Modal states
const showPlansModal = ref(false)
const showPaymentModal = ref(false)
const showCancelModal = ref(false)

// Save settings function
const handleSaveSettings = () => {
  try {
    saveSettings()
    success('Settings Saved', 'Your agent settings have been saved successfully!')
  } catch (err) {
    error('Save Failed', 'Failed to save your settings. Please try again.')
  }
}

// Subscription functions
const formatDate = (date) => {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}

const removePaymentMethod = () => {
  paymentMethod.value = null
  success('Payment Method Removed', 'Your payment method has been removed successfully.')
}

const downloadInvoice = (invoiceId) => {
  // Mock download functionality
  success('Download Started', 'Your invoice is being downloaded.')
}

const selectPlan = async (planId) => {
  try {
    // Find the selected plan
    const selectedPlan = availablePlans.value.find(plan => plan.id === planId)
    if (!selectedPlan) return

    // Mock plan selection - in real app, this would call the subscription store
    success('Plan Selected', `You've selected the ${selectedPlan.name} plan. Redirecting to checkout...`)

    // Close modal
    showPlansModal.value = false

    // In real implementation, this would redirect to payment processor
    // await subscriptionStore.createCheckoutSession(planId, billingCycle.value)
  } catch (err) {
    error('Plan Selection Failed', 'Failed to select plan. Please try again.')
  }
}
</script>
