import React from 'react';
import { Box, Typography, Stack } from '@mui/material';
import { useSelector } from 'react-redux';
import { RootState } from '../../store';
import AgentCard from './AgentCard';
import AgentInsights from './AgentInsights';

const MultiAgentDashboard: React.FC = () => {
  const { agents } = useSelector((state: RootState) => state.agents);
  const agentList = Object.values(agents);

  return (
    <Stack spacing={4}>
      <Box>
        <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
          AI Agent Dashboard
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Monitor and interact with your specialized AI agents
        </Typography>
      </Box>

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
        {agentList.map((agent) => (
          <AgentCard key={agent.id} agent={agent} />
        ))}
      </Box>

      <AgentInsights />
    </Stack>
  );
};

export default MultiAgentDashboard;