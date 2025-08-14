import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Stack,
  Chip,
  LinearProgress,
} from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import LightbulbIcon from '@mui/icons-material/Lightbulb';
import WarningIcon from '@mui/icons-material/Warning';

const AgentInsights: React.FC = () => {
  const mockInsights = [
    {
      id: '1',
      agentName: 'Content Analyst',
      type: 'content_performance',
      title: 'Video Performance Spike Detected',
      description: 'Your latest video is performing 150% better than average. Consider creating similar content.',
      confidence: 92,
      priority: 'high' as const,
      timestamp: new Date(),
    },
    {
      id: '2',
      agentName: 'SEO Specialist',
      type: 'seo_opportunity',
      title: 'Keyword Optimization Opportunity',
      description: 'Adding "YouTube Analytics" to your video titles could increase discoverability by 35%.',
      confidence: 78,
      priority: 'medium' as const,
      timestamp: new Date(),
    },
    {
      id: '3',
      agentName: 'Revenue Optimizer',
      type: 'monetization_tip',
      title: 'Revenue Stream Diversification',
      description: 'Consider adding channel memberships - similar channels see 20% revenue increase.',
      confidence: 85,
      priority: 'medium' as const,
      timestamp: new Date(),
    },
  ];

  const getInsightIcon = (type: string) => {
    switch (type) {
      case 'content_performance': return <TrendingUpIcon />;
      case 'seo_opportunity': return <LightbulbIcon />;
      case 'monetization_tip': return <TrendingUpIcon />;
      default: return <LightbulbIcon />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'error';
      case 'medium': return 'warning';
      case 'low': return 'info';
      default: return 'default';
    }
  };

  return (
    <Card>
      <CardContent sx={{ p: 3 }}>
        <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
          Latest Agent Insights
        </Typography>
        
        <Stack spacing={3}>
          {mockInsights.map((insight) => (
            <Box
              key={insight.id}
              sx={{
                p: 2,
                border: '1px solid',
                borderColor: 'divider',
                borderRadius: 2,
                bgcolor: 'background.paper',
              }}
            >
              <Stack spacing={2}>
                <Box sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
                  <Stack direction="row" alignItems="center" spacing={2}>
                    <Box sx={{ color: 'primary.main' }}>
                      {getInsightIcon(insight.type)}
                    </Box>
                    <Box>
                      <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                        {insight.title}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        by {insight.agentName}
                      </Typography>
                    </Box>
                  </Stack>
                  <Chip
                    label={insight.priority}
                    size="small"
                    color={getPriorityColor(insight.priority) as any}
                    variant="outlined"
                    sx={{ textTransform: 'capitalize' }}
                  />
                </Box>

                <Typography variant="body2" color="text.secondary">
                  {insight.description}
                </Typography>

                <Box>
                  <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ mb: 1 }}>
                    <Typography variant="caption" color="text.secondary">
                      Confidence Score
                    </Typography>
                    <Typography variant="caption" sx={{ fontWeight: 600 }}>
                      {insight.confidence}%
                    </Typography>
                  </Stack>
                  <LinearProgress
                    variant="determinate"
                    value={insight.confidence}
                    sx={{
                      height: 6,
                      borderRadius: 3,
                      bgcolor: 'grey.200',
                      '& .MuiLinearProgress-bar': {
                        borderRadius: 3,
                      },
                    }}
                  />
                </Box>
              </Stack>
            </Box>
          ))}
        </Stack>
      </CardContent>
    </Card>
  );
};

export default AgentInsights;