import React, { useState, useRef, useEffect } from 'react';
import { Terminal as TerminalIcon, CornerDownLeft } from 'lucide-react';
import { apiClient } from '../api/client';

interface TerminalPanelProps {
  challengeId: number;
  targetPort: number;
  onResetLab?: () => void;
  onShowHint?: () => void;
}

export const TerminalPanel: React.FC<TerminalPanelProps> = ({
  challengeId,
  targetPort,
  onResetLab,
  onShowHint,
}) => {
  const [history, setHistory] = useState<string[]>([
    '⚡ STARK INDUSTRIES LAB TERMINAL v1.0',
    'Connected to isolated environment: stark-lab-ch' + challengeId,
    'Type "help" for available commands.',
    '',
  ]);
  const [input, setInput] = useState('');
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [history]);

  const handleCommand = (cmd: string) => {
    const trimmed = cmd.trim().toLowerCase();
    const newHist = [...history, `student@stark-lab:~$ ${cmd}`];

    if (!trimmed) {
      setHistory(newHist);
      return;
    }

    switch (trimmed) {
      case 'help':
        newHist.push(
          'Available Commands:',
          '  help      - Display available commands',
          '  status    - Check target lab status',
          '  target    - View target URL and port information',
          '  reset     - Reset laboratory database instance',
          '  hint      - Show current mission hint',
          '  clear     - Clear terminal buffer'
        );
        break;

      case 'status':
        newHist.push(`Target Status: OPERATIONAL (Port: ${targetPort})`);
        break;

      case 'target':
        newHist.push(`Target URL: http://localhost:${targetPort}`);
        break;

      case 'reset':
        newHist.push('Triggering lab reset sequence...');
        if (onResetLab) onResetLab();
        break;

      case 'hint':
        newHist.push('Opening hint modal...');
        if (onShowHint) onShowHint();
        break;

      case 'clear':
        setHistory([]);
        return;

      default:
        newHist.push(`bash: command not found: ${trimmed}. Type "help" for command list.`);
        break;
    }

    setHistory(newHist);
  };

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleCommand(input);
    setInput('');
  };

  return (
    <div className="bg-[#010409] border border-[#30363d] rounded-xl overflow-hidden shadow-2xl flex flex-col h-64 font-mono text-xs">
      <div className="bg-[#161b22] px-4 py-2 border-b border-[#30363d] flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <TerminalIcon className="w-4 h-4 text-[#00d4ff]" />
          <span className="text-xs font-bold text-[#e6edf3]">STUDENT LAB TERMINAL</span>
        </div>
        <span className="text-[10px] text-[#8b949e]">student@stark-lab:~$</span>
      </div>

      <div className="p-4 overflow-y-auto flex-1 space-y-1 text-[#8b949e]">
        {history.map((line, i) => (
          <div key={i} className={line.startsWith('student@') ? 'text-[#00d4ff] font-semibold' : ''}>
            {line}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <form onSubmit={onSubmit} className="border-t border-[#21262d] bg-[#0d1117] px-3 py-2 flex items-center space-x-2">
        <span className="text-[#00d4ff] font-bold">student@stark-lab:~$</span>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="type a command (e.g. help, target, reset)..."
          className="flex-1 bg-transparent border-none text-[#e6edf3] focus:outline-none font-mono text-xs"
        />
        <button type="submit" className="text-[#8b949e] hover:text-[#00d4ff]">
          <CornerDownLeft className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
};
