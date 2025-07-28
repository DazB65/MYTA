import React, { useState, useEffect } from 'react';
import Card from '../../common/Card';
import LoadingSpinner from '../../common/LoadingSpinner';

interface CommunityHealthData {
  overall_health_score: number;
  engagement_metrics: {
    total_comments: number;
    avg_likes_per_comment: number;
    total_engagement: number;
    engagement_rate: number;
  };
  community_responsiveness: {
    creator_response_rate: number;
    avg_response_time: string;
    community_self_moderation: string;
  };
  content_quality_indicators: {
    spam_percentage: number;
    negativity_percentage: number;
    constructive_feedback_rate: number;
  };
  growth_indicators: {
    recent_activity_rate: number;
    new_commenter_rate: number;
    returning_viewer_engagement: string;
  };
  sentiment_analysis: {
    overall_sentiment: number;
    sentiment_breakdown: {
      positive: number;
      neutral: number;
      negative: number;
    };
    key_topics: Array<{
      topic: string;
      sentiment: number;
      frequency: number;
    }>;
    sentiment_trends: {
      trending_up: string[];
      trending_down: string[];
    };
  };
  collaboration_insights: {
    potential_score: number;
    collaboration_suggestions: Array<{
      channel: string;
      compatibility: number;
      reason: string;
      type: string;
    }>;
    audience_overlap: Array<{
      niche: string;
      overlap_percentage: number;
      potential: 'high' | 'medium' | 'low';
    }>;
    ideal_collaborator_profile: {
      size_range: string;
      content_type: string;
      audience_match: number;
    };
  };
  health_rating: string;
  improvement_areas: Array<{
    area: string;
    priority: 'high' | 'medium' | 'low';
    suggestion: string;
  }>;
  strengths: Array<{
    strength: string;
    impact: 'high' | 'medium' | 'low';
    details: string;
  }>;
}

interface CommunityHealthWidgetProps {
  userId: string;
  className?: string;
}

export const CommunityHealthWidget: React.FC<CommunityHealthWidgetProps> = ({ 
  userId, 
  className = "" 
}) => {
  const [healthData, setHealthData] = useState<CommunityHealthData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchCommunityHealth();
  }, [userId]);

  const fetchCommunityHealth = async () => {
    try {
      setLoading(true);
      setError(null);

      // Call the audience insights agent for community health data
      const response = await fetch('/api/agent/task/audience-insights', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          query_type: 'audience_insights',
          context: {
            channel_id: 'user_channel',
            time_period: 'last_30d'
          },
          analysis_depth: 'deep',
          include_sentiment_analysis: true,
          include_collaboration_analysis: true,
          include_community_health: true,
          token_budget: {
            input_tokens: 4000,
            output_tokens: 2000
          }
        })
      });

      if (!response.ok) {
        throw new Error('Failed to fetch community health data');
      }

      const result = await response.json();
      
      if (result.success && result.data?.analysis?.sentiment_analysis?.community_health) {
        setHealthData(result.data.analysis.sentiment_analysis.community_health);
      } else {
        throw new Error('Invalid response format');
      }
    } catch (err) {
      console.error('Error fetching community health:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const getHealthColor = (score: number): string => {
    if (score >= 80) return 'text-green-600';
    if (score >= 70) return 'text-blue-600';
    if (score >= 60) return 'text-yellow-600';
    if (score >= 50) return 'text-orange-600';
    return 'text-red-600';
  };

  const getHealthBgColor = (score: number): string => {
    if (score >= 80) return 'bg-green-100';
    if (score >= 70) return 'bg-blue-100';
    if (score >= 60) return 'bg-yellow-100';
    if (score >= 50) return 'bg-orange-100';
    return 'bg-red-100';
  };

  const formatPercentage = (value: number): string => {
    return `${value.toFixed(1)}%`;
  };

  if (loading) {
    return (
      <Card className={`p-6 ${className}`}>
        <div className="flex items-center justify-center h-64">
          <LoadingSpinner size="lg" />
        </div>
      </Card>
    );
  }

  if (error || !healthData) {
    return (
      <Card className={`p-6 ${className}`}>
        <div className="text-center py-8">
          <div className="text-gray-500 mb-4">
            <svg className="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Community Health Unavailable
          </div>
          <p className="text-sm text-gray-400 mb-4">
            {error || 'Unable to load community health data'}
          </p>
          <button
            onClick={fetchCommunityHealth}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </Card>
    );
  }

  return (
    <Card className={`p-6 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
            <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Community Health</h3>
            <p className="text-sm text-gray-500">Audience engagement & community metrics</p>
          </div>
        </div>
        <button
          onClick={fetchCommunityHealth}
          className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
          title="Refresh data"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>

      {/* Overall Health Score */}
      <div className={`rounded-lg p-4 mb-6 ${getHealthBgColor(healthData.overall_health_score)}`}>
        <div className="flex items-center justify-between">
          <div>
            <div className="text-sm text-gray-600 mb-1">Overall Health Score</div>
            <div className={`text-3xl font-bold ${getHealthColor(healthData.overall_health_score)}`}>
              {healthData.overall_health_score}/100
            </div>
            <div className="text-sm text-gray-600 mt-1">
              {healthData.health_rating}
            </div>
          </div>
          <div className="text-right">
            <div className={`text-2xl ${getHealthColor(healthData.overall_health_score)}`}>
              {healthData.overall_health_score >= 80 ? '🌟' : 
               healthData.overall_health_score >= 60 ? '👍' : 
               healthData.overall_health_score >= 40 ? '📈' : '⚠️'}
            </div>
          </div>
        </div>
      </div>

      {/* Sentiment Analysis */}
      <div className="mb-6">
        <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
          <svg className="w-4 h-4 text-indigo-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Sentiment Analysis
        </h4>
        
        {/* Sentiment Score and Breakdown */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="bg-indigo-50 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-600">Overall Sentiment</span>
              <div className={`text-2xl font-bold ${getHealthColor(healthData.sentiment_analysis.overall_sentiment)}`}>
                {healthData.sentiment_analysis.overall_sentiment}/100
              </div>
            </div>
            <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
              <div 
                className="h-2 bg-indigo-500 rounded-full" 
                style={{ width: `${healthData.sentiment_analysis.overall_sentiment}%` }}
              />
            </div>
          </div>
          
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-xs text-gray-500">Positive</span>
                <span className="text-sm font-medium text-green-600">
                  {formatPercentage(healthData.sentiment_analysis.sentiment_breakdown.positive)}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-gray-500">Neutral</span>
                <span className="text-sm font-medium text-blue-600">
                  {formatPercentage(healthData.sentiment_analysis.sentiment_breakdown.neutral)}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-gray-500">Negative</span>
                <span className="text-sm font-medium text-red-600">
                  {formatPercentage(healthData.sentiment_analysis.sentiment_breakdown.negative)}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Key Topics */}
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <h5 className="text-sm font-medium text-gray-700 mb-3">Key Discussion Topics</h5>
          <div className="space-y-2">
            {healthData.sentiment_analysis.key_topics.slice(0, 3).map((topic, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className="text-xs text-gray-600">{topic.topic}</span>
                  <span className={`text-xs px-2 py-0.5 rounded ${topic.sentiment >= 70 ? 'bg-green-100 text-green-800' : topic.sentiment >= 40 ? 'bg-blue-100 text-blue-800' : 'bg-red-100 text-red-800'}`}>
                    {topic.sentiment >= 70 ? 'Positive' : topic.sentiment >= 40 ? 'Neutral' : 'Negative'}
                  </span>
                </div>
                <span className="text-xs text-gray-500">{topic.frequency} mentions</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Collaboration Insights */}
      <div className="mb-6">
        <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
          <svg className="w-4 h-4 text-purple-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          Collaboration Opportunities
        </h4>

        {/* Collaboration Score and Suggestions */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="bg-purple-50 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-600">Collaboration Potential</span>
              <div className={`text-2xl font-bold ${getHealthColor(healthData.collaboration_insights.potential_score)}`}>
                {healthData.collaboration_insights.potential_score}/100
              </div>
            </div>
            <div className="text-xs text-gray-600">
              Ideal Partner Profile:
              <ul className="mt-1 space-y-1">
                <li>• Size: {healthData.collaboration_insights.ideal_collaborator_profile.size_range}</li>
                <li>• Type: {healthData.collaboration_insights.ideal_collaborator_profile.content_type}</li>
                <li>• Match: {formatPercentage(healthData.collaboration_insights.ideal_collaborator_profile.audience_match)}</li>
              </ul>
            </div>
          </div>

          <div className="bg-gray-50 rounded-lg p-4">
            <h5 className="text-sm font-medium text-gray-700 mb-2">Audience Overlap</h5>
            <div className="space-y-2">
              {healthData.collaboration_insights.audience_overlap.slice(0, 3).map((overlap, index) => (
                <div key={index} className="flex justify-between items-center">
                  <span className="text-xs text-gray-600">{overlap.niche}</span>
                  <div className="flex items-center space-x-2">
                    <span className="text-xs font-medium">{formatPercentage(overlap.overlap_percentage)}</span>
                    <span className={`text-xs px-2 py-0.5 rounded ${overlap.potential === 'high' ? 'bg-green-100 text-green-800' : overlap.potential === 'medium' ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800'}`}>
                      {overlap.potential}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Collaboration Suggestions */}
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <h5 className="text-sm font-medium text-gray-700 mb-3">Suggested Collaborations</h5>
          <div className="space-y-3">
            {healthData.collaboration_insights.collaboration_suggestions.slice(0, 3).map((suggestion, index) => (
              <div key={index} className="flex items-start space-x-3">
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-900">{suggestion.channel}</span>
                    <span className={`text-xs px-2 py-0.5 rounded ${suggestion.compatibility >= 80 ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'}`}>
                      {formatPercentage(suggestion.compatibility)} match
                    </span>
                  </div>
                  <p className="text-xs text-gray-600 mt-1">{suggestion.reason}</p>
                  <span className="text-xs text-purple-600 mt-1 block">{suggestion.type}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        {/* Engagement Metrics */}
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="text-sm font-medium text-gray-700 mb-3">Engagement</h4>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-xs text-gray-500">Total Comments</span>
              <span className="text-sm font-medium">{healthData.engagement_metrics.total_comments.toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-xs text-gray-500">Avg Likes/Comment</span>
              <span className="text-sm font-medium">{healthData.engagement_metrics.avg_likes_per_comment.toFixed(1)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-xs text-gray-500">Engagement Rate</span>
              <span className="text-sm font-medium">{formatPercentage(healthData.engagement_metrics.engagement_rate)}</span>
            </div>
          </div>
        </div>

        {/* Content Quality */}
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="text-sm font-medium text-gray-700 mb-3">Content Quality</h4>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-xs text-gray-500">Constructive</span>
              <span className="text-sm font-medium text-green-600">{formatPercentage(healthData.content_quality_indicators.constructive_feedback_rate)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-xs text-gray-500">Spam</span>
              <span className="text-sm font-medium text-red-600">{formatPercentage(healthData.content_quality_indicators.spam_percentage)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-xs text-gray-500">Negativity</span>
              <span className="text-sm font-medium text-orange-600">{formatPercentage(healthData.content_quality_indicators.negativity_percentage)}</span>
            </div>
          </div>
        </div>

        {/* Responsiveness */}
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="text-sm font-medium text-gray-700 mb-3">Responsiveness</h4>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-xs text-gray-500">Response Rate</span>
              <span className="text-sm font-medium">{formatPercentage(healthData.community_responsiveness.creator_response_rate)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-xs text-gray-500">Self-Moderation</span>
              <span className="text-sm font-medium">{healthData.community_responsiveness.community_self_moderation}</span>
            </div>
          </div>
        </div>

        {/* Growth */}
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="text-sm font-medium text-gray-700 mb-3">Growth</h4>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-xs text-gray-500">Recent Activity</span>
              <span className="text-sm font-medium">{formatPercentage(healthData.growth_indicators.recent_activity_rate)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-xs text-gray-500">New Commenters</span>
              <span className="text-sm font-medium">{formatPercentage(healthData.growth_indicators.new_commenter_rate)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-xs text-gray-500">Returning Viewers</span>
              <span className="text-sm font-medium">{healthData.growth_indicators.returning_viewer_engagement}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Strengths and Improvements */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Strengths */}
        {healthData.strengths.length > 0 && (
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
              <svg className="w-4 h-4 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Community Strengths
            </h4>
            <div className="space-y-3">
              {healthData.strengths.map((strength, index) => (
                <div key={index} className="border-l-2 border-green-500 pl-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-900">{strength.strength}</span>
                    <span className={`text-xs px-2 py-0.5 rounded ${strength.impact === 'high' ? 'bg-green-100 text-green-800' : strength.impact === 'medium' ? 'bg-blue-100 text-blue-800' : 'bg-yellow-100 text-yellow-800'}`}>
                      {strength.impact} impact
                    </span>
                  </div>
                  <p className="text-xs text-gray-600 mt-1">{strength.details}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Improvement Areas */}
        {healthData.improvement_areas.length > 0 && (
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
              <svg className="w-4 h-4 text-orange-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
              Areas for Improvement
            </h4>
            <div className="space-y-3">
              {healthData.improvement_areas.map((area, index) => (
                <div key={index} className="border-l-2 border-orange-500 pl-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-900">{area.area}</span>
                    <span className={`text-xs px-2 py-0.5 rounded ${area.priority === 'high' ? 'bg-red-100 text-red-800' : area.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' : 'bg-blue-100 text-blue-800'}`}>
                      {area.priority} priority
                    </span>
                  </div>
                  <p className="text-xs text-gray-600 mt-1">{area.suggestion}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </Card>
  );
};

export default CommunityHealthWidget;