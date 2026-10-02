import React from 'react';
import { GitBranch, CheckCircle2, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

const LEVELS = [
  { level: 1, name: 'LEVEL 1 — SQL Fundamentals', desc: 'Understanding relational databases, SELECT query structure, and parameters.', challenges: [1] },
  { level: 2, name: 'LEVEL 2 — Basic SQL Injection', desc: 'Single-quote escaping, OR 1=1 boolean short-circuiting, and string comments.', challenges: [1, 15, 17, 18] },
  { level: 3, name: 'LEVEL 3 — Authentication Bypass', desc: 'Bypassing username and password queries without passwords using comments.', challenges: [2] },
  { level: 4, name: 'LEVEL 4 — Data Extraction', desc: 'Error-based leakage with ExtractValue and UNION SELECT column matching.', challenges: [3, 4, 16] },
  { level: 5, name: 'LEVEL 5 — Blind SQL Injection', desc: 'Inferring hidden data via boolean true/false responses and MySQL SLEEP() timing.', challenges: [5, 6] },
  { level: 6, name: 'LEVEL 6 — Advanced Injection', desc: 'Out-of-band callbacks, stacked queries, and stored procedure dynamic SQL.', challenges: [7, 9, 10, 11, 12, 13] },
  { level: 7, name: 'LEVEL 7 — Application-Layer Injection', desc: 'ORDER BY identifiers, JSON REST APIs, HTTP headers, and Cookie values.', challenges: [14, 19, 20, 21] },
  { level: 8, name: 'LEVEL 8 — Filter / WAF Concepts', desc: 'HTTP Parameter Pollution, signature WAF evasions, and non-recursive filter bypass.', challenges: [22, 23, 24] },
  { level: 9, name: 'LEVEL 9 — Second-Order Attacks', desc: 'Stored payload execution in secondary processing routines and authorization checks.', challenges: [8, 25] },
  { level: 10, name: 'LEVEL 10 — Database-Specific SQLi', desc: 'Dedicated SQLite, MySQL 8, PostgreSQL 15, and MSSQL 2022 dialect deep dives.', challenges: [26, 27, 28, 29, 30] },
];

export const LearningPath: React.FC = () => {
  return (
    <div className="p-8 max-w-5xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-[#e6edf3] tracking-wider flex items-center gap-3">
          <GitBranch className="w-7 h-7 text-[#00d4ff]" /> LEARNING PATH (10 LEVELS)
        </h1>
        <p className="text-xs text-[#8b949e] mt-1">Structured educational progression from basic SQL concepts to database engine mastery.</p>
      </div>

      <div className="space-y-6">
        {LEVELS.map((lvl) => (
          <div key={lvl.level} className="bg-[#0d1117] border border-[#30363d] rounded-2xl p-6 relative overflow-hidden">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="space-y-1">
                <h2 className="text-lg font-bold text-[#00d4ff]">{lvl.name}</h2>
                <p className="text-xs text-[#8b949e]">{lvl.desc}</p>
              </div>

              <div className="flex items-center space-x-2 flex-wrap gap-2">
                {lvl.challenges.map((chId) => (
                  <Link
                    key={chId}
                    to={`/challenge/${chId}`}
                    className="bg-[#161b22] border border-[#00d4ff44] hover:border-[#00d4ff] text-[#00d4ff] text-xs font-bold px-3 py-1.5 rounded-lg transition-colors"
                  >
                    CH {chId.toString().padStart(2, '0')}
                  </Link>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
