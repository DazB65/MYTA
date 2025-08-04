"use client";

export default function DashboardPage() {
  return (
    <div className="bg-gray-900 text-white min-h-screen flex">
      {/* Left Sidebar Navigation */}
      <div className="w-72 bg-gray-800 h-screen flex flex-col">
        {/* Logo Section */}
        <div className="p-6">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-pink-500 rounded flex items-center justify-center">
              <span className="text-white text-sm">✨</span>
            </div>
            <h1 className="text-xl font-bold text-white">Vidalytics</h1>
          </div>
          <p className="text-xs text-gray-400 mt-1">
            Your AI Agent for Content and Growth
          </p>
        </div>

        {/* Main Menu */}
        <div className="px-4">
          <h3 className="text-sm font-medium text-gray-400 mb-4">Main Menu</h3>
          <nav className="space-y-2">
            <a
              href="#"
              className="flex items-center px-4 py-3 text-white bg-pink-500 rounded-lg"
            >
              <svg
                className="w-5 h-5 mr-3"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"></path>
              </svg>
              Dashboard
            </a>
            <a
              href="#"
              className="flex items-center px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
            >
              <svg
                className="w-5 h-5 mr-3"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"></path>
              </svg>
              Pillars
            </a>
            <a
              href="#"
              className="flex items-center px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
            >
              <svg
                className="w-5 h-5 mr-3"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z"></path>
              </svg>
              Videos
            </a>
            <a
              href="#"
              className="flex items-center px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
            >
              <svg
                className="w-5 h-5 mr-3"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"></path>
              </svg>
              Content Studio
            </a>
            <a
              href="#"
              className="flex items-center px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
            >
              <svg
                className="w-5 h-5 mr-3"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              AI Assistant
            </a>
          </nav>
        </div>

        {/* General Section */}
        <div className="px-4 mt-8">
          <h3 className="text-sm font-medium text-gray-400 mb-4">General</h3>
          <nav className="space-y-2">
            <a
              href="#"
              className="flex items-center px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
            >
              <svg
                className="w-5 h-5 mr-3"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z"
                  clipRule="evenodd"
                ></path>
              </svg>
              Setting
            </a>
          </nav>
        </div>

        {/* User Profile Section */}
        <div className="mt-auto p-6 border-t border-gray-700">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-pink-500 rounded-full flex items-center justify-center">
              <span className="text-white font-bold">M</span>
            </div>
            <div className="flex-1">
              <p className="text-sm text-white">Good Morning</p>
              <p className="text-sm font-bold text-white">
                MARCELINE ANDERSON!
              </p>
              <p className="text-xs text-gray-400">
                Let&apos;s see your current task work today
              </p>
            </div>
          </div>
          <div className="mt-4 flex items-center justify-between">
            <div className="text-xs text-gray-400">📅 23 July, 2026</div>
            <button className="text-gray-400 hover:text-white">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z"
                  clipRule="evenodd"
                ></path>
              </svg>
            </button>
          </div>
          <button className="mt-2 text-gray-400 hover:text-white text-sm flex items-center">
            <svg
              className="w-4 h-4 mr-1"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z"
                clipRule="evenodd"
              ></path>
            </svg>
            Log Out
          </button>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 bg-gray-100 p-8 overflow-y-auto">
        {/* Top Banner */}
        <div className="bg-black rounded-xl p-8 mb-8 relative overflow-hidden">
          <div className="absolute top-4 right-4 flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-pink-500 rounded-full"></div>
              <span className="bg-green-500 text-white px-3 py-1 rounded-full text-sm">
                ● Online
              </span>
            </div>
          </div>
          <div className="text-center">
            <h2 className="text-white text-2xl font-bold mb-2">
              📱iPhone 16 Pro
            </h2>
            <p className="text-gray-300">Hello, Apple Intelligence</p>
          </div>
          <div className="absolute bottom-4 right-8">
            <span className="bg-green-500 text-white px-3 py-1 rounded-full text-sm">
              Youtube connected
            </span>
          </div>
        </div>

        {/* Middle Section: Two Column Layout */}
        <div className="grid grid-cols-3 gap-8 mb-8">
          {/* Left Column: Task Manager */}
          <div className="col-span-2 bg-white rounded-xl p-6">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-xl font-bold text-gray-900">
                  Task Manager
                </h3>
                <p className="text-sm text-gray-500">0 of 3 tasks completed</p>
              </div>
              <div className="flex items-center space-x-2">
                <button className="px-4 py-2 bg-pink-500 text-white rounded-lg text-sm">
                  All
                </button>
                <button className="px-4 py-2 text-gray-500 rounded-lg text-sm hover:bg-gray-100">
                  Pending
                </button>
                <button className="px-4 py-2 text-gray-500 rounded-lg text-sm hover:bg-gray-100">
                  Completed
                </button>
                <button className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center">
                  <span className="text-pink-500">👤</span>
                </button>
                <button className="px-4 py-2 bg-pink-500 text-white rounded-lg text-sm">
                  + Add New Goal
                </button>
              </div>
            </div>

            {/* Task Items */}
            <div className="space-y-4">
              {/* Task 1 */}
              <div className="flex items-start space-x-4 p-4 border border-gray-200 rounded-lg hover:border-pink-300 transition-colors">
                <input
                  type="checkbox"
                  className="mt-1 w-5 h-5 text-pink-500 rounded border-gray-300"
                />
                <div className="flex-1">
                  <h4 className="font-medium text-gray-900">
                    Create AI content creation assistant
                  </h4>
                  <p className="text-sm text-gray-500 mt-1">
                    Hello! I&apos;m your AI content creation assistant. How can
                    I help you today?
                  </p>
                  <div className="flex items-center space-x-2 mt-3">
                    <span className="px-2 py-1 bg-blue-100 text-blue-600 rounded text-xs font-medium">
                      Medium
                    </span>
                    <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs font-medium">
                      Content
                    </span>
                    <div className="flex items-center text-xs text-gray-500">
                      <svg
                        className="w-4 h-4 mr-1"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.414L11 9.586V6z"
                          clipRule="evenodd"
                        ></path>
                      </svg>
                      Due: 18/7/2025
                    </div>
                  </div>
                </div>
                <button className="text-gray-400 hover:text-gray-600">
                  <svg
                    className="w-5 h-5"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
                  </svg>
                </button>
              </div>

              {/* Task 2 */}
              <div className="flex items-start space-x-4 p-4 border border-gray-200 rounded-lg hover:border-pink-300 transition-colors">
                <input
                  type="checkbox"
                  className="mt-1 w-5 h-5 text-pink-500 rounded border-gray-300"
                />
                <div className="flex-1">
                  <h4 className="font-medium text-gray-900">
                    Schedule social media posts
                  </h4>
                  <p className="text-sm text-gray-500 mt-1">
                    Plan and schedule posts for next week
                  </p>
                  <div className="flex items-center space-x-2 mt-3">
                    <span className="px-2 py-1 bg-red-100 text-red-600 rounded text-xs font-medium">
                      High
                    </span>
                    <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs font-medium">
                      Content
                    </span>
                    <div className="flex items-center text-xs text-gray-500">
                      <svg
                        className="w-4 h-4 mr-1"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.414L11 9.586V6z"
                          clipRule="evenodd"
                        ></path>
                      </svg>
                      Due: 18/7/2025
                    </div>
                  </div>
                </div>
                <button className="text-gray-400 hover:text-gray-600">
                  <svg
                    className="w-5 h-5"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
                  </svg>
                </button>
              </div>

              {/* Task 3 */}
              <div className="flex items-start space-x-4 p-4 border border-gray-200 rounded-lg hover:border-pink-300 transition-colors">
                <input
                  type="checkbox"
                  className="mt-1 w-5 h-5 text-pink-500 rounded border-gray-300"
                />
                <div className="flex-1">
                  <h4 className="font-medium text-gray-900">
                    Update channel banner
                  </h4>
                  <p className="text-sm text-gray-500 mt-1">
                    Design new banner with current subscriber count
                  </p>
                  <div className="flex items-center space-x-2 mt-3">
                    <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs font-medium">
                      Low
                    </span>
                    <span className="px-2 py-1 bg-pink-100 text-pink-600 rounded text-xs font-medium">
                      Marketing
                    </span>
                    <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs font-medium">
                      Content
                    </span>
                    <div className="flex items-center text-xs text-gray-500">
                      <svg
                        className="w-4 h-4 mr-1"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.414L11 9.586V6z"
                          clipRule="evenodd"
                        ></path>
                      </svg>
                      Due: 18/7/2025
                    </div>
                  </div>
                </div>
                <button className="text-gray-400 hover:text-gray-600">
                  <svg
                    className="w-5 h-5"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
                  </svg>
                </button>
              </div>

              {/* Task 4 */}
              <div className="flex items-start space-x-4 p-4 border border-gray-200 rounded-lg hover:border-pink-300 transition-colors">
                <input
                  type="checkbox"
                  className="mt-1 w-5 h-5 text-pink-500 rounded border-gray-300"
                />
                <div className="flex-1">
                  <h4 className="font-medium text-gray-900">
                    Reply to community comments
                  </h4>
                  <p className="text-sm text-gray-500 mt-1">
                    Engage with your audience by responding to comments on your
                    latest video posts.
                  </p>
                </div>
                <button className="text-gray-400 hover:text-gray-600">
                  <svg
                    className="w-5 h-5"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          {/* Right Column: Goals & Statistics */}
          <div className="space-y-6">
            {/* Channel Goals Card */}
            <div className="bg-white rounded-xl p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-bold text-gray-900">
                  Channel Goals
                </h3>
                <button className="px-4 py-2 bg-pink-500 text-white rounded-lg text-sm hover:bg-pink-600 transition-colors">
                  + Add New Task
                </button>
              </div>

              {/* Views Goal */}
              <div className="bg-gradient-to-br from-pink-400 to-purple-500 rounded-xl p-6 mb-4">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-2">
                    <svg
                      className="w-5 h-5 text-white"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"></path>
                      <path
                        fillRule="evenodd"
                        d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                        clipRule="evenodd"
                      ></path>
                    </svg>
                    <span className="text-white font-medium">Views</span>
                  </div>
                  <button className="text-white hover:text-gray-200">
                    <svg
                      className="w-5 h-5"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
                    </svg>
                  </button>
                </div>
                <div className="flex items-center justify-center mb-4">
                  <div className="relative w-20 h-20">
                    <svg
                      className="w-20 h-20 transform -rotate-90"
                      viewBox="0 0 100 100"
                    >
                      <circle
                        cx="50"
                        cy="50"
                        r="35"
                        stroke="#ffffff20"
                        strokeWidth="6"
                        fill="none"
                      />
                      <circle
                        cx="50"
                        cy="50"
                        r="35"
                        stroke="#ffffff"
                        strokeWidth="6"
                        fill="none"
                        strokeDasharray="164.93"
                        strokeDashoffset="41.23"
                        strokeLinecap="round"
                      />
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-xl font-bold text-white">75%</span>
                    </div>
                  </div>
                </div>
                <div className="flex justify-between text-white text-sm">
                  <div className="text-center">
                    <div className="font-bold">7.5k</div>
                    <div className="opacity-80 text-xs">Completed</div>
                  </div>
                  <div className="text-center">
                    <div className="font-bold">2.5k</div>
                    <div className="opacity-80 text-xs">Remaining</div>
                  </div>
                  <div className="text-center">
                    <div className="font-bold">10k</div>
                    <div className="opacity-80 text-xs">Total</div>
                  </div>
                </div>
              </div>

              {/* Subscribers Goal */}
              <div className="bg-gradient-to-br from-blue-400 to-cyan-500 rounded-xl p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-2">
                    <svg
                      className="w-5 h-5 text-white"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"></path>
                    </svg>
                    <span className="text-white font-medium">Subscribers</span>
                  </div>
                  <button className="text-white hover:text-gray-200">
                    <svg
                      className="w-5 h-5"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
                    </svg>
                  </button>
                </div>
                <div className="flex items-center justify-center mb-4">
                  <div className="relative w-20 h-20">
                    <svg
                      className="w-20 h-20 transform -rotate-90"
                      viewBox="0 0 100 100"
                    >
                      <circle
                        cx="50"
                        cy="50"
                        r="35"
                        stroke="#ffffff20"
                        strokeWidth="6"
                        fill="none"
                      />
                      <circle
                        cx="50"
                        cy="50"
                        r="35"
                        stroke="#ffffff"
                        strokeWidth="6"
                        fill="none"
                        strokeDasharray="164.93"
                        strokeDashoffset="41.23"
                        strokeLinecap="round"
                      />
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-xl font-bold text-white">75%</span>
                    </div>
                  </div>
                </div>
                <div className="flex justify-between text-white text-sm">
                  <div className="text-center">
                    <div className="font-bold">7.5k</div>
                    <div className="opacity-80 text-xs">Completed</div>
                  </div>
                  <div className="text-center">
                    <div className="font-bold">2.5k</div>
                    <div className="opacity-80 text-xs">Remaining</div>
                  </div>
                  <div className="text-center">
                    <div className="font-bold">10k</div>
                    <div className="opacity-80 text-xs">Total</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Quick Statistic Card */}
            <div className="bg-white rounded-xl p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-bold text-gray-900">
                  Quick Statistic
                </h3>
                <button className="bg-pink-500 text-white px-4 py-2 rounded-lg text-sm hover:bg-pink-600 transition-colors flex items-center space-x-2">
                  <svg
                    className="w-4 h-4"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span>AI Assistant</span>
                </button>
              </div>
              <div className="text-center py-8">
                <div className="text-3xl font-bold text-gray-900 mb-2">48%</div>
                <div className="text-gray-500">Audience Retention</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
