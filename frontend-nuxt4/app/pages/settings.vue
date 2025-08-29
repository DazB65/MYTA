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
              <label class="mb-2 block text-sm font-medium text-white">Boss Agent Name</label>
              <input
                v-model="agentName"
                type="text"
                placeholder="Enter your Boss Agent's name"
                class="w-full rounded-lg border border-forest-600 bg-forest-700 px-4 py-3 text-white placeholder-gray-400 focus:border-orange-500 focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
              <p class="mt-1 text-xs text-gray-400">
                Your Boss Agent coordinates with specialized agents behind the scenes
              </p>
            </div>

            <!-- Boss Agent Display -->
            <div>
              <label class="mb-2 block text-sm font-medium text-white">Your Personal Boss Agent</label>
              <p class="mb-4 text-xs text-gray-400">
                Your Boss Agent coordinates with all specialists behind the scenes.
              </p>
              <div class="mb-6 text-center">
                <div class="mx-auto mb-4 h-48 w-48 overflow-hidden rounded-xl bg-forest-700 ring-4 ring-orange-500 ring-opacity-50">
                  <img :src="selectedAgent.image" :alt="selectedAgent.name" class="h-full w-full object-cover" />
                </div>
                <div class="text-xl font-semibold text-white">{{ agentName || selectedAgent.name }}</div>
                <div class="text-sm text-gray-400">{{ selectedAgent.description }}</div>
              </div>
            </div>

            <!-- Specialist Agents Display -->
            <div>
              <label class="mb-2 block text-sm font-medium text-white">Your Specialist Team</label>
              <p class="mb-4 text-xs text-gray-400">
                Your Boss Agent coordinates with these specialists behind the scenes.
              </p>
              <div class="grid grid-cols-5 gap-3">
                <div
                  v-for="agent in specialistAgents"
                  :key="agent.id"
                  class="text-center p-3 rounded-lg bg-forest-700"
                >
                  <div class="mx-auto mb-2 h-12 w-12 overflow-hidden rounded-lg bg-forest-600">
                    <img :src="agent.image" :alt="agent.name" class="h-full w-full object-cover" />
                  </div>
                  <div class="text-xs font-medium text-gray-300">{{ agent.name }}</div>
                  <div class="text-xs text-gray-500 mt-1">{{ agent.description }}</div>
                </div>
              </div>
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

        <!-- Team Management Tab -->
        <div v-if="activeTab === 'team'" class="space-y-6">
          <!-- Team Overview -->
          <div class="rounded-xl bg-forest-800 p-6">
            <div class="mb-6 flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-500">
                  <svg class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z"/>
                  </svg>
                </div>
                <div>
                  <h3 class="text-lg font-semibold text-white">Team Management</h3>
                  <p class="text-sm text-gray-400">Manage your team members and collaboration settings</p>
                </div>
              </div>
              <div class="flex space-x-3">
                <button
                  @click="openTeamEdit"
                  class="bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 transition-colors flex items-center space-x-2"
                >
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/>
                  </svg>
                  <span>Edit Team</span>
                </button>
                <button
                  @click="openTeamInvite"
                  class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2"
                >
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M8 9a3 3 0 100-6 3 3 0 000 6zM8 11a6 6 0 016 6H2a6 6 0 016-6zM16 7a1 1 0 10-2 0v1h-1a1 1 0 100 2h1v1a1 1 0 102 0v-1h1a1 1 0 100-2h-1V7z"/>
                  </svg>
                  <span>Invite Member</span>
                </button>
              </div>
            </div>

            <!-- Team Info -->
            <div v-if="currentTeam" class="mb-6 rounded-lg bg-forest-700 p-4">
              <div class="flex items-center justify-between mb-4">
                <div>
                  <h4 class="font-medium text-white">{{ currentTeam.name }}</h4>
                  <p class="text-sm text-gray-400">{{ currentTeam.member_count }} of {{ currentTeam.max_seats }} seats used</p>
                </div>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  Team Plan
                </span>
              </div>

              <div class="w-full bg-forest-600 rounded-full h-2 mb-4">
                <div
                  class="bg-blue-500 h-2 rounded-full transition-all duration-300"
                  :style="{ width: `${(currentTeam.member_count / currentTeam.max_seats) * 100}%` }"
                ></div>
              </div>
            </div>

            <!-- No Team State -->
            <div v-else-if="!teamLoading" class="mb-6 rounded-lg bg-forest-700 p-4 text-center">
              <div class="py-8">
                <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                </svg>
                <h4 class="font-medium text-white mb-2">No Team Yet</h4>
                <p class="text-sm text-gray-400 mb-4">Create a team to collaborate with others</p>
                <button
                  @click="handleCreateTeam"
                  class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Create Team
                </button>
              </div>
            </div>

            <!-- Loading State -->
            <div v-else class="mb-6 rounded-lg bg-forest-700 p-4">
              <div class="animate-pulse">
                <div class="flex items-center justify-between mb-4">
                  <div>
                    <div class="h-4 bg-forest-600 rounded w-32 mb-2"></div>
                    <div class="h-3 bg-forest-600 rounded w-24"></div>
                  </div>
                  <div class="h-6 bg-forest-600 rounded w-20"></div>
                </div>
                <div class="w-full bg-forest-600 rounded-full h-2"></div>
              </div>
            </div>

            <!-- Team Members -->
            <div v-if="currentTeam && currentTeam.members" class="mb-6">
              <div class="flex items-center justify-between mb-4">
                <h4 class="font-medium text-white">Team Members</h4>
                <span class="text-sm text-gray-400">{{ currentTeam.members.length }} members</span>
              </div>
              <div class="space-y-3">
                <div
                  v-for="member in currentTeam.members"
                  :key="member.id"
                  class="flex items-center justify-between p-3 rounded-lg bg-forest-700 hover:bg-forest-600 transition-colors"
                >
                  <div class="flex items-center space-x-3">
                    <div
                      class="w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-medium"
                      :style="{ backgroundColor: getMemberColor(member) }"
                    >
                      {{ getMemberInitials(member) }}
                    </div>
                    <div>
                      <p class="text-white font-medium">
                        {{ member.user_name }}
                        <span v-if="isCurrentUser(member)" class="text-gray-400">(You)</span>
                      </p>
                      <p class="text-xs text-gray-400">{{ member.user_email }}</p>
                      <p v-if="member.joined_at" class="text-xs text-gray-500">
                        Joined {{ formatMemberSince(member.joined_at) }}
                      </p>
                    </div>
                  </div>
                  <div class="flex items-center space-x-2">
                    <span
                      class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
                      :class="getRoleBadgeClasses(member.role)"
                    >
                      {{ getRoleDisplayName(member.role) }}
                    </span>
                    <button
                      v-if="canRemoveMember(member)"
                      @click="openMemberRemoveModal(member)"
                      class="text-red-400 hover:text-red-300 text-sm transition-colors"
                    >
                      Remove
                    </button>
                  </div>
                </div>
              </div>

              <!-- Pending Invitations -->
              <div v-if="currentTeam.pending_invitations && currentTeam.pending_invitations.length > 0" class="mt-6">
                <h5 class="font-medium text-white mb-3">Pending Invitations</h5>
                <div class="space-y-2">
                  <div
                    v-for="invitation in currentTeam.pending_invitations"
                    :key="invitation.id"
                    class="flex items-center justify-between p-3 rounded-lg bg-forest-700/50 border border-forest-600"
                  >
                    <div class="flex items-center space-x-3">
                      <div class="w-8 h-8 bg-gray-500 rounded-full flex items-center justify-center">
                        <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                          <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
                        </svg>
                      </div>
                      <div>
                        <p class="text-white font-medium">{{ invitation.email }}</p>
                        <p class="text-xs text-gray-400">
                          Invited {{ formatDate(invitation.created_at) }} • Expires {{ formatDate(invitation.expires_at) }}
                        </p>
                      </div>
                    </div>
                    <span
                      class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800"
                    >
                      {{ getRoleDisplayName(invitation.role) }} • Pending
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Demo Links (Keep for testing) -->
            <div class="mt-6 p-4 bg-blue-900/20 border border-blue-500/30 rounded-lg">
              <h4 class="font-medium text-blue-300 mb-2">🚀 Demo the Invitation System</h4>
              <p class="text-sm text-blue-200 mb-3">Test the team invitation workflow:</p>
              <div class="space-y-2">
                <a
                  href="/invite/accept?token=demo_token_123"
                  target="_blank"
                  class="block text-blue-300 hover:text-blue-200 text-sm underline"
                >
                  → View Accept Invitation Page
                </a>
                <a
                  href="/invite/decline?token=demo_token_123"
                  target="_blank"
                  class="block text-blue-300 hover:text-blue-200 text-sm underline"
                >
                  → View Decline Invitation Page
                </a>
              </div>
            </div>
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
                  class="px-6 py-2 bg-forest-600 text-white rounded-lg hover:bg-forest-500 transition-colors"
                  @click="manageBilling"
                >
                  Manage Billing
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
                @click="addPaymentMethod"
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
                @click="addPaymentMethod"
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
      <div class="bg-forest-800 rounded-xl p-6 max-w-7xl w-full mx-4 max-h-[95vh] overflow-y-auto">
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
                v-for="feature in plan.features"
                :key="feature"
                class="flex items-start space-x-2"
              >
                <svg class="h-4 w-4 text-green-400 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                </svg>
                <span class="text-sm text-gray-300">{{ feature }}</span>
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
import { useRoute } from 'vue-router'
import { useAgentSettings } from '../../composables/useAgentSettings'
import { useModals } from '../../composables/useModals'
import { useTeamManagement } from '../../composables/useTeamManagement'
import { useAuthStore } from '../../stores/auth'
import { useSubscriptionStore } from '../../stores/subscription'

// Protect this route with authentication
definePageMeta({
  middleware: 'auth'
})

// Agent settings
const { agentName, selectedAgentId, selectedAgent, allAgents, setSelectedAgent, setAgentName, saveSettings } = useAgentSettings()

// Use agents from composable
const agents = allAgents

// Computed property for specialist agents (exclude Boss Agent)
const specialistAgents = computed(() => allAgents.value.slice(1))

// Toast notifications
const { success, error } = useToast()

// Subscription store
const subscriptionStore = useSubscriptionStore()

// Team management
const {
  currentTeam,
  loading: teamLoading,
  error: teamError,
  fetchMyTeam,
  createTeam,
  getRoleDisplayName,
  formatMemberSince
} = useTeamManagement()

// Modal management
const {
  openTeamInvite,
  openTeamEdit,
  openTeamMemberRemove
} = useModals()

// Auth store
const authStore = useAuthStore()

// Tab management
const route = useRoute()
const activeTab = ref(route.query.tab || 'agent')

const tabs = [
  { id: 'agent', name: 'Agent Settings', icon: '🤖' },
  { id: 'team', name: 'Team Management', icon: '👥' },
  { id: 'subscription', name: 'Subscription', icon: '💳' },
  { id: 'general', name: 'General', icon: '⚙️' }
]

// Subscription data
const currentPlan = ref({
  id: 'creator',
  name: 'Creator',
  billing: '$19/month',
  features: [
    'All 5 AI Agents with full personalities',
    '100 AI conversations/month',
    'Advanced analytics with engagement insights',
    'Unlimited content pillars',
    'Smart task management with AI suggestions',
    'Unlimited goal tracking',
    'Research Workspace PRO with templates',
    'Competitor analysis (3 competitors)',
    'Video performance analysis (50/month)',
    'Daily trending alerts',
    'Priority email support (24-48h response)'
  ],
  limits: {
    aiConversations: 100,
    agentsCount: 5,
    contentPillars: -1,
    goals: -1,
    competitors: 3,
    researchProjects: 10,
    videoAnalysis: 50
  }
})

const usage = ref({
  aiConversations: 34,
  agentsCount: 5,
  contentPillars: 12,
  goals: 4,
  competitors: 2,
  researchProjects: 3,
  videoAnalysis: 18
})

// Available plans for upgrade modal
const availablePlans = ref([
  {
    id: 'starter',
    name: 'Starter',
    description: 'Perfect for new YouTubers getting started',
    price: { monthly: 7, yearly: 70 },
    popular: false,
    features: [
      'All 5 AI Agents with full personalities',
      '30 AI conversations/month',
      '4 content pillars',
      'Task management (up to 25 tasks)',
      'Goal tracking (2 goals)',
      'Weekly trending alerts',
      'Email support (72h response)'
    ]
  },
  {
    id: 'creator',
    name: 'Creator',
    description: 'For serious creators ready to scale',
    price: { monthly: 19, yearly: 190 },
    popular: true,
    features: [
      'All of Starter, plus:',
      '70 additional AI conversations/month (100 total)',
      '4 additional content pillars (8 total)',
      '3 additional goal tracking (5 total)',
      'Research Workspace PRO with templates'
    ]
  },
  {
    id: 'pro',
    name: 'Pro',
    description: 'For established creators maximizing revenue',
    price: { monthly: 39, yearly: 390 },
    popular: false,
    features: [
      'All of Creator, plus:',
      '200 additional AI conversations/month (300 total)',
      'Unlimited content pillars (vs 8)',
      'Unlimited goal tracking (vs 5)',
      'Team collaboration (2 members including owner)'
    ]
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    description: 'For agencies and multi-channel operations',
    price: { monthly: 99, yearly: 990 },
    popular: false,
    features: [
      '500 AI conversations/month',
      'Team collaboration (4 members including owner)',
      'Advanced team permissions & roles',
      'Dedicated account management',
      'Priority feature development'
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

// Team management functions
const showInviteDemo = () => {
  success('Demo Invitation Sent! 📧', 'In a real app, this would send an email invitation. Check the demo links below to see the invitation pages.')
}

// Helper functions for team members
const getMemberInitials = (member) => {
  if (!member?.user_name) return '??'
  return member.user_name
    .split(' ')
    .map(name => name.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const getMemberColor = (member) => {
  const colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']
  const index = member?.user_name?.charCodeAt(0) % colors.length || 0
  return colors[index]
}

const getRoleBadgeClasses = (role) => {
  switch (role) {
    case 'owner':
      return 'bg-orange-100 text-orange-800'
    case 'editor':
      return 'bg-blue-100 text-blue-800'
    case 'viewer':
      return 'bg-gray-100 text-gray-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

const isCurrentUser = (member) => {
  return authStore.user?.id === member.user_id
}

const canRemoveMember = (member) => {
  // Can't remove yourself or if you're not the owner
  return !isCurrentUser(member) && authStore.user?.id === currentTeam.value?.owner_id
}

// Modal functions
const openMemberRemoveModal = (member) => {
  openTeamMemberRemove(member)
}

const handleCreateTeam = async () => {
  try {
    await createTeam('My Content Team', 3)
    success('Team Created! 🎉', 'Your team has been created successfully')
  } catch (err) {
    error('Creation Failed', err.message || 'Failed to create team')
  }
}

// Initialize team data when component mounts
onMounted(async () => {
  if (authStore.isLoggedIn) {
    try {
      await fetchMyTeam()
    } catch (err) {
      console.warn('Failed to fetch team data:', err)
    }
  }
})

// Save settings function
const handleSaveSettings = () => {
  try {
    saveSettings()
    success('Settings Saved', 'Your agent settings have been saved successfully!')
  } catch (err) {
    error('Save Failed', 'Failed to save your settings. Please try again.')
  }
}

// Utility functions
const formatDate = (date) => {
  if (!date) return 'Unknown'

  // Handle both string and Date objects
  const dateObj = typeof date === 'string' ? new Date(date) : date

  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(dateObj)
}

const removePaymentMethod = () => {
  paymentMethod.value = null
  success('Payment Method Removed', 'Your payment method has been removed successfully.')
}

const downloadInvoice = (invoiceId) => {
  if (process.env.NODE_ENV === 'development') {
    console.log('downloadInvoice called for:', invoiceId)
  }

  // Mock download functionality with reliable alert
  alert('✅ Download Started\n\nIn a real app, this would download the invoice PDF from Stripe. Your invoice download would begin automatically.')

  // Also try the toast (might work if toast container is available)
  try {
    success('Download Started', 'Your invoice is being downloaded.')
  } catch (e) {
    if (process.env.NODE_ENV === 'development') {
      console.log('Toast failed, but alert worked')
    }
  }
}

const selectPlan = async (planId) => {
  try {
    // Find the selected plan
    const selectedPlan = availablePlans.value.find(plan => plan.id === planId)
    if (!selectedPlan) return

    // Use Stripe integration through subscription store
    const result = await subscriptionStore.createCheckoutSession(planId, billingCycle.value)

    if (result.success) {
      success('Checkout Initiated', result.message)

      // Close modal
      showPlansModal.value = false

      // In production, user would be redirected to Stripe Checkout
      // For demo, we just show success message
    }
  } catch (err) {
    error('Plan Selection Failed', 'Failed to select plan. Please try again.')
  }
}

// Manage billing portal function
const manageBilling = () => {
  if (process.env.NODE_ENV === 'development') {
    console.log('manageBilling called')
  }

  // Use both alert and toast for reliability
  alert('✅ Billing Portal\n\nIn a real app, this would redirect to Stripe Customer Portal where users can manage billing, update payment methods, download invoices, and cancel subscriptions.')

  // Also try the toast (might work if toast container is available)
  try {
    success('Billing Portal', 'In a real app, this would redirect to Stripe Customer Portal where users can manage billing, update payment methods, download invoices, and cancel subscriptions.')
  } catch (e) {
    if (process.env.NODE_ENV === 'development') {
      console.log('Toast failed, but alert worked')
    }
  }
}

// Add payment method function
const addPaymentMethod = () => {
  if (process.env.NODE_ENV === 'development') {
    console.log('addPaymentMethod called')
  }

  // Use both alert and toast for reliability
  alert('✅ Payment Method\n\nIn a real app, this would open a secure form to add or update payment methods via Stripe.')

  // Also try the toast (might work if toast container is available)
  try {
    success('Payment Method', 'In a real app, this would open a secure form to add or update payment methods via Stripe.')
  } catch (e) {
    if (process.env.NODE_ENV === 'development') {
      console.log('Toast failed, but alert worked')
    }
  }
}
</script>
