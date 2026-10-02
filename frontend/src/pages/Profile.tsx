import React from 'react';
import { useAuthStore } from '../store/authStore';
import { User as UserIcon, Shield, Award, Calendar, CheckCircle2 } from 'lucide-react';

export const Profile: React.FC = () => {
  const { user } = useAuthStore();

  if (!user) return null;

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-[#e6edf3] tracking-wider flex items-center gap-3">
          <UserIcon className="w-7 h-7 text-[#00d4ff]" /> OPERATOR PROFILE
        </h1>
        <p className="text-xs text-[#8b949e] mt-1">Stark Industries SQL Cyber Range Operator Identity.</p>
      </div>

      <div className="bg-[#0d1117] border border-[#00d4ff44] rounded-2xl p-8 shadow-2xl space-y-6">
        <div className="flex items-center space-x-6">
          <div className="w-20 h-20 rounded-2xl bg-gradient-to-tr from-[#00d4ff] to-[#0066cc] p-1 flex items-center justify-center shadow-[0_0_30px_rgba(0,212,255,0.3)]">
            <div className="w-full h-full bg-[#0a0a0f] rounded-[14px] flex items-center justify-center">
              <UserIcon className="w-10 h-10 text-[#00d4ff]" />
            </div>
          </div>

          <div className="space-y-1">
            <h2 className="text-2xl font-bold text-[#e6edf3]">{user.username}</h2>
            <div className="text-xs text-[#00d4ff] font-semibold">
              {user.rank} • Level {user.level}
            </div>
            {user.is_admin && (
              <span className="inline-block text-[10px] bg-[#ff224422] text-[#ff2244] border border-[#ff2244] px-2 py-0.5 rounded font-bold">
                INSTRUCTOR / ADMIN
              </span>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-6 border-t border-[#21262d] font-mono">
          <div className="bg-[#161b22] border border-[#30363d] p-4 rounded-xl">
            <div className="text-xs text-[#8b949e]">TOTAL XP</div>
            <div className="text-2xl font-bold text-[#ffd700] mt-1">{user.xp} XP</div>
          </div>

          <div className="bg-[#161b22] border border-[#30363d] p-4 rounded-xl">
            <div className="text-xs text-[#8b949e]">CURRENT LEVEL</div>
            <div className="text-2xl font-bold text-[#00d4ff] mt-1">LEVEL {user.level}</div>
          </div>

          <div className="bg-[#161b22] border border-[#30363d] p-4 rounded-xl">
            <div className="text-xs text-[#8b949e]">RANK TITLE</div>
            <div className="text-lg font-bold text-[#00ff88] mt-1">{user.rank}</div>
          </div>
        </div>
      </div>
    </div>
  );
};
