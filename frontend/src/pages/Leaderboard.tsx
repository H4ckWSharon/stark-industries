import React, { useEffect, useState } from 'react';
import { apiClient } from '../api/client';
import { LeaderboardEntry } from '../types';
import { Trophy, Award, Medal, Shield } from 'lucide-react';

export const Leaderboard: React.FC = () => {
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const response = await apiClient.get('/challenges/leaderboard/all');
        setLeaderboard(response.data.leaderboard || []);
      } catch (err) {
        console.error('Failed to load leaderboard', err);
      } finally {
        setLoading(false);
      }
    };
    fetchLeaderboard();
  }, []);

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-8">
      <div className="text-center space-y-2">
        <Trophy className="w-12 h-12 text-[#ffd700] mx-auto animate-bounce" />
        <h1 className="text-3xl font-bold text-[#e6edf3] tracking-wider">STARK SQL LEADERBOARD</h1>
        <p className="text-xs text-[#8b949e]">Top security researchers and students ranked by total XP.</p>
      </div>

      <div className="bg-[#0d1117] border border-[#30363d] rounded-2xl overflow-hidden shadow-2xl">
        <div className="bg-[#161b22] px-6 py-4 border-b border-[#30363d] grid grid-cols-12 text-xs font-bold text-[#8b949e]">
          <span className="col-span-2">RANK</span>
          <span className="col-span-4">OPERATOR</span>
          <span className="col-span-3">LEVEL & TITLE</span>
          <span className="col-span-3 text-right">XP SCORED</span>
        </div>

        <div className="divide-y divide-[#21262d] font-mono text-sm">
          {leaderboard.map((entry) => (
            <div
              key={entry.rank}
              className={`px-6 py-4 grid grid-cols-12 items-center transition-colors ${
                entry.rank === 1
                  ? 'bg-[#ffd70008]'
                  : entry.rank === 2
                  ? 'bg-[#c0c0c008]'
                  : entry.rank === 3
                  ? 'bg-[#cd7f3208]'
                  : 'hover:bg-[#161b22]'
              }`}
            >
              <div className="col-span-2 flex items-center space-x-2">
                {entry.rank === 1 && <Medal className="w-5 h-5 text-[#ffd700]" />}
                {entry.rank === 2 && <Medal className="w-5 h-5 text-[#c0c0c0]" />}
                {entry.rank === 3 && <Medal className="w-5 h-5 text-[#cd7f32]" />}
                <span className="font-bold text-[#e6edf3]">#{entry.rank}</span>
              </div>

              <div className="col-span-4 font-bold text-[#00d4ff] flex items-center space-x-2">
                <span>{entry.username}</span>
              </div>

              <div className="col-span-3 text-xs space-y-0.5">
                <div className="text-[#e6edf3]">LVL {entry.level}</div>
                <div className="text-[#8b949e]">{entry.rank_title}</div>
              </div>

              <div className="col-span-3 text-right font-bold text-[#ffd700] text-base">
                {entry.xp} <span className="text-xs text-[#8b949e]">XP</span>
              </div>
            </div>
          ))}

          {leaderboard.length === 0 && !loading && (
            <div className="p-8 text-center text-[#8b949e] text-xs">
              No students logged on leaderboard yet. Complete challenges to gain XP!
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
