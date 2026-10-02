import React, { useEffect, useState, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { apiClient } from '../api/client';
import { Challenge } from '../types';
import { AttackMonitor } from '../components/AttackMonitor';
import { TerminalPanel } from '../components/TerminalPanel';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ExternalLink,
  HelpCircle,
  RotateCcw,
  CheckCircle2,
  AlertTriangle,
  BookOpen,
  Code2,
  ShieldCheck,
  ChevronLeft,
  Trophy,
  Zap,
  Star,
} from 'lucide-react';

// ── Confetti Particle ─────────────────────────────────────────────────────────
interface Particle {
  id: number;
  x: number;
  y: number;
  color: string;
  size: number;
  angle: number;
  speed: number;
  spin: number;
  shape: 'circle' | 'rect' | 'star';
}

const COLORS = [
  '#ff2244', '#ffd700', '#00d4ff', '#00ff88',
  '#ff6600', '#ff00ff', '#ffffff', '#ffaa00',
];

const CongratsOverlay: React.FC<{ xp: number; challengeName: string; onClose: () => void }> = ({
  xp, challengeName, onClose,
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const particlesRef = useRef<Particle[]>([]);
  const rafRef = useRef<number>(0);
  const [displayXP, setDisplayXP] = useState(0);

  // Spawn confetti particles
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles: Particle[] = Array.from({ length: 160 }, (_, i) => ({
      id: i,
      x: Math.random() * canvas.width,
      y: -20 - Math.random() * 200,
      color: COLORS[Math.floor(Math.random() * COLORS.length)],
      size: 6 + Math.random() * 10,
      angle: Math.random() * 360,
      speed: 2 + Math.random() * 4,
      spin: (Math.random() - 0.5) * 8,
      shape: ['circle', 'rect', 'star'][Math.floor(Math.random() * 3)] as Particle['shape'],
    }));
    particlesRef.current = particles;

    const ctx = canvas.getContext('2d')!;

    const drawStar = (ctx: CanvasRenderingContext2D, cx: number, cy: number, r: number) => {
      ctx.beginPath();
      for (let i = 0; i < 5; i++) {
        const angle = (i * 4 * Math.PI) / 5 - Math.PI / 2;
        const x = cx + r * Math.cos(angle);
        const y = cy + r * Math.sin(angle);
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      }
      ctx.closePath();
    };

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      particlesRef.current.forEach((p) => {
        p.y += p.speed;
        p.angle += p.spin;
        if (p.y > canvas.height + 20) {
          p.y = -20;
          p.x = Math.random() * canvas.width;
        }
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate((p.angle * Math.PI) / 180);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = 0.85;
        if (p.shape === 'circle') {
          ctx.beginPath();
          ctx.arc(0, 0, p.size / 2, 0, Math.PI * 2);
          ctx.fill();
        } else if (p.shape === 'rect') {
          ctx.fillRect(-p.size / 2, -p.size / 4, p.size, p.size / 2);
        } else {
          drawStar(ctx, 0, 0, p.size / 2);
          ctx.fill();
        }
        ctx.restore();
      });
      rafRef.current = requestAnimationFrame(animate);
    };
    animate();

    return () => cancelAnimationFrame(rafRef.current);
  }, []);

  // Animate XP counter up
  useEffect(() => {
    let current = 0;
    const target = xp;
    const step = Math.ceil(target / 40);
    const timer = setInterval(() => {
      current = Math.min(current + step, target);
      setDisplayXP(current);
      if (current >= target) clearInterval(timer);
    }, 40);
    return () => clearInterval(timer);
  }, [xp]);

  // Auto-close after 5s
  useEffect(() => {
    const t = setTimeout(onClose, 5000);
    return () => clearTimeout(t);
  }, [onClose]);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-center justify-center"
      onClick={onClose}
    >
      {/* Confetti canvas */}
      <canvas ref={canvasRef} className="absolute inset-0 pointer-events-none" />

      {/* Dark overlay */}
      <div className="absolute inset-0 bg-black/70 backdrop-blur-sm" />

      {/* Card */}
      <motion.div
        initial={{ scale: 0.5, y: 60, opacity: 0 }}
        animate={{ scale: 1, y: 0, opacity: 1 }}
        exit={{ scale: 0.8, opacity: 0 }}
        transition={{ type: 'spring', stiffness: 220, damping: 18 }}
        className="relative z-10 bg-[#0d1117] border-2 border-[#ffd700] rounded-3xl p-10 max-w-lg w-full mx-4 text-center shadow-[0_0_80px_rgba(255,215,0,0.35)]"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Glowing ring */}
        <div className="absolute -inset-px rounded-3xl bg-gradient-to-r from-[#ff2244] via-[#ffd700] to-[#00d4ff] opacity-20 blur-sm pointer-events-none" />

        {/* Trophy icon bounce */}
        <motion.div
          initial={{ scale: 0, rotate: -30 }}
          animate={{ scale: 1, rotate: 0 }}
          transition={{ type: 'spring', stiffness: 300, damping: 14, delay: 0.1 }}
          className="flex justify-center mb-4"
        >
          <div className="relative">
            <Trophy className="w-20 h-20 text-[#ffd700] drop-shadow-[0_0_24px_rgba(255,215,0,0.8)]" />
            {/* Orbiting stars */}
            {[0, 120, 240].map((deg, i) => (
              <motion.div
                key={i}
                animate={{ rotate: [deg, deg + 360] }}
                transition={{ duration: 3, repeat: Infinity, ease: 'linear', delay: i * 0.2 }}
                className="absolute inset-0 flex items-center justify-center"
                style={{ transformOrigin: 'center' }}
              >
                <Star
                  className="w-4 h-4 text-[#ffd700] absolute"
                  style={{
                    transform: `translateY(-44px) rotate(${-deg}deg)`,
                    opacity: 0.8,
                  }}
                />
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* MISSION COMPLETE text */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <p className="text-xs tracking-[0.4em] text-[#00d4ff] font-bold mb-1 uppercase">
            ⚡ Mission Complete
          </p>
          <h1 className="text-4xl font-black text-[#ffd700] tracking-tight drop-shadow-[0_0_20px_rgba(255,215,0,0.5)] mb-2">
            CONGRATULATIONS!
          </h1>
          <p className="text-sm text-[#8b949e] mb-6 font-mono">
            {challengeName}
          </p>
        </motion.div>

        {/* XP Badge */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', stiffness: 260, damping: 14, delay: 0.35 }}
          className="inline-flex items-center gap-2 bg-[#161b22] border border-[#ffd70066] rounded-2xl px-6 py-3 mb-6"
        >
          <Zap className="w-5 h-5 text-[#ffd700]" />
          <span className="text-3xl font-black text-[#ffd700]">+{displayXP}</span>
          <span className="text-sm font-bold text-[#8b949e]">XP EARNED</span>
        </motion.div>

        {/* Sub-label */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="space-y-3"
        >
          <div className="flex items-center justify-center gap-2 text-[#00ff88] text-sm font-bold">
            <CheckCircle2 className="w-4 h-4" />
            <span>Flag captured — Defensive Learning Mode Unlocked</span>
          </div>
          <p className="text-xs text-[#6e7681]">
            Closing in 5 seconds… or click anywhere to dismiss
          </p>
        </motion.div>

        {/* Progress bar auto-close */}
        <motion.div
          className="mt-5 h-1 bg-[#21262d] rounded-full overflow-hidden"
        >
          <motion.div
            initial={{ width: '100%' }}
            animate={{ width: '0%' }}
            transition={{ duration: 5, ease: 'linear' }}
            className="h-full bg-gradient-to-r from-[#ffd700] to-[#ff2244] rounded-full"
          />
        </motion.div>
      </motion.div>
    </motion.div>
  );
};

// ── Main Challenge Page ────────────────────────────────────────────────────────
export const ChallengePage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const challengeId = parseInt(id || '1', 10);

  const [challenge, setChallenge] = useState<Challenge | null>(null);
  const [flagInput, setFlagInput] = useState('');
  const [submitResult, setSubmitResult] = useState<{
    success: boolean;
    message: string;
    xp_earned?: number;
  } | null>(null);
  const [showCongrats, setShowCongrats] = useState(false);
  const [earnedXP, setEarnedXP] = useState(0);
  const [hint, setHint] = useState<string | null>(null);
  const [hintNumber, setHintNumber] = useState<number>(1);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchChallenge();
  }, [challengeId]);

  const fetchChallenge = async () => {
    try {
      const response = await apiClient.get(`/challenges/${challengeId}`);
      setChallenge(response.data);
    } catch (err) {
      console.error('Failed to load challenge detail', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFlagSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!flagInput) return;
    try {
      const response = await apiClient.post(`/challenges/${challengeId}/submit`, { flag: flagInput });
      setSubmitResult(response.data);
      if (response.data.success) {
        setEarnedXP(response.data.xp_earned ?? challenge?.points ?? 0);
        // Refresh challenge data then show overlay
        await fetchChallenge();
        setShowCongrats(true);
        setFlagInput('');
      }
    } catch (err: any) {
      setSubmitResult({
        success: false,
        message: err.response?.data?.detail || 'Submission failed.',
      });
    }
  };

  const handleRequestHint = async (num: number) => {
    try {
      const response = await apiClient.post(`/challenges/${challengeId}/hint`, { hint_number: num });
      if (response.data.success) {
        setHint(response.data.hint);
        setHintNumber(num);
      }
    } catch (err) {
      console.error('Hint fetch failed', err);
    }
  };

  const handleResetLab = async () => {
    try {
      await apiClient.get(`http://localhost:${challenge?.port}/reset`);
      alert('Laboratory database re-seeded successfully.');
    } catch {
      alert('Laboratory container reset triggered.');
    }
  };

  if (loading || !challenge) {
    return (
      <div className="flex items-center justify-center h-64 text-[#00d4ff] font-mono">
        <motion.div
          animate={{ opacity: [0.4, 1, 0.4] }}
          transition={{ duration: 1.5, repeat: Infinity }}
        >
          LOADING CHALLENGE DATA...
        </motion.div>
      </div>
    );
  }

  const targetUrl = `http://localhost:${challenge.port}`;

  return (
    <>
      {/* ── Congratulations Overlay ────────────────────────────────────── */}
      <AnimatePresence>
        {showCongrats && (
          <CongratsOverlay
            xp={earnedXP}
            challengeName={challenge.subtitle}
            onClose={() => setShowCongrats(false)}
          />
        )}
      </AnimatePresence>

      <div className="p-8 max-w-7xl mx-auto space-y-8">
        {/* Top Bar */}
        <div className="flex items-center justify-between border-b border-[#30363d] pb-4">
          <Link to="/challenges" className="flex items-center text-xs text-[#8b949e] hover:text-[#00d4ff]">
            <ChevronLeft className="w-4 h-4 mr-1" /> Back to Challenges
          </Link>
          <div className="flex items-center space-x-3">
            <span className="text-xs text-[#6e7681]">DB ENGINE: <strong className="text-[#00d4ff]">{challenge.db_type}</strong></span>
            <span className="text-xs text-[#ffd700] font-bold">+{challenge.points} XP</span>
            {challenge.completed && (
              <span className="flex items-center gap-1 text-xs text-[#00ff88] font-bold bg-[#00ff8822] border border-[#00ff8844] px-2 py-0.5 rounded-full">
                <CheckCircle2 className="w-3 h-3" /> SOLVED
              </span>
            )}
          </div>
        </div>

        {/* Mission Brief Banner */}
        <div className="bg-[#0d1117] border border-[#00d4ff44] rounded-2xl p-8 shadow-2xl relative overflow-hidden">
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <span className="text-xs font-bold text-[#00d4ff] tracking-widest uppercase">
                  MISSION {challenge.challenge_id.toString().padStart(2, '0')}
                </span>
                <span className="text-xs bg-[#00ff8822] text-[#00ff88] border border-[#00ff8844] px-2 py-0.5 rounded font-bold uppercase">
                  {challenge.difficulty}
                </span>
              </div>
              <h1 className="text-3xl font-bold text-[#e6edf3]">{challenge.subtitle}</h1>
              <p className="text-sm text-[#8b949e] max-w-3xl leading-relaxed">{challenge.scenario}</p>
            </div>

            <div className="flex flex-col space-y-3 min-w-[200px]">
              <a
                href={targetUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="bg-gradient-to-r from-[#00d4ff] to-[#0066cc] text-[#0a0a0f] font-bold py-3 px-6 rounded-xl text-center flex items-center justify-center space-x-2 shadow-[0_0_20px_rgba(0,212,255,0.3)] hover:opacity-95 transition-opacity"
              >
                <span>LAUNCH LAB</span>
                <ExternalLink className="w-4 h-4" />
              </a>

              <button
                onClick={handleResetLab}
                className="bg-[#161b22] border border-[#30363d] text-[#8b949e] hover:text-[#e6edf3] hover:border-[#ff2244] py-2 px-4 rounded-xl text-xs flex items-center justify-center space-x-2 transition-colors"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>RESET LAB DATABASE</span>
              </button>
            </div>
          </div>
        </div>

        {/* Main Lab Interface Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-6">
            {/* Mission Objective */}
            <div className="bg-[#0d1117] border border-[#30363d] rounded-xl p-6 space-y-4">
              <h2 className="text-sm font-bold text-[#00d4ff] tracking-wider uppercase">// MISSION OBJECTIVE</h2>
              <div className="bg-[#010409] border border-[#21262d] rounded-lg p-4 text-xs text-[#e6edf3] font-mono leading-relaxed">
                {challenge.objective}
              </div>
              <div className="text-xs text-[#8b949e]">
                Target URL: <code className="text-[#00d4ff] bg-[#010409] px-2 py-1 rounded">{targetUrl}</code>
              </div>
            </div>

            {/* Flag Submission */}
            <div className="bg-[#0d1117] border border-[#30363d] rounded-xl p-6 space-y-4">
              <h2 className="text-sm font-bold text-[#ffd700] tracking-wider uppercase">// SUBMIT CAPTURED FLAG</h2>

              {challenge.completed ? (
                <div className="flex items-center gap-3 p-4 rounded-lg border bg-[#0d2b0d] border-[#00ff88] text-[#00ff88] text-sm font-mono">
                  <CheckCircle2 className="w-5 h-5 shrink-0" />
                  <span>Challenge solved! Flag already captured. ✓</span>
                </div>
              ) : (
                <form onSubmit={handleFlagSubmit} className="flex gap-3">
                  <input
                    type="text"
                    value={flagInput}
                    onChange={(e) => setFlagInput(e.target.value)}
                    placeholder="STARKSQL{...}"
                    className="flex-1 bg-[#010409] border border-[#30363d] text-[#ffd700] rounded-lg px-4 py-2.5 font-mono text-sm focus:border-[#ffd700] focus:outline-none"
                  />
                  <button
                    type="submit"
                    className="bg-[#ffd700] text-[#0a0a0f] font-bold px-6 py-2.5 rounded-lg hover:bg-[#ffe033] transition-colors"
                  >
                    [ SUBMIT ]
                  </button>
                </form>
              )}

              <AnimatePresence>
                {submitResult && !submitResult.success && (
                  <motion.div
                    initial={{ opacity: 0, y: -6 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0 }}
                    className="p-4 rounded-lg border text-xs font-mono flex items-center space-x-3 bg-[#2d1b1b] border-[#ff2244] text-[#ff8080]"
                  >
                    <AlertTriangle className="w-5 h-5 shrink-0" />
                    <div>{submitResult.message}</div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Terminal Panel */}
            <TerminalPanel
              challengeId={challenge.challenge_id}
              targetPort={challenge.port}
              onResetLab={handleResetLab}
              onShowHint={() => handleRequestHint(1)}
            />

            {/* Post-Solve Learning Mode */}
            {challenge.completed && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="bg-[#0d1117] border border-[#00ff8844] rounded-2xl p-6 space-y-6"
              >
                <div className="flex items-center space-x-3 border-b border-[#30363d] pb-4">
                  <CheckCircle2 className="w-6 h-6 text-[#00ff88]" />
                  <div>
                    <h2 className="text-base font-bold text-[#00ff88]">SOLVED — DEFENSIVE LEARNING MODE UNLOCKED</h2>
                    <p className="text-xs text-[#8b949e]">Review attack mechanics, vulnerable implementation, and prepared secure code.</p>
                  </div>
                </div>

                {challenge.solution_explanation && (
                  <div className="space-y-2">
                    <h3 className="text-xs font-bold text-[#00d4ff] flex items-center gap-2">
                      <BookOpen className="w-4 h-4" /> ATTACK EXPLANATION
                    </h3>
                    <div className="bg-[#010409] p-4 rounded-lg text-xs text-[#8b949e] whitespace-pre-wrap leading-relaxed border border-[#21262d]">
                      {challenge.solution_explanation}
                    </div>
                  </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {challenge.vulnerable_code && (
                    <div className="space-y-2">
                      <h3 className="text-xs font-bold text-[#ff2244] flex items-center gap-2">
                        <Code2 className="w-4 h-4" /> VULNERABLE IMPLEMENTATION
                      </h3>
                      <pre className="bg-[#1a0a0a] border border-[#ff224444] p-3 rounded-lg text-[11px] text-[#ff8080] overflow-x-auto">
                        {challenge.vulnerable_code}
                      </pre>
                    </div>
                  )}

                  {challenge.secure_code && (
                    <div className="space-y-2">
                      <h3 className="text-xs font-bold text-[#00ff88] flex items-center gap-2">
                        <ShieldCheck className="w-4 h-4" /> SECURE CODE SOLUTION
                      </h3>
                      <pre className="bg-[#0a1a0a] border border-[#00ff8844] p-3 rounded-lg text-[11px] text-[#00ff88] overflow-x-auto">
                        {challenge.secure_code}
                      </pre>
                    </div>
                  )}
                </div>
              </motion.div>
            )}
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            {/* Progressive Hints */}
            <div className="bg-[#0d1117] border border-[#30363d] rounded-xl p-6 space-y-4">
              <h2 className="text-sm font-bold text-[#00d4ff] tracking-wider uppercase flex items-center gap-2">
                <HelpCircle className="w-4 h-4" /> PROGRESSIVE HINTS (-10 XP EACH)
              </h2>

              <div className="flex gap-2">
                {[1, 2, 3].map((num) => (
                  <button
                    key={num}
                    onClick={() => handleRequestHint(num)}
                    className={`flex-1 py-2 rounded-lg text-xs font-bold transition-colors ${
                      hintNumber === num && hint
                        ? 'bg-[#00d4ff] text-[#0a0a0f]'
                        : 'bg-[#161b22] text-[#8b949e] hover:text-[#e6edf3] border border-[#30363d]'
                    }`}
                  >
                    HINT {num}
                  </button>
                ))}
              </div>

              {hint && (
                <motion.div
                  initial={{ opacity: 0, y: 6 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-[#0d1b0d] border border-[#00ff8844] p-4 rounded-lg text-xs text-[#00ff88] leading-relaxed"
                >
                  💡 {hint}
                </motion.div>
              )}
            </div>

            {/* Attack Event Stream */}
            <div className="space-y-2">
              <h2 className="text-xs font-bold text-[#8b949e] uppercase">LIVE LAB MONITOR</h2>
              <AttackMonitor challengeId={challenge.challenge_id} />
            </div>
          </div>
        </div>
      </div>
    </>
  );
};
