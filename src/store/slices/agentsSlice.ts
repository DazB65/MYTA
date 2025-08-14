import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Agent, AgentStatus } from '../../types';

interface AgentsState {
  agents: Record<string, Agent>;
  loading: boolean;
  error: string | null;
}

const defaultAgents: Agent[] = [
  {
    id: 'boss_agent',
    name: 'Boss Agent',
    type: 'boss_agent',
    status: 'online',
    capabilities: ['coordination', 'strategy', 'overview'],
    description: 'Coordinates all specialist agents and provides strategic oversight',
    lastActive: new Date()
  },
  {
    id: 'content_analysis',
    name: 'Content Analyst',
    type: 'content_analysis',
    status: 'online',
    capabilities: ['video_analysis', 'performance_metrics', 'content_optimization'],
    description: 'Analyzes video content performance and provides optimization recommendations',
    lastActive: new Date()
  },
  {
    id: 'audience_insights',
    name: 'Audience Expert',
    type: 'audience_insights',
    status: 'online',
    capabilities: ['demographic_analysis', 'engagement_patterns', 'audience_growth'],
    description: 'Provides deep insights into audience behavior and growth opportunities',
    lastActive: new Date()
  },
  {
    id: 'seo_discoverability',
    name: 'SEO Specialist',
    type: 'seo_discoverability',
    status: 'online',
    capabilities: ['keyword_optimization', 'search_ranking', 'discoverability'],
    description: 'Optimizes content for search and improves discoverability',
    lastActive: new Date()
  },
  {
    id: 'monetization_strategy',
    name: 'Revenue Optimizer',
    type: 'monetization_strategy',
    status: 'online',
    capabilities: ['revenue_analysis', 'monetization_strategies', 'financial_optimization'],
    description: 'Analyzes revenue streams and suggests monetization improvements',
    lastActive: new Date()
  },
  {
    id: 'competitive_analysis',
    name: 'Market Analyst',
    type: 'competitive_analysis',
    status: 'online',
    capabilities: ['competitor_tracking', 'market_trends', 'benchmarking'],
    description: 'Tracks competitors and identifies market opportunities',
    lastActive: new Date()
  }
];

const initialState: AgentsState = {
  agents: defaultAgents.reduce((acc, agent) => ({ ...acc, [agent.id]: agent }), {}),
  loading: false,
  error: null,
};

const agentsSlice = createSlice({
  name: 'agents',
  initialState,
  reducers: {
    updateAgentStatus: (state, action: PayloadAction<{ agentId: string; status: AgentStatus }>) => {
      const { agentId, status } = action.payload;
      if (state.agents[agentId]) {
        state.agents[agentId].status = status;
        state.agents[agentId].lastActive = new Date();
      }
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
  },
});

export const { updateAgentStatus, setLoading, setError } = agentsSlice.actions;
export default agentsSlice.reducer;