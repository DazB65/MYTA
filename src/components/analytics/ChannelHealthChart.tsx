import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';
import { Gauge } from '@mui/x-charts/Gauge';

interface ChannelHealthChartProps {
  healthScore: number;
}

const ChannelHealthChart: React.FC<ChannelHealthChartProps> = ({ healthScore }) => {
  const getHealthColor = (score: number): string => {
    if (score >= 80) return '#10b981';
    if (score >= 60) return '#f59e0b';
    return '#ef4444';
  };

  const getHealthStatus = (score: number): string => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Needs Improvement';
  };

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent sx={{ p: 3 }}>
        <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
          Channel Health Score
        </Typography>
        
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <Box sx={{ width: '100%', height: 200, mb: 2 }}>
            <Gauge
              value={healthScore}
              startAngle={-90}
              endAngle={90}
              valueMax={100}
              sx={{
                '& .MuiGauge-valueText': {
                  fontSize: '2rem',
                  fontWeight: 700,
                },
                '& .MuiGauge-valueArc': {
                  fill: getHealthColor(healthScore),
                },
              }}
            />
          </Box>
          
          <Typography 
            variant="h6" 
            sx={{ 
              fontWeight: 600, 
              color: getHealthColor(healthScore),
              mb: 1 
            }}
          >
            {getHealthStatus(healthScore)}
          </Typography>
          
          <Typography variant="body2" color="text.secondary" textAlign="center">
            Based on engagement rate, view velocity, and subscriber retention
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default ChannelHealthChart;