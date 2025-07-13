import { NavLink } from 'react-router-dom'
import { LayoutDashboard, Building2, Clapperboard, Settings, LogOut } from 'lucide-react'
import { cn } from '@/utils'
import { useOAuthStore } from '@/store/oauthStore'

const navigation = [
  {
    name: 'Dashboard',
    href: '/dashboard',
    icon: LayoutDashboard,
  },
  {
    name: 'Pillars',
    href: '/pillars',
    icon: Building2,
  },
  {
    name: 'Videos',
    href: '/videos',
    icon: Clapperboard,
  },
  {
    name: 'Settings',
    href: '/settings',
    icon: Settings,
  },
]

export default function Sidebar() {
  const { isAuthenticated, revokeToken } = useOAuthStore()

  const handleLogout = async () => {
    if (!isAuthenticated) return
    
    const confirmed = confirm('Are you sure you want to logout from YouTube? You will need to reconnect to access video analytics.')
    if (confirmed) {
      await revokeToken()
      // Clear any other user data if needed
      localStorage.removeItem('creatormate_user_id')
      window.location.href = '/'
    }
  }

  return (
    <div className="h-16 bg-purple-900/95 backdrop-blur-md border border-purple-500/30 group rounded-2xl shadow-2xl relative z-40 animate-float-bottom">
      <div className="flex items-center h-full overflow-hidden px-4">
        {/* Logo */}
        <div className="flex items-center justify-center h-full px-4 border-r border-purple-400/20 flex-shrink-0">
          <div className="flex items-center gap-3 min-w-0">
            <img
              src="/assets/images/CM Text White.svg"
              alt="CreatorMate"
              className="h-8 w-auto"
            />
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex items-center px-4 space-x-2">
          {navigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.href}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-2 px-3 py-2 rounded-xl transition-all duration-200',
                  'hover:bg-primary-600/10 hover:border-b-4 hover:border-primary-500',
                  'text-dark-400 hover:text-white',
                  'transform hover:scale-105 relative overflow-hidden',
                  'min-w-[40px] min-h-[40px] justify-start',
                  isActive && 'active bg-primary-600/20 border-b-4 border-primary-500 text-white'
                )
              }
            >
              <item.icon className="w-5 h-5 flex-shrink-0" />
              <span className="whitespace-nowrap overflow-hidden font-medium text-sm">
                {item.name}
              </span>
            </NavLink>
          ))}
        </nav>
        
        {/* Status section */}
        <div className="border-l border-purple-400/20 pl-4 flex-shrink-0 flex items-center gap-3">
          <div className="flex items-center">
            <div className="w-6 h-6 rounded-full bg-primary-600/20 flex items-center justify-center">
              <div className="w-2 h-2 bg-primary-400 rounded-full animate-pulse"></div>
            </div>
            <span className="ml-2 text-sm text-dark-400 whitespace-nowrap">
              Online
            </span>
          </div>
          
          {/* Logout button */}
          {isAuthenticated && (
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 px-2 py-1 rounded-lg transition-all duration-200 hover:bg-red-500/20 text-red-300 hover:text-red-200 border border-red-500/30 hover:border-red-400"
              title="Logout from YouTube"
            >
              <LogOut className="w-4 h-4" />
              <span className="text-xs font-medium">Logout</span>
            </button>
          )}
        </div>
      </div>
    </div>
  )
}