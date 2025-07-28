import React, { useState, useEffect } from 'react';
import Card from '../../common/Card';
import LoadingSpinner from '../../common/LoadingSpinner';

interface AlgorithmPerformanceData {
  overall_score: number;
  favorability: string;
  recommendation: string;
  viral_potential: number;
  algorithm_prediction: {
    score: number;
    factors: Array<{
      name: string;
      score: number;
      impact: 'high' | 'medium' | 'low';
    }>;
    risks: Array<{
      issue: string;
      severity: 'high' | 'medium' | 'low';
    }>;
  };
  score_components: {
    engagement_velocity: number;
    retention_strength: number;
    searcher_intent: number;
    topic_momentum: number;
    production_quality: number;
    metadata_strength: number;
  };
  improvement_areas: Array<{
    area: string;
    priority: 'high' | 'medium' | 'low';
    action: string;
  }>;
  metrics_breakdown: {
    ctr_trend: 'up' | 'down' | 'stable';
    retention_trend: 'up' | 'down' | 'stable';
    engagement_trend: 'up' | 'down' | 'stable';
    watch_time_trend: 'up' | 'down' | 'stable';
    growth_trend: 'up' | 'down' | 'stable';
  };
}

interface AlgorithmPerformanceWidgetProps {
  userId: string;
  className?: string;
}

export const AlgorithmPerformanceWidget: React.FC<AlgorithmPerformanceWidgetProps> = ({ 
  userId, 
  className = "" 
}) => {
  const [algorithmData, setAlgorithmData] = useState<AlgorithmPerformanceData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAlgorithmPerformance();
  }, [userId]);

  const fetchAlgorithmPerformance = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch recent analytics data
      const response = await fetch(`/api/agent/insights/${userId}`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch algorithm performance data');
      }

      const result = await response.json();
      
      // Extract algorithm performance from insights or analytics
      if (result.success && result.data?.insights) {
        // Look for algorithm performance in insights
        const algorithmInsight = result.data.insights.find((insight: any) => 
          insight.title?.includes('Algorithm') || insight.content?.includes('algorithm')
        );
        
        if (algorithmInsight) {
          // Parse algorithm data from insight content
          // This would be replaced with direct API call to analytics service
          setAlgorithmData(generateMockAlgorithmData());
        } else {
          setAlgorithmData(generateMockAlgorithmData());
        }
      } else {
        throw new Error('Invalid response format');
      }
    } catch (err) {
      console.error('Error fetching algorithm performance:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
      // Set mock data for demo purposes
      setAlgorithmData(generateMockAlgorithmData());
    } finally {
      setLoading(false);
    }
  };

  // Generate mock data for demonstration
  const generateMockAlgorithmData = (): AlgorithmPerformanceData => {
    return {
      overall_score: 72,
      favorability: "Very Good",
      recommendation: "Algorithm performance is strong with high viral potential",
      viral_potential: 85,
      algorithm_prediction: {
        score: 78,
        factors: [
          { name: 'Engagement Velocity', score: 85, impact: 'high' },
          { name: 'Topic Momentum', score: 82, impact: 'high' },
          { name: 'Production Quality', score: 75, impact: 'medium' }
        ],
        risks: [
          { issue: 'Retention drops after 5 minutes', severity: 'medium' },
          { issue: 'Limited keyword optimization', severity: 'low' }
        ]
      },
      score_components: {
        engagement_velocity: 85,
        retention_strength: 75,
        searcher_intent: 70,
        topic_momentum: 82,
        production_quality: 75,
        metadata_strength: 68
      },
      improvement_areas: [
        { area: 'Hook Strength', priority: 'high', action: 'Add pattern interrupts in first 30 seconds' },
        { area: 'Metadata', priority: 'medium', action: 'Optimize title and description with trending keywords' },
        { area: 'Content Pacing', priority: 'medium', action: 'Adjust content length for optimal retention' }
      ],
      metrics_breakdown: {
        ctr_trend: 'up',
        retention_trend: 'stable',
        engagement_trend: 'up',
        watch_time_trend: 'up',
        growth_trend: 'stable'
      }
    };
  };

  const getScoreColor = (score: number): string => {
    if (score >= 85) return 'text-green-600';
    if (score >= 70) return 'text-blue-600';
    if (score >= 55) return 'text-yellow-600';
    if (score >= 40) return 'text-orange-600';
    return 'text-red-600';
  };

  const getScoreBgColor = (score: number): string => {
    if (score >= 85) return 'bg-green-100';
    if (score >= 70) return 'bg-blue-100';
    if (score >= 55) return 'bg-yellow-100';
    if (score >= 40) return 'bg-orange-100';
    return 'bg-red-100';
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

  if (error || !algorithmData) {
    return (
      <Card className={`p-6 ${className}`}>
        <div className="text-center py-8">
          <div className="text-gray-500 mb-4">
            <svg className="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            Algorithm Performance Unavailable
          </div>
          <p className="text-sm text-gray-400 mb-4">
            {error || 'Unable to load algorithm performance data'}
          </p>
          <button
            onClick={fetchAlgorithmPerformance}
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
          <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
            <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Algorithm Performance</h3>
            <p className="text-sm text-gray-500">YouTube algorithm favorability score</p>
          </div>
        </div>
        <button
          onClick={fetchAlgorithmPerformance}
          className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
          title="Refresh data"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>

      {/* Algorithm Score & Viral Potential */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className={`rounded-lg p-4 ${getScoreBgColor(algorithmData.overall_score)}`}>
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm text-gray-600 mb-1">Algorithm Score</div>
              <div className={`text-3xl font-bold ${getScoreColor(algorithmData.overall_score)}`}>
                {algorithmData.overall_score}/100
              </div>
              <div className="text-sm text-gray-600 mt-1">
                {algorithmData.favorability}
              </div>
            </div>
            <div className="text-right">
              <div className={`text-2xl ${getScoreColor(algorithmData.overall_score)}`}>
                {algorithmData.metrics_breakdown.engagement_trend === 'up' ? '⚡' : 
                 algorithmData.metrics_breakdown.engagement_trend === 'stable' ? '📊' : '📉'}
              </div>
            </div>
          </div>
        </div>

        <div className={`rounded-lg p-4 ${getScoreBgColor(algorithmData.viral_potential)}`}>
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm text-gray-600 mb-1">Viral Potential</div>
              <div className={`text-3xl font-bold ${getScoreColor(algorithmData.viral_potential)}`}>
                {algorithmData.viral_potential}/100
              </div>
              <div className="text-sm text-gray-600 mt-1">
                {algorithmData.viral_potential >= 80 ? 'Excellent' : 
                 algorithmData.viral_potential >= 60 ? 'Good' : 'Needs Work'}
              </div>
            </div>
            <div className="text-right">
              <div className={`text-2xl ${getScoreColor(algorithmData.viral_potential)}`}>
                {algorithmData.viral_potential >= 80 ? '🔥' : 
                 algorithmData.viral_potential >= 60 ? '🚀' : '📈'}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="text-sm text-gray-700 mb-6 p-3 bg-blue-50 rounded-lg">
        {algorithmData.recommendation}
      </div>

      {/* Algorithm Factors */}
      <div className="mb-6">
        <h4 className="text-sm font-medium text-gray-700 mb-4">Algorithm Factors</h4>
        <div className="space-y-3">
          {Object.entries(algorithmData.score_components).map(([component, score]) => {
            const percentage = score;
            const impact = algorithmData.algorithm_prediction.factors.find(
              f => f.name.toLowerCase().includes(component.toLowerCase())
            )?.impact || 'medium';
            
            return (
              <div key={component} className="flex items-center justify-between">
                <div className="flex items-center space-x-3 flex-1">
                  <span className="text-sm text-gray-600 w-32">
                    {component.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                  </span>
                  <div className="flex-1 bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full transition-all duration-300 ${
                        impact === 'high' ? 'bg-green-500' :
                        impact === 'medium' ? 'bg-blue-500' : 'bg-yellow-500'
                      }`}
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-medium text-gray-700">
                      {score}%
                    </span>
                    <span className={`text-xs px-2 py-0.5 rounded ${impact === 'high' ? 'bg-green-100 text-green-800' : impact === 'medium' ? 'bg-blue-100 text-blue-800' : 'bg-yellow-100 text-yellow-800'}`}>
                      {impact}
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Trend Analysis */}
      <div className="mb-6">
        <h4 className="text-sm font-medium text-gray-700 mb-4">Performance Trends</h4>
        <div className="grid grid-cols-2 lg:grid-cols-3 gap-3">
          {Object.entries(algorithmData.metrics_breakdown).map(([metric, trend]) => (
            <div key={metric} className="flex items-center justify-between p-2 rounded-lg bg-gray-50">
              <div className="text-xs text-gray-500">
                {metric.replace('_trend', '').replace('_', ' ').toUpperCase()}
              </div>
              <div className={`flex items-center gap-1 ${trend === 'up' ? 'text-green-600' : trend === 'down' ? 'text-red-600' : 'text-blue-600'}`}>
                {trend === 'up' ? (
                  <>
                    <span className="text-xs font-medium">Rising</span>
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                    </svg>
                  </>
                ) : trend === 'down' ? (
                  <>
                    <span className="text-xs font-medium">Declining</span>
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0v-8m0 8l-8-8-4 4-6-6" />
                    </svg>
                  </>
                ) : (
                  <>
                    <span className="text-xs font-medium">Stable</span>
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14" />
                    </svg>
                  </>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Optimization Recommendations */}
      {algorithmData.improvement_areas.length > 0 && (
        <div className="mb-6">
          <h4 className="text-sm font-medium text-gray-700 mb-4 flex items-center">
            <svg className="w-4 h-4 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            Algorithm Optimization Actions
          </h4>
          <div className="space-y-3">
            {algorithmData.improvement_areas.map((item, index) => (
              <div key={index} className="p-3 bg-white rounded-lg border border-gray-200 flex items-start">
                <div className={`w-2 h-2 mt-1.5 rounded-full mr-3 flex-shrink-0 ${item.priority === 'high' ? 'bg-red-500' : item.priority === 'medium' ? 'bg-yellow-500' : 'bg-blue-500'}`} />
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <h5 className="text-sm font-medium text-gray-900">{item.area}</h5>
                    <span className={`text-xs px-2 py-0.5 rounded ${item.priority === 'high' ? 'bg-red-100 text-red-800' : item.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' : 'bg-blue-100 text-blue-800'}`}>
                      {item.priority} priority
                    </span>
                  </div>
                  <p className="text-xs text-gray-600">{item.action}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action Suggestions */}
      <div className="mt-4 p-3 bg-blue-50 rounded-lg">
        <div className="text-xs font-medium text-blue-800 mb-1">💡 Quick Win</div>
        <div className="text-xs text-blue-700">
          {algorithmData.overall_score < 70 
            ? "Focus on improving CTR with better thumbnails and retention with stronger hooks"
            : "Continue current strategy and test small optimizations to reach the next level"}
        </div>
      </div>
    </Card>
  );
};

export default AlgorithmPerformanceWidget;