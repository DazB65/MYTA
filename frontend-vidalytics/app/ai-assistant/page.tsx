"use client";

import { useState } from "react";

export default function AIAssistantPage() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: "AI Assistant",
      content:
        "Hello! I'm your AI content creation assistant. How can I help you today?",
      timestamp: "10:30 AM",
      isAI: true,
    },
  ]);

  const handleSendMessage = () => {
    if (message.trim()) {
      const newMessage = {
        id: messages.length + 1,
        sender: "You",
        content: message,
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
        isAI: false,
      };
      setMessages([...messages, newMessage]);
      setMessage("");
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="bg-gray-900 text-white min-h-screen flex">
      {/* Left Sidebar Navigation - Reusing from other pages */}
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
              href="/videos"
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
              href="/content-studio"
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
              className="flex items-center px-4 py-3 text-white bg-pink-500 rounded-lg"
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

        {/* AI Assistant Chat Interface */}
        <div className="bg-white rounded-xl flex flex-col h-[600px]">
          {/* Chat Interface Header */}
          <div className="flex items-center justify-between p-6 border-b border-gray-200">
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 bg-gradient-to-br from-purple-400 to-pink-500 rounded-lg flex items-center justify-center">
                <svg
                  className="w-6 h-6 text-white"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-bold text-gray-900">
                  Professional Assistant
                </h3>
                <p className="text-sm text-gray-600">AI Content Creator</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <button className="w-10 h-10 bg-pink-100 rounded-full flex items-center justify-center hover:bg-pink-200 transition-colors">
                <svg
                  className="w-5 h-5 text-pink-600"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
                    clipRule="evenodd"
                  ></path>
                </svg>
              </button>
              <button className="w-10 h-10 bg-pink-100 rounded-full flex items-center justify-center hover:bg-pink-200 transition-colors">
                <svg
                  className="w-5 h-5 text-pink-600"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z"
                    clipRule="evenodd"
                  ></path>
                </svg>
              </button>
            </div>
          </div>

          {/* Tab Navigation */}
          <div className="px-6 pt-4">
            <div className="flex items-center space-x-8 border-b border-gray-200">
              <button className="pb-3 text-gray-900 font-medium border-b-2 border-pink-500">
                💬 Chats
              </button>
              <button className="pb-3 text-gray-500 hover:text-gray-700">
                📊 Visualizer View
              </button>
            </div>
          </div>

          {/* Suggestion Buttons */}
          <div className="px-6 py-4">
            <div className="flex items-center space-x-3">
              <button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-full text-sm hover:bg-gray-200 transition-colors">
                Trending Topics
              </button>
              <button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-full text-sm hover:bg-gray-200 transition-colors">
                Competitor Analysis
              </button>
              <button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-full text-sm hover:bg-gray-200 transition-colors">
                Channel Insights
              </button>
            </div>
          </div>

          {/* Chat History Area */}
          <div className="flex-1 px-6 overflow-y-auto">
            <div className="space-y-4">
              {messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex ${msg.isAI ? "justify-start" : "justify-end"}`}
                >
                  <div
                    className={`max-w-[70%] ${msg.isAI ? "bg-gray-100" : "bg-pink-500 text-white"} rounded-lg p-4`}
                  >
                    <div className="text-xs text-gray-500 mb-1">
                      {msg.sender} {msg.timestamp}
                    </div>
                    <div
                      className={`text-sm ${msg.isAI ? "text-gray-900" : "text-white"}`}
                    >
                      {msg.content}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Message Input Field */}
          <div className="p-6 border-t border-gray-200">
            <div className="flex items-center space-x-3">
              <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type Something..."
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent outline-none text-gray-900"
              />
              <button
                onClick={handleSendMessage}
                className="px-6 py-3 bg-gradient-to-r from-pink-500 to-purple-600 text-white rounded-lg font-medium hover:from-pink-600 hover:to-purple-700 transition-all duration-200 flex items-center space-x-2"
              >
                <span>Send</span>
                <svg
                  className="w-4 h-4"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
                    clipRule="evenodd"
                  ></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
