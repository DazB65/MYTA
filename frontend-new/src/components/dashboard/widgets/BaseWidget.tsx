import React from 'react';
import Card from '../../common/Card';
import LoadingSpinner from '../../common/LoadingSpinner';

export interface BaseWidgetProps {
  title: string;
  loading?: boolean;
  error?: string;
  className?: string;
  children?: React.ReactNode;
  height?: string;
  onRefresh?: () => void;
}

const BaseWidget: React.FC<BaseWidgetProps> = ({
  title,
  loading = false,
  error,
  className = '',
  children,
  height = 'h-96',
  onRefresh
}) => {
  return (
    <Card className={`w-full ${height} overflow-hidden shadow-sm ${className}`}>
      <div className="px-4 py-3 border-b border-gray-100 flex justify-between items-center">
        <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
        {onRefresh && (
          <button
            onClick={onRefresh}
            className="p-1 hover:bg-gray-100 rounded-full transition-colors"
            disabled={loading}
          >
            <svg
              className={`w-5 h-5 text-gray-500 ${loading ? 'animate-spin' : ''}`}
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
              />
            </svg>
          </button>
        )}
      </div>
      <div className="p-4 h-full">
        {loading ? (
          <div className="flex items-center justify-center h-full">
            <LoadingSpinner size="lg" />
          </div>
        ) : error ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <svg
              className="w-12 h-12 text-red-400 mb-3"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
            <p className="text-gray-600">{error}</p>
          </div>
        ) : (
          children
        )}
      </div>
    </Card>
  );
};

export default BaseWidget;