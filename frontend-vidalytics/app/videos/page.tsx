"use client";

export default function VideosPage() {
  return (
    <div className="bg-gray-900 text-white min-h-screen flex">
      {/* Left Sidebar Navigation - Reusing from Dashboard */}
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
              href="/dashboard"
              className="flex items-center px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
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
              className="flex items-center px-4 py-3 text-white bg-pink-500 rounded-lg"
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

        {/* Video Analytics Section */}
        <div className="bg-white rounded-xl p-6 mb-8">
          <div className="mb-6">
            <h3 className="text-2xl font-bold text-gray-900 mb-2">
              Video Analytics
            </h3>
            <p className="text-gray-600">
              Track performance and monitor your content. CTR Generation, Watch
              Time, Community and CTR
            </p>
          </div>

          {/* Key Metrics Overview */}
          <div className="grid grid-cols-6 gap-6 mb-8">
            {/* Total Videos */}
            <div className="text-center">
              <div className="text-3xl font-bold text-gray-900 mb-1">122</div>
              <div className="text-sm text-gray-600">Total Videos</div>
              <div className="text-xs text-green-500 mt-1">
                ↗ 18% vs last month
              </div>
            </div>

            {/* Total Views */}
            <div className="text-center">
              <div className="text-3xl font-bold text-gray-900 mb-1">2.0M</div>
              <div className="text-sm text-gray-600">Total Views</div>
              <div className="text-xs text-green-500 mt-1">
                ↗ 15% vs last month
              </div>
            </div>

            {/* Total Likes */}
            <div className="text-center">
              <div className="text-3xl font-bold text-gray-900 mb-1">9.8k</div>
              <div className="text-sm text-gray-600">Total Likes</div>
              <div className="text-xs text-green-500 mt-1">
                ↗ 12% vs last month
              </div>
            </div>

            {/* Total Comments */}
            <div className="text-center">
              <div className="text-3xl font-bold text-gray-900 mb-1">5.5k</div>
              <div className="text-sm text-gray-600">Total Comments</div>
              <div className="text-xs text-green-500 mt-1">
                ↗ 7% vs last month
              </div>
            </div>

            {/* Avg CTR */}
            <div className="text-center">
              <div className="text-3xl font-bold text-gray-900 mb-1">34%</div>
              <div className="text-sm text-gray-600">Avg CTR</div>
              <div className="text-xs text-green-500 mt-1">
                ↗ 3% vs last month
              </div>
            </div>

            {/* Avg Views */}
            <div className="text-center">
              <div className="text-3xl font-bold text-gray-900 mb-1">200k</div>
              <div className="text-sm text-gray-600">Avg Views</div>
              <div className="text-xs text-gray-500 mt-1">
                → 0% vs last month
              </div>
            </div>
          </div>
        </div>

        {/* Recent Videos Section */}
        <div className="bg-white rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-xl font-bold text-gray-900 mb-1">
                Recent Videos
              </h3>
              <p className="text-gray-600">Showing 1 to 6 of 48 videos</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-600">Sort by:</span>
                <select className="border border-gray-300 rounded-lg px-3 py-1 text-sm bg-white">
                  <option>Date</option>
                  <option>Views</option>
                  <option>Duration</option>
                </select>
              </div>
              <button className="text-gray-500 hover:text-gray-700">
                <svg
                  className="w-5 h-5"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"></path>
                </svg>
              </button>
            </div>
          </div>

          {/* Videos Table */}
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-medium text-gray-600 text-sm">
                    Time
                  </th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600 text-sm">
                    Views
                  </th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600 text-sm">
                    Comments
                  </th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600 text-sm">
                    CTR
                  </th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600 text-sm">
                    Stats
                  </th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 text-sm"></th>
                </tr>
              </thead>
              <tbody>
                {/* Video Row 1 */}
                <tr className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-4 px-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-16 h-10 bg-pink-500 rounded flex items-center justify-center">
                        <svg
                          className="w-6 h-6 text-white"
                          fill="currentColor"
                          viewBox="0 0 20 20"
                        >
                          <path d="M8 5v10l8-5-8-5z"></path>
                        </svg>
                      </div>
                      <div>
                        <div className="text-sm text-gray-600">
                          📅 29/05/2026 ⏰ 09:14
                        </div>
                        <div className="font-medium text-gray-900">
                          How to Create Engaging YouTube Content in 2024
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="py-4 px-4 text-gray-900">34/32</td>
                  <td className="py-4 px-4 text-gray-900">1.2M</td>
                  <td className="py-4 px-4 text-gray-900">234</td>
                  <td className="py-4 px-4 text-gray-900">4,4 GB</td>
                  <td className="py-4 px-4 text-right">
                    <div className="text-sm text-gray-600">
                      Hi! Has been Anleysed
                    </div>
                  </td>
                </tr>

                {/* Video Row 2 */}
                <tr className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-4 px-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-16 h-10 bg-pink-500 rounded flex items-center justify-center">
                        <svg
                          className="w-6 h-6 text-white"
                          fill="currentColor"
                          viewBox="0 0 20 20"
                        >
                          <path d="M8 5v10l8-5-8-5z"></path>
                        </svg>
                      </div>
                      <div>
                        <div className="text-sm text-gray-600">
                          📅 29/05/2026 ⏰ 09:14
                        </div>
                        <div className="font-medium text-gray-900">
                          Top 5 Video Editing Tips for Beginners
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="py-4 px-4 text-gray-900">25/48</td>
                  <td className="py-4 px-4 text-gray-900">876K</td>
                  <td className="py-4 px-4 text-gray-900">654</td>
                  <td className="py-4 px-4 text-gray-900">8,4 GB</td>
                  <td className="py-4 px-4 text-right">
                    <div className="text-sm text-gray-600">
                      Hi! Has been Anleysed
                    </div>
                  </td>
                </tr>

                {/* Video Row 3 */}
                <tr className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-4 px-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-16 h-10 bg-pink-500 rounded flex items-center justify-center">
                        <svg
                          className="w-6 h-6 text-white"
                          fill="currentColor"
                          viewBox="0 0 20 20"
                        >
                          <path d="M8 5v10l8-5-8-5z"></path>
                        </svg>
                      </div>
                      <div>
                        <div className="text-sm text-gray-600">
                          📅 29/05/2026 ⏰ 09:14
                        </div>
                        <div className="font-medium text-gray-900">
                          Understanding YouTube Analytics Dashboard
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="py-4 px-4 text-gray-900">23/68</td>
                  <td className="py-4 px-4 text-gray-900">543</td>
                  <td className="py-4 px-4 text-gray-900">432</td>
                  <td className="py-4 px-4 text-gray-900">8,4 GB</td>
                  <td className="py-4 px-4 text-right">
                    <div className="text-sm text-green-600">
                      Hi! Has been Anleysed
                    </div>
                  </td>
                </tr>

                {/* Video Row 4 */}
                <tr className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-4 px-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-16 h-10 bg-pink-500 rounded flex items-center justify-center">
                        <svg
                          className="w-6 h-6 text-white"
                          fill="currentColor"
                          viewBox="0 0 20 20"
                        >
                          <path d="M8 5v10l8-5-8-5z"></path>
                        </svg>
                      </div>
                      <div>
                        <div className="text-sm text-gray-600">
                          📅 29/05/2026 ⏰ 09:14
                        </div>
                        <div className="font-medium text-gray-900">
                          Building Your Personal Brand on Social Media
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="py-4 px-4 text-gray-900">21/69</td>
                  <td className="py-4 px-4 text-gray-900">995</td>
                  <td className="py-4 px-4 text-gray-900">123</td>
                  <td className="py-4 px-4 text-gray-900">8,4 GB</td>
                  <td className="py-4 px-4 text-right">
                    <div className="text-sm text-green-600">
                      Hi! Has been Anleysed
                    </div>
                  </td>
                </tr>

                {/* Video Row 5 */}
                <tr className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-4 px-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-16 h-10 bg-pink-500 rounded flex items-center justify-center">
                        <svg
                          className="w-6 h-6 text-white"
                          fill="currentColor"
                          viewBox="0 0 20 20"
                        >
                          <path d="M8 5v10l8-5-8-5z"></path>
                        </svg>
                      </div>
                      <div>
                        <div className="text-sm text-gray-600">
                          📅 29/05/2026 ⏰ 09:14
                        </div>
                        <div className="font-medium text-gray-900">
                          Scaling Your Revenue Brand on Social Media
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="py-4 px-4 text-gray-900">23/48</td>
                  <td className="py-4 px-4 text-gray-900">12,5k</td>
                  <td className="py-4 px-4 text-gray-900">909</td>
                  <td className="py-4 px-4 text-gray-900">8,4 GB</td>
                  <td className="py-4 px-4 text-right">
                    <div className="text-sm text-green-600">
                      Hi! Has been Anleysed
                    </div>
                  </td>
                </tr>

                {/* Video Row 6 */}
                <tr className="hover:bg-gray-50">
                  <td className="py-4 px-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-16 h-10 bg-pink-500 rounded flex items-center justify-center">
                        <svg
                          className="w-6 h-6 text-white"
                          fill="currentColor"
                          viewBox="0 0 20 20"
                        >
                          <path d="M8 5v10l8-5-8-5z"></path>
                        </svg>
                      </div>
                      <div>
                        <div className="text-sm text-gray-600">
                          📅 29/05/2026 ⏰ 09:14
                        </div>
                        <div className="font-medium text-gray-900">
                          Starting Your Personal Brand on Social Media
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="py-4 px-4 text-gray-900">23/48</td>
                  <td className="py-4 px-4 text-gray-900">432</td>
                  <td className="py-4 px-4 text-gray-900">678</td>
                  <td className="py-4 px-4 text-gray-900">8,4 GB</td>
                  <td className="py-4 px-4 text-right">
                    <div className="text-sm text-green-600">
                      Hi! Has been Anleysed
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* AI Assistant Button */}
          <div className="mt-6 flex justify-end">
            <button className="bg-pink-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-pink-600 transition-colors flex items-center space-x-2">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <span>AI Assistant</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
