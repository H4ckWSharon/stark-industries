import React, { useEffect, useState } from 'react';
import { useAuthStore } from '../store/authStore';
import { apiClient } from '../api/client';
import { UserStats, Challenge } from '../types';
import { AttackMonitor } from '../components/AttackMonitor';
import { ArcReactorLogo } from '../components/ArcReactorLogo';
import { Shield, Target, Award, Activity, ArrowRight, CheckCircle2, Cpu, Zap } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Dashboard: React.FC = () => {
  const { user } = useAuthStore();
  const [stats, setStats] = useState<UserStats | null>(null);
  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, chRes] = await Promise.all([
          apiClient.get('/challenges/stats/me'),
          apiClient.get('/challenges/'),
        ]);
        setStats(statsRes.data);
        setChallenges(chRes.data.challenges || []);
      } catch (err) {
        console.error('Failed to load dashboard data', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full text-[#ff2244] font-mono">
        <Activity className="w-8 h-8 animate-spin mr-3 text-[#ff2244]" /> INITIALIZING STARK HUD TELEMETRY...
      </div>
    );
  }

  const completedCount = stats?.completed || 0;
  const totalCount = stats?.total_challenges || 30;
  const progressPercent = Math.round((completedCount / totalCount) * 100);

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto font-mono">
      {/* Iron Man Hero Telemetry Banner */}
      <div className="bg-gradient-to-r from-[#0d1117] via-[#200a0d] to-[#0d1117] border border-[#ff224455] rounded-3xl p-8 relative overflow-hidden shadow-[0_0_40px_rgba(255,34,68,0.2)]">
        <div className="absolute top-0 right-0 p-8 opacity-15 pointer-events-none">
          <Zap className="w-72 h-72 text-[#ff2244]" />
        </div>

        <div className="relative z-10 space-y-3">
          <div className="flex items-center space-x-3 text-xs text-[#ffd700] font-bold tracking-widest">
            <span className="px-3 py-1 rounded-md bg-[#ff224422] border border-[#ff224444] text-[#ff2244]">MARK VIII HUD</span>
            <span className="flex items-center gap-1.5 text-[#00ff88]">
              <Cpu className="w-4 h-4 animate-pulse" /> JARVIS ONLINE
            </span>
          </div>

          <h1 className="text-3xl font-extrabold text-[#e6edf3] tracking-wide">
            WELCOME BACK, OPERATOR <span className="text-[#ff2244]">{user?.username.toUpperCase()}</span>
          </h1>

          <p className="text-xs text-[#8b949e] max-w-2xl leading-relaxed">
            Stark Industries SQL Cyber Range is online. Execute offensive database operations across 30 progressive challenge labs running inside isolated Docker containers.
          </p>
        </div>
      </div>

      {/* Hot Rod Red & Gold Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-[#0d1117] border border-[#ffd70044] rounded-2xl p-6 shadow-[0_0_20px_rgba(255,215,0,0.15)]">
          <div className="flex items-center justify-between text-[#8b949e] text-xs mb-2">
            <span>STARK XP SCORE</span>
            <Award className="w-5 h-5 text-[#ffd700]" />
          </div>
          <div className="text-3xl font-extrabold text-[#ffd700]">{stats?.xp || 0} XP</div>
          <div className="text-xs text-[#8b949e] mt-2">Rank: <span className="text-[#ff2244] font-bold">{stats?.rank}</span></div>
        </div>

        <div className="bg-[#0d1117] border border-[#00ff8844] rounded-2xl p-6 shadow-[0_0_20px_rgba(0,255,136,0.15)]">
          <div className="flex items-center justify-between text-[#8b949e] text-xs mb-2">
            <span>TARGETS SOLVED</span>
            <CheckCircle2 className="w-5 h-5 text-[#00ff88]" />
          </div>
          <div className="text-3xl font-extrabold text-[#00ff88]">
            {completedCount} <span className="text-lg text-[#8b949e]">/ {totalCount}</span>
          </div>
          <div className="w-full bg-[#161b22] h-2 rounded-full mt-3 overflow-hidden border border-[#30363d]">
            <div className="bg-gradient-to-r from-[#00ff88] to-[#00d4ff] h-full transition-all duration-500" style={{ width: `${progressPercent}%` }} />
          </div>
        </div>

        <div className="bg-[#0d1117] border border-[#ff224444] rounded-2xl p-6 shadow-[0_0_20px_rgba(255,34,68,0.15)]">
          <div className="flex items-center justify-between text-[#8b949e] text-xs mb-2">
            <span>PILOT LEVEL</span>
            <Target className="w-5 h-5 text-[#ff2244]" />
          </div>
          <div className="text-3xl font-extrabold text-[#ff2244]">LEVEL {stats?.level || 1}</div>
          <div className="text-xs text-[#8b949e] mt-2">Success Rate: <span className="text-[#00ff88]">{stats?.success_rate}%</span></div>
        </div>

        <div className="bg-[#0d1117] border border-[#00d4ff44] rounded-2xl p-6 shadow-[0_0_20px_rgba(0,212,255,0.15)]">
          <div className="flex items-center justify-between text-[#8b949e] text-xs mb-2">
            <span>ACTIVE MISSIONS</span>
            <Shield className="w-5 h-5 text-[#00d4ff]" />
          </div>
          <div className="text-3xl font-extrabold text-[#00d4ff]">{stats?.remaining || 30}</div>
          <div className="text-xs text-[#8b949e] mt-2">Ready to capture</div>
        </div>
      </div>

      {/* Main Grid: Challenge Schematics & Attack Monitor */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Recommended Challenges */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-extrabold text-[#e6edf3] tracking-wider flex items-center gap-2">
              <Target className="w-5 h-5 text-[#ff2244]" /> TARGET MISSIONS
            </h2>
            <Link to="/challenges" className="text-xs text-[#ffd700] hover:underline flex items-center gap-1 font-bold">
              View All 30 Schematics <ArrowRight className="w-4 h-4" />
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {challenges.slice(0, 6).map((ch) => (
              <Link
                key={ch.challenge_id}
                to={`/challenge/${ch.challenge_id}`}
                className={`block bg-[#0d1117] border rounded-2xl p-5 transition-all duration-200 hover:-translate-y-1 ${
                  ch.completed
                    ? 'border-[#00ff8866] bg-[#00ff8805]'
                    : 'border-[#30363d] hover:border-[#ff2244aa] hover:shadow-[0_0_25px_rgba(255,34,68,0.2)]'
                }`}
              >
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs text-[#ff2244] font-bold tracking-widest">
                    MISSION {ch.challenge_id.toString().padStart(2, '0')}
                  </span>
                  <span
                    className={`text-[10px] px-2 py-0.5 rounded font-bold uppercase ${
                      ch.difficulty === 'easy'
                        ? 'bg-[#00ff8822] text-[#00ff88] border border-[#00ff8844]'
                        : ch.difficulty === 'medium'
                        ? 'bg-[#ffd70022] text-[#ffd700] border border-[#ffd70044]'
                        : ch.difficulty === 'hard'
                        ? 'bg-[#ff224422] text-[#ff2244] border border-[#ff224444]'
                        : 'bg-[#a371f722] text-[#a371f7] border border-[#a371f744]'
                    }`}
                  >
                    {ch.difficulty}
                  </span>
                </div>

                <h3 className="text-base font-bold text-[#e6edf3] mb-1">{ch.subtitle}</h3>
                <p className="text-xs text-[#8b949e] line-clamp-2 mb-4">{ch.description}</p>

                <div className="flex items-center justify-between text-xs pt-3 border-t border-[#21262d]">
                  <span className="text-[#ffd700] font-bold">+{ch.points} XP</span>
                  <span className="text-[#6e7681]">{ch.db_type}</span>
                  {ch.completed && (
                    <span className="text-[#00ff88] font-bold flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5" /> SOLVED
                    </span>
                  )}
                </div>
              </Link>
            ))}
          </div>
        </div>

        {/* Live Attack Monitor Column */}
        <div className="space-y-6">
          <h2 className="text-base font-extrabold text-[#e6edf3] tracking-wider flex items-center gap-2">
            <Activity className="w-5 h-5 text-[#00d4ff]" /> JARVIS ATTACK MONITOR
          </h2>
          <AttackMonitor />
        </div>
      </div>
    </div>
  );
};
