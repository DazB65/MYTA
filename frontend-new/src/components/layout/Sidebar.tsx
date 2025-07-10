import { NavLink } from 'react-router-dom'
import { LayoutDashboard, Tv, Building2, Clapperboard, Settings } from 'lucide-react'
import { cn } from '@/utils'

const navigation = [
  {
    name: 'Dashboard',
    href: '/dashboard',
    icon: LayoutDashboard,
  },
  {
    name: 'Channel',
    href: '/channel',
    icon: Tv,
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
  return (
    <div className="h-20 bg-background-tertiary/95 backdrop-blur-md border border-white/20 group rounded-2xl shadow-2xl relative z-40 animate-float-bottom">
      <div className="flex items-center h-full overflow-hidden px-4">
        {/* Logo */}
        <div className="flex items-center justify-center h-full px-4 border-r border-white/10 flex-shrink-0">
          <div className="flex items-center gap-3 min-w-0">
            <div className="w-8 h-8 rounded-lg bg-primary-600/20 flex items-center justify-center flex-shrink-0">
              <img
                src="/assets/images/CM Logo White.svg"
                alt="CreatorMate"
                className="w-6 h-6"
              />
            </div>
            <span className="font-bold text-base whitespace-nowrap bg-gradient-to-r from-primary-400 to-white bg-clip-text text-transparent">
              CreatorMate
            </span>
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
                  'flex items-center gap-2 px-4 py-3 rounded-xl transition-all duration-200',
                  'hover:bg-primary-600/10 hover:border-b-4 hover:border-primary-500',
                  'text-dark-400 hover:text-white',
                  'transform hover:scale-105 relative overflow-hidden',
                  'min-w-[48px] min-h-[48px] justify-start',
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
        <div className="border-l border-white/10 pl-4 flex-shrink-0">
          <div className="flex items-center justify-center">
            <div className="w-6 h-6 rounded-full bg-primary-600/20 flex items-center justify-center">
              <div className="w-2 h-2 bg-primary-400 rounded-full animate-pulse"></div>
            </div>
            <span className="ml-2 text-sm text-dark-400 whitespace-nowrap">
              Online
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}