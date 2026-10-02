import React from 'react';
import { useAuthStore } from '../store/authStore';
import { ArcReactorLogo } from './ArcReactorLogo';
import { LogOut, User as UserIcon, Shield, Cpu } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Navbar: React.FC = () => {
  const { user, logout } = useAuthStore();

  return (
    <nav className="h-16 bg-[#0d1117] border-b border-[#ff224444] px-6 flex items-center justify-between sticky top-0 z-40 shadow-[0_4px_20px_rgba(255,34,68,0.15)]">
      <div className="flex items-center space-x-6">
        <Link to="/">
          <ArcReactorLogo size={42} showText={true} />
        </Link>
      </div>

      <div className="flex items-center space-x-6 font-mono">
        {/* JARVIS Telemetry Badge */}
        <div className="hidden md:flex items-center space-x-2 bg-[#161b22] px-3 py-1.5 rounded-lg border border-[#00d4ff44] text-xs">
          <Cpu className="w-4 h-4 text-[#00d4ff] animate-pulse" />
          <span className="text-[#8b949e]">JARVIS:</span>
          <span className="text-[#00ff88] font-bold">ONLINE</span>
        </div>

        {user && (
          <>
            {/* User XP & Level Badge */}
            <div className="flex items-center space-x-3 bg-gradient-to-r from-[#161b22] to-[#251015] px-4 py-1.5 rounded-xl border border-[#ffd70066] shadow-[0_0_15px_rgba(255,215,0,0.15)]">
              <div className="flex items-center space-x-1.5 text-xs text-[#ffd700]">
                <span className="font-extrabold text-sm">{user.xp}</span>
                <span className="text-[10px] text-[#8b949e]">XP</span>
              </div>
              <div className="w-px h-4 bg-[#ffd70044]" />
              <div className="text-xs text-[#ff2244] font-bold">
                LVL {user.level} • <span className="text-[#ffd700]">{user.rank}</span>
              </div>
            </div>

            {/* Account Info & Logout */}
            <div className="flex items-center space-x-3">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-[#ff2244] to-[#ffd700] p-0.5 shadow-[0_0_12px_rgba(255,34,68,0.3)]">
                <div className="w-full h-full bg-[#0a0a0f] rounded-[10px] flex items-center justify-center">
                  <UserIcon className="w-4 h-4 text-[#ffd700]" />
                </div>
              </div>
              <span className="font-bold text-sm text-[#e6edf3]">{user.username}</span>
              {user.is_admin && (
                <span className="text-[10px] bg-[#ff224422] text-[#ff2244] border border-[#ff2244] px-2 py-0.5 rounded font-bold tracking-wider">
                  JARVIS ADMIN
                </span>
              )}
            </div>

            <button
              onClick={logout}
              className="p-2 text-[#8b949e] hover:text-[#ff2244] hover:bg-[#ff224411] rounded-lg transition-colors"
              title="Logout System"
            >
              <LogOut className="w-5 h-5" />
            </button>
          </>
        )}
      </div>
    </nav>
  );
};
