import React, { useEffect, useState } from 'react';
import { Terminal, Shield, AlertTriangle } from 'lucide-react';
import { AttackLogEntry } from '../types';

interface AttackMonitorProps {
  challengeId?: number;
}

export const AttackMonitor: React.FC<AttackMonitorProps> = ({ challengeId }) => {
  const [logs, setLogs] = useState<AttackLogEntry[]>([
    {
      id: 1,
      challenge_id: challengeId || 1,
      event_type: 'SYSTEM_INIT',
      message: 'Monitoring container initialized. Event stream active.',
      timestamp: new Date().toISOString(),
    },
  ]);

  useEffect(() => {
    const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';
    const endpoint = challengeId ? `/ws/monitor/${challengeId}` : '/ws/monitor/global/stream';
    const ws = new WebSocket(`${wsUrl}${endpoint}`);

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'CONNECTED' || data.type === 'PING') return;
        setLogs((prev) => [
          {
            id: Date.now(),
            challenge_id: data.challenge_id || challengeId || 1,
            event_type: data.type || 'EVENT',
            message: data.message || JSON.stringify(data),
            timestamp: data.timestamp || new Date().toISOString(),
          },
          ...prev.slice(0, 49),
        ]);
      } catch (err) {
        console.error('WS Parse error', err);
      }
    };

    return () => {
      ws.close();
    };
  }, [challengeId]);

  return (
    <div className="bg-[#0d1117] border border-[#30363d] rounded-xl overflow-hidden shadow-lg flex flex-col h-72">
      <div className="bg-[#161b22] px-4 py-2.5 border-b border-[#30363d] flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Terminal className="w-4 h-4 text-[#00d4ff]" />
          <span className="text-xs font-bold text-[#00d4ff] tracking-wider">LIVE ATTACK MONITOR</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-2 h-2 rounded-full bg-[#00ff88] animate-ping" />
          <span className="text-[11px] text-[#00ff88]">LIVE STREAM</span>
        </div>
      </div>

      <div className="p-3 overflow-y-auto flex-1 font-mono text-xs space-y-2 bg-[#010409]">
        {logs.map((log) => (
          <div key={log.id} className="flex items-start space-x-2 border-b border-[#161b22] pb-1.5">
            <span className="text-[#6e7681] text-[10px] whitespace-nowrap">
              [{new Date(log.timestamp).toLocaleTimeString()}]
            </span>
            <span
              className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
                log.event_type.includes('CORRECT') || log.event_type.includes('FLAG')
                  ? 'bg-[#00ff8822] text-[#00ff88] border border-[#00ff8866]'
                  : log.event_type.includes('INCORRECT') || log.event_type.includes('ERROR')
                  ? 'bg-[#ff224422] text-[#ff2244] border border-[#ff224466]'
                  : 'bg-[#00d4ff11] text-[#00d4ff] border border-[#00d4ff33]'
              }`}
            >
              CH{log.challenge_id} • {log.event_type}
            </span>
            <span className="text-[#8b949e] flex-1 break-all">{log.message}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
