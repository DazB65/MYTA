import React from 'react';
import { Card, CardContent, Typography, Box, Stack } from '@mui/material';
import { AnalyticsData } from '../../types';
import VisibilityIcon from '@mui/icons-material/Visibility';
import PeopleIcon from '@mui/icons-material/People';
import VideoLibraryIcon from '@mui/icons-material/VideoLibrary';
import MonetizationOnIcon from '@mui/icons-material/MonetizationOn';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import HealthAndSafetyIcon from '@mui/icons-material/HealthAndSafety';

interface MetricsCardsProps {
  data: AnalyticsData;
}

const MetricsCards: React.FC<MetricsCardsProps> = ({ data }) => {
  const formatNumber = (num: number): string => {
    if (num >= 1000000) {
      return `${(num / 1000000).toFixed(1)}M`;
    } else if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}K`;
    }
    return num.toString();
  };

  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  const metrics = [
    {
      title: 'Total Views',
      value: formatNumber(data.totalViews),
      icon: <VisibilityIcon />,
      color: '#70B4FF',
    },
    {
      title: 'Subscribers',
      value: formatNumber(data.totalSubscribers),
      icon: <PeopleIcon />,
      color: '#E475A3',
    },
    {
      title: 'Total Videos',
      value: data.totalVideos.toString(),
      icon: <VideoLibraryIcon />,
      color: '#10b981',
    },
    {
      title: 'Channel Health',
      value: `${data.healthScore}%`,
      icon: <HealthAndSafetyIcon />,
      color: data.healthScore >= 80 ? '#10b981' : data.healthScore >= 60 ? '#f59e0b' : '#ef4444',
    },
    {
      title: 'Monthly Revenue',
      value: formatCurrency(data.revenueMetrics.total),
      icon: <MonetizationOnIcon />,
      color: '#f59e0b',
    },
    {
      title: 'Growth Rate',
      value: `+${data.subscriberGrowth.rate}%`,
      icon: <TrendingUpIcon />,
      color: '#6366f1',
    },
  ];

  return (
    <Box
      sx={{
        display: 'grid',
        gridTemplateColumns: {
          xs: '1fr',
          sm: 'repeat(2, 1fr)',
          lg: 'repeat(3, 1fr)',
        },
        gap: 3,
      }}
    >
      {metrics.map((metric) => (
        <Card
          key={metric.title}
          sx={{
            transition: 'all 0.3s ease',
            '&:hover': {
              transform: 'translateY(-2px)',
              boxShadow: 3,
            },
          }}
        >
          <CardContent sx={{ p: 3 }}>
            <Stack direction="row" alignItems="center" justifyContent="space-between">
              <Box>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  {metric.title}
                </Typography>
                <Typography variant="h4" sx={{ fontWeight: 700 }}>
                  {metric.value}
                </Typography>
              </Box>
              <Box
                sx={{
                  p: 2,
                  borderRadius: 2,
                  bgcolor: `${metric.color}20`,
                  color: metric.color,
                }}
              >
                {metric.icon}
              </Box>
            </Stack>
          </CardContent>
        </Card>
      ))}
    </Box>
  );
};

export default MetricsCards;