<template>
  <div class="min-h-screen bg-gradient-to-b from-slate-800 via-gray-850 to-gray-900 text-white">
    <div class="p-6 pt-24">
      <div class="space-y-8">
      <!-- Page Header -->
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <h1 class="text-2xl font-bold text-white">Task Management</h1>
          <span class="text-gray-400">•</span>
          <p class="text-gray-400">Organize and track your content creation tasks with Agent-powered insights</p>
        </div>

        <div class="flex items-center space-x-3">
          <button
            :class="currentView === 'dashboard' ? 'rounded-lg bg-orange-500 px-4 py-2 text-sm text-white' : 'rounded-lg bg-gray-700 px-4 py-2 text-sm text-gray-300 hover:bg-gray-600'"
            @click="currentView = 'dashboard'"
          >
            📅 Calendar
          </button>
          <button
            :class="currentView === 'manager' ? 'rounded-lg bg-orange-500 px-4 py-2 text-sm text-white' : 'rounded-lg bg-gray-700 px-4 py-2 text-sm text-gray-300 hover:bg-gray-600'"
            @click="currentView = 'manager'"
          >
            📋 Task Manager
          </button>
        </div>
      </div>

      <!-- Dashboard View -->
      <div v-if="currentView === 'dashboard'" class="space-y-6">
        <!-- Two Column Layout: Calendar + Levi Suggestions -->
        <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <!-- Left Column: Calendar (2/3 width) -->
          <div class="lg:col-span-2">
            <!-- Calendar Container -->
            <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
              <!-- Calendar Header -->
              <div class="mb-6 flex items-center justify-between">
                <div class="flex items-center space-x-4">
                  <button @click="previousMonth" class="p-2 rounded-lg bg-gray-700 hover:bg-gray-600 text-white">
                    <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                  </button>
                  <h2 class="text-xl font-bold text-white">{{ currentMonthYear }}</h2>
                  <button @click="nextMonth" class="p-2 rounded-lg bg-gray-700 hover:bg-gray-600 text-white">
                    <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                    </svg>
                  </button>
                </div>
                <div class="flex items-center space-x-2">
                  <button @click="goToToday" class="px-4 py-2 rounded-lg bg-orange-500 hover:bg-orange-600 text-white text-sm">
                    Today
                  </button>
                </div>
              </div>

              <!-- Calendar Grid -->
              <div class="grid grid-cols-7 gap-1">
                <!-- Day Headers -->
                <div v-for="day in dayHeaders" :key="day" class="p-3 text-center text-sm font-medium text-gray-400">
                  {{ day }}
                </div>

                <!-- Calendar Days -->
                <div
                  v-for="day in calendarDays"
                  :key="`${day.date.getFullYear()}-${day.date.getMonth()}-${day.date.getDate()}`"
                  :class="[
                    'min-h-[120px] p-2 border-2 border-gray-600/70 shadow-lg rounded-lg cursor-pointer transition-colors',
                    day.isCurrentMonth ? 'bg-gray-800 hover:bg-gray-700' : 'bg-gray-900 opacity-50',
                    day.isToday ? 'ring-2 ring-orange-500' : '',
                    selectedDate && day.date.toDateString() === selectedDate.toDateString() ? 'bg-gray-600' : ''
                  ]"
                  @click="selectDate(day.date)"
                  @dragover.prevent="handleDragOver"
                  @dragenter.prevent="handleDragEnter"
                  @dragleave="handleDragLeave"
                  @drop="handleTaskDrop(day.date, $event)"
                >
                  <!-- Day Number -->
                  <div class="flex items-center justify-between mb-2">
                    <span :class="[
                      'text-sm font-medium',
                      day.isToday ? 'text-orange-400' : day.isCurrentMonth ? 'text-white' : 'text-gray-500'
                    ]">
                      {{ day.date.getDate() }}
                    </span>
                    <button
                      v-if="day.isCurrentMonth"
                      @click.stop="addTaskToDate(day.date)"
                      class="text-gray-400 hover:text-white text-xs opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      +
                    </button>
                  </div>

                  <!-- Tasks, Content, and Goals for this day -->
                  <div class="space-y-1">
                    <div
                      v-for="item in getTasksForDate(day.date)"
                      :key="`${item.type || 'task'}-${item.id}`"
                      :class="getCalendarItemClasses(item)"
                      :draggable="item.type === 'task' || item.type === 'goal' || !item.type"
                      @dragstart="handleCalendarTaskDragStart(item, $event)"
                      @click.stop="handleTaskClick(item)"
                      :title="item.type === 'content' ? `${item.title} (${getStageLabel(item.status)})` :
                               item.type === 'goal' ? `Goal: ${item.title} (${Math.round((item.current / item.target) * 100)}%)` :
                               item.title"
                    >
                      <div class="flex items-center space-x-1">
                        <span v-if="item.type === 'content'" class="text-xs opacity-75">
                          {{ item.pillar?.icon || '📄' }}
                        </span>
                        <span v-else-if="item.type === 'goal'" class="text-xs opacity-75">
                          {{ item.icon || '🎯' }}
                        </span>
                        <span v-else class="text-xs opacity-75">📋</span>
                        <span class="truncate">{{ item.title }}</span>
                      </div>
                      <div v-if="item.type === 'content'" class="text-xs opacity-60 mt-0.5">
                        {{ getStageLabel(item.status) }}
                      </div>
                      <div v-else-if="item.type === 'goal'" class="text-xs opacity-60 mt-0.5">
                        {{ Math.round((item.current / item.target) * 100) }}% Complete
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Enhanced Calendar Legend -->
              <div class="mt-4 pt-4 border-t border-gray-700">
                <div class="space-y-3">
                  <!-- Header -->
                  <div class="flex items-center justify-between">
                    <h4 class="text-sm font-medium text-white">Color Legend</h4>
                    <span class="text-xs text-gray-500">Enhanced Border System</span>
                  </div>

                  <!-- Task Priority Colors -->
                  <div class="flex items-center space-x-4">
                    <div class="text-xs font-medium text-gray-300">📋 Task Priority</div>
                    <div class="flex items-center space-x-4 text-xs">
                      <div class="flex items-center space-x-2">
                        <div class="w-4 h-3 rounded bg-red-900/70 border-2 border-red-600/60 shadow-red-600/20 shadow-sm"></div>
                        <span class="text-red-300">🔴 Urgent</span>
                      </div>
                      <div class="flex items-center space-x-2">
                        <div class="w-4 h-3 rounded bg-orange-900/70 border-2 border-orange-600/60 shadow-orange-600/20 shadow-sm"></div>
                        <span class="text-orange-300">🟠 High</span>
                      </div>
                      <div class="flex items-center space-x-2">
                        <div class="w-4 h-3 rounded bg-blue-900/70 border-2 border-blue-600/60 shadow-blue-600/20 shadow-sm"></div>
                        <span class="text-blue-300">🔵 Medium</span>
                      </div>
                      <div class="flex items-center space-x-2">
                        <div class="w-4 h-3 rounded bg-green-900/70 border-2 border-green-600/60 shadow-green-600/20 shadow-sm"></div>
                        <span class="text-green-300">🟢 Low</span>
                      </div>
                    </div>
                  </div>



                  <!-- Goals -->
                  <div class="flex items-center space-x-4">
                    <div class="text-xs font-medium text-gray-300">🎯 Goals</div>
                    <div class="flex items-center space-x-2 text-xs">
                      <div class="w-4 h-3 rounded bg-cyan-900/70 border-2 border-cyan-600/60 shadow-cyan-600/20 shadow-sm"></div>
                      <span class="text-cyan-300">Goals Tracking</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column: Tasks to Schedule (1/3 width) -->
          <div class="space-y-6">
            <!-- Tasks to Schedule -->
            <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
              <div class="mb-6 flex items-center justify-between">
                <div class="flex items-center space-x-3">
                  <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-orange-500/20">
                    <svg class="h-6 w-6 text-orange-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-white">Tasks to Schedule</h3>
                    <p class="text-sm text-gray-400">Drag tasks to calendar or set due dates</p>
                  </div>
                </div>

                <!-- Task Count Badge -->
                <div v-if="unscheduledTasks.length > 0" class="flex items-center space-x-2">
                  <span class="px-2 py-1 bg-orange-500/20 text-orange-400 text-xs rounded-full font-medium">
                    {{ unscheduledTasks.length }} tasks
                  </span>
                </div>
              </div>

              <!-- Empty State for Unscheduled Tasks -->
              <EmptyState
                v-if="unscheduledTasks.length === 0"
                icon="✅"
                title="All Caught Up!"
                description="All your tasks are scheduled. Great job staying organized!"
                :show-plus-icon="false"
                variant="success"
              />

              <!-- Unscheduled Tasks List -->
              <div v-else class="space-y-3">
                <div
                  v-for="task in unscheduledTasks"
                  :key="task.id"
                  class="rounded-lg p-4 bg-gray-700 hover:bg-gray-600 transition-colors cursor-pointer border-2 border-gray-600/70 shadow-lg"
                  draggable="true"
                  @dragstart="startDragTask(task, $event)"
                  @click="scheduleTask(task)"
                >
                  <div class="flex items-start space-x-3">
                    <!-- Priority Indicator -->
                    <div
                      class="w-3 h-3 rounded-full flex-shrink-0 mt-1"
                      :class="{
                        'bg-red-500': task.priority === 'urgent',
                        'bg-orange-500': task.priority === 'high',
                        'bg-yellow-500': task.priority === 'medium',
                        'bg-green-500': task.priority === 'low'
                      }"
                    ></div>

                    <!-- Task Content -->
                    <div class="flex-1 min-w-0">
                      <div class="flex items-start justify-between mb-2">
                        <h4 class="font-medium text-white text-sm truncate">{{ task.title }}</h4>
                        <span
                          class="px-2 py-1 rounded-full text-xs font-medium ml-2 flex-shrink-0"
                          :class="{
                            'bg-red-500/20 text-red-400': task.priority === 'urgent',
                            'bg-orange-500/20 text-orange-400': task.priority === 'high',
                            'bg-yellow-500/20 text-yellow-400': task.priority === 'medium',
                            'bg-green-500/20 text-green-400': task.priority === 'low'
                          }"
                        >
                          {{ task.priority }}
                        </span>
                      </div>

                      <p class="text-xs text-gray-400 mb-3 line-clamp-2">{{ task.description }}</p>

                      <!-- Task Meta Info -->
                      <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-3 text-xs text-gray-500">
                          <span class="capitalize">{{ task.category }}</span>
                          <span v-if="task.estimatedTime">{{ task.estimatedTime }}m</span>
                          <span v-if="task.tags.includes('agent-generated')" class="text-orange-400">🤖 AI</span>
                          <span v-if="task.tags.includes('video-optimization')" class="text-blue-400">📹 Video</span>
                        </div>
                        <div class="flex space-x-2">
                          <button
                            @click.stop="scheduleTask(task)"
                            class="rounded bg-orange-500 px-2 py-1 text-xs text-white transition-colors hover:bg-orange-400"
                          >
                            Schedule
                          </button>
                          <button
                            @click.stop="editTask(task)"
                            class="rounded bg-gray-600 px-2 py-1 text-xs text-white transition-colors hover:bg-gray-500"
                          >
                            Edit
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>


          </div>
        </div>

        <!-- Task Details Sidebar (when date selected) -->
        <div v-if="selectedDate" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Selected Date Tasks -->
          <div class="lg:col-span-2 rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
            <div class="mb-4 flex items-center justify-between">
              <h3 class="text-lg font-semibold text-white">
                Tasks for {{ formatDate(selectedDate) }}
              </h3>
              <button
                @click="addTaskToSelectedDate"
                class="rounded-lg bg-orange-500 px-4 py-2 text-sm text-white hover:bg-orange-600"
              >
                + Add Task
              </button>
            </div>

            <div class="space-y-3">
              <div
                v-for="item in getTasksForDate(selectedDate)"
                :key="`${item.type || 'task'}-${item.id}`"
                :class="[
                  'flex items-center justify-between rounded-lg p-4',
                  item.type === 'content' ? 'bg-gray-700/50 border-2 border-gray-600/70 shadow-lg' :
                  item.type === 'goal' ? 'bg-gray-700/30 border-2 border-gray-600/70 shadow-lg/20' :
                  'bg-gray-700'
                ]"
              >
                <div class="flex items-center space-x-3">
                  <!-- Different indicators for each type -->
                  <div v-if="item.type === 'content'" :class="['w-4 h-4 rounded border-2 flex items-center justify-center', getContentColor()]">
                    <span v-if="item.stageCompletions && item.stageCompletions[item.status]" class="text-xs">✓</span>
                  </div>
                  <div v-else-if="item.type === 'goal'" :class="['w-4 h-4 rounded-full border-2 flex items-center justify-center', getGoalColor()]">
                    <span class="text-xs">🎯</span>
                  </div>
                  <input
                    v-else
                    :checked="item.completed"
                    @change="toggleTaskCompletion(item.id)"
                    type="checkbox"
                    class="h-4 w-4 rounded border-gray-300 text-orange-500 focus:ring-orange-500"
                  />

                  <div class="flex-1">
                    <div class="flex items-center space-x-2">
                      <span v-if="item.type === 'content'" class="text-sm">{{ item.pillar?.icon || '📄' }}</span>
                      <span v-else-if="item.type === 'goal'" class="text-sm">{{ item.icon || '🎯' }}</span>
                      <span v-else class="text-sm">📋</span>
                      <h4 :class="['font-medium', item.completed ? 'line-through text-gray-500' : 'text-white']">
                        {{ item.title }}
                      </h4>
                    </div>
                    <p class="text-sm text-gray-400">{{ item.description || (item.type === 'goal' ? `Target: ${item.target}` : '') }}</p>
                    <div class="flex items-center space-x-2 mt-1">
                      <span v-if="item.type === 'content'" :class="['text-xs px-2 py-1 rounded', getContentColor()]">
                        {{ getStageLabel(item.status) }}
                      </span>
                      <span v-else-if="item.type === 'goal'" :class="['text-xs px-2 py-1 rounded', getGoalColor()]">
                        {{ Math.round((item.current / item.target) * 100) }}% Complete
                      </span>
                      <span v-else :class="['text-xs px-2 py-1 rounded', getTaskColor()]">
                        {{ formatPriority(item.priority) }}
                      </span>
                      <span v-if="item.type === 'task'" class="text-xs text-gray-400">{{ formatCategory(item.category) }}</span>
                      <span v-if="item.type === 'content'" class="text-xs text-gray-400">
                        Due: {{ getCurrentStageDueDate(item) }}
                      </span>
                      <span v-if="item.type === 'goal'" class="text-xs text-gray-400">
                        Deadline: {{ new Date(item.deadline).toLocaleDateString() }}
                      </span>
                    </div>
                  </div>
                </div>
                <button
                  @click="item.type === 'content' ? openContentModal(item) : item.type === 'goal' ? openGoalModal(item) : editTask(item)"
                  class="text-gray-400 hover:text-white transition-colors p-2"
                >
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/>
                  </svg>
                </button>
              </div>

              <!-- Empty state -->
              <div v-if="getTasksForDate(selectedDate).length === 0" class="text-center py-8">
                <div class="text-gray-400 mb-4">
                  <svg class="h-12 w-12 mx-auto" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <p class="text-gray-400 mb-4">No tasks scheduled for this date</p>
                <button
                  @click="addTaskToSelectedDate"
                  class="rounded-lg bg-orange-500 px-4 py-2 text-sm text-white hover:bg-orange-600"
                >
                  + Add First Task
                </button>
              </div>
            </div>
          </div>

          <!-- Quick Stats -->
          <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
            <h3 class="text-lg font-semibold text-white mb-4">Quick Stats</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="text-gray-400">Total Tasks</span>
                <span class="text-white font-medium">{{ taskStats.total }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-400">Completed</span>
                <span class="text-green-400 font-medium">{{ taskStats.completed }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-400">In Progress</span>
                <span class="text-yellow-400 font-medium">{{ taskStats.inProgress }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-400">Overdue</span>
                <span class="text-red-400 font-medium">{{ taskStats.overdue }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Task Manager View -->
      <div v-if="currentView === 'manager'" class="space-y-6">
        <!-- Filters and Search -->
        <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
          <div class="flex flex-col md:flex-row gap-4 items-center justify-between">
            <div class="flex flex-wrap gap-2">
              <button
                v-for="filter in filters"
                :key="filter.value"
                :class="activeFilter === filter.value ? 'rounded-full bg-orange-500 px-4 py-2 text-sm text-white' : 'rounded-full bg-gray-700 px-4 py-2 text-sm text-gray-300 hover:bg-gray-600'"
                @click="activeFilter = filter.value"
              >
                {{ filter.label }}
              </button>
            </div>
            <div class="flex gap-2">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search tasks..."
                class="rounded-lg bg-gray-700 border-2 border-gray-600/70 shadow-lg px-3 py-2 text-sm text-white placeholder-gray-400 focus:border-orange-500 focus:outline-none"
              />
              <button
                class="rounded-lg bg-orange-500 px-4 py-2 text-sm text-white hover:bg-orange-600"
                @click="showCreateModal = true"
              >
                ➕ Add Task
              </button>
            </div>
          </div>
        </div>

        <!-- Task List -->
        <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
          <div class="space-y-3">
            <div
              v-for="task in filteredTasks"
              :key="task.id"
              :class="getTaskCardClasses(task)"
            >
              <div class="flex items-center space-x-3">
                <input
                  :checked="task.completed"
                  type="checkbox"
                  class="rounded border-gray-600 bg-gray-700 text-orange-500 focus:ring-orange-500"
                  @change="toggleTaskCompletion(task.id)"
                />
                <div class="flex-1">
                  <div class="flex items-center space-x-2">
                    <span class="text-sm" :class="getPriorityIconColor(task.priority)">📋</span>
                    <h4
                      class="font-medium"
                      :class="task.completed ? 'line-through text-gray-500' : 'text-white'"
                    >
                      {{ task.title }}
                    </h4>
                  </div>
                  <p
                    v-if="task.description"
                    class="text-sm mt-1"
                    :class="task.completed ? 'text-gray-500' : 'text-gray-400'"
                  >
                    {{ task.description }}
                  </p>
                  <div class="mt-2 flex items-center space-x-2">
                    <span class="rounded bg-gray-600 px-2 py-1 text-xs text-gray-300">
                      {{ formatCategory(task.category) }}
                    </span>
                    <span
                      class="rounded px-2 py-1 text-xs"
                      :class="getPriorityClass(task.priority)"
                    >
                      {{ formatPriority(task.priority) }}
                    </span>
                    <span class="text-xs text-gray-400">
                      {{ formatDueDate(task.dueDate) }}
                    </span>
                  </div>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <button
                  class="text-gray-400 hover:text-white transition-colors p-2"
                  @click="editTask(task)"
                >
                  ✏️
                </button>
                <button
                  class="text-gray-400 hover:text-red-400 transition-colors p-2"
                  @click="deleteTask(task.id)"
                >
                  🗑️
                </button>
              </div>
            </div>

            <!-- Empty State -->
            <EmptyState
              v-if="filteredTasks.length === 0"
              icon="📝"
              title="No Tasks Found"
              description="Create your first task to get started with organizing your content workflow"
              action-text="Create Task"
              help-text="Tasks help you stay organized and track your content creation progress"
              variant="primary"
              @action="showCreateModal = true"
            />
          </div>
        </div>
      </div>

      <!-- Create Task Modal -->
      <TaskModal
        v-if="showCreateModal || editingTask"
        :task="editingTask"
        @close="closeModal"
        @save="saveTask"
        @delete="handleDeleteTask"
      />




      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useModals } from '../../composables/useModals.js'
import { useAnalyticsStore } from '../../stores/analytics'
import { useTasksStore } from '../../stores/tasks'

// Protect this route with authentication
definePageMeta({
  middleware: 'auth'
})

// Type definitions
type Task = {
  id: string
  title: string
  description: string
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled' | 'on_hold'
  priority: 'low' | 'medium' | 'high' | 'urgent'
  category: 'content' | 'marketing' | 'analytics' | 'seo' | 'monetization' | 'community' | 'planning' | 'research' | 'general'
  dueDate: Date
  createdAt: Date
  updatedAt: Date
  completed: boolean
  userId?: string
  agentId?: string
  tags: string[]
  estimatedTime?: number
  actualTime?: number
}

type TaskCategory = 'content' | 'marketing' | 'analytics' | 'seo' | 'monetization' | 'community' | 'planning' | 'research' | 'general'
type TaskPriority = 'low' | 'medium' | 'high' | 'urgent'
type TaskFilter = 'all' | 'pending' | 'completed' | 'in_progress' | 'high_priority' | 'due_today' | 'overdue'

// Set page title
useHead({
  title: 'Task Management'
})

const tasksStore = useTasksStore()
const analyticsStore = useAnalyticsStore()

// Use modal composable
const { openTask, openGoal, openContent } = useModals()
console.log('🔥 Tasks page - using modal composable')

// Tasks store is now initialized globally via plugin

// Watch for task changes
watch(() => tasksStore.tasks.length, (newLength, oldLength) => {
  console.log('🔥 Tasks page: Task count changed from', oldLength, 'to', newLength)
}, { immediate: true })

// Local state
const currentView = ref<'dashboard' | 'manager'>('dashboard')
const showCreateModal = ref(false)
const editingTask = ref<Task | null>(null)
const activeFilter = ref<TaskFilter>('all')
const searchQuery = ref('')

// Agent notifications state
const suggestionNotifications = ref([
  {
    id: 1,
    type: 'agent_recommendation',
    priority: 'high',
    title: 'Create AI Gaming Tools Video',
    message: 'AI Gaming Tools is trending in your niche - perfect timing for a comprehensive review!',
    description: 'Research and create a video about the latest AI tools for gaming. Include tool reviews, comparisons, and practical demonstrations.',
    category: 'content',
    estimatedTime: '2-3 hours',
    icon: '🔥',
    created_at: new Date().toISOString(),
    is_read: false
  },
  {
    id: 2,
    type: 'optimization_opportunity',
    priority: 'medium',
    title: 'Optimize Recent Thumbnails',
    message: 'Your last 3 videos have lower CTR than usual. Thumbnail refresh could boost performance.',
    description: 'Redesign thumbnails for recent videos focusing on bright colors, clear text, and emotional expressions.',
    category: 'optimization',
    estimatedTime: '1 hour',
    icon: '🎨',
    created_at: new Date(Date.now() - 3600000).toISOString(),
    is_read: false
  },
  {
    id: 3,
    type: 'performance_alert',
    priority: 'medium',
    title: 'Plan Consistency Schedule',
    message: 'You haven\'t uploaded in 5 days. Maintaining regular uploads boosts algorithm performance.',
    description: 'Create and schedule your next 3 videos to maintain audience engagement. Focus on your best-performing content pillars.',
    category: 'planning',
    estimatedTime: '45 min',
    icon: '📅',
    created_at: new Date(Date.now() - 7200000).toISOString(),
    is_read: true
  },
  {
    id: 4,
    type: 'seo_opportunity',
    priority: 'low',
    title: 'Update Video SEO',
    message: 'New trending keywords detected in your niche. Update descriptions to boost discoverability.',
    description: 'Research current trending keywords and update descriptions for your top 5 performing videos to improve search rankings.',
    category: 'seo',
    estimatedTime: '30 min',
    icon: '🔍',
    created_at: new Date(Date.now() - 10800000).toISOString(),
    is_read: false
  }
])

// Agent settings
const { selectedAgent, agentName, allAgents } = useAgentSettings()

// Computed property for selected agent data
const selectedAgentData = computed(() => {
  return {
    ...selectedAgent.value,
    name: agentName.value || selectedAgent.value.name
  }
})

// Agent settings are automatically loaded by the composable

// Filter options
const filters = [
  { label: 'All Tasks', value: 'all' as TaskFilter },
  { label: 'Pending', value: 'pending' as TaskFilter },
  { label: 'In Progress', value: 'in_progress' as TaskFilter },
  { label: 'Completed', value: 'completed' as TaskFilter },
  { label: 'High Priority', value: 'high_priority' as TaskFilter },
  { label: 'Due Today', value: 'due_today' as TaskFilter },
  { label: 'Overdue', value: 'overdue' as TaskFilter },
]

// Computed properties
const taskStats = computed(() => tasksStore.taskStats)
const productivityStats = computed(() => tasksStore.getProductivityStats())

// Filtered tasks based on active filter and search
const filteredTasks = computed(() => {
  let tasks = tasksStore.tasks
  console.log('🔥 Tasks page: Computing filtered tasks, total tasks:', tasks.length)

  // Apply filter
  switch (activeFilter.value) {
    case 'pending':
      tasks = tasks.filter(t => t.status === 'pending')
      break
    case 'in_progress':
      tasks = tasks.filter(t => t.status === 'in_progress')
      break
    case 'completed':
      tasks = tasks.filter(t => t.completed)
      break
    case 'high_priority':
      tasks = tasks.filter(t => t.priority === 'high' || t.priority === 'urgent')
      break
    case 'due_today':
      tasks = tasks.filter(t => isDueToday(t))
      break
    case 'overdue':
      tasks = tasks.filter(t => isOverdue(t))
      break
    default:
      // 'all' - no filter
      break
  }

  // Apply search
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    tasks = tasks.filter(t =>
      t.title.toLowerCase().includes(query) ||
      t.description.toLowerCase().includes(query) ||
      t.category.toLowerCase().includes(query) ||
      t.tags.some(tag => tag.toLowerCase().includes(query))
    )
  }

  return tasks
})

// AI Suggestions - removed, now using only suggestionNotifications for unified insights

// Analytics computed properties
const averageTaskTime = computed(() => {
  const tasks = tasksStore.tasks.filter(t => t.actualTime)
  if (tasks.length === 0) return '0m'
  const avg = tasks.reduce((sum, t) => sum + (t.actualTime || 0), 0) / tasks.length
  return `${Math.round(avg)}m`
})

const tasksThisWeek = computed(() => {
  const weekAgo = new Date()
  weekAgo.setDate(weekAgo.getDate() - 7)
  return tasksStore.tasks.filter(t => new Date(t.createdAt) >= weekAgo).length
})

const productivityScore = computed(() => {
  const stats = productivityStats.value
  const weeklyCompletion = stats.thisWeek.completed
  const weeklyCreated = stats.thisWeek.created
  
  if (weeklyCreated === 0) return 0
  
  const completionRate = (weeklyCompletion / weeklyCreated) * 100
  const activityBonus = Math.min(weeklyCompletion * 2, 20)
  
  return Math.min(Math.round(completionRate + activityBonus), 100)
})

// Methods
const editTask = (task: Task) => {
  console.log('✏️ Tasks Page: editTask called with:', {
    id: task.id,
    title: task.title,
    tags: task.tags,
    isInsightTask: task.tags?.includes('levi-insight'),
    estimatedTime: task.estimatedTime,
    estimatedTimeType: typeof task.estimatedTime
  })
  // Use local modal instead of global modal
  editingTask.value = task
}

const createTaskWithCategory = (category?: TaskCategory) => {
  showCreateModal.value = true
  // Could pre-fill category if provided
}

const closeModal = () => {
  showCreateModal.value = false
  editingTask.value = null
}

const saveTask = (taskData: any) => {
  console.log('🔄 Tasks Page: saveTask called with:', taskData)
  console.log('📝 Tasks Page: editingTask.value:', editingTask.value)

  if (editingTask.value) {
    const updateData = { id: editingTask.value.id, ...taskData }
    console.log('📤 Tasks Page: Calling updateTask with:', updateData)
    tasksStore.updateTask(updateData)
  } else {
    console.log('➕ Tasks Page: Calling addTask with:', taskData)
    tasksStore.addTask(taskData)
  }
  closeModal()
}

const createFromSuggestion = (suggestion: any) => {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  
  tasksStore.addTask({
    title: suggestion.title,
    description: suggestion.description,
    priority: suggestion.priority,
    category: suggestion.category,
    dueDate: tomorrow,
    estimatedTime: suggestion.estimatedTime,
    tags: ['ai-suggested'],
  })
  
  dismissSuggestion(suggestion.id)
}

const dismissSuggestion = (id: string) => {
  const index = aiSuggestions.value.findIndex(s => s.id === id)
  if (index !== -1) {
    aiSuggestions.value.splice(index, 1)
  }
}

// Utility functions
const formatCategory = (category: string) => {
  return category.charAt(0).toUpperCase() + category.slice(1).replace('_', ' ')
}

const formatPriority = (priority: string) => {
  return priority.charAt(0).toUpperCase() + priority.slice(1)
}

const getPriorityClass = (priority: TaskPriority) => {
  switch (priority) {
    case 'urgent': return 'bg-red-500 text-white'
    case 'high': return 'bg-orange-500 text-white'
    case 'medium': return 'bg-yellow-500 text-black'
    case 'low': return 'bg-green-500 text-white'
    default: return 'bg-gray-600 text-white'
  }
}

// Task utility functions
const isOverdue = (task: Task) => {
  return new Date(task.dueDate) < new Date() && !task.completed
}

const isDueToday = (task: Task) => {
  const today = new Date()
  const dueDate = new Date(task.dueDate)
  return (
    dueDate.getDate() === today.getDate() &&
    dueDate.getMonth() === today.getMonth() &&
    dueDate.getFullYear() === today.getFullYear() &&
    !task.completed
  )
}

const formatDueDate = (date: Date) => {
  const now = new Date()
  const dueDate = new Date(date)
  const diffTime = dueDate.getTime() - now.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays < 0) {
    return `${Math.abs(diffDays)}d overdue`
  } else if (diffDays === 0) {
    return 'Due today'
  } else if (diffDays === 1) {
    return 'Due tomorrow'
  } else if (diffDays <= 7) {
    return `Due in ${diffDays}d`
  } else {
    return dueDate.toLocaleDateString()
  }
}

const toggleTaskCompletion = (taskId: string) => {
  const task = tasksStore.tasks.find(t => t.id === taskId)
  if (task) {
    tasksStore.updateTask({
      id: taskId,
      completed: !task.completed,
      status: !task.completed ? 'completed' : 'pending'
    })
  }
}

const deleteTask = (taskId: string) => {
  if (confirm('Are you sure you want to delete this task?')) {
    tasksStore.deleteTask(taskId)
  }
}

const handleDeleteTask = (taskId: string) => {
  console.log('🗑️ Tasks Page: handleDeleteTask called with ID:', taskId)
  tasksStore.deleteTask(taskId)
  closeModal() // Close the modal after deletion
}

// Calendar functionality
const currentDate = ref(new Date())
const selectedDate = ref<Date | null>(null)

const dayHeaders = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

const currentMonthYear = computed(() => {
  return currentDate.value.toLocaleDateString('en-US', {
    month: 'long',
    year: 'numeric'
  })
})

const calendarDays = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()

  // First day of the month
  const firstDay = new Date(year, month, 1)
  // Last day of the month
  const lastDay = new Date(year, month + 1, 0)

  // Start from the first Sunday of the calendar view
  const startDate = new Date(firstDay)
  startDate.setDate(startDate.getDate() - startDate.getDay())

  // End at the last Saturday of the calendar view
  const endDate = new Date(lastDay)
  endDate.setDate(endDate.getDate() + (6 - endDate.getDay()))

  const days = []
  const currentDateObj = new Date(startDate)

  while (currentDateObj <= endDate) {
    const today = new Date()
    days.push({
      date: new Date(currentDateObj),
      isCurrentMonth: currentDateObj.getMonth() === month,
      isToday: currentDateObj.toDateString() === today.toDateString(),
    })
    currentDateObj.setDate(currentDateObj.getDate() + 1)
  }

  return days
})

const previousMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() - 1, 1)
}

const nextMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() + 1, 1)
}

const goToToday = () => {
  currentDate.value = new Date()
  selectedDate.value = new Date()
}

const selectDate = (date: Date) => {
  selectedDate.value = date
}

const addTaskToDate = (date: Date) => {
  selectedDate.value = date
  showCreateModal.value = true
}

const addTaskToSelectedDate = () => {
  if (selectedDate.value) {
    showCreateModal.value = true
  }
}

// Content items data (imported from Content Studio)
const contentItems = ref([
  // Ideas
  {
    id: 1,
    title: 'YouTube Shorts Strategy Guide',
    description: 'Create a comprehensive guide on YouTube Shorts best practices',
    status: 'ideas',
    priority: 'high',
    assignee: 'M',
    createdAt: '2023-12-15',
    dueDate: '2024-01-15',
    stageDueDates: {
      ideas: '2025-08-25',
      planning: '2025-08-28',
      'in-progress': '2025-09-02',
      published: '2025-09-05'
    },
    stageCompletions: {
      ideas: false,
      planning: false,
      'in-progress': false,
      published: false
    },
    pillar: { id: 1, name: 'Marketing', icon: '📈' },
    type: 'content'
  },
  {
    id: 2,
    title: 'AI Content Creation Tools Review',
    description: 'Review and compare top AI tools for content creators',
    status: 'ideas',
    priority: 'medium',
    assignee: 'M',
    createdAt: '2023-12-14',
    dueDate: '2024-01-20',
    stageDueDates: {
      ideas: '2025-08-26',
      planning: '2025-08-29',
      'in-progress': '2025-09-03',
      published: '2025-09-06'
    },
    stageCompletions: {
      ideas: false,
      planning: false,
      'in-progress': false,
      published: false
    },
    pillar: { id: 2, name: 'Technology', icon: '💻' },
    type: 'content'
  },
  // Planning
  {
    id: 4,
    title: 'Content Calendar Template',
    description: 'Design a comprehensive content calendar template',
    status: 'planning',
    priority: 'high',
    assignee: 'M',
    createdAt: '2023-12-12',
    dueDate: '2024-01-10',
    stageDueDates: {
      ideas: '2025-08-20',
      planning: '2025-08-23',
      'in-progress': '2025-08-27',
      published: '2025-08-30'
    },
    stageCompletions: {
      ideas: true,
      planning: false,
      'in-progress': false,
      published: false
    },
    pillar: { id: 3, name: 'Content Strategy', icon: '📝' },
    type: 'content'
  },
  // In Progress
  {
    id: 6,
    title: 'Video Editing Masterclass',
    description: 'Complete tutorial series on advanced video editing',
    status: 'in-progress',
    priority: 'high',
    assignee: 'M',
    progress: 75,
    createdAt: '2023-12-10',
    dueDate: '2024-01-05',
    stageDueDates: {
      ideas: '2025-08-15',
      planning: '2025-08-20',
      'in-progress': '2025-08-24',
      published: '2025-08-28'
    },
    stageCompletions: {
      ideas: true,
      planning: true,
      'in-progress': false,
      published: false
    },
    pillar: { id: 2, name: 'Technology', icon: '💻' },
    type: 'content'
  },
  // Published
  {
    id: 8,
    title: 'TikTok Algorithm Secrets',
    description: 'Deep dive into how TikTok algorithm works in 2024',
    status: 'published',
    priority: 'high',
    assignee: 'M',
    publishDate: 'Dec 8, 2023',
    createdAt: '2023-12-08',
    dueDate: '2023-12-08',
    stageDueDates: {
      ideas: '2025-08-10',
      planning: '2025-08-15',
      'in-progress': '2025-08-20',
      published: '2025-08-22'
    },
    stageCompletions: {
      ideas: true,
      planning: true,
      'in-progress': true,
      published: true
    },
    pillar: { id: 1, name: 'Marketing', icon: '📈' },
    type: 'content'
  }
])

// Function to get the current stage due date for content items
const getCurrentStageDueDate = (item: any) => {
  if (!item.stageDueDates || !item.status) return item.dueDate

  // Find the current stage that should be worked on
  const stageOrder = ['ideas', 'planning', 'in-progress', 'published']
  const currentStageIndex = stageOrder.indexOf(item.status)

  // If current stage is completed, move to next stage
  if (item.stageCompletions && item.stageCompletions[item.status]) {
    const nextStageIndex = currentStageIndex + 1
    if (nextStageIndex < stageOrder.length) {
      const nextStage = stageOrder[nextStageIndex]
      return item.stageDueDates[nextStage] || item.dueDate
    }
  }

  // Return current stage due date
  return item.stageDueDates[item.status] || item.dueDate
}

const getTasksForDate = (date: Date) => {
  // Get regular tasks
  const tasks = tasksStore.tasks.filter(task => {
    const taskDate = new Date(task.dueDate)
    return (
      taskDate.getDate() === date.getDate() &&
      taskDate.getMonth() === date.getMonth() &&
      taskDate.getFullYear() === date.getFullYear()
    )
  }).map(task => ({ ...task, type: 'task' }))

  // Get content items for this date based on their current stage due date
  const contentForDate = contentItems.value.filter(item => {
    const itemDate = new Date(getCurrentStageDueDate(item))
    return (
      itemDate.getDate() === date.getDate() &&
      itemDate.getMonth() === date.getMonth() &&
      itemDate.getFullYear() === date.getFullYear()
    )
  })

  // Get goals for this date based on their deadline
  const goalsForDate = analyticsStore.goals.filter(goal => {
    const goalDate = new Date(goal.deadline)
    return (
      goalDate.getDate() === date.getDate() &&
      goalDate.getMonth() === date.getMonth() &&
      goalDate.getFullYear() === date.getFullYear()
    )
  }).map(goal => ({ ...goal, type: 'goal' }))

  // Debug logging
  if (goalsForDate.length > 0) {
    console.log(`🎯 Found ${goalsForDate.length} goals for ${date.toDateString()}:`, goalsForDate.map(g => g.title))
  }

  // Combine tasks, content items, and goals
  const allItems = [...tasks, ...contentForDate, ...goalsForDate]
  console.log(`📅 Total items for ${date.toDateString()}:`, allItems.length, 'items')
  return allItems
}

// Enhanced calendar item classes with colored borders
const getCalendarItemClasses = (item: any) => {
  const baseClasses = 'text-xs p-2 rounded transition-all duration-300 hover:scale-[1.02] hover:shadow-sm cursor-move'
  const completedClasses = item.completed ? 'opacity-50 line-through' : ''
  const cursorClasses = (item.type === 'task' || !item.type) ? 'cursor-move' : 'cursor-pointer'

  let typeClasses = ''

  if (item.type === 'content') {
    typeClasses = 'bg-purple-900/70 backdrop-blur-sm border-2 border-purple-600/60 text-purple-100 shadow-purple-600/20 shadow-sm'
  } else if (item.type === 'goal') {
    typeClasses = 'bg-cyan-900/70 backdrop-blur-sm border-2 border-cyan-600/60 text-cyan-100 shadow-cyan-600/20 shadow-sm'
  } else {
    // For tasks, use priority-based colors
    switch (item.priority) {
      case 'urgent':
        typeClasses = 'bg-red-900/70 backdrop-blur-sm border-2 border-red-600/60 text-red-100 shadow-red-600/20 shadow-sm'
        break
      case 'high':
        typeClasses = 'bg-orange-900/70 backdrop-blur-sm border-2 border-orange-600/60 text-orange-100 shadow-orange-600/20 shadow-sm'
        break
      case 'medium':
        typeClasses = 'bg-blue-900/70 backdrop-blur-sm border-2 border-blue-600/60 text-blue-100 shadow-blue-600/20 shadow-sm'
        break
      case 'low':
        typeClasses = 'bg-green-900/70 backdrop-blur-sm border-2 border-green-600/60 text-green-100 shadow-green-600/20 shadow-sm'
        break
      default:
        typeClasses = 'bg-gray-700/70 border-2 border-gray-600/70 shadow-lg text-gray-300'
    }
  }

  return `${baseClasses} ${typeClasses} ${completedClasses} ${cursorClasses}`
}

// Content-specific helper functions
const getContentColor = () => {
  return 'bg-blue-500/20 border border-blue-500/40 text-blue-300'
}

const getStageLabel = (status: string) => {
  switch (status) {
    case 'ideas':
      return 'Ideas'
    case 'planning':
      return 'Planning'
    case 'in-progress':
      return 'In Progress'
    case 'published':
      return 'Published'
    default:
      return status
  }
}

const openContentModal = (item: any) => {
  openContent(item)
}

// Goal-specific helper functions
const getGoalColor = () => {
  return 'bg-green-500/20 border border-green-500/40 text-green-300'
}

// Task-specific helper functions
const getTaskColor = () => {
  return 'bg-orange-500/20 border border-orange-500/40 text-orange-300'
}

const openGoalModal = (goal: any) => {
  openGoal(goal)
}

const formatDate = (date: Date) => {
  return date.toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getPriorityColor = (priority: TaskPriority) => {
  switch (priority) {
    case 'urgent': return 'bg-red-500 text-white'
    case 'high': return 'bg-orange-500 text-white'
    case 'medium': return 'bg-yellow-500 text-black'
    case 'low': return 'bg-green-500 text-white'
    default: return 'bg-gray-600 text-white'
  }
}

const addSuggestionAsTask = (suggestion: any) => {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)

  tasksStore.addTask({
    title: suggestion.title,
    description: suggestion.description,
    priority: suggestion.priority,
    category: suggestion.category,
    dueDate: selectedDate.value || tomorrow,
    estimatedTime: suggestion.estimatedTime,
    tags: ['ai-suggested'],
  })

  dismissSuggestion(suggestion.id)
}

// Combined insights functionality
const combinedInsights = computed(() => {
  // Use only suggestionNotifications as unified insights
  const insights = suggestionNotifications.value.map(notification => ({
    ...notification,
    type: 'insight',
    icon: notification.icon || '🔔'
  }))

  return insights.sort((a, b) => {
    // Sort by read status first (unread first)
    if (a.is_read !== b.is_read) {
      return a.is_read ? 1 : -1
    }

    // Then by priority
    const priorityOrder = { high: 0, medium: 1, low: 2 }
    const aPriority = priorityOrder[a.priority] ?? 3
    const bPriority = priorityOrder[b.priority] ?? 3

    if (aPriority !== bPriority) {
      return aPriority - bPriority
    }

    // Finally by date (newest first)
    const aDate = new Date(a.created_at || 0)
    const bDate = new Date(b.created_at || 0)
    return bDate.getTime() - aDate.getTime()
  })
})

const unreadInsightsCount = computed(() => {
  return combinedInsights.value.filter(insight => !insight.is_read).length
})

// Unscheduled tasks - tasks that need to be scheduled into the calendar
const unscheduledTasks = computed(() => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  return filteredTasks.value.filter(task => {
    // Include tasks that:
    // 1. Are not completed
    // 2. Have due dates in the past (overdue) or are pending without proper scheduling
    // 3. Are pending or in progress
    if (task.completed || task.status === 'completed') return false

    const taskDate = new Date(task.dueDate)
    taskDate.setHours(0, 0, 0, 0)

    // Include tasks that are overdue OR pending status (indicating they need proper scheduling)
    return taskDate < today || task.status === 'pending'
  }).slice(0, 10) // Limit to 10 tasks to avoid overwhelming the UI
})

const markInsightAsRead = (insight: any) => {
  if (insight.type === 'notification') {
    insight.is_read = true
  }
  // Suggestions don't need to be marked as read
}

const markAllInsightsAsRead = () => {
  suggestionNotifications.value.forEach(n => n.is_read = true)
}

const addInsightAsTask = (insight: any) => {
  // Set loading state
  insight.isAdding = true

  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)

  // Create task from insight
  const taskData = {
    title: insight.title,
    description: insight.description || insight.message,
    priority: insight.priority,
    category: insight.category || 'content',
    dueDate: selectedDate.value || tomorrow,
    estimatedTime: typeof insight.estimatedTime === 'number' ? insight.estimatedTime : 30, // Convert to minutes
    tags: ['levi-insight'],
  }

  tasksStore.addTask(taskData)

  // Small delay for better UX, then remove insight
  setTimeout(() => {
    dismissInsight(insight)
    console.log(`✅ Added "${insight.title}" as task and removed from insights`)
  }, 300)
}

const dismissInsight = (insight: any) => {
  // Remove insight from suggestionNotifications
  const index = suggestionNotifications.value.findIndex(n => n.id === insight.id)
  if (index > -1) {
    suggestionNotifications.value.splice(index, 1)
    console.log(`🗑️ Removed insight "${insight.title}" from list (index: ${index})`)
  } else {
    console.warn(`⚠️ Could not find insight "${insight.title}" to remove`)
  }
}

// Task scheduling functions
const scheduleTask = (task: any) => {
  // When manually scheduling a task, also update its status to remove from unscheduled list
  tasksStore.updateTask({
    id: task.id,
    status: 'in_progress' // Change from 'pending' to 'in_progress' to remove from unscheduled list
  })

  // Open task modal for editing with focus on due date
  editTask(task)
}

const startDragTask = (task: any, event: DragEvent) => {
  if (event.dataTransfer) {
    event.dataTransfer.setData('application/json', JSON.stringify({
      type: 'task',
      task: task
    }))
    event.dataTransfer.effectAllowed = 'move'
  }
}

const startDragCalendarTask = (item: any, event: DragEvent) => {
  if (event.dataTransfer) {
    event.dataTransfer.setData('application/json', JSON.stringify({
      type: 'calendar-task',
      task: item
    }))
    event.dataTransfer.effectAllowed = 'move'
  }
}

const handleCalendarTaskDragStart = (item: any, event: DragEvent) => {
  console.log('🔥 Drag start for item:', item.type, item.title)
  // Allow dragging for tasks and goals (not content)
  if (item.type === 'task' || item.type === 'goal' || !item.type) {
    console.log('✅ Allowing drag for:', item.type)
    startDragCalendarTask(item, event)
  } else {
    console.log('❌ Preventing drag for:', item.type)
    event.preventDefault()
  }
}

const handleTaskClick = (item: any) => {
  console.log('🔥 Click on item:', item.type, item.title)
  if (item.type === 'content') {
    console.log('📄 Opening content modal')
    openContentModal(item)
  } else if (item.type === 'goal') {
    console.log('🎯 Opening goal modal')
    openGoalModal(item)
  } else {
    console.log('📝 Opening task modal')
    editTask(item)
  }
}

// Drag feedback handlers
const handleDragOver = (event: DragEvent) => {
  event.preventDefault()
  event.dataTransfer!.dropEffect = 'move'
}

const handleDragEnter = (event: DragEvent) => {
  event.preventDefault()
  const target = event.currentTarget as HTMLElement
  target.classList.add('bg-orange-500/20', 'border-orange-500')
}

const handleDragLeave = (event: DragEvent) => {
  const target = event.currentTarget as HTMLElement
  target.classList.remove('bg-orange-500/20', 'border-orange-500')
}

const handleTaskDrop = (date: Date, event: DragEvent) => {
  event.preventDefault()

  // Remove visual feedback
  const target = event.currentTarget as HTMLElement
  target.classList.remove('bg-orange-500/20', 'border-orange-500')

  if (!event.dataTransfer) return

  try {
    const data = JSON.parse(event.dataTransfer.getData('application/json'))

    if ((data.type === 'task' || data.type === 'calendar-task') && data.task) {
      if (data.type === 'task') {
        // From "Tasks to Schedule" - update due date and change status to in_progress
        // This will remove it from the "Tasks to Schedule" list
        tasksStore.updateTask({
          id: data.task.id,
          dueDate: date,
          status: 'in_progress' // Change from 'pending' to 'in_progress' to remove from unscheduled list
        })

        console.log(`📅 Scheduled task "${data.task.title}" to ${date.toDateString()}`)
      } else if (data.type === 'calendar-task') {
        console.log('🔥 Calendar task drop - item type:', data.task.type, 'title:', data.task.title)
        // Check if it's a goal or task
        if (data.task.type === 'goal') {
          // Update goal deadline
          console.log('🎯 Updating goal deadline for:', data.task.id)
          analyticsStore.updateGoal(data.task.id, {
            deadline: date
          })
          console.log(`🎯 Moved goal "${data.task.title}" deadline to ${date.toDateString()}`)
        } else {
          // From calendar - just update the due date (move between calendar days)
          tasksStore.updateTask({
            id: data.task.id,
            dueDate: date
          })
          console.log(`📅 Moved task "${data.task.title}" to ${date.toDateString()}`)
        }
      }
    }
  } catch (error) {
    console.error('Error handling task drop:', error)
  }
}

// Get task card classes based on priority for enhanced borders
const getTaskCardClasses = (task: Task) => {
  const baseClasses = "flex items-center justify-between rounded-lg p-4 transition-all duration-300 hover:scale-[1.01] hover:shadow-lg"

  // Priority-based border colors
  let priorityClasses = ""
  switch (task.priority) {
    case 'urgent':
      priorityClasses = "bg-gray-900/70 backdrop-blur-sm border-2 border-red-600/60 shadow-red-600/20 shadow-sm"
      break
    case 'high':
      priorityClasses = "bg-gray-900/70 backdrop-blur-sm border-2 border-orange-600/60 shadow-orange-600/20 shadow-sm"
      break
    case 'medium':
      priorityClasses = "bg-gray-900/70 backdrop-blur-sm border-2 border-blue-600/60 shadow-blue-600/20 shadow-sm"
      break
    case 'low':
      priorityClasses = "bg-gray-900/70 backdrop-blur-sm border-2 border-green-600/60 shadow-green-600/20 shadow-sm"
      break
    default:
      priorityClasses = "bg-gray-700 border-2 border-gray-600/70 shadow-lg"
  }

  // Add left border for due dates (keeping existing functionality)
  let dueDateClasses = ""
  if (isOverdue(task)) {
    dueDateClasses = "border-l-4 border-red-500"
  } else if (isDueToday(task)) {
    dueDateClasses = "border-l-4 border-yellow-500"
  }

  return `${baseClasses} ${priorityClasses} ${dueDateClasses}`
}

// Get priority icon color to match border colors
const getPriorityIconColor = (priority: TaskPriority) => {
  switch (priority) {
    case 'urgent':
      return 'text-red-300'
    case 'high':
      return 'text-orange-300'
    case 'medium':
      return 'text-blue-300'
    case 'low':
      return 'text-green-300'
    default:
      return 'text-gray-300'
  }
}

const formatNotificationTime = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = now.getTime() - date.getTime()
  const diffHours = Math.floor(diffTime / (1000 * 60 * 60))
  const diffMinutes = Math.floor(diffTime / (1000 * 60))

  if (diffMinutes < 60) {
    return `${diffMinutes}m ago`
  } else if (diffHours < 24) {
    return `${diffHours}h ago`
  } else {
    return date.toLocaleDateString()
  }
}
</script>

<style scoped>
.transition-colors {
  transition: background-color 0.2s ease-in-out;
}
</style>
