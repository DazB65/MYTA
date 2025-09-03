<template>
  <div class="rounded-xl bg-forest-800 p-6">
    <div class="mb-6 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-500">
          <svg class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z"/>
          </svg>
        </div>
        <div>
          <h3 class="text-lg font-semibold text-white">Team Seat Management</h3>
          <p class="text-sm text-gray-400">Manage your team members and seats</p>
        </div>
      </div>
      <div class="text-right">
        <div class="text-lg font-semibold text-white">{{ seatInfo.current_seats }}/{{ seatInfo.max_seats }}</div>
        <div class="text-sm text-gray-400">Seats Used</div>
      </div>
    </div>

    <!-- Current Seat Usage -->
    <div class="mb-6 grid grid-cols-1 gap-4 md:grid-cols-3">
      <div class="rounded-lg bg-forest-700 p-4">
        <div class="text-2xl font-bold text-white">{{ seatInfo.current_seats }}</div>
        <div class="text-sm text-gray-400">Current Seats</div>
        <div class="text-xs text-green-400">${{ seatInfo.total_monthly_cost }}/month</div>
      </div>
      <div class="rounded-lg bg-forest-700 p-4">
        <div class="text-2xl font-bold text-white">{{ seatInfo.team_members.length }}</div>
        <div class="text-sm text-gray-400">Active Members</div>
        <div class="text-xs text-blue-400">{{ seatInfo.current_seats - seatInfo.team_members.length }} available</div>
      </div>
      <div class="rounded-lg bg-forest-700 p-4">
        <div class="text-2xl font-bold text-white">${{ seatInfo.seat_price_monthly }}</div>
        <div class="text-sm text-gray-400">Per Additional Seat</div>
        <div class="text-xs text-gray-400">per month</div>
      </div>
    </div>

    <!-- Seat Management Actions -->
    <div class="mb-6 flex flex-col space-y-4 sm:flex-row sm:space-y-0 sm:space-x-4">
      <div class="flex-1">
        <label class="mb-2 block text-sm font-medium text-white">Add Seats</label>
        <div class="flex space-x-2">
          <input
            v-model.number="seatsToAdd"
            type="number"
            min="1"
            max="10"
            class="flex-1 rounded-lg border border-forest-600 bg-forest-700 px-3 py-2 text-white focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Number of seats"
          />
          <button
            @click="addSeats"
            :disabled="loading || seatsToAdd < 1 || (seatInfo.current_seats + seatsToAdd) > seatInfo.max_seats"
            class="rounded-lg bg-blue-500 px-4 py-2 text-white hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">Adding...</span>
            <span v-else>Add Seats</span>
          </button>
        </div>
        <p class="mt-1 text-xs text-gray-400">
          Cost: ${{ (seatsToAdd * seatInfo.seat_price_monthly).toFixed(2) }}/month
        </p>
      </div>

      <div class="flex-1">
        <label class="mb-2 block text-sm font-medium text-white">Remove Seats</label>
        <div class="flex space-x-2">
          <input
            v-model.number="seatsToRemove"
            type="number"
            min="1"
            :max="Math.max(1, seatInfo.current_seats - seatInfo.team_members.length)"
            class="flex-1 rounded-lg border border-forest-600 bg-forest-700 px-3 py-2 text-white focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500"
            placeholder="Number of seats"
          />
          <button
            @click="removeSeats"
            :disabled="loading || seatsToRemove < 1 || (seatInfo.current_seats - seatsToRemove) < seatInfo.team_members.length"
            class="rounded-lg bg-red-500 px-4 py-2 text-white hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">Removing...</span>
            <span v-else>Remove</span>
          </button>
        </div>
        <p class="mt-1 text-xs text-gray-400">
          Savings: ${{ (seatsToRemove * seatInfo.seat_price_monthly).toFixed(2) }}/month
        </p>
      </div>
    </div>

    <!-- Team Members List -->
    <div>
      <h4 class="mb-4 text-lg font-medium text-white">Team Members</h4>
      <div class="space-y-3">
        <div
          v-for="member in seatInfo.team_members"
          :key="member.id"
          class="flex items-center justify-between rounded-lg bg-forest-700 p-4"
        >
          <div class="flex items-center space-x-3">
            <div class="h-10 w-10 rounded-full bg-forest-600 flex items-center justify-center">
              <span class="text-sm font-medium text-white">
                {{ member.email.charAt(0).toUpperCase() }}
              </span>
            </div>
            <div>
              <div class="font-medium text-white">{{ member.email }}</div>
              <div class="text-sm text-gray-400">
                {{ member.role }} • Joined {{ formatDate(member.joined_at) }}
              </div>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <span
              :class="[
                'px-2 py-1 rounded-full text-xs font-medium',
                member.status === 'active' 
                  ? 'bg-green-500/20 text-green-300'
                  : 'bg-yellow-500/20 text-yellow-300'
              ]"
            >
              {{ member.status }}
            </span>
            <button
              v-if="member.role !== 'owner'"
              @click="removeMember(member)"
              class="text-red-400 hover:text-red-300"
            >
              <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Seat Purchase Confirmation Modal -->
    <div v-if="showConfirmModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-forest-800 rounded-xl p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-semibold text-white mb-4">Confirm Seat Purchase</h3>
        <p class="text-gray-300 mb-4">
          You're about to add {{ pendingSeats }} seat{{ pendingSeats > 1 ? 's' : '' }} to your team.
        </p>
        <div class="bg-forest-700 rounded-lg p-4 mb-4">
          <div class="flex justify-between text-sm">
            <span class="text-gray-400">Additional seats:</span>
            <span class="text-white">{{ pendingSeats }}</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-gray-400">Cost per seat:</span>
            <span class="text-white">${{ seatInfo.seat_price_monthly }}/month</span>
          </div>
          <div class="flex justify-between text-sm font-medium border-t border-forest-600 pt-2 mt-2">
            <span class="text-white">Total additional cost:</span>
            <span class="text-white">${{ (pendingSeats * seatInfo.seat_price_monthly).toFixed(2) }}/month</span>
          </div>
        </div>
        <div class="flex space-x-3">
          <button
            @click="showConfirmModal = false"
            class="flex-1 px-4 py-2 border border-forest-600 text-gray-300 rounded-lg hover:bg-forest-700"
          >
            Cancel
          </button>
          <button
            @click="confirmAddSeats"
            class="flex-1 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            Purchase Seats
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from '../../composables/useToast'

const { success, error } = useToast()

// State
const loading = ref(false)
const seatsToAdd = ref(1)
const seatsToRemove = ref(1)
const showConfirmModal = ref(false)
const pendingSeats = ref(0)

// Mock seat information - replace with API call
const seatInfo = ref({
  current_seats: 3,
  max_seats: 20,
  seat_price_monthly: 9.99,
  seat_price_yearly: 99.99,
  total_monthly_cost: 49.97, // 29.99 base + 2 * 9.99
  team_members: [
    {
      id: '1',
      email: 'owner@example.com',
      role: 'owner',
      status: 'active',
      joined_at: '2024-01-01T00:00:00Z'
    },
    {
      id: '2',
      email: 'member1@example.com',
      role: 'member',
      status: 'active',
      joined_at: '2024-01-15T00:00:00Z'
    },
    {
      id: '3',
      email: 'member2@example.com',
      role: 'member',
      status: 'pending',
      joined_at: '2024-01-20T00:00:00Z'
    }
  ]
})

// Methods
const addSeats = () => {
  if (seatsToAdd.value < 1 || (seatInfo.value.current_seats + seatsToAdd.value) > seatInfo.value.max_seats) {
    error('Invalid number of seats', 'Please enter a valid number of seats to add.')
    return
  }
  
  pendingSeats.value = seatsToAdd.value
  showConfirmModal.value = true
}

const confirmAddSeats = async () => {
  loading.value = true
  showConfirmModal.value = false
  
  try {
    // TODO: Call API to add seats
    // const response = await $fetch('/api/subscription/seats/add', {
    //   method: 'POST',
    //   body: { additional_seats: pendingSeats.value }
    // })
    
    // Mock success
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    seatInfo.value.current_seats += pendingSeats.value
    seatInfo.value.total_monthly_cost += (pendingSeats.value * seatInfo.value.seat_price_monthly)
    
    success('Seats Added', `Successfully added ${pendingSeats.value} seat${pendingSeats.value > 1 ? 's' : ''} to your team.`)
    seatsToAdd.value = 1
    
  } catch (err) {
    error('Failed to Add Seats', 'There was an error adding seats to your team. Please try again.')
  } finally {
    loading.value = false
  }
}

const removeSeats = async () => {
  if (seatsToRemove.value < 1 || (seatInfo.value.current_seats - seatsToRemove.value) < seatInfo.value.team_members.length) {
    error('Cannot Remove Seats', 'You cannot remove seats that are currently in use.')
    return
  }
  
  loading.value = true
  
  try {
    // TODO: Call API to remove seats
    // const response = await $fetch('/api/subscription/seats/remove', {
    //   method: 'POST',
    //   body: { seats_to_remove: seatsToRemove.value }
    // })
    
    // Mock success
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    seatInfo.value.current_seats -= seatsToRemove.value
    seatInfo.value.total_monthly_cost -= (seatsToRemove.value * seatInfo.value.seat_price_monthly)
    
    success('Seats Removed', `Successfully removed ${seatsToRemove.value} seat${seatsToRemove.value > 1 ? 's' : ''} from your team.`)
    seatsToRemove.value = 1
    
  } catch (err) {
    error('Failed to Remove Seats', 'There was an error removing seats from your team. Please try again.')
  } finally {
    loading.value = false
  }
}

const removeMember = async (member) => {
  if (confirm(`Are you sure you want to remove ${member.email} from the team?`)) {
    // TODO: Call API to remove team member
    success('Member Removed', `${member.email} has been removed from the team.`)
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

// Load seat information on mount
onMounted(async () => {
  // TODO: Load actual seat information from API
  // const response = await $fetch('/api/subscription/seats/current')
  // seatInfo.value = response.data
})
</script>
