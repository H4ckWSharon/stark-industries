import React, { useEffect, useState } from 'react';
import { apiClient } from '../api/client';
import { UserStats } from '../types';
import { Award, CheckCircle2, Circle, Trophy } from 'lucide-react';

export const Progress: React.FC = () => {
  const [stats, setStats] = useState<UserStats | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await apiClient.get('/challenges/stats/me');
        setStats(response.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchStats();
  }, []);

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-[#e6edf3] tracking-wider flex items-center gap-3">
          <Award className="w-7 h-7 text-[#ffd700]" /> PROGRESS & ACHIEVEMENTS
        </h1>
        <p className="text-xs text-[#8b949e] mt-1">Track your XP milestones and unlocked laboratory badges.</p>
      </div>

      {/* Badges Section */}
      <div className="bg-[#0d1117] border border-[#30363d] rounded-2xl p-6 space-y-4">
        <h2 className="text-sm font-bold text-[#00d4ff] tracking-wider uppercase">// EARNED ACHIEVEMENTS</h2>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {(stats?.achievements || []).map((ach) => (
            <div key={ach.id} className="bg-[#161b22] border border-[#ffd70044] p-4 rounded-xl text-center space-y-2">
              <Trophy className="w-8 h-8 text-[#ffd700] mx-auto" />
              <div className="text-xs font-bold text-[#ffd700]">{ach.name}</div>
            </div>
          ))}
          {(!stats?.achievements || stats.achievements.length === 0) && (
            <div className="col-span-4 text-xs text-[#8b949e] p-4 text-center">
              No achievements earned yet. Complete challenges to unlock badges!
            </div>
          )}
        </div>
      </div>

      {/* Challenge Checklist */}
      <div className="bg-[#0d1117] border border-[#30363d] rounded-2xl p-6 space-y-4">
        <h2 className="text-sm font-bold text-[#00d4ff] tracking-wider uppercase">// MISSION TRACKER (30 CHALLENGES)</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 font-mono text-xs">
          {Array.from({ length: 30 }, (_, i) => i + 1).map((chId) => {
            const pr = stats?.progress.find((p) => p.challenge_id === chId);
            const isCompleted = pr?.completed || false;
            return (
              <div
                key={chId}
                className={`p-3 rounded-lg border flex items-center justify-between ${
                  isCompleted
                    ? 'bg-[#00ff8808] border-[#00ff8844] text-[#00ff88]'
                    : 'bg-[#161b22] border-[#30363d] text-[#8b949e]'
                }`}
              >
                <div className="flex items-center space-x-3">
                  {isCompleted ? <CheckCircle2 className="w-4 h-4 text-[#00ff88]" /> : <Circle className="w-4 h-4 text-[#6e7681]" />}
                  <span className="font-bold">MISSION {chId.toString().padStart(2, '0')}</span>
                </div>
                {isCompleted && <span className="font-bold">+{pr?.xp_earned} XP</span>}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
