<template>
  <div class="min-h-screen bg-forest-900 text-white">

    <!-- Main Content Area -->
    <div class="p-6 pt-24">
      <!-- Header -->
      <div class="mb-4 flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <h1 class="text-2xl font-bold text-white">Content Studio</h1>
          <span class="text-gray-400">•</span>
          <p class="text-gray-400">Manage your content workflow from idea to publication</p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="relative">
            <input
              type="text"
              placeholder="Search content..."
              class="w-64 rounded-lg bg-forest-800 px-4 py-2 pl-10 text-white focus:outline-none focus:ring-2 focus:ring-orange-500"
            />
            <svg
              class="absolute left-3 top-2.5 h-5 w-5 text-gray-400"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
          <button
            class="flex items-center space-x-2 rounded-lg bg-orange-500 px-4 py-2 text-white transition-colors hover:bg-orange-600"
            @click="openCreateModal"
          >
            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                clip-rule="evenodd"
              />
            </svg>
            <span>New Content</span>
          </button>
        </div>
      </div>



      <!-- Kanban Board -->
      <div class="rounded-xl bg-forest-800 p-6">
        <div class="grid grid-cols-4 gap-4 pb-6">
          <!-- Ideas Column -->
          <div class="flex flex-col bg-forest-800/30 rounded-lg p-4 border border-forest-600/20">
            <div class="flex items-center justify-between -m-4 mb-4 p-4 bg-forest-700/50 rounded-t-lg">
              <div class="flex items-center space-x-2">
                <div class="h-3 w-3 rounded-full bg-orange-500"/>
                <h3 class="font-semibold text-white">Ideas</h3>
                <span class="rounded-full bg-forest-700 px-2 py-1 text-xs text-gray-300">{{
                  getColumnCount('ideas')
                }}</span>
              </div>
              <button class="text-gray-400 hover:text-white">
                <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </div>
            <div
              class="flex-1 space-y-3 min-h-[200px]"
              @dragover="onDragOver"
              @drop="onDrop($event, 'ideas')"
            >
              <div
                v-for="item in getColumnItems('ideas')"
                :key="item.id"
                class="cursor-pointer rounded-lg bg-forest-700 p-4 transition-all duration-300 hover:bg-forest-600 hover:scale-[1.02] hover:shadow-lg w-full relative"
                draggable="true"
                @dragstart="onDragStart($event, item)"
                @click="openEditModal(item)"
              >
                <div class="mb-2 flex items-start justify-between">
                  <h4 class="text-sm font-medium text-white">{{ item.title }}</h4>
                  <div class="relative">
                    <button
                      @click.stop="toggleDropdown(item.id)"
                      class="text-gray-400 hover:text-white"
                    >
                      <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                        <path
                          d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"
                        />
                      </svg>
                    </button>
                    <!-- Dropdown Menu -->
                    <div
                      v-if="showDropdownMenu === item.id"
                      class="absolute right-0 top-6 z-50 w-32 rounded-md bg-forest-600 shadow-lg border border-forest-500"
                    >
                      <button
                        @click.stop="openEditModal(item)"
                        class="block w-full px-3 py-2 text-left text-sm text-gray-300 hover:bg-forest-500 hover:text-white rounded-t-md transition-colors duration-150"
                      >
                        Edit
                      </button>
                      <button
                        @click.stop="openDeleteModal(item)"
                        class="block w-full px-3 py-2 text-left text-sm text-red-400 hover:bg-forest-500 hover:text-red-300 rounded-b-md transition-colors duration-150"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                </div>
                <p class="mb-3 text-xs text-gray-300">{{ item.description }}</p>
                <!-- Pillar Badge -->
                <div v-if="item.pillar" class="mb-3">
                  <span class="inline-flex items-center space-x-1 rounded-full bg-forest-600 px-2 py-1 text-xs text-gray-300">
                    <span>{{ item.pillar.icon }}</span>
                    <span>{{ item.pillar.name }}</span>
                  </span>
                </div>
                <!-- Stage Due Date / Completion Status -->
                <div v-if="item.stageDueDates && item.stageDueDates[item.status]" class="mb-3">
                  <div v-if="item.stageCompletions && item.stageCompletions[item.status]" class="flex items-center space-x-1 text-xs text-green-400">
                    <svg class="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                    <span>Completed</span>
                  </div>
                  <div v-else class="flex items-center space-x-1 text-xs text-gray-400">
                    <svg class="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
                    </svg>
                    <span>Due: {{ item.stageDueDates[item.status] }}</span>
                  </div>
                </div>
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <span
                      :class="
                        item.priority === 'high'
                          ? 'bg-red-500'
                          : item.priority === 'medium'
                            ? 'bg-yellow-500'
                            : 'bg-green-500'
                      "
                      class="h-2 w-2 rounded-full"
                    />
                    <span class="text-xs text-gray-400">{{ item.priority }}</span>
                  </div>
                  <div class="flex items-center space-x-1">
                    <div class="flex h-6 w-6 items-center justify-center rounded-full bg-orange-500">
                      <span class="text-xs text-white">{{ item.assignee }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Planning Column -->
          <div class="flex flex-col bg-forest-800/30 rounded-lg p-4 border border-forest-600/20">
            <div class="flex items-center justify-between -m-4 mb-4 p-4 bg-forest-700/50 rounded-t-lg">
              <div class="flex items-center space-x-2">
                <div class="h-3 w-3 rounded-full bg-orange-500"/>
                <h3 class="font-semibold text-white">Planning</h3>
                <span class="rounded-full bg-forest-700 px-2 py-1 text-xs text-gray-300">{{
                  getColumnCount('planning')
                }}</span>
              </div>
              <button class="text-gray-400 hover:text-white">
                <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </div>
            <div
              class="flex-1 space-y-3 min-h-[200px]"
              @dragover="onDragOver"
              @drop="onDrop($event, 'planning')"
            >
              <div
                v-for="item in getColumnItems('planning')"
                :key="item.id"
                class="cursor-pointer rounded-lg bg-forest-700 p-4 transition-all duration-300 hover:bg-forest-600 hover:scale-[1.02] hover:shadow-lg w-full relative"
                draggable="true"
                @dragstart="onDragStart($event, item)"
                @click="openEditModal(item)"
              >
                <div class="mb-2 flex items-start justify-between">
                  <h4 class="text-sm font-medium text-white">{{ item.title }}</h4>
                  <div class="relative">
                    <button
                      @click.stop="toggleDropdown(item.id)"
                      class="text-gray-400 hover:text-white"
                    >
                      <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"
                      />
                    </svg>
                  </button>
                  <!-- Dropdown Menu -->
                  <div
                    v-if="showDropdownMenu === item.id"
                    class="absolute right-0 top-6 z-50 w-32 rounded-md bg-forest-600 shadow-lg border border-forest-500"
                  >
                    <button
                      @click.stop="openEditModal(item)"
                      class="block w-full px-3 py-2 text-left text-sm text-gray-300 hover:bg-forest-500 hover:text-white rounded-t-md transition-colors duration-150"
                    >
                      Edit
                    </button>
                    <button
                      @click.stop="openDeleteModal(item)"
                      class="block w-full px-3 py-2 text-left text-sm text-red-400 hover:bg-forest-500 hover:text-red-300 rounded-b-md transition-colors duration-150"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
                <p class="mb-3 text-xs text-gray-300">{{ item.description }}</p>
                <!-- Pillar Badge -->
                <div v-if="item.pillar" class="mb-3">
                  <span class="inline-flex items-center space-x-1 rounded-full bg-forest-600 px-2 py-1 text-xs text-gray-300">
                    <span>{{ item.pillar.icon }}</span>
                    <span>{{ item.pillar.name }}</span>
                  </span>
                </div>
                <!-- Stage Due Date / Completion Status -->
                <div v-if="item.stageDueDates && item.stageDueDates[item.status]" class="mb-3">
                  <div v-if="item.stageCompletions && item.stageCompletions[item.status]" class="flex items-center space-x-1 text-xs text-green-400">
                    <svg class="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                    <span>Completed</span>
                  </div>
                  <div v-else class="flex items-center space-x-1 text-xs text-gray-400">
                    <svg class="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
                    </svg>
                    <span>Due: {{ item.stageDueDates[item.status] }}</span>
                  </div>
                </div>
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <span
                      :class="
                        item.priority === 'high'
                          ? 'bg-red-500'
                          : item.priority === 'medium'
                            ? 'bg-yellow-500'
                            : 'bg-green-500'
                      "
                      class="h-2 w-2 rounded-full"
                    />
                    <span class="text-xs text-gray-400">{{ item.priority }}</span>
                  </div>
                  <div class="flex items-center space-x-1">
                    <div class="flex h-6 w-6 items-center justify-center rounded-full bg-orange-500">
                      <span class="text-xs text-white">{{ item.assignee }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- In Progress Column -->
          <div class="flex flex-col bg-forest-800/30 rounded-lg p-4 border border-forest-600/20">
            <div class="flex items-center justify-between -m-4 mb-4 p-4 bg-forest-700/50 rounded-t-lg">
              <div class="flex items-center space-x-2">
                <div class="h-3 w-3 rounded-full bg-orange-500"/>
                <h3 class="font-semibold text-white">In Progress</h3>
                <span class="rounded-full bg-forest-700 px-2 py-1 text-xs text-gray-300">{{
                  getColumnCount('in-progress')
                }}</span>
              </div>
              <button class="text-gray-400 hover:text-white">
                <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </div>
            <div
              class="flex-1 space-y-3 min-h-[200px]"
              @dragover="onDragOver"
              @drop="onDrop($event, 'in-progress')"
            >
              <div
                v-for="item in getColumnItems('in-progress')"
                :key="item.id"
                class="cursor-pointer rounded-lg bg-forest-700 p-4 transition-all duration-300 hover:bg-forest-600 hover:scale-[1.02] hover:shadow-lg w-full relative"
                draggable="true"
                @dragstart="onDragStart($event, item)"
                @click="openEditModal(item)"
              >
                <div class="mb-2 flex items-start justify-between">
                  <h4 class="text-sm font-medium text-white">{{ item.title }}</h4>
                  <div class="relative">
                    <button
                      @click.stop="toggleDropdown(item.id)"
                      class="text-gray-400 hover:text-white"
                    >
                      <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                        <path
                          d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"
                        />
                      </svg>
                    </button>
                    <!-- Dropdown Menu -->
                    <div
                      v-if="showDropdownMenu === item.id"
                      class="absolute right-0 top-6 z-50 w-32 rounded-md bg-forest-600 shadow-lg border border-forest-500"
                    >
                      <button
                        @click.stop="openEditModal(item)"
                        class="block w-full px-3 py-2 text-left text-sm text-gray-300 hover:bg-forest-500 hover:text-white rounded-t-md transition-colors duration-150"
                      >
                        Edit
                      </button>
                      <button
                        @click.stop="openDeleteModal(item)"
                        class="block w-full px-3 py-2 text-left text-sm text-red-400 hover:bg-forest-500 hover:text-red-300 rounded-b-md transition-colors duration-150"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                </div>
                <p class="mb-3 text-xs text-gray-300">{{ item.description }}</p>
                <!-- Pillar Badge -->
                <div v-if="item.pillar" class="mb-3">
                  <span class="inline-flex items-center space-x-1 rounded-full bg-forest-600 px-2 py-1 text-xs text-gray-300">
                    <span>{{ item.pillar.icon }}</span>
                    <span>{{ item.pillar.name }}</span>
                  </span>
                </div>
                <!-- Stage Due Date / Completion Status -->
                <div v-if="item.stageDueDates && item.stageDueDates[item.status]" class="mb-3">
                  <div v-if="item.stageCompletions && item.stageCompletions[item.status]" class="flex items-center space-x-1 text-xs text-green-400">
                    <svg class="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                    <span>Completed</span>
                  </div>
                  <div v-else class="flex items-center space-x-1 text-xs text-gray-400">
                    <svg class="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
                    </svg>
                    <span>Due: {{ item.stageDueDates[item.status] }}</span>
                  </div>
                </div>
                <div class="mb-2 flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <span
                      :class="
                        item.priority === 'high'
                          ? 'bg-red-500'
                          : item.priority === 'medium'
                            ? 'bg-yellow-500'
                            : 'bg-green-500'
                      "
                      class="h-2 w-2 rounded-full"
                    />
                    <span class="text-xs text-gray-400">{{ item.priority }}</span>
                  </div>
                  <div class="flex items-center space-x-1">
                    <div class="flex h-6 w-6 items-center justify-center rounded-full bg-orange-500">
                      <span class="text-xs text-white">{{ item.assignee }}</span>
                    </div>
                  </div>
                </div>
                <div v-if="item.progress" class="h-2 w-full rounded-full bg-forest-600">
                  <div
                    class="h-2 rounded-full bg-orange-500"
                    :style="`width: ${item.progress}%`"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Published Column -->
          <div class="flex flex-col bg-forest-800/30 rounded-lg p-4 border border-forest-600/20">
            <div class="flex items-center justify-between -m-4 mb-4 p-4 bg-forest-700/50 rounded-t-lg">
              <div class="flex items-center space-x-2">
                <div class="h-3 w-3 rounded-full bg-green-500"/>
                <h3 class="font-semibold text-white">Published</h3>
                <span class="rounded-full bg-forest-700 px-2 py-1 text-xs text-gray-300">{{
                  getColumnCount('published')
                }}</span>
              </div>
              <button class="text-gray-400 hover:text-white">
                <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </div>
            <div
              class="flex-1 space-y-3 min-h-[200px]"
              @dragover="onDragOver"
              @drop="onDrop($event, 'published')"
            >
              <div
                v-for="item in getColumnItems('published')"
                :key="item.id"
                class="cursor-pointer rounded-lg bg-forest-700 p-4 transition-all duration-300 hover:bg-forest-600 hover:scale-[1.02] hover:shadow-lg w-full relative"
                draggable="true"
                @dragstart="onDragStart($event, item)"
                @click="openEditModal(item)"
              >
                <div class="mb-2 flex items-start justify-between">
                  <h4 class="text-sm font-medium text-white">{{ item.title }}</h4>
                  <div class="relative">
                    <button
                      @click.stop="toggleDropdown(item.id)"
                      class="text-gray-400 hover:text-white"
                    >
                      <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                        <path
                          d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"
                        />
                      </svg>
                    </button>
                    <!-- Dropdown Menu -->
                    <div
                      v-if="showDropdownMenu === item.id"
                      class="absolute right-0 top-6 z-50 w-32 rounded-md bg-forest-600 shadow-lg border border-forest-500"
                    >
                      <button
                        @click.stop="openEditModal(item)"
                        class="block w-full px-3 py-2 text-left text-sm text-gray-300 hover:bg-forest-500 hover:text-white rounded-t-md transition-colors duration-150"
                      >
                        Edit
                      </button>
                      <button
                        @click.stop="openDeleteModal(item)"
                        class="block w-full px-3 py-2 text-left text-sm text-red-400 hover:bg-forest-500 hover:text-red-300 rounded-b-md transition-colors duration-150"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                </div>
                <p class="mb-3 text-xs text-gray-300">{{ item.description }}</p>
                <!-- Pillar Badge -->
                <div v-if="item.pillar" class="mb-3">
                  <span class="inline-flex items-center space-x-1 rounded-full bg-forest-600 px-2 py-1 text-xs text-gray-300">
                    <span>{{ item.pillar.icon }}</span>
                    <span>{{ item.pillar.name }}</span>
                  </span>
                </div>
                <!-- Stage Due Date / Completion Status -->
                <div v-if="item.stageDueDates && item.stageDueDates[item.status]" class="mb-3">
                  <div v-if="item.stageCompletions && item.stageCompletions[item.status]" class="flex items-center space-x-1 text-xs text-green-400">
                    <svg class="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                    <span>Completed</span>
                  </div>
                  <div v-else class="flex items-center space-x-1 text-xs text-gray-400">
                    <svg class="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
                    </svg>
                    <span>Due: {{ item.stageDueDates[item.status] }}</span>
                  </div>
                </div>
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <span class="h-2 w-2 rounded-full bg-green-500"/>
                    <span class="text-xs text-gray-400">Published</span>
                  </div>
                  <div class="flex items-center space-x-1">
                    <div class="flex h-6 w-6 items-center justify-center rounded-full bg-orange-500">
                      <span class="text-xs text-white">{{ item.assignee }}</span>
                    </div>
                    <span class="text-xs text-green-400">{{ item.publishDate || 'Live' }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>


        </div>
      </div>



      <!-- Agent Content Suggestions -->
      <div class="mt-6 rounded-xl bg-forest-800 p-6">
        <div class="mb-6 flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg overflow-hidden bg-purple-600/20">
              <img
                v-if="selectedAgent.image"
                :src="selectedAgent.image"
                :alt="selectedAgent.name"
                class="h-full w-full object-cover"
              />
              <svg v-else class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-white">{{ agentName || selectedAgent.name }} Content Suggestions</h3>
              <p class="text-sm text-gray-400">Personalized recommendations to boost your content strategy</p>
            </div>
          </div>
          <button class="flex items-center space-x-2 rounded-lg bg-forest-700 px-4 py-2 text-sm text-white hover:bg-forest-600 transition-colors">
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"/>
            </svg>
            <span>Refresh</span>
          </button>
        </div>

        <!-- Performance Predictions Widget -->
        <div class="rounded-lg bg-forest-700/50 p-6 border border-forest-600/20">
          <!-- Header -->
          <div class="flex items-center justify-between mb-6">
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-purple-100 rounded-lg">
                <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                </svg>
              </div>
              <div>
                <h4 class="text-lg font-semibold text-white">Performance Predictions</h4>
                <p class="text-sm text-gray-400">AI-powered forecasts for your content</p>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <div class="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded">
                {{ confidenceLevel }}% Confidence
              </div>
            </div>
          </div>

          <!-- Prediction Cards -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <!-- Next Video Prediction -->
            <div class="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-4 border border-blue-200">
              <div class="flex items-center justify-between mb-3">
                <h5 class="font-medium text-blue-900">Next Video Forecast</h5>
                <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                </svg>
              </div>
              <div class="space-y-2">
                <div class="flex justify-between">
                  <span class="text-sm text-blue-700">Expected Views:</span>
                  <span class="font-semibold text-blue-900">{{ formatNumber(nextVideoViews.min) }} - {{ formatNumber(nextVideoViews.max) }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-blue-700">Engagement Rate:</span>
                  <span class="font-semibold text-blue-900">{{ nextVideoEngagement }}%</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-blue-700">Best Upload Time:</span>
                  <span class="font-semibold text-blue-900">{{ bestUploadTime }}</span>
                </div>
              </div>
            </div>

            <!-- Growth Milestone -->
            <div class="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-4 border border-green-200">
              <div class="flex items-center justify-between mb-3">
                <h5 class="font-medium text-green-900">Growth Milestone</h5>
                <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
                </svg>
              </div>
              <div class="space-y-2">
                <div class="flex justify-between">
                  <span class="text-sm text-green-700">Next Milestone:</span>
                  <span class="font-semibold text-green-900">{{ formatNumber(nextMilestone.target) }} subs</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-green-700">Estimated Date:</span>
                  <span class="font-semibold text-green-900">{{ nextMilestone.date }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-green-700">Progress:</span>
                  <span class="font-semibold text-green-900">{{ nextMilestone.progress }}%</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Trend Analysis -->
          <div class="bg-forest-600 rounded-lg p-4 mb-4">
            <h5 class="font-medium text-white mb-3">30-Day Trend Analysis</h5>
            <div class="grid grid-cols-3 gap-4">
              <div class="text-center">
                <div class="text-2xl font-bold text-blue-400">{{ trendAnalysis.views.change }}%</div>
                <div class="text-sm text-gray-300">Views Change</div>
                <div class="flex items-center justify-center mt-1">
                  <svg v-if="trendAnalysis.views.change > 0" class="w-4 h-4 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                  </svg>
                  <svg v-else class="w-4 h-4 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                </div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-green-400">{{ trendAnalysis.engagement.change }}%</div>
                <div class="text-sm text-gray-300">Engagement</div>
                <div class="flex items-center justify-center mt-1">
                  <svg v-if="trendAnalysis.engagement.change > 0" class="w-4 h-4 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                  </svg>
                  <svg v-else class="w-4 h-4 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                </div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-purple-400">{{ trendAnalysis.subscribers.change }}%</div>
                <div class="text-sm text-gray-300">Subscribers</div>
                <div class="flex items-center justify-center mt-1">
                  <svg v-if="trendAnalysis.subscribers.change > 0" class="w-4 h-4 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                  </svg>
                  <svg v-else class="w-4 h-4 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                </div>
              </div>
            </div>
          </div>

          <!-- AI Recommendations -->
          <div class="border-t border-forest-600 pt-4">
            <h5 class="font-medium text-white mb-3">🤖 AI Recommendations</h5>
            <div class="space-y-2">
              <div
                v-for="recommendation in aiRecommendations"
                :key="recommendation.id"
                class="flex items-start space-x-3 p-3 bg-forest-600 rounded-lg border border-forest-500"
              >
                <div class="text-lg">{{ recommendation.icon }}</div>
                <div class="flex-1">
                  <div class="font-medium text-white">{{ recommendation.title }}</div>
                  <div class="text-sm text-gray-300">{{ recommendation.description }}</div>
                </div>
                <button
                  @click="applyRecommendation(recommendation)"
                  class="px-3 py-1 bg-orange-500 text-white text-xs rounded hover:bg-orange-600 transition-colors"
                >
                  Apply
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="mt-6 flex flex-wrap gap-3">
          <button class="flex items-center space-x-2 rounded-lg bg-orange-500 px-4 py-2 text-sm text-white hover:bg-orange-600 transition-colors">
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"/>
            </svg>
            <span>Add to Ideas</span>
          </button>
          <button class="flex items-center space-x-2 rounded-lg bg-forest-700 px-4 py-2 text-sm text-white hover:bg-forest-600 transition-colors">
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/>
            </svg>
            <span>Customize Suggestions</span>
          </button>
          <button class="flex items-center space-x-2 rounded-lg bg-forest-700 px-4 py-2 text-sm text-white hover:bg-forest-600 transition-colors">
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"/>
            </svg>
            <span>View Analytics</span>
          </button>
        </div>
      </div>
    </div>







    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirmModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-forest-800 rounded-xl p-6 w-full max-w-md mx-4">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-white">Delete Content</h3>
          <button @click="showDeleteConfirmModal = false" class="text-gray-400 hover:text-white">
            <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>

        <div class="mb-6">
          <p class="text-gray-300">
            Are you sure you want to delete "<span class="font-semibold text-white">{{ selectedContentItem?.title }}</span>"?
          </p>
          <p class="text-sm text-gray-400 mt-2">This action cannot be undone.</p>
        </div>

        <div class="flex items-center justify-end space-x-3">
          <button
            @click="showDeleteConfirmModal = false"
            class="px-4 py-2 text-gray-400 hover:text-white transition-colors"
          >
            Cancel
          </button>
          <button
            @click="deleteContent"
            class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
          >
            Delete
          </button>
        </div>
      </div>
    </div>

    <!-- Click outside to close dropdown -->
    <div v-if="showDropdownMenu" @click="closeDropdown" class="fixed inset-0 z-0"></div>
  </div>
</template>

<script setup>
import { nextTick, onMounted, onUnmounted, ref } from 'vue'

import { useAgentSettings } from '../../composables/useAgentSettings'
import { useModals } from '../../composables/useModals.js'
import { usePillars } from '../../composables/usePillars.js'

// Protect this route with authentication
definePageMeta({
  middleware: 'auth'
})

// Agent settings
const { selectedAgent, agentName } = useAgentSettings()

// Use modal composable
const { openContent, openTask } = useModals()

// Listen for content updates from the modal system
const handleContentUpdate = (event) => {
  const updatedContent = event.detail
  console.log('🔥 Content update event received:', updatedContent)

  if (updatedContent.id) {
    // Update existing content
    const itemIndex = contentItems.value.findIndex(item => item.id === updatedContent.id)
    if (itemIndex !== -1) {
      // Create a completely new object to ensure Vue reactivity
      const updatedItem = {
        ...contentItems.value[itemIndex],
        ...updatedContent
      }

      // Use array splice to ensure reactivity
      contentItems.value.splice(itemIndex, 1, updatedItem)

      // Save to localStorage to persist changes
      saveContentItems(contentItems.value)

      console.log('🔥 Content updated in kanban:', updatedItem)
      console.log('🔥 New status:', updatedItem.status)
      console.log('🔥 Items in new status column:', contentItems.value.filter(item => item.status === updatedItem.status).length)

      // Force reactivity update using nextTick
      nextTick(() => {
        console.log('🔥 After nextTick - Items in status columns:')
        console.log('Ideas:', contentItems.value.filter(item => item.status === 'ideas').length)
        console.log('Planning:', contentItems.value.filter(item => item.status === 'planning').length)
        console.log('In Progress:', contentItems.value.filter(item => item.status === 'in-progress').length)
        console.log('Published:', contentItems.value.filter(item => item.status === 'published').length)
      })
    }
  } else {
    // Add new content
    const newItem = {
      id: Date.now(),
      ...updatedContent,
      createdAt: new Date().toISOString()
    }
    contentItems.value.push(newItem)

    // Save to localStorage to persist changes
    saveContentItems(contentItems.value)

    console.log('🔥 New content added to kanban:', newItem)
  }
}

// Setup event listeners for content updates and load from localStorage
onMounted(() => {
  if (typeof window !== 'undefined') {
    // Load content items from localStorage after hydration is complete
    const savedItems = loadContentItemsFromStorage()
    if (savedItems) {
      contentItems.value = savedItems
      console.log('🔥 Content items loaded from localStorage after hydration')
    } else {
      console.log('🔥 Using default content items (no localStorage data found)')
    }

    // Setup event listener for content updates
    window.addEventListener('contentUpdated', handleContentUpdate)
    console.log('🔥 Content update event listener added')
  }
})

onUnmounted(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('contentUpdated', handleContentUpdate)
    console.log('🔥 Content update event listener removed')
  }
})

// Get pillars from the main pillars composable
const { pillars } = usePillars()

// Open create modal using global system
const openCreateModal = () => {
  console.log('🔥 Opening create content modal')
  openContent(null) // null means create new content
}

// Open edit modal using global system
const openEditModal = (content) => {
  console.log('🔥 Opening edit content modal with data:', content)
  console.log('🔥 openContent function:', openContent)

  try {
    openContent(content)
    console.log('🔥 openContent called successfully')
  } catch (error) {
    console.error('🔥 Error calling openContent:', error)
  }

  // Close dropdown if open
  showDropdownMenu.value = null
}

// Modal states
const showDeleteConfirmModal = ref(false)
const selectedContentItem = ref(null)
const showDropdownMenu = ref(null)

// New content form data
const newContent = ref({
  title: '',
  description: '',
  pillarId: '',
  priority: 'medium',
  dueDate: '', // Overall completion date
  status: 'ideas',
  stageDueDates: {
    ideas: '',
    planning: '',
    'in-progress': '',
    published: ''
  },
  stageCompletions: {
    ideas: false,
    planning: false,
    'in-progress': false,
    published: false
  }
})

// Edit content form data
const editContent = ref({
  title: '',
  description: '',
  pillarId: '',
  priority: 'medium',
  dueDate: '', // Overall completion date
  status: 'ideas',
  stageDueDates: {
    ideas: '',
    planning: '',
    'in-progress': '',
    published: ''
  },
  stageCompletions: {
    ideas: false,
    planning: false,
    'in-progress': false,
    published: false
  }
})

// Available workflow stages
const workflowStages = ref([
  { value: 'ideas', label: 'Ideas', description: 'Initial content concepts' },
  { value: 'planning', label: 'Planning', description: 'Content being planned and structured' },
  { value: 'in-progress', label: 'In Progress', description: 'Content currently being created' },
  { value: 'published', label: 'Published', description: 'Content that has been published' }
])

// Auto-complete previous stages when status changes
const autoCompletePreviousStages = (currentStatus, stageCompletions) => {
  const stageOrder = ['ideas', 'planning', 'in-progress', 'published']
  const currentIndex = stageOrder.indexOf(currentStatus)

  // Mark all previous stages as completed
  for (let i = 0; i < currentIndex; i++) {
    stageCompletions[stageOrder[i]] = true
  }

  return stageCompletions
}

// Watch for status changes to auto-complete previous stages
watch(() => newContent.value.status, (newStatus) => {
  newContent.value.stageCompletions = autoCompletePreviousStages(newStatus, { ...newContent.value.stageCompletions })
})

watch(() => editContent.value.status, (newStatus) => {
  editContent.value.stageCompletions = autoCompletePreviousStages(newStatus, { ...editContent.value.stageCompletions })
})

// Transform pillars for the dropdown (use actual pillars from pillars page)
const availablePillars = computed(() => {
  return pillars.value.map(pillar => ({
    id: pillar.id,
    name: pillar.name,
    icon: getIconEmoji(pillar.icon) // Convert icon name to emoji
  }))
})

// Helper function to convert icon names to emojis
const getIconEmoji = (iconName) => {
  const iconMap = {
    'GameIcon': '🎮',
    'ReviewIcon': '⭐',
    'TechIcon': '💻',
    'ProductivityIcon': '⏰'
  }
  return iconMap[iconName] || '📝'
}

// Default content items data
const defaultContentItems = [
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
      ideas: '2024-01-05',
      planning: '2024-01-08',
      'in-progress': '2024-01-12',
      published: '2024-01-15'
    },
    stageCompletions: {
      ideas: false,
      planning: false,
      'in-progress': false,
      published: false
    },
    pillar: { id: 1, name: 'Marketing', icon: '📈' }
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
      ideas: '2024-01-08',
      planning: '2024-01-12',
      'in-progress': '2024-01-17',
      published: '2024-01-20'
    },
    pillar: { id: 2, name: 'Technology', icon: '💻' }
  },
  {
    id: 3,
    title: 'Social Media Trends 2024',
    description: 'Analyze upcoming social media trends for next year',
    status: 'ideas',
    priority: 'low',
    assignee: 'M',
    createdAt: '2023-12-13',
    dueDate: '2024-02-01',
    stageDueDates: {
      ideas: '2024-01-15',
      planning: '2024-01-20',
      'in-progress': '2024-01-28',
      published: '2024-02-01'
    },
    pillar: { id: 1, name: 'Marketing', icon: '📈' }
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
      ideas: '2023-12-20',
      planning: '2024-01-03',
      'in-progress': '2024-01-08',
      published: '2024-01-10'
    },
    stageCompletions: {
      ideas: true,
      planning: false,
      'in-progress': false,
      published: false
    },
    pillar: { id: 3, name: 'Content Strategy', icon: '📝' }
  },
  {
    id: 5,
    title: 'Brand Voice Guidelines',
    description: 'Establish consistent brand voice across all platforms',
    status: 'planning',
    priority: 'medium',
    assignee: 'M',
    createdAt: '2023-12-11',
    dueDate: '2024-01-25',
    stageDueDates: {
      ideas: '2023-12-25',
      planning: '2024-01-10',
      'in-progress': '2024-01-20',
      published: '2024-01-25'
    },
    pillar: { id: 4, name: 'Branding', icon: '🎨' }
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
      ideas: '2023-12-15',
      planning: '2023-12-20',
      'in-progress': '2024-01-03',
      published: '2024-01-05'
    },
    stageCompletions: {
      ideas: true,
      planning: true,
      'in-progress': false,
      published: false
    },
    pillar: { id: 2, name: 'Technology', icon: '💻' }
  },
  {
    id: 7,
    title: 'Instagram Growth Hacks',
    description: 'Proven strategies to grow Instagram following organically',
    status: 'in-progress',
    priority: 'medium',
    assignee: 'M',
    progress: 45,
    createdAt: '2023-12-09',
    dueDate: '2024-01-18',
    stageDueDates: {
      ideas: '2023-12-20',
      planning: '2023-12-28',
      'in-progress': '2024-01-15',
      published: '2024-01-18'
    },
    pillar: { id: 1, name: 'Marketing', icon: '📈' }
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
      ideas: '2023-11-20',
      planning: '2023-11-28',
      'in-progress': '2023-12-05',
      published: '2023-12-08'
    },
    stageCompletions: {
      ideas: true,
      planning: true,
      'in-progress': true,
      published: true
    },
    pillar: { id: 1, name: 'Marketing', icon: '📈' }
  },
  {
    id: 9,
    title: 'Content Monetization Guide',
    description: 'Complete guide to monetizing your content across platforms',
    status: 'published',
    priority: 'medium',
    assignee: 'M',
    publishDate: 'Dec 7, 2023',
    createdAt: '2023-12-07',
    dueDate: '2023-12-07',
    stageDueDates: {
      ideas: '2023-11-15',
      planning: '2023-11-25',
      'in-progress': '2023-12-03',
      published: '2023-12-07'
    },
    pillar: { id: 5, name: 'Business', icon: '💼' }
  },
  {
    id: 10,
    title: 'Q4 Performance Report',
    description: 'Comprehensive analysis of Q4 content performance',
    status: 'published',
    priority: 'high',
    assignee: 'M',
    publishDate: 'Dec 6, 2023',
    createdAt: '2023-12-06',
    dueDate: '2023-12-06',
    stageDueDates: {
      ideas: '2023-11-10',
      planning: '2023-11-20',
      'in-progress': '2023-12-01',
      published: '2023-12-06'
    },
    pillar: { id: 5, name: 'Analytics', icon: '📊' }
  },
];

// Save content items to localStorage
const saveContentItems = (items) => {
  if (typeof window !== 'undefined') {
    try {
      localStorage.setItem('myta-content-items', JSON.stringify(items))
      console.log('🔥 Saved content items to localStorage:', items.length, 'items')
    } catch (error) {
      console.error('🔥 Error saving content items to localStorage:', error)
    }
  }
}

// Load content items from localStorage (client-side only)
const loadContentItemsFromStorage = () => {
  if (typeof window !== 'undefined') {
    try {
      const saved = localStorage.getItem('myta-content-items')
      if (saved) {
        const parsed = JSON.parse(saved)
        console.log('🔥 Loaded content items from localStorage:', parsed.length, 'items')
        return parsed
      }
    } catch (error) {
      console.error('🔥 Error loading content items from localStorage:', error)
    }
  }
  return null
}

// Initialize content items with default data (for SSR compatibility)
const contentItems = ref([...defaultContentItems])

// Content Suggestions Data
const contentSuggestions = ref({
  trendingTopics: [
    {
      id: 'ai-tools',
      title: 'AI Tools for Content Creation',
      description: 'High engagement potential',
      type: 'task',
      taskData: {
        title: 'Research AI Tools for Content Creation',
        description: 'Research and create content about trending AI tools for content creation. High engagement potential topic.',
        priority: 'high',
        dueDate: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000).toISOString().split('T')[0] // 2 days from now
      }
    },
    {
      id: 'social-predictions',
      title: '2024 Social Media Predictions',
      description: 'Seasonal relevance',
      type: 'task',
      taskData: {
        title: 'Create 2024 Social Media Predictions Content',
        description: 'Research and develop content around 2024 social media predictions. Seasonal relevance makes this timely.',
        priority: 'high',
        dueDate: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString().split('T')[0] // 3 days from now
      }
    },
    {
      id: 'short-form-video',
      title: 'Short-form Video Strategies',
      description: 'Platform trending',
      type: 'task',
      taskData: {
        title: 'Develop Short-form Video Strategy',
        description: 'Create a comprehensive strategy for short-form video content. Currently trending across platforms.',
        priority: 'medium',
        dueDate: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000).toISOString().split('T')[0] // 5 days from now
      }
    }
  ],
  contentIdeas: [
    {
      id: 'behind-scenes',
      title: 'Behind-the-Scenes Content',
      description: 'Builds audience connection',
      type: 'content',
      contentData: {
        title: 'Behind-the-Scenes: My Content Creation Process',
        description: 'Take your audience behind the scenes of your content creation process. Show your workspace, tools, and creative workflow.',
        status: 'ideas',
        priority: 'medium'
      }
    },
    {
      id: 'tutorial-series',
      title: 'Tutorial Series: Beginner to Pro',
      description: 'Educational content',
      type: 'content',
      contentData: {
        title: 'Complete Tutorial Series: From Beginner to Pro',
        description: 'Create a comprehensive tutorial series that takes viewers from beginner level to advanced skills in your niche.',
        status: 'ideas',
        priority: 'high'
      }
    },
    {
      id: 'community-qa',
      title: 'Community Q&A Sessions',
      description: 'Interactive engagement',
      type: 'content',
      contentData: {
        title: 'Weekly Community Q&A Sessions',
        description: 'Host regular Q&A sessions to answer audience questions and build stronger community engagement.',
        status: 'ideas',
        priority: 'medium'
      }
    }
  ],
  optimizationTips: [
    {
      id: 'posting-time',
      title: 'Post at 2-4 PM for max reach',
      description: 'Timing optimization',
      type: 'task',
      taskData: {
        title: 'Optimize posting schedule for maximum reach',
        description: 'Research and implement optimal posting times (2-4 PM) for your content to maximize audience reach and engagement.',
        priority: 'medium',
        dueDate: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString().split('T')[0] // 3 days from now
      }
    },
    {
      id: 'hashtag-strategy',
      title: 'Use 3-5 hashtags per post',
      description: 'Hashtag strategy',
      type: 'task',
      taskData: {
        title: 'Develop hashtag strategy (3-5 per post)',
        description: 'Research and create a hashtag strategy using 3-5 relevant hashtags per post to improve discoverability.',
        priority: 'medium',
        dueDate: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000).toISOString().split('T')[0] // 5 days from now
      }
    },
    {
      id: 'video-captions',
      title: 'Add captions to videos',
      description: 'Accessibility boost',
      type: 'task',
      taskData: {
        title: 'Add captions to all video content',
        description: 'Implement captions for all video content to improve accessibility and engagement.',
        priority: 'high',
        dueDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0] // 1 week from now
      }
    }
  ]
})

// Create content function
const createContent = () => {
  try {
    // Validate required fields
    if (!newContent.value.title.trim()) {
      alert('Please enter a title')
      return
    }

    if (!newContent.value.pillarId) {
      alert('Please select a content pillar')
      return
    }

    // Find the selected pillar
    const selectedPillar = availablePillars.value.find(p => p.id === newContent.value.pillarId)

    // Create new content item
    const newItem = {
      id: Date.now(), // Simple ID generation
      title: newContent.value.title.trim(),
      description: newContent.value.description.trim() || 'No description provided',
      status: newContent.value.status, // Use selected status
      priority: newContent.value.priority,
      assignee: 'M',
      dueDate: newContent.value.dueDate || null,
      stageDueDates: { ...newContent.value.stageDueDates },
      stageCompletions: { ...newContent.value.stageCompletions },
      createdAt: new Date().toISOString().split('T')[0],
      pillar: selectedPillar ? {
        id: selectedPillar.id,
        name: selectedPillar.name,
        icon: selectedPillar.icon
      } : null
    }

    // Add to content items
    contentItems.value.unshift(newItem)

    // Reset form
    newContent.value.title = ''
    newContent.value.description = ''
    newContent.value.pillarId = ''
    newContent.value.priority = 'medium'
    newContent.value.dueDate = ''
    newContent.value.status = 'ideas'
    newContent.value.stageDueDates = {
      ideas: '',
      planning: '',
      'in-progress': '',
      published: ''
    }
    newContent.value.stageCompletions = {
      ideas: false,
      planning: false,
      'in-progress': false,
      published: false
    }

    // Close modal
    showCreateContentModal.value = false

    // Show success feedback with due date info
    const dueDateText = newItem.dueDate ? ` (Due: ${new Date(newItem.dueDate).toLocaleDateString()})` : ''
    alert(`Created new content: "${newItem.title}"${dueDateText}`)
  } catch (error) {
    console.error('Error creating content:', error)
    alert('Error creating content. Please try again.')
  }
}



const updateContent = () => {
  try {
    if (!editContent.value.title.trim()) {
      alert('Please enter a title')
      return
    }

    const selectedPillar = availablePillars.value.find(p => p.id === editContent.value.pillarId)

    // Update the content item
    const itemIndex = contentItems.value.findIndex(item => item.id === selectedContentItem.value.id)
    if (itemIndex !== -1) {
      // Create a completely new object to ensure Vue reactivity
      const updatedItem = {
        ...contentItems.value[itemIndex],
        title: editContent.value.title.trim(),
        description: editContent.value.description.trim() || 'No description provided',
        priority: editContent.value.priority,
        dueDate: editContent.value.dueDate || null,
        status: editContent.value.status,
        stageDueDates: { ...editContent.value.stageDueDates },
        stageCompletions: { ...editContent.value.stageCompletions },
        pillar: selectedPillar ? {
          id: selectedPillar.id,
          name: selectedPillar.name,
          icon: selectedPillar.icon
        } : null
      }

      // Use array splice to ensure reactivity
      contentItems.value.splice(itemIndex, 1, updatedItem)

      // Save to localStorage to persist changes
      saveContentItems(contentItems.value)

      console.log('🔥 Content updated:', updatedItem)
      console.log('🔥 New status:', updatedItem.status)
      console.log('🔥 Items in new status column:', contentItems.value.filter(item => item.status === updatedItem.status).length)
    }

    // Close modal and reset
    showEditContentModal.value = false
    selectedContentItem.value = null

    const dueDateText = editContent.value.dueDate ? ` (Due: ${new Date(editContent.value.dueDate).toLocaleDateString()})` : ''
    alert(`Updated content: "${editContent.value.title}"${dueDateText}`)

    // Force reactivity update using nextTick
    nextTick(() => {
      console.log('🔥 After nextTick - Items in status columns:')
      console.log('Ideas:', contentItems.value.filter(item => item.status === 'ideas').length)
      console.log('Planning:', contentItems.value.filter(item => item.status === 'planning').length)
      console.log('In Progress:', contentItems.value.filter(item => item.status === 'in-progress').length)
      console.log('Published:', contentItems.value.filter(item => item.status === 'published').length)
    })

  } catch (error) {
    console.error('Error updating content:', error)
    alert('Error updating content. Please try again.')
  }
}

// Delete content function
const openDeleteModal = (item) => {
  try {
    console.log('🔥 openDeleteModal called with item:', item)

    // Close dropdown first
    if (showDropdownMenu.value !== null) {
      showDropdownMenu.value = null
    }

    // Set selected item and show modal
    selectedContentItem.value = item
    showDeleteConfirmModal.value = true

    console.log('🔥 Delete modal state:', showDeleteConfirmModal.value)
    console.log('🔥 Delete modal should be open now')
  } catch (error) {
    console.error('🔥 Error in openDeleteModal:', error)
    console.error('🔥 Error stack:', error.stack)
    alert('Error opening delete modal: ' + error.message)
  }
}

// Content Suggestions Functions
const handleSuggestionClick = (suggestion) => {
  console.log('🔥 Suggestion clicked:', suggestion)

  if (suggestion.type === 'content') {
    saveAsContent(suggestion)
  } else if (suggestion.type === 'task') {
    saveAsTask(suggestion)
  }
}

const saveAsContent = (suggestion) => {
  console.log('🔥 Saving suggestion as content:', suggestion)

  if (suggestion.contentData) {
    openContent(suggestion.contentData)
  } else {
    // Create basic content from suggestion
    const contentData = {
      title: suggestion.title,
      description: suggestion.description,
      status: 'ideas',
      priority: 'medium'
    }
    openContent(contentData)
  }
}

const saveAsTask = (suggestion) => {
  console.log('🔥 Saving suggestion as task:', suggestion)

  let taskData

  if (suggestion.taskData) {
    // Use suggestion's task data and create proper task structure
    taskData = {
      id: `task-${Date.now()}`, // Generate unique ID
      title: suggestion.taskData.title,
      description: suggestion.taskData.description,
      status: 'pending',
      priority: suggestion.taskData.priority || 'medium',
      category: 'content', // Default category for content suggestions
      dueDate: new Date(suggestion.taskData.dueDate),
      createdAt: new Date(),
      updatedAt: new Date(),
      tags: ['ai-suggested', 'content-strategy'],
      estimatedTime: 60 // Default 1 hour
    }
  } else {
    // Create basic task from suggestion
    taskData = {
      id: `task-${Date.now()}`,
      title: suggestion.title,
      description: suggestion.description,
      status: 'pending',
      priority: 'medium',
      category: 'content',
      dueDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 1 week from now
      createdAt: new Date(),
      updatedAt: new Date(),
      tags: ['ai-suggested'],
      estimatedTime: 60
    }
  }

  console.log('🔥 Opening task modal with structured data:', taskData)
  openTask(taskData)
}

const deleteContent = () => {
  try {
    const itemIndex = contentItems.value.findIndex(item => item.id === selectedContentItem.value.id)
    if (itemIndex !== -1) {
      const deletedTitle = contentItems.value[itemIndex].title
      contentItems.value.splice(itemIndex, 1)

      // Save to localStorage to persist changes
      saveContentItems(contentItems.value)

      alert(`Deleted content: "${deletedTitle}"`)
    }

    showDeleteConfirmModal.value = false
    selectedContentItem.value = null
  } catch (error) {
    console.error('Error deleting content:', error)
    alert('Error deleting content. Please try again.')
  }
}

// Drag and drop functions
const onDragStart = (event, item) => {
  event.dataTransfer.setData('text/plain', JSON.stringify({
    id: item.id,
    fromStatus: item.status
  }))
  event.dataTransfer.effectAllowed = 'move'
}

const onDragOver = (event) => {
  event.preventDefault()
  event.dataTransfer.dropEffect = 'move'
}

const onDrop = (event, toStatus) => {
  event.preventDefault()

  try {
    const data = JSON.parse(event.dataTransfer.getData('text/plain'))
    const itemIndex = contentItems.value.findIndex(item => item.id === data.id)

    if (itemIndex !== -1 && data.fromStatus !== toStatus) {
      contentItems.value[itemIndex].status = toStatus

      // Save to localStorage to persist changes
      saveContentItems(contentItems.value)

      console.log(`Moved content from ${data.fromStatus} to ${toStatus}`)
    }
  } catch (error) {
    console.error('Error moving content:', error)
  }
}

// Dropdown menu functions
const toggleDropdown = async (itemId) => {
  try {
    console.log('toggleDropdown called with itemId:', itemId)
    await nextTick()
    showDropdownMenu.value = showDropdownMenu.value === itemId ? null : itemId
    console.log('Dropdown toggled, current value:', showDropdownMenu.value)
  } catch (error) {
    console.error('Error in toggleDropdown:', error)
  }
}

const closeDropdown = async () => {
  try {
    await nextTick()
    showDropdownMenu.value = null
  } catch (error) {
    console.error('Error in closeDropdown:', error)
  }
}

// Performance Predictions Data
const confidenceLevel = ref(87)

const nextVideoViews = ref({
  min: 15000,
  max: 25000
})

const nextVideoEngagement = ref(4.2)
const bestUploadTime = ref('2:00 PM PST')

const nextMilestone = ref({
  target: 100000,
  date: 'March 15, 2024',
  progress: 73
})

const trendAnalysis = ref({
  views: { change: 12.5 },
  engagement: { change: 8.3 },
  subscribers: { change: 15.7 }
})

const aiRecommendations = ref([
  {
    id: 1,
    icon: '🎯',
    title: 'Optimize Upload Schedule',
    description: 'Upload on Tuesdays at 2 PM for 23% higher engagement'
  },
  {
    id: 2,
    icon: '📱',
    title: 'Create YouTube Shorts',
    description: 'Shorts content could increase discovery by 45%'
  },
  {
    id: 3,
    icon: '🔥',
    title: 'Trending Topic Alert',
    description: 'Cover "AI productivity tools" - trending in your niche'
  }
])

const formatNumber = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

const applyRecommendation = (recommendation) => {
  console.log('🔥 Applying recommendation:', recommendation.title)
  // Integrate with task creation or content planning
}

// Helper functions
const getColumnItems = status => {
  return contentItems.value.filter(item => item.status === status)
}

const getColumnCount = status => {
  return getColumnItems(status).length
}
</script>
