import React from 'react';
import { Card, CardContent, Typography, Box, Stack } from '@mui/material';
import { PieChart } from '@mui/x-charts/PieChart';

interface RevenueChartProps {
  revenueMetrics: {
    total: number;
    rpm: number;
    cpm: number;
  };
}

const RevenueChart: React.FC<RevenueChartProps> = ({ revenueMetrics }) => {
  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  // Mock revenue breakdown data
  const revenueData = [
    { id: 0, value: 60, label: 'Ad Revenue', color: '#E475A3' },
    { id: 1, value: 25, label: 'Memberships', color: '#70B4FF' },
    { id: 2, value: 10, label: 'Super Chat', color: '#10b981' },
    { id: 3, value: 5, label: 'Other', color: '#f59e0b' },
  ];

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent sx={{ p: 3 }}>
        <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
          Revenue Breakdown
        </Typography>
        
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <Box sx={{ width: '100%', height: 200, mb: 2 }}>
            <PieChart
              series={[
                {
                  data: revenueData,
                  highlightScope: { fade: 'global', highlight: 'item' },
                },
              ]}
              height={200}
              slotProps={{
                legend: { 
                  direction: 'horizontal',
                  position: { vertical: 'bottom', horizontal: 'center' }
                },
              }}
            />
          </Box>
          
          <Stack spacing={2} sx={{ width: '100%' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
              <Typography variant="body2" color="text.secondary">
                RPM (Revenue per Mille)
              </Typography>
              <Typography variant="body2" sx={{ fontWeight: 600 }}>
                {formatCurrency(revenueMetrics.rpm)}
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
              <Typography variant="body2" color="text.secondary">
                CPM (Cost per Mille)
              </Typography>
              <Typography variant="body2" sx={{ fontWeight: 600 }}>
                {formatCurrency(revenueMetrics.cpm)}
              </Typography>
            </Box>
          </Stack>
        </Box>
      </CardContent>
    </Card>
  );
};

export default RevenueChart;