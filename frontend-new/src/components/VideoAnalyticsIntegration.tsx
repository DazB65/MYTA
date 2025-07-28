import React, { useState } from 'react';
import VideoAnalytics from './VideoAnalytics';

// Example integration into your existing Videos page or Video detail modal
// This shows how to use the VideoAnalytics component

interface VideoData {
  id: string;
  title: string;
  // ... other video properties
}

interface VideoDetailModalProps {
  video: VideoData;
  isOpen: boolean;
  onClose: () => void;
}

// Example 1: In a modal or detail view
export const VideoDetailModal: React.FC<VideoDetailModalProps> = ({ video, isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto p-6">
        <div className="flex justify-between items-start mb-4">
          <h2 className="text-2xl font-bold text-gray-900">{video.title}</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        {/* Video Analytics Component */}
        <VideoAnalytics videoId={video.id} />
      </div>
    </div>
  );
};

// Example 2: In a tab view within your Videos page
export const VideoDetailsWithTabs: React.FC<{ video: VideoData }> = ({ video }) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'analytics' | 'comments'>('overview');

  return (
    <div className="bg-white rounded-lg shadow-sm">
      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8 px-6">
          <button
            onClick={() => setActiveTab('overview')}
            className={`py-3 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'overview'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Overview
          </button>
          <button
            onClick={() => setActiveTab('analytics')}
            className={`py-3 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'analytics'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Analytics
          </button>
          <button
            onClick={() => setActiveTab('comments')}
            className={`py-3 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'comments'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Comments
          </button>
        </nav>
      </div>

      {/* Tab Content */}
      <div className="p-6">
        {activeTab === 'overview' && (
          <div>
            <h3 className="text-lg font-semibold mb-4">Video Overview</h3>
            {/* Your existing video overview content */}
            <p className="text-gray-600">Basic video information goes here...</p>
          </div>
        )}
        
        {activeTab === 'analytics' && (
          <VideoAnalytics videoId={video.id} />
        )}
        
        {activeTab === 'comments' && (
          <div>
            <h3 className="text-lg font-semibold mb-4">Comments</h3>
            {/* Your comments section */}
            <p className="text-gray-600">Comments analysis goes here...</p>
          </div>
        )}
      </div>
    </div>
  );
};

// Example 3: Inline expansion in video list
export const VideoListItemWithAnalytics: React.FC<{ video: VideoData }> = ({ video }) => {
  const [showAnalytics, setShowAnalytics] = useState(false);

  return (
    <div className="border border-gray-200 rounded-lg p-4 mb-4">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold">{video.title}</h3>
          <p className="text-sm text-gray-600">Video ID: {video.id}</p>
        </div>
        <button
          onClick={() => setShowAnalytics(!showAnalytics)}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          {showAnalytics ? 'Hide' : 'Show'} Analytics
        </button>
      </div>
      
      {showAnalytics && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <VideoAnalytics videoId={video.id} />
        </div>
      )}
    </div>
  );
};