import React, { useEffect, useState } from 'react';
import { apiClient } from '../api/client';
import { Challenge } from '../types';
import { Target, Search, Filter, CheckCircle2 } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Challenges: React.FC = () => {
  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [filterDifficulty, setFilterDifficulty] = useState<string>('all');
  const [filterCategory, setFilterCategory] = useState<string>('all');
  const [search, setSearch] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchChallenges = async () => {
      try {
        const response = await apiClient.get('/challenges/');
        setChallenges(response.data.challenges || []);
      } catch (err) {
        console.error('Failed to load challenges', err);
      } finally {
        setLoading(false);
      }
    };
    fetchChallenges();
  }, []);

  const filtered = challenges.filter((ch) => {
    if (filterDifficulty !== 'all' && ch.difficulty !== filterDifficulty) return false;
    if (filterCategory !== 'all' && ch.category !== filterCategory) return false;
    if (
      search &&
      !ch.title.toLowerCase().includes(search.toLowerCase()) &&
      !ch.subtitle.toLowerCase().includes(search.toLowerCase()) &&
      !ch.vulnerability_type.toLowerCase().includes(search.toLowerCase())
    ) {
      return false;
    }
    return true;
  });

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto font-mono">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-[#ff2244] tracking-wider flex items-center gap-3">
            <Target className="w-7 h-7 text-[#ff2244]" /> STARK CYBER RANGE // ALL 30 TARGET LABS
          </h1>
          <p className="text-xs text-[#8b949e] mt-1">
            Progressive target laboratory across SQLite, MySQL, PostgreSQL, and MSSQL environments.
          </p>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-[#0d1117] border border-[#ff224444] rounded-2xl p-4 flex flex-wrap items-center justify-between gap-4 font-mono text-xs shadow-[0_0_20px_rgba(255,34,68,0.1)]">
        <div className="flex items-center space-x-3 flex-1 min-w-[240px]">
          <Search className="w-4 h-4 text-[#8b949e]" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search target by title, vulnerability type..."
            className="bg-[#010409] border border-[#30363d] text-[#ffd700] px-3 py-2 rounded-xl w-full focus:outline-none focus:border-[#ff2244]"
          />
        </div>

        <div className="flex items-center space-x-3">
          <Filter className="w-4 h-4 text-[#8b949e]" />
          <select
            value={filterDifficulty}
            onChange={(e) => setFilterDifficulty(e.target.value)}
            className="bg-[#010409] border border-[#30363d] text-[#e6edf3] px-3 py-2 rounded-xl focus:outline-none"
          >
            <option value="all">All Difficulties</option>
            <option value="easy">Easy (100 XP)</option>
            <option value="medium">Medium (200 XP)</option>
            <option value="hard">Hard (300 XP)</option>
            <option value="expert">Expert (500 XP)</option>
          </select>

          <select
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
            className="bg-[#010409] border border-[#30363d] text-[#e6edf3] px-3 py-2 rounded-xl focus:outline-none"
          >
            <option value="all">All Categories</option>
            <option value="Core SQL Injection">Core SQL Injection</option>
            <option value="Advanced/Specialized">Advanced/Specialized</option>
            <option value="Database-Specific">Database-Specific</option>
          </select>
        </div>
      </div>

      {/* Challenge Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.map((ch) => (
          <Link
            key={ch.challenge_id}
            to={`/challenge/${ch.challenge_id}`}
            className={`block bg-[#0d1117] border rounded-2xl p-6 transition-all duration-200 hover:-translate-y-1 relative group ${
              ch.completed
                ? 'border-[#00ff8866] bg-[#00ff8803]'
                : 'border-[#30363d] hover:border-[#ff2244aa] hover:shadow-[0_0_25px_rgba(255,34,68,0.2)]'
            }`}
          >
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-bold text-[#ff2244] tracking-widest">
                MISSION {ch.challenge_id.toString().padStart(2, '0')}
              </span>
              <span
                className={`text-[10px] px-2.5 py-0.5 rounded font-bold uppercase ${
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

            <h3 className="text-lg font-bold text-[#e6edf3] mb-1 group-hover:text-[#ffd700] transition-colors">
              {ch.subtitle}
            </h3>

            <div className="text-xs text-[#6e7681] mb-3">{ch.category} • {ch.db_type}</div>

            <p className="text-xs text-[#8b949e] line-clamp-3 mb-6 leading-relaxed">
              {ch.description}
            </p>

            <div className="flex items-center justify-between pt-4 border-t border-[#21262d] text-xs">
              <span className="text-[#ffd700] font-bold">+{ch.points} XP</span>
              {ch.completed ? (
                <span className="text-[#00ff88] font-bold flex items-center gap-1">
                  <CheckCircle2 className="w-4 h-4" /> SOLVED
                </span>
              ) : (
                <span className="text-[#ff2244] group-hover:underline flex items-center gap-1 font-bold">
                  Engage Target &rarr;
                </span>
              )}
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};
