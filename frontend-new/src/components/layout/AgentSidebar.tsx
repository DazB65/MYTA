import ChatInterface from '@/components/chat/ChatInterface'
import QuickActions from '@/components/agent/QuickActions'
import AgentHeader from '@/components/agent/AgentHeader'
import InsightsPanel from '@/components/agent/InsightsPanel'
import OAuthConnection from '@/components/oauth/OAuthConnection'

export default function AgentSidebar() {
  return (
    <aside className="w-80 xl:w-96 bg-background-secondary border-l border-white/10 flex flex-col h-screen">
      {/* Agent Header */}
      <div className="flex-shrink-0">
        <AgentHeader />
      </div>
      
      {/* Scrollable Content Area */}
      <div className="flex-1 flex flex-col min-h-0">
        {/* Insights Section */}
        <div className="px-4 flex-shrink-0">
          <div className="text-sm font-semibold text-dark-400 mb-3 uppercase tracking-wider">
            Insights
          </div>
          <InsightsPanel />
        </div>
        
        {/* OAuth Connection */}
        <div className="px-4 mt-6 flex-shrink-0">
          <OAuthConnection variant="sidebar" />
        </div>
        
        {/* Quick Actions */}
        <div className="px-4 mt-6 flex-shrink-0">
          <div className="text-sm font-semibold text-dark-400 mb-3 uppercase tracking-wider">
            Quick Actions
          </div>
          <QuickActions />
        </div>
        
        {/* Chat Interface - Takes remaining space */}
        <div className="flex-1 px-4 mt-6 flex flex-col min-h-0">
          <div className="text-sm font-semibold text-dark-400 mb-3 uppercase tracking-wider flex-shrink-0">
            Ask Your Agent
          </div>
          <div className="flex-1 min-h-0 pb-4">
            <ChatInterface />
          </div>
        </div>
      </div>
    </aside>
  )
}