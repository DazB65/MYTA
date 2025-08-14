import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';
import { LineChart } from '@mui/x-charts/LineChart';

interface SubscriberGrowthChartProps {
  subscriberGrowth: {
    net: number;
    rate: number;
  };
}

const SubscriberGrowthChart: React.FC<SubscriberGrowthChartProps> = ({ subscriberGrowth }) => {
  // Mock data for the last 30 days
  const generateMockData = () => {
    const data = [];
    const baseGrowth = subscriberGrowth.net / 30;
    
    for (let i = 0; i < 30; i++) {
      const date = new Date();
      date.setDate(date.getDate() - (29 - i));
      
      // Add some randomness to make it look realistic
      const variation = (Math.random() - 0.5) * baseGrowth * 0.5;
      const growth = Math.max(0, baseGrowth + variation);
      
      data.push({
        date: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
        subscribers: Math.round(growth),
      });
    }
    
    return data;
  };

  const data = generateMockData();
  const xAxisData = data.map(item => item.date);
  const seriesData = data.map(item => item.subscribers);

  return (
    <Card>
      <CardContent sx={{ p: 3 }}>
        <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
          Subscriber Growth (Last 30 Days)
        </Typography>
        
        <Box sx={{ width: '100%', height: 300 }}>
          <LineChart
            xAxis={[{ 
              scaleType: 'point', 
              data: xAxisData,
              tickLabelStyle: {
                fontSize: 12,
              },
            }]}
            series={[
              {
                data: seriesData,
                area: true,
                color: '#E475A3',
                curve: 'monotoneX',
              },
            ]}
            height={300}
            margin={{ left: 60, right: 20, top: 20, bottom: 60 }}
            grid={{ vertical: true, horizontal: true }}
            slotProps={{
              legend: { 
                direction: 'horizontal',
                position: { vertical: 'bottom', horizontal: 'center' }
              },
            }}
          />
        </Box>
        
        <Box sx={{ mt: 2, textAlign: 'center' }}>
          <Typography variant="body2" color="text.secondary">
            Net growth: +{subscriberGrowth.net} subscribers ({subscriberGrowth.rate}% increase)
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default SubscriberGrowthChart;