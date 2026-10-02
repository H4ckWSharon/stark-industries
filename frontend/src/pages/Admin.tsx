import React, { useEffect, useState } from 'react';
import { apiClient } from '../api/client';
import { ShieldAlert, Users, Award, FileText, CheckCircle2 } from 'lucide-react';

export const Admin: React.FC = () => {
  const [overview, setOverview] = useState<any>(null);
  const [students, setStudents] = useState<any[]>([]);
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAdminData = async () => {
      try {
        const [overviewRes, studentsRes, logsRes] = await Promise.all([
          apiClient.get('/admin/overview'),
          apiClient.get('/admin/students'),
          apiClient.get('/admin/logs?limit=50'),
        ]);
        setOverview(overviewRes.data);
        setStudents(studentsRes.data.students || []);
        setLogs(logsRes.data.logs || []);
      } catch (err) {
        console.error('Failed to fetch admin data', err);
      } finally {
        setLoading(false);
      }
    };
    fetchAdminData();
  }, []);

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-[#ff2244] tracking-wider flex items-center gap-3">
          <ShieldAlert className="w-7 h-7 text-[#ff2244]" /> INSTRUCTOR ADMIN DASHBOARD
        </h1>
        <p className="text-xs text-[#8b949e] mt-1">Classroom analytics, student progress tracking, and audit event logs.</p>
      </div>

      {/* Admin Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-[#0d1117] border border-[#30363d] rounded-xl p-6">
          <div className="text-xs text-[#8b949e]">TOTAL STUDENTS</div>
          <div className="text-3xl font-bold text-[#00d4ff] mt-2">{overview?.total_users || 0}</div>
        </div>
        <div className="bg-[#0d1117] border border-[#30363d] rounded-xl p-6">
          <div className="text-xs text-[#8b949e]">TOTAL COMPLETIONS</div>
          <div className="text-3xl font-bold text-[#00ff88] mt-2">{overview?.total_completions || 0}</div>
        </div>
        <div className="bg-[#0d1117] border border-[#30363d] rounded-xl p-6">
          <div className="text-xs text-[#8b949e]">CHALLENGE COUNT</div>
          <div className="text-3xl font-bold text-[#ffd700] mt-2">{overview?.total_challenges || 30}</div>
        </div>
        <div className="bg-[#0d1117] border border-[#30363d] rounded-xl p-6">
          <div className="text-xs text-[#8b949e]">TOTAL EVENTS LOGGED</div>
          <div className="text-3xl font-bold text-[#e6edf3] mt-2">{overview?.total_events || 0}</div>
        </div>
      </div>

      {/* Student Progress Table */}
      <div className="bg-[#0d1117] border border-[#30363d] rounded-2xl overflow-hidden shadow-xl">
        <div className="bg-[#161b22] px-6 py-4 border-b border-[#30363d] flex items-center justify-between">
          <h2 className="text-sm font-bold text-[#e6edf3] flex items-center gap-2">
            <Users className="w-4 h-4 text-[#00d4ff]" /> STUDENT ACCOUNTS ({students.length})
          </h2>
        </div>

        <div className="divide-y divide-[#21262d] font-mono text-xs">
          {students.map((st) => (
            <div key={st.id} className="px-6 py-4 flex items-center justify-between hover:bg-[#161b22]">
              <div className="space-y-0.5">
                <div className="font-bold text-[#00d4ff]">{st.username}</div>
                <div className="text-[#8b949e]">{st.rank} • Level {st.level}</div>
              </div>

              <div className="flex items-center space-x-8">
                <div className="text-right">
                  <div className="text-[#00ff88] font-bold">{st.completed_challenges} / 30 Solved</div>
                  <div className="text-[#8b949e]">{st.total_attempts} Attempts</div>
                </div>

                <div className="text-right">
                  <div className="text-[#ffd700] font-bold">{st.xp} XP</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Audit Logs */}
      <div className="bg-[#0d1117] border border-[#30363d] rounded-2xl overflow-hidden p-6 space-y-4">
        <h2 className="text-sm font-bold text-[#e6edf3] flex items-center gap-2">
          <FileText className="w-4 h-4 text-[#00d4ff]" /> AUDIT & ATTACK LOGS
        </h2>

        <div className="bg-[#010409] border border-[#21262d] rounded-xl p-4 font-mono text-xs space-y-2 max-h-72 overflow-y-auto">
          {logs.map((lg) => (
            <div key={lg.id} className="flex justify-between border-b border-[#161b22] pb-1 text-[#8b949e]">
              <span>[{new Date(lg.timestamp).toLocaleTimeString()}] CH{lg.challenge_id} - <strong className="text-[#00d4ff]">{lg.event_type}</strong>: {lg.message}</span>
              <span className="text-[10px] text-[#6e7681]">User #{lg.user_id}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
