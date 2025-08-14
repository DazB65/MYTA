import React from 'react';
import { Box, Typography, Stack } from '@mui/material';
import { useSelector } from 'react-redux';
import { RootState } from '../../store';
import MetricsCards from './MetricsCards';
import ChannelHealthChart from './ChannelHealthChart';
import RevenueChart from './RevenueChart';
import SubscriberGrowthChart from './SubscriberGrowthChart';

const AnalyticsOverview: React.FC = () => {
  const { data, isConnected } = useSelector((state: RootState) => state.analytics);

  if (!isConnected) {
    return (
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <Typography variant="h5" sx={{ mb: 2 }}>
          Connect Your YouTube Channel
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Connect your YouTube channel to view detailed analytics and insights.
        </Typography>
      </Box>
    );
  }

  return (
    <Stack spacing={4}>
      <Box>
        <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
          Analytics Overview
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Comprehensive insights into your YouTube channel performance
        </Typography>
      </Box>

      <MetricsCards data={data} />

      <Box
        sx={{
          display: 'grid',
          gridTemplateColumns: {
            xs: '1fr',
            lg: 'repeat(2, 1fr)',
          },
          gap: 3,
        }}
      >
        <ChannelHealthChart healthScore={data.healthScore} />
        <RevenueChart revenueMetrics={data.revenueMetrics} />
      </Box>

      <SubscriberGrowthChart subscriberGrowth={data.subscriberGrowth} />
    </Stack>
  );
};

export default AnalyticsOverview;