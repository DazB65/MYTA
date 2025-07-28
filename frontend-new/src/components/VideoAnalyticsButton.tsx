import React, { useState } from 'react';
import { BarChart3, X } from 'lucide-react';
import VideoAnalytics from './VideoAnalytics';

interface VideoAnalyticsButtonProps {
  videoId: string;
  videoTitle?: string;
  className?: string;
}

export const VideoAnalyticsButton: React.FC<VideoAnalyticsButtonProps> = ({ 
  videoId, 
  videoTitle = 'Video',
  className = '' 
}) => {
  const [showAnalytics, setShowAnalytics] = useState(false);

  return (
    <>
      <button
        onClick={() => setShowAnalytics(true)}
        className={`inline-flex items-center gap-2 px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm ${className}`}
      >
        <BarChart3 className="w-4 h-4" />
        Analytics
      </button>

      {showAnalytics && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
            <div className="flex justify-between items-center p-6 border-b border-gray-200">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">Video Analytics</h2>
                <p className="text-sm text-gray-600 mt-1">{videoTitle}</p>
              </div>
              <button
                onClick={() => setShowAnalytics(false)}
                className="text-gray-500 hover:text-gray-700 transition-colors"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
              <VideoAnalytics videoId={videoId} />
            </div>
          </div>
        </div>
      )}
    </>
  );
};

// Simple expandable version for inline use
export const VideoAnalyticsExpander: React.FC<VideoAnalyticsButtonProps> = ({ 
  videoId,
  className = '' 
}) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className={className}>
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full text-left px-4 py-2 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors flex items-center justify-between"
      >
        <span className="flex items-center gap-2 text-sm font-medium text-gray-700">
          <BarChart3 className="w-4 h-4" />
          {expanded ? 'Hide' : 'Show'} Detailed Analytics
        </span>
        <svg 
          className={`w-4 h-4 transition-transform ${expanded ? 'rotate-180' : ''}`} 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      
      {expanded && (
        <div className="mt-4">
          <VideoAnalytics videoId={videoId} />
        </div>
      )}
    </div>
  );
};