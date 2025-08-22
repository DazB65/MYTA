<template>
  <div class="min-h-screen bg-forest-900 text-white">
    <!-- Header with MYTA styling -->
    <div class="p-6 pt-24">
      <div class="max-w-6xl mx-auto">
        <!-- Page Header -->
        <div class="mb-8 text-center">
          <h1 class="text-3xl font-bold text-white mb-4">🚀 Team Collaboration Demo</h1>
          <p class="text-gray-400">Experience MYTA's team invitation system</p>
        </div>

        <!-- Demo Cards Grid -->
        <div class="grid md:grid-cols-2 gap-6 mb-8">

          <!-- Team Management Card -->
          <div class="rounded-xl bg-forest-800 p-6">
            <div class="flex items-center mb-6">
              <div class="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center mr-4">
                <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z"/>
                </svg>
              </div>
              <div>
                <h3 class="text-xl font-bold text-white">Team Management</h3>
                <p class="text-gray-400">Manage your team in Settings</p>
              </div>
            </div>

            <div class="space-y-4 mb-6">
              <div class="flex items-center justify-between p-3 bg-forest-700 rounded-lg">
                <span class="text-gray-300">👥 Team Members</span>
                <span class="text-blue-400 font-medium">2 of 3 seats</span>
              </div>
              <div class="flex items-center justify-between p-3 bg-forest-700 rounded-lg">
                <span class="text-gray-300">📧 Pending Invites</span>
                <span class="text-orange-400 font-medium">1 pending</span>
              </div>
              <div class="flex items-center justify-between p-3 bg-forest-700 rounded-lg">
                <span class="text-gray-300">🔐 Your Role</span>
                <span class="text-green-400 font-medium">Owner</span>
              </div>
            </div>

            <a
              href="/settings?tab=team"
              class="block w-full bg-blue-600 text-white text-center py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
            >
              Open Team Settings
            </a>
          </div>

          <!-- Invitation System Card -->
          <div class="rounded-xl bg-forest-800 p-6">
            <div class="flex items-center mb-6">
              <div class="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center mr-4">
                <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                  <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
                </svg>
              </div>
              <div>
                <h3 class="text-xl font-bold text-white">Invitation System</h3>
                <p class="text-gray-400">Test invitation workflows</p>
              </div>
            </div>

            <div class="space-y-3 mb-6">
              <a
                href="/invite/accept?token=demo_token_123"
                target="_blank"
                class="block p-3 bg-green-900/30 border border-green-500/30 rounded-lg hover:bg-green-900/50 transition-colors"
              >
                <div class="flex items-center justify-between">
                  <span class="text-green-300 font-medium">✅ Accept Invitation (Success)</span>
                  <svg class="w-4 h-4 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <p class="text-sm text-green-400 mt-1">See successful invitation acceptance</p>
              </a>

              <a
                href="/invite/accept?token=demo_error_token"
                target="_blank"
                class="block p-3 bg-orange-900/30 border border-orange-500/30 rounded-lg hover:bg-orange-900/50 transition-colors"
              >
                <div class="flex items-center justify-between">
                  <span class="text-orange-300 font-medium">⚠️ Accept Invitation (Error)</span>
                  <svg class="w-4 h-4 text-orange-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <p class="text-sm text-orange-400 mt-1">See error handling for expired invitations</p>
              </a>

              <a
                href="/invite/accept?token=login_required"
                target="_blank"
                class="block p-3 bg-blue-900/30 border border-blue-500/30 rounded-lg hover:bg-blue-900/50 transition-colors"
              >
                <div class="flex items-center justify-between">
                  <span class="text-blue-300 font-medium">🔐 Accept Invitation (Login Required)</span>
                  <svg class="w-4 h-4 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <p class="text-sm text-blue-400 mt-1">See login required state</p>
              </a>

              <a
                href="/invite/decline?token=demo_token_123"
                target="_blank"
                class="block p-3 bg-red-900/30 border border-red-500/30 rounded-lg hover:bg-red-900/50 transition-colors"
              >
                <div class="flex items-center justify-between">
                  <span class="text-red-300 font-medium">❌ Decline Invitation</span>
                  <svg class="w-4 h-4 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <p class="text-sm text-red-400 mt-1">See the invitation decline flow</p>
              </a>
            </div>

            <button
              @click="showEmailPreview = true"
              class="w-full bg-green-600 text-white py-3 rounded-lg font-medium hover:bg-green-700 transition-colors"
            >
              Preview Email Template
            </button>
          </div>
        </div>

        <!-- Features Overview -->
        <div class="rounded-xl bg-forest-800 p-6 mb-6">
          <h3 class="text-2xl font-bold text-white mb-6 text-center">🎯 Team Collaboration Features</h3>

          <div class="grid md:grid-cols-3 gap-6">
            <div class="text-center">
              <div class="w-16 h-16 bg-blue-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg class="w-8 h-8 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M8 9a3 3 0 100-6 3 3 0 000 6zM8 11a6 6 0 016 6H2a6 6 0 016-6zM16 7a1 1 0 10-2 0v1h-1a1 1 0 100 2h1v1a1 1 0 102 0v-1h1a1 1 0 100-2h-1V7z"/>
                </svg>
              </div>
              <h4 class="font-semibold text-white mb-2">Role-Based Access</h4>
              <p class="text-sm text-gray-400">Owner, Editor, and Viewer roles with specific permissions</p>
            </div>

            <div class="text-center">
              <div class="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg class="w-8 h-8 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                  <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
                </svg>
              </div>
              <h4 class="font-semibold text-white mb-2">Email Invitations</h4>
              <p class="text-sm text-gray-400">Beautiful HTML emails with secure token-based invitations</p>
            </div>

            <div class="text-center">
              <div class="w-16 h-16 bg-purple-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg class="w-8 h-8 text-purple-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
                </svg>
              </div>
              <h4 class="font-semibold text-white mb-2">Secure Workflow</h4>
              <p class="text-sm text-gray-400">Cryptographically secure tokens with expiration handling</p>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Email Preview Modal -->
    <div v-if="showEmailPreview" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-forest-800 rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-forest-600">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-bold text-white">📧 Email Template Preview</h3>
            <button @click="showEmailPreview = false" class="text-gray-400 hover:text-gray-300">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
              </svg>
            </button>
          </div>
        </div>

        <div class="p-6">
          <div class="bg-white rounded-lg p-6 mb-4">
            <div class="text-center mb-6">
              <div class="text-2xl font-bold text-indigo-600 mb-2">MYTA</div>
              <h2 class="text-xl font-semibold text-gray-900">You're Invited to Join a Team!</h2>
            </div>

            <p class="text-gray-700 mb-4">Hi there!</p>
            <p class="text-gray-700 mb-4"><strong>John Doe</strong> (john@example.com) has invited you to join their team on MYTA.</p>

            <div class="bg-gray-50 border-l-4 border-indigo-500 p-4 mb-4">
              <div class="flex justify-between mb-2">
                <span class="font-medium text-gray-700">Team:</span>
                <span class="text-gray-900"><strong>My Content Team</strong></span>
              </div>
              <div class="flex justify-between mb-2">
                <span class="font-medium text-gray-700">Your Role:</span>
                <span class="bg-indigo-100 text-indigo-800 px-2 py-1 rounded-full text-sm">Editor</span>
              </div>
            </div>

            <div class="text-center space-x-4 mb-4">
              <button class="bg-green-500 text-white px-6 py-2 rounded-lg font-medium">Accept Invitation</button>
              <button class="bg-red-500 text-white px-6 py-2 rounded-lg font-medium">Decline</button>
            </div>

            <p class="text-sm text-gray-600 text-center">This invitation expires in 7 days</p>
          </div>

          <p class="text-sm text-gray-400">This is a preview of the actual HTML email that gets sent to team members.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Set page title
useHead({
  title: 'Team Collaboration Demo'
})

// State
const showEmailPreview = ref(false)
</script>
