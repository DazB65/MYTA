import React, { useState } from 'react';
import Card from '@/components/common/Card';
import Button from '@/components/common/Button';
import {
  AlgorithmPerformanceWidget,
  CommunityHealthWidget,
  HookAnalysisWidget
} from '@/components/dashboard/widgets';
import { useUserStore } from '@/store/userStore';

interface MetricCardProps {
  title: string;
  value: string | number;
  change?: number;
  icon: JSX.Element;
}

const MetricCard: React.FC<MetricCardProps> = ({ title, value, change, icon }) => {
  return (
    <Card className="p-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-500">{title}</p>
          <h3 className="text-2xl font-bold mt-1">{value}</h3>
          {change !== undefined && (
            <p className={`text-sm ${change >= 0 ? 'text-green-600' : 'text-red-600'} mt-1`}>
              {change >= 0 ? '+' : ''}{change}%
            </p>
          )}
        </div>
        <div className="text-gray-400">{icon}</div>
      </div>
    </Card>
  );
};

export const EnhancedAnalytics: React.FC = () => {
  const { userId } = useUserStore();
  const [activeTab, setActiveTab] = useState('algorithm');

  // Key Performance Metrics
  const metrics = [
    {
      title: "Algorithm Score",
      value: "82/100",
      change: 5,
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
      )
    },
    {
      title: "Viral Potential",
      value: "85%",
      change: 12,
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      )
    },
    {
      title: "Community Health",
      value: "78/100",
      change: -2,
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      )
    },
    {
      title: "Hook Performance",
      value: "7.8/10",
      change: 8,
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
        </svg>
      )
    }
  ];

  // Time Range Options
  const timeRanges = [
    { label: "7 Days", value: "7d" },
    { label: "30 Days", value: "30d" },
    { label: "90 Days", value: "90d" }
  ];

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Enhanced Analytics</h1>
          <p className="text-sm text-gray-500 mt-1">
            Advanced insights powered by AI analysis
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <div className="inline-flex rounded-md shadow-sm">
            {timeRanges.map((range) => (
              <Button
                key={range.value}
                variant={range.value === "30d" ? "primary" : "ghost"}
                className="px-4"
              >
                {range.label}
              </Button>
            ))}
          </div>
          <Button variant="ghost" className="ml-4">
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Export
          </Button>
        </div>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {metrics.map((metric) => (
          <MetricCard
            key={metric.title}
            title={metric.title}
            value={metric.value}
            change={metric.change}
            icon={metric.icon}
          />
        ))}
      </div>

      {/* Main Content */}
      <div className="w-full">
        <div className="flex space-x-4 mb-6 border-b border-gray-200">
          <button
            onClick={() => setActiveTab('algorithm')}
            className={`pb-2 px-1 font-medium transition-colors ${
              activeTab === 'algorithm'
                ? 'text-primary-600 border-b-2 border-primary-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Algorithm Performance
          </button>
          <button
            onClick={() => setActiveTab('community')}
            className={`pb-2 px-1 font-medium transition-colors ${
              activeTab === 'community'
                ? 'text-primary-600 border-b-2 border-primary-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Community Health
          </button>
          <button
            onClick={() => setActiveTab('hooks')}
            className={`pb-2 px-1 font-medium transition-colors ${
              activeTab === 'hooks'
                ? 'text-primary-600 border-b-2 border-primary-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Hook Analysis
          </button>
        </div>

        <div className="space-y-6">
          {activeTab === 'algorithm' && <AlgorithmPerformanceWidget userId={userId || ''} />}
          {activeTab === 'community' && <CommunityHealthWidget userId={userId || ''} />}
          {activeTab === 'hooks' && <HookAnalysisWidget userId={userId || ''} />}
        </div>
      </div>
    </div>
  );
};

export default EnhancedAnalytics;