import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import {
  LayoutDashboard,
  Target,
  Trophy,
  GitBranch,
  User,
  Activity,
  Award
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const { user } = useAuthStore();

  const navItems = [
    { to: '/', label: 'STARK COMMAND', icon: LayoutDashboard },
    { to: '/challenges', label: 'TARGET LABS (30)', icon: Target },
    { to: '/path', label: 'TACTICAL PATHS', icon: GitBranch },
    { to: '/leaderboard', label: 'STARK HALL OF FAME', icon: Trophy },
    { to: '/progress', label: 'ACHIEVEMENTS & XP', icon: Award },
    { to: '/profile', label: 'SUIT PROFILE', icon: User },
  ];


  return (
    <aside className="w-64 bg-[#0d1117] border-r border-[#ff224433] flex flex-col h-[calc(100vh-4rem)] sticky top-16 select-none font-mono">
      <div className="p-4 border-b border-[#21262d] flex items-center space-x-2 text-xs text-[#ff2244] tracking-widest font-bold">
        <Activity className="w-4 h-4 animate-pulse text-[#ff2244]" />
        <span>MARK VIII TELEMETRY</span>
      </div>

      <nav className="flex-1 p-3 space-y-1.5 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              className={({ isActive }) =>
                `flex items-center space-x-3 px-4 py-3 rounded-xl text-xs transition-all duration-200 ${
                  isActive
                    ? 'bg-gradient-to-r from-[#ff224422] to-[#ffd70011] text-[#ffd700] border border-[#ff224466] shadow-[0_0_15px_rgba(255,34,68,0.2)] font-bold'
                    : 'text-[#8b949e] hover:text-[#e6edf3] hover:bg-[#161b22]'
                }`
              }
            >
              <Icon className="w-4 h-4 shrink-0" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      <div className="p-4 border-t border-[#21262d] bg-[#010409]">
        <div className="text-[11px] text-[#8b949e] space-y-1.5">
          <div className="flex justify-between">
            <span>SUIT PROTOCOL:</span>
            <span className="text-[#00ff88] font-bold">ISOLATED DOCKER</span>
          </div>
          <div className="flex justify-between">
            <span>ARMOR STATUS:</span>
            <span className="text-[#ffd700] font-bold">ARC POWERED</span>
          </div>
          <div className="text-[10px] text-[#6e7681] pt-2 border-t border-[#21262d] text-center tracking-wider">
            STARK INDUSTRIES // FOR EDUCATIONAL USE ONLY
          </div>
        </div>
      </div>
    </aside>
  );
};
