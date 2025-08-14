import React from 'react';
import { Box, Typography, Stack, Card, CardContent, Chip } from '@mui/material';

const ContentManagement: React.FC = () => {
  const mockContent = [
    {
      id: '1',
      title: 'How to Optimize YouTube Thumbnails',
      status: 'published',
      views: 15420,
      publishedAt: '2024-01-15',
      performance: 'high',
    },
    {
      id: '2',
      title: 'YouTube Analytics Deep Dive',
      status: 'draft',
      views: 0,
      publishedAt: null,
      performance: null,
    },
    {
      id: '3',
      title: 'Content Strategy for 2024',
      status: 'scheduled',
      views: 0,
      publishedAt: '2024-01-20',
      performance: null,
    },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'published': return 'success';
      case 'draft': return 'default';
      case 'scheduled': return 'info';
      default: return 'default';
    }
  };

  const getPerformanceColor = (performance: string | null) => {
    switch (performance) {
      case 'high': return 'success';
      case 'medium': return 'warning';
      case 'low': return 'error';
      default: return 'default';
    }
  };

  return (
    <Stack spacing={4}>
      <Box>
        <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
          Content Management
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Manage your video content, strategy planning, and performance tracking
        </Typography>
      </Box>

      <Box
        sx={{
          display: 'grid',
          gridTemplateColumns: {
            xs: '1fr',
            md: 'repeat(2, 1fr)',
            lg: 'repeat(3, 1fr)',
          },
          gap: 3,
        }}
      >
        {mockContent.map((content) => (
          <Card
            key={content.id}
            sx={{
              transition: 'all 0.3s ease',
              '&:hover': {
                transform: 'translateY(-2px)',
                boxShadow: 3,
              },
            }}
          >
            <CardContent sx={{ p: 3 }}>
              <Stack spacing={2}>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  {content.title}
                </Typography>
                
                <Stack direction="row" spacing={1}>
                  <Chip
                    label={content.status}
                    size="small"
                    color={getStatusColor(content.status) as any}
                    variant="outlined"
                    sx={{ textTransform: 'capitalize' }}
                  />
                  {content.performance && (
                    <Chip
                      label={`${content.performance} performance`}
                      size="small"
                      color={getPerformanceColor(content.performance) as any}
                      variant="outlined"
                      sx={{ textTransform: 'capitalize' }}
                    />
                  )}
                </Stack>

                {content.views > 0 && (
                  <Typography variant="body2" color="text.secondary">
                    {content.views.toLocaleString()} views
                  </Typography>
                )}

                {content.publishedAt && (
                  <Typography variant="caption" color="text.secondary">
                    {content.status === 'published' ? 'Published' : 'Scheduled'}: {content.publishedAt}
                  </Typography>
                )}
              </Stack>
            </CardContent>
          </Card>
        ))}
      </Box>
    </Stack>
  );
};

export default ContentManagement;