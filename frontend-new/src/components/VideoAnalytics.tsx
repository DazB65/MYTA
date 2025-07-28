import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

interface VideoAnalyticsProps {
  videoId: string;
  userId?: string;
}

interface VideoPerformanceMetrics {
  views: number;
  likes: number;
  dislikes: number;
  comments: number;
  shares: number;
  impressions: number;
  click_through_rate: number;
  average_view_duration_seconds: number;
  views_first_24_hours: number;
}

interface ChannelAverageMetrics {
  average_ctr: number;
  average_views_first_24_hours: number;
  average_view_duration_seconds: number;
  total_videos_analyzed: number;
}

interface VideoAnalyticsData {
  video_id: string;
  title: string;
  published_at: string;
  duration_seconds: number;
  performance_metrics: VideoPerformanceMetrics;
  traffic_sources: Record<string, number>;
  audience_retention: Array<{ time_seconds: number; percentage_retained: number }>;
  channel_averages: ChannelAverageMetrics;
  performance_vs_average: {
    ctr_vs_average: number;
    view_duration_vs_average: number;
    first_24h_views_vs_average: number;
  };
  analysis_date: string;
  data_quality_score: number;
}

const VideoAnalytics: React.FC<VideoAnalyticsProps> = ({ videoId, userId = 'default_user' }) => {
  const [analyticsData, setAnalyticsData] = useState<VideoAnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const response = await fetch('/api/youtube/video-analytics', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            video_id: videoId,
            user_id: userId,
          }),
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => null);
          
          // Handle specific error cases
          if (response.status === 405) {
            throw new Error('Advanced analytics feature is currently being updated. Please try again later.');
          }
          
          throw new Error(errorData?.detail || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        if (data.status === 'success' && data.data?.video_analytics) {
          setAnalyticsData(data.data.video_analytics);
        } else {
          throw new Error('Invalid response format');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch analytics');
      } finally {
        setLoading(false);
      }
    };

    if (videoId) {
      fetchAnalytics();
    }
  }, [videoId, userId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 rounded-lg p-6">
        <div className="flex items-start space-x-3">
          <div className="text-2xl">⚠️</div>
          <div>
            <p className="font-semibold text-lg">Advanced Analytics Temporarily Unavailable</p>
            <p className="text-sm mt-2">{error}</p>
            <div className="mt-4 p-3 bg-yellow-100 rounded-md">
              <p className="text-xs text-yellow-700">
                💡 <strong>What you can see:</strong> Basic metrics (views, likes, comments) are available in the videos list above.
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!analyticsData) {
    return (
      <div className="bg-gray-50 border border-gray-200 text-gray-600 rounded-lg p-4">
        <p>No analytics data available</p>
      </div>
    );
  }

  const formatDuration = (seconds: number): string => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  const formatNumber = (num: number): string => {
    if (num >= 1000000) {
      return `${(num / 1000000).toFixed(1)}M`;
    } else if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}K`;
    }
    return num.toString();
  };

  const getPerformanceColor = (percentage: number): string => {
    return percentage >= 0 ? 'text-green-500' : 'text-red-500';
  };

  const getPerformanceIcon = (percentage: number) => {
    return percentage >= 0 ? (
      <TrendingUp className="w-4 h-4 inline ml-1" />
    ) : (
      <TrendingDown className="w-4 h-4 inline ml-1" />
    );
  };

  const { performance_metrics: metrics, channel_averages: averages, performance_vs_average: vsAverage } = analyticsData;

  return (
    <div className="space-y-6">
      {/* Section 1: Performance Snapshot */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-6">Performance Snapshot</h2>
        
        {/* KPI Card - Views in First 24 Hours */}
        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg p-6 mb-6">
          <div className="text-center">
            <p className="text-sm text-gray-600 mb-2">Views in First 24 Hours</p>
            <p className="text-4xl font-bold text-gray-900">{formatNumber(metrics.views_first_24_hours)}</p>
            <p className="text-sm text-gray-500 mt-2">Channel Average: {formatNumber(averages.average_views_first_24_hours)}</p>
            <div className={`text-2xl font-bold mt-3 ${getPerformanceColor(vsAverage.first_24h_views_vs_average)}`}>
              {vsAverage.first_24h_views_vs_average >= 0 ? '+' : ''}{vsAverage.first_24h_views_vs_average.toFixed(0)}%
              {getPerformanceIcon(vsAverage.first_24h_views_vs_average)}
            </div>
          </div>
        </div>

        {/* Core Metrics Trio */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* CTR */}
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-600 mb-1">Click-Through Rate</p>
            <p className="text-2xl font-bold text-gray-900">{metrics.click_through_rate.toFixed(2)}%</p>
            <div className={`text-sm font-medium mt-1 ${getPerformanceColor(vsAverage.ctr_vs_average)}`}>
              {vsAverage.ctr_vs_average >= 0 ? '+' : ''}{vsAverage.ctr_vs_average.toFixed(1)}%
              {getPerformanceIcon(vsAverage.ctr_vs_average)}
            </div>
          </div>

          {/* Average View Duration */}
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-600 mb-1">Average View Duration</p>
            <p className="text-2xl font-bold text-gray-900">{formatDuration(metrics.average_view_duration_seconds)}</p>
            <div className={`text-sm font-medium mt-1 ${getPerformanceColor(vsAverage.view_duration_vs_average)}`}>
              {vsAverage.view_duration_vs_average >= 0 ? '+' : ''}{vsAverage.view_duration_vs_average.toFixed(1)}%
              {getPerformanceIcon(vsAverage.view_duration_vs_average)}
            </div>
          </div>

          {/* Total Views */}
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-600 mb-1">Total Views</p>
            <p className="text-2xl font-bold text-gray-900">{formatNumber(metrics.views)}</p>
            <div className="text-sm text-gray-500 mt-1">
              Lifetime
            </div>
          </div>
        </div>

        {/* Data Quality Indicator */}
        {analyticsData.data_quality_score < 1 && (
          <div className="mt-4 text-sm text-gray-500 text-center">
            Data Quality: {(analyticsData.data_quality_score * 100).toFixed(0)}%
          </div>
        )}
      </div>
    </div>
  );
};

export default VideoAnalytics;