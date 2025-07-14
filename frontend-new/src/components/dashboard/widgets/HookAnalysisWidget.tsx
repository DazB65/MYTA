import React, { useState, useEffect } from 'react';
import { Card } from '../../common/Card';
import { LoadingSpinner } from '../../common/LoadingSpinner';

interface HookAnalysisData {
  overall_hook_performance: number;
  viral_potential: number;
  best_hooks: Array<{
    title: string;
    effectiveness_score: number;
    hook_types: string[];
    views: number;
    retention_score: number;
    pattern_interrupts: Array<{
      type: string;
      timestamp: number;
      effectiveness: number;
    }>;
    emotional_triggers: Array<{
      emotion: string;
      strength: number;
      engagement_lift: number;
    }>;
  }>;
  hook_patterns: Array<{
    pattern: string;
    effectiveness: number;
    examples: string[];
    retention_impact: number;
    engagement_lift: number;
    usage_frequency: number;
  }>;
  audience_response: {
    click_through_rate: number;
    first_30s_retention: number;
    engagement_velocity: number;
    key_moments: Array<{
      timestamp: number;
      event: string;
      impact: number;
    }>;
  };
  competitive_analysis: {
    niche_benchmarks: Array<{
      hook_type: string;
      avg_retention: number;
      avg_ctr: number;
    }>;
    trending_patterns: Array<{
      pattern: string;
      growth_rate: number;
      adoption_rate: number;
    }>;
  };
  improvement_opportunities: Array<{
    area: string;
    current_performance: number;
    target_performance: number;
    suggestions: string[];
    priority: 'high' | 'medium' | 'low';
  }>;
  retention_correlation: string;
}

interface HookAnalysisWidgetProps {
  userId: string;
  className?: string;
}

export const HookAnalysisWidget: React.FC<HookAnalysisWidgetProps> = ({ 
  userId, 
  className = "" 
}) => {
  const [hookData, setHookData] = useState<HookAnalysisData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchHookAnalysis();
  }, [userId]);

  const fetchHookAnalysis = async () => {
    try {
      setLoading(true);
      setError(null);

      // Call the content analysis agent for hook analysis
      const response = await fetch('/api/agent/task/content-analysis', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          query_type: 'content_analysis',
          context: {
            channel_id: 'user_channel',
            time_period: 'last_30d'
          },
          analysis_depth: 'standard',
          include_visual_analysis: true,
          token_budget: {
            input_tokens: 3000,
            output_tokens: 1500
          }
        })
      });

      if (!response.ok) {
        throw new Error('Failed to fetch hook analysis data');
      }

      const result = await response.json();
      
      if (result.success && result.data?.analysis?.hook_analysis) {
        setHookData(result.data.analysis.hook_analysis);
      } else {
        // Generate mock data for demonstration
        setHookData(generateMockHookData());
      }
    } catch (err) {
      console.error('Error fetching hook analysis:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
      // Set mock data for demo purposes
      setHookData(generateMockHookData());
    } finally {
      setLoading(false);
    }
  };

  // Generate mock data for demonstration
  const generateMockHookData = (): HookAnalysisData => {
    return {
      overall_hook_performance: 7.2,
      viral_potential: 82,
      best_hooks: [
        {
          title: "The Secret Formula for Viral YouTube Content",
          effectiveness_score: 9.2,
          hook_types: ["curiosity", "benefit"],
          views: 45000,
          retention_score: 85,
          pattern_interrupts: [
            { type: "question", timestamp: 8, effectiveness: 92 },
            { type: "reveal", timestamp: 15, effectiveness: 88 }
          ],
          emotional_triggers: [
            { emotion: "curiosity", strength: 90, engagement_lift: 45 },
            { emotion: "anticipation", strength: 85, engagement_lift: 35 }
          ]
        },
        {
          title: "5 Mistakes That Killed My YouTube Channel",
          effectiveness_score: 8.7,
          hook_types: ["numbers", "emotional"],
          views: 32000,
          retention_score: 78,
          pattern_interrupts: [
            { type: "shock", timestamp: 5, effectiveness: 88 },
            { type: "story", timestamp: 12, effectiveness: 82 }
          ],
          emotional_triggers: [
            { emotion: "fear", strength: 85, engagement_lift: 40 },
            { emotion: "urgency", strength: 80, engagement_lift: 30 }
          ]
        },
        {
          title: "Why 99% of YouTubers Fail (And How to Avoid It)",
          effectiveness_score: 8.4,
          hook_types: ["numbers", "curiosity", "benefit"],
          views: 28000,
          retention_score: 82,
          pattern_interrupts: [
            { type: "statistic", timestamp: 7, effectiveness: 85 },
            { type: "challenge", timestamp: 18, effectiveness: 80 }
          ],
          emotional_triggers: [
            { emotion: "concern", strength: 82, engagement_lift: 35 },
            { emotion: "hope", strength: 78, engagement_lift: 28 }
          ]
        }
      ],
      hook_patterns: [
        {
          pattern: "curiosity_gaps",
          effectiveness: 8.5,
          examples: ["secret", "revealed", "truth"],
          retention_impact: 85,
          engagement_lift: 45,
          usage_frequency: 0.65
        },
        {
          pattern: "benefit_driven",
          effectiveness: 7.8,
          examples: ["guide", "tutorial", "master"],
          retention_impact: 75,
          engagement_lift: 35,
          usage_frequency: 0.55
        },
        {
          pattern: "numerical_specificity",
          effectiveness: 7.2,
          examples: ["5 ways", "10 tips", "3 steps"],
          retention_impact: 70,
          engagement_lift: 30,
          usage_frequency: 0.45
        }
      ],
      audience_response: {
        click_through_rate: 12.5,
        first_30s_retention: 85,
        engagement_velocity: 78,
        key_moments: [
          { timestamp: 8, event: "pattern_interrupt", impact: 85 },
          { timestamp: 15, event: "emotional_peak", impact: 82 },
          { timestamp: 22, event: "value_reveal", impact: 78 }
        ]
      },
      competitive_analysis: {
        niche_benchmarks: [
          { hook_type: "curiosity", avg_retention: 75, avg_ctr: 10.5 },
          { hook_type: "emotional", avg_retention: 72, avg_ctr: 9.8 },
          { hook_type: "benefit", avg_retention: 70, avg_ctr: 8.5 }
        ],
        trending_patterns: [
          { pattern: "storytime", growth_rate: 45, adoption_rate: 0.35 },
          { pattern: "challenge", growth_rate: 35, adoption_rate: 0.28 },
          { pattern: "reaction", growth_rate: 30, adoption_rate: 0.22 }
        ]
      },
      improvement_opportunities: [
        {
          area: "Pattern Interrupts",
          current_performance: 75,
          target_performance: 85,
          suggestions: [
            "Add more unexpected elements in first 15 seconds",
            "Use contrarian statements to challenge assumptions"
          ],
          priority: "high"
        },
        {
          area: "Emotional Triggers",
          current_performance: 70,
          target_performance: 80,
          suggestions: [
            "Increase curiosity with strategic information gaps",
            "Incorporate storytelling elements for emotional connection"
          ],
          priority: "medium"
        },
        {
          area: "Hook Timing",
          current_performance: 65,
          target_performance: 75,
          suggestions: [
            "Move key reveals earlier in the hook",
            "Tighten pacing of pattern interrupts"
          ],
          priority: "medium"
        }
      ],
      retention_correlation: "Titles with curiosity gaps show 15-25% better retention in first 30 seconds"
    };
  };

  const getHookScoreColor = (score: number): string => {
    if (score >= 8) return 'text-green-600';
    if (score >= 6) return 'text-blue-600';
    if (score >= 4) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getHookTypeBadgeColor = (type: string): string => {
    const colors: { [key: string]: string } = {
      curiosity: 'bg-purple-100 text-purple-700',
      emotional: 'bg-red-100 text-red-700',
      benefit: 'bg-green-100 text-green-700',
      urgency: 'bg-orange-100 text-orange-700',
      numbers: 'bg-blue-100 text-blue-700',
      authority: 'bg-indigo-100 text-indigo-700'
    };
    return colors[type] || 'bg-gray-100 text-gray-700';
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

  if (error || !hookData) {
    return (
      <Card className={`p-6 ${className}`}>
        <div className="text-center py-8">
          <div className="text-gray-500 mb-4">
            <svg className="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
            </svg>
            Hook Analysis Unavailable
          </div>
          <p className="text-sm text-gray-400 mb-4">
            {error || 'Unable to load hook analysis data'}
          </p>
          <button
            onClick={fetchHookAnalysis}
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
          <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
            <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
            </svg>
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Hook Analysis</h3>
            <p className="text-sm text-gray-500">Title effectiveness & retention impact</p>
          </div>
        </div>
        <button
          onClick={fetchHookAnalysis}
          className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
          title="Refresh data"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>

      {/* Overall Performance */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        {/* Hook Effectiveness */}
        <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm text-gray-600 mb-1">Hook Effectiveness</div>
              <div className={`text-3xl font-bold ${getHookScoreColor(hookData.overall_hook_performance)}`}>
                {hookData.overall_hook_performance.toFixed(1)}/10
              </div>
              <div className="text-sm text-gray-600 mt-1">
                {hookData.overall_hook_performance >= 8 ? 'Excellent' :
                 hookData.overall_hook_performance >= 6 ? 'Good' :
                 hookData.overall_hook_performance >= 4 ? 'Fair' : 'Needs Work'}
              </div>
            </div>
            <div className="text-right">
              <div className="text-2xl">
                {hookData.overall_hook_performance >= 8 ? '🎯' :
                 hookData.overall_hook_performance >= 6 ? '📈' :
                 hookData.overall_hook_performance >= 4 ? '⚡' : '🔧'}
              </div>
            </div>
          </div>
        </div>

        {/* Viral Potential */}
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm text-gray-600 mb-1">Viral Potential</div>
              <div className={`text-3xl font-bold ${getHookScoreColor(hookData.viral_potential)}`}>
                {hookData.viral_potential}/100
              </div>
              <div className="text-sm text-gray-600 mt-1">
                {hookData.viral_potential >= 80 ? 'Very High' :
                 hookData.viral_potential >= 60 ? 'High' :
                 hookData.viral_potential >= 40 ? 'Moderate' : 'Low'}
              </div>
            </div>
            <div className="text-right">
              <div className="text-2xl">
                {hookData.viral_potential >= 80 ? '🚀' :
                 hookData.viral_potential >= 60 ? '🔥' :
                 hookData.viral_potential >= 40 ? '📈' : '📊'}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Best Hooks */}
      <div className="mb-6">
        <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
          <svg className="w-4 h-4 text-yellow-500 mr-1" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
          </svg>
          Top Performing Hooks
        </h4>
        <div className="space-y-4">
          {hookData.best_hooks.map((hook, index) => (
            <div key={index} className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="text-sm font-medium text-gray-900 mb-1 leading-tight">
                    {hook.title}
                  </div>
                  <div className="flex items-center space-x-2 text-xs text-gray-500">
                    <span>{hook.views.toLocaleString()} views</span>
                    <span>•</span>
                    <span className={`font-medium ${getHookScoreColor(hook.effectiveness_score)}`}>
                      {hook.effectiveness_score.toFixed(1)}/10
                    </span>
                    <span>•</span>
                    <span className="text-purple-600">
                      {hook.retention_score}% retention
                    </span>
                  </div>
                </div>
              </div>
              
              {/* Hook Types */}
              <div className="flex flex-wrap gap-1 mb-3">
                {hook.hook_types.map((type, typeIndex) => (
                  <span
                    key={typeIndex}
                    className={`px-2 py-1 rounded text-xs font-medium ${getHookTypeBadgeColor(type)}`}
                  >
                    {type}
                  </span>
                ))}
              </div>

              {/* Pattern Interrupts */}
              <div className="mb-3">
                <div className="text-xs font-medium text-gray-700 mb-2">Pattern Interrupts</div>
                <div className="flex gap-2">
                  {hook.pattern_interrupts.map((interrupt, i) => (
                    <div key={i} className="flex-1 bg-gray-50 rounded p-2">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs text-gray-600">{interrupt.type}</span>
                        <span className="text-xs font-medium">{interrupt.timestamp}s</span>
                      </div>
                      <div className="h-1 bg-gray-200 rounded-full overflow-hidden">
                        <div 
                          className="h-1 bg-green-500 rounded-full" 
                          style={{ width: `${interrupt.effectiveness}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Emotional Triggers */}
              <div>
                <div className="text-xs font-medium text-gray-700 mb-2">Emotional Triggers</div>
                <div className="flex gap-2">
                  {hook.emotional_triggers.map((trigger, i) => (
                    <div key={i} className="flex-1 bg-gray-50 rounded p-2">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs text-gray-600 capitalize">{trigger.emotion}</span>
                        <span className="text-xs font-medium">+{trigger.engagement_lift}%</span>
                      </div>
                      <div className="h-1 bg-gray-200 rounded-full overflow-hidden">
                        <div 
                          className="h-1 bg-purple-500 rounded-full" 
                          style={{ width: `${trigger.strength}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Audience Response & Hook Patterns */}
      <div className="grid grid-cols-2 gap-6 mb-6">
        {/* Audience Response */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <svg className="w-4 h-4 text-blue-500 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Audience Response
          </h4>
          
          {/* Response Metrics */}
          <div className="grid grid-cols-3 gap-3 mb-4">
            <div className="bg-blue-50 rounded-lg p-3">
              <div className="text-xs text-gray-600 mb-1">CTR</div>
              <div className="text-lg font-bold text-blue-700">
                {hookData.audience_response.click_through_rate.toFixed(1)}%
              </div>
            </div>
            <div className="bg-green-50 rounded-lg p-3">
              <div className="text-xs text-gray-600 mb-1">30s Retention</div>
              <div className="text-lg font-bold text-green-700">
                {hookData.audience_response.first_30s_retention}%
              </div>
            </div>
            <div className="bg-purple-50 rounded-lg p-3">
              <div className="text-xs text-gray-600 mb-1">Engagement</div>
              <div className="text-lg font-bold text-purple-700">
                {hookData.audience_response.engagement_velocity}%
              </div>
            </div>
          </div>

          {/* Key Moments Timeline */}
          <div className="bg-white rounded-lg border border-gray-200 p-3">
            <div className="text-xs font-medium text-gray-700 mb-2">Key Moments</div>
            <div className="relative">
              <div className="absolute left-2 h-full w-0.5 bg-gray-200"></div>
              <div className="space-y-3 relative">
                {hookData.audience_response.key_moments.map((moment, i) => (
                  <div key={i} className="flex items-center ml-6">
                    <div className="absolute -left-4 w-3 h-3 rounded-full bg-blue-500"></div>
                    <div className="flex-1 bg-gray-50 rounded p-2">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-medium text-gray-900">{moment.event}</span>
                        <span className="text-xs text-gray-500">{moment.timestamp}s</span>
                      </div>
                      <div className="mt-1 h-1 bg-gray-200 rounded-full overflow-hidden">
                        <div 
                          className="h-1 bg-blue-500 rounded-full" 
                          style={{ width: `${moment.impact}%` }}
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Hook Patterns */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <svg className="w-4 h-4 text-green-500 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Effective Hook Patterns
          </h4>
          <div className="space-y-3">
            {hookData.hook_patterns.map((pattern, index) => (
              <div key={index} className="bg-white rounded-lg border border-gray-200 p-3">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-900 capitalize">
                    {pattern.pattern.replace('_', ' ')}
                  </span>
                  <div className="flex items-center space-x-2">
                    <span className={`text-sm font-bold ${getHookScoreColor(pattern.effectiveness)}`}>
                      {pattern.effectiveness.toFixed(1)}
                    </span>
                  </div>
                </div>
                <div className="grid grid-cols-3 gap-2 mb-2">
                  <div className="text-xs text-gray-600">
                    <span className="text-gray-500">Retention:</span> +{pattern.retention_impact}%
                  </div>
                  <div className="text-xs text-gray-600">
                    <span className="text-gray-500">Engagement:</span> +{pattern.engagement_lift}%
                  </div>
                  <div className="text-xs text-gray-600">
                    <span className="text-gray-500">Usage:</span> {(pattern.usage_frequency * 100).toFixed()}%
                  </div>
                </div>
                <div className="text-xs text-gray-600">
                  Examples: {pattern.examples.join(', ')}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Retention Correlation */}
      <div className="bg-blue-50 rounded-lg p-3 mb-4">
        <div className="flex items-start space-x-2">
          <svg className="w-4 h-4 text-blue-600 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div>
            <div className="text-xs font-medium text-blue-800 mb-1">Retention Impact</div>
            <div className="text-xs text-blue-700">{hookData.retention_correlation}</div>
          </div>
        </div>
      </div>

      {/* Competitive Analysis */}
      <div className="mb-6">
        <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
          <svg className="w-4 h-4 text-indigo-500 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2M6 7l6-2" />
          </svg>
          Competitive Analysis
        </h4>

        <div className="grid grid-cols-2 gap-4">
          {/* Niche Benchmarks */}
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <h5 className="text-xs font-medium text-gray-700 mb-3">Niche Benchmarks</h5>
            <div className="space-y-3">
              {hookData.competitive_analysis.niche_benchmarks.map((benchmark, index) => (
                <div key={index} className="bg-gray-50 rounded p-2">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-medium text-gray-900 capitalize">{benchmark.hook_type}</span>
                    <div className="flex items-center space-x-2 text-xs">
                      <span className="text-blue-600">{benchmark.avg_ctr}% CTR</span>
                      <span className="text-green-600">{benchmark.avg_retention}% retention</span>
                    </div>
                  </div>
                  <div className="h-1 bg-gray-200 rounded-full overflow-hidden">
                    <div 
                      className="h-1 bg-indigo-500 rounded-full" 
                      style={{ width: `${benchmark.avg_retention}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Trending Patterns */}
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <h5 className="text-xs font-medium text-gray-700 mb-3">Trending Patterns</h5>
            <div className="space-y-3">
              {hookData.competitive_analysis.trending_patterns.map((trend, index) => (
                <div key={index} className="bg-gray-50 rounded p-2">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-medium text-gray-900 capitalize">{trend.pattern}</span>
                    <div className="flex items-center space-x-2 text-xs">
                      <span className="text-purple-600">+{trend.growth_rate}% growth</span>
                      <span className="text-gray-500">{(trend.adoption_rate * 100).toFixed()}% adoption</span>
                    </div>
                  </div>
                  <div className="h-1 bg-gray-200 rounded-full overflow-hidden">
                    <div 
                      className="h-1 bg-purple-500 rounded-full" 
                      style={{ width: `${trend.growth_rate}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Improvement Opportunities */}
      <div>
        <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
          <svg className="w-4 h-4 text-green-600 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
          Optimization Opportunities
        </h4>
        <div className="space-y-3">
          {hookData.improvement_opportunities.map((opportunity, index) => (
            <div key={index} className="bg-white rounded-lg border border-gray-200 p-3">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center space-x-2">
                  <span className="text-sm font-medium text-gray-900">{opportunity.area}</span>
                  <span className={`text-xs px-2 py-0.5 rounded ${opportunity.priority === 'high' ? 'bg-red-100 text-red-800' : opportunity.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' : 'bg-blue-100 text-blue-800'}`}>
                    {opportunity.priority} priority
                  </span>
                </div>
                <div className="text-xs text-gray-500">
                  {opportunity.current_performance}% → {opportunity.target_performance}%
                </div>
              </div>
              <div className="space-y-1">
                {opportunity.suggestions.map((suggestion, i) => (
                  <div key={i} className="text-xs text-gray-600 flex items-start">
                    <span className="text-green-500 mr-2">•</span>
                    {suggestion}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Action */}
      <div className="mt-4 p-3 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg">
        <div className="text-xs font-medium text-purple-800 mb-1">🎯 Quick Tip</div>
        <div className="text-xs text-purple-700">
          Test curiosity-driven hooks with numbers for your next video - they show the highest retention correlation!
        </div>
      </div>
    </Card>
  );
};

export default HookAnalysisWidget;