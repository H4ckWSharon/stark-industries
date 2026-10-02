import React, { useState } from 'react';
import { useAuthStore } from '../store/authStore';
import { ArcReactorLogo } from '../components/ArcReactorLogo';
import { Lock, User as UserIcon, Mail, ShieldCheck } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { apiClient } from '../api/client';

export const Login: React.FC = () => {
  const { login } = useAuthStore();
  const [isRegister, setIsRegister] = useState(false);

  // Login state
  const [loginId, setLoginId] = useState('');
  const [loginPass, setLoginPass] = useState('');

  // Register state
  const [regUsername, setRegUsername] = useState('');
  const [regEmail, setRegEmail] = useState('');
  const [regPass, setRegPass] = useState('');
  const [regPassConfirm, setRegPassConfirm] = useState('');

  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // ── Login ──────────────────────────────────────────────────────────────────
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login(loginId, loginPass);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Incorrect username/email or password.');
    } finally {
      setLoading(false);
    }
  };

  // ── Register ───────────────────────────────────────────────────────────────
  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (regPass !== regPassConfirm) {
      setError('Passwords do not match.');
      return;
    }
    if (regPass.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }

    setLoading(true);
    try {
      await apiClient.post('/auth/register', {
        username: regUsername,
        email: regEmail || undefined,
        password: regPass,
      });
      // Auto-login after successful registration
      await login(regUsername, regPass);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0f] flex flex-col justify-center items-center p-4 relative overflow-hidden font-mono">
      {/* Background grid */}
      <div className="absolute inset-0 bg-[radial-gradient(#ff224415_1px,transparent_1px)] [background-size:28px_28px] pointer-events-none" />

      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4 }}
        className="w-full max-w-md bg-[#0d1117] border border-[#ff224455] rounded-3xl p-8 shadow-[0_0_50px_rgba(255,34,68,0.2)] relative z-10"
      >
        {/* Logo & Title */}
        <div className="flex flex-col items-center text-center mb-7">
          <ArcReactorLogo size={64} showText={false} />
          <h1 className="text-2xl font-extrabold text-[#ff2244] tracking-widest mt-4 drop-shadow-[0_0_10px_rgba(255,34,68,0.4)]">
            STARK INDUSTRIES
          </h1>
          <p className="text-xs text-[#ffd700] tracking-widest mt-1 font-bold">
            SQL INJECTION CYBER RANGE // MARK VIII
          </p>
        </div>

        {/* Tab Toggle */}
        <div className="flex bg-[#161b22] rounded-xl p-1 mb-6 border border-[#21262d]">
          <button
            type="button"
            onClick={() => { setIsRegister(false); setError(null); }}
            className={`flex-1 py-2 rounded-lg text-xs font-bold tracking-wider transition-all ${
              !isRegister
                ? 'bg-[#ff2244] text-white shadow-[0_0_12px_rgba(255,34,68,0.4)]'
                : 'text-[#8b949e] hover:text-white'
            }`}
          >
            LOGIN
          </button>
          <button
            type="button"
            onClick={() => { setIsRegister(true); setError(null); }}
            className={`flex-1 py-2 rounded-lg text-xs font-bold tracking-wider transition-all ${
              isRegister
                ? 'bg-[#ff2244] text-white shadow-[0_0_12px_rgba(255,34,68,0.4)]'
                : 'text-[#8b949e] hover:text-white'
            }`}
          >
            REGISTER
          </button>
        </div>

        {/* Error / Success */}
        <AnimatePresence>
          {error && (
            <motion.div
              key="error"
              initial={{ opacity: 0, y: -6 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="bg-[#2d1b1b] border border-[#ff2244] text-[#ff8080] p-3 rounded-xl text-xs mb-5 font-mono"
            >
              ⚠ {error}
            </motion.div>
          )}
          {success && (
            <motion.div
              key="success"
              initial={{ opacity: 0, y: -6 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="bg-[#0d2b1b] border border-[#00ff88] text-[#00ff88] p-3 rounded-xl text-xs mb-5 font-mono"
            >
              ✔ {success}
            </motion.div>
          )}
        </AnimatePresence>

        {/* ── LOGIN FORM ─────────────────────────────────────────────────── */}
        <AnimatePresence mode="wait">
          {!isRegister ? (
            <motion.form
              key="login"
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 10 }}
              transition={{ duration: 0.2 }}
              onSubmit={handleLogin}
              className="space-y-4"
            >
              <div>
                <label className="block text-xs text-[#8b949e] mb-1.5">
                  // USERNAME OR EMAIL
                </label>
                <div className="relative">
                  <UserIcon className="w-4 h-4 text-[#8b949e] absolute left-3.5 top-3.5" />
                  <input
                    id="login-username"
                    type="text"
                    required
                    value={loginId}
                    onChange={(e) => setLoginId(e.target.value)}
                    placeholder="username or email@example.com"
                    autoComplete="username"
                    className="w-full bg-[#010409] border border-[#30363d] text-[#ffd700] rounded-xl pl-10 pr-4 py-2.5 focus:border-[#ff2244] focus:outline-none transition-colors"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs text-[#8b949e] mb-1.5">
                  // PASSWORD
                </label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-[#8b949e] absolute left-3.5 top-3.5" />
                  <input
                    id="login-password"
                    type="password"
                    required
                    value={loginPass}
                    onChange={(e) => setLoginPass(e.target.value)}
                    placeholder="Your password"
                    autoComplete="current-password"
                    className="w-full bg-[#010409] border border-[#30363d] text-[#ffd700] rounded-xl pl-10 pr-4 py-2.5 focus:border-[#ff2244] focus:outline-none transition-colors"
                  />
                </div>
              </div>

              <button
                id="login-submit"
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-[#ff2244] to-[#d63031] text-white font-extrabold py-3.5 rounded-xl hover:opacity-90 disabled:opacity-50 transition-opacity shadow-[0_0_25px_rgba(255,34,68,0.4)] tracking-wider mt-2"
              >
                {loading ? 'INITIALIZING SUIT...' : '[ ACCESS CYBER RANGE ]'}
              </button>
            </motion.form>

          ) : (

            /* ── REGISTER FORM ───────────────────────────────────────────── */
            <motion.form
              key="register"
              initial={{ opacity: 0, x: 10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -10 }}
              transition={{ duration: 0.2 }}
              onSubmit={handleRegister}
              className="space-y-4"
            >
              <div>
                <label className="block text-xs text-[#8b949e] mb-1.5">
                  // USERNAME <span className="text-[#ff2244]">*</span>
                </label>
                <div className="relative">
                  <UserIcon className="w-4 h-4 text-[#8b949e] absolute left-3.5 top-3.5" />
                  <input
                    id="reg-username"
                    type="text"
                    required
                    value={regUsername}
                    onChange={(e) => setRegUsername(e.target.value)}
                    placeholder="Choose a username"
                    autoComplete="username"
                    className="w-full bg-[#010409] border border-[#30363d] text-[#ffd700] rounded-xl pl-10 pr-4 py-2.5 focus:border-[#ff2244] focus:outline-none transition-colors"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs text-[#8b949e] mb-1.5">
                  // EMAIL <span className="text-[#6e7681]">(optional)</span>
                </label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-[#8b949e] absolute left-3.5 top-3.5" />
                  <input
                    id="reg-email"
                    type="email"
                    value={regEmail}
                    onChange={(e) => setRegEmail(e.target.value)}
                    placeholder="email@example.com"
                    autoComplete="email"
                    className="w-full bg-[#010409] border border-[#30363d] text-[#ffd700] rounded-xl pl-10 pr-4 py-2.5 focus:border-[#ff2244] focus:outline-none transition-colors"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs text-[#8b949e] mb-1.5">
                  // PASSWORD <span className="text-[#ff2244]">*</span>
                </label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-[#8b949e] absolute left-3.5 top-3.5" />
                  <input
                    id="reg-password"
                    type="password"
                    required
                    value={regPass}
                    onChange={(e) => setRegPass(e.target.value)}
                    placeholder="Min. 6 characters"
                    autoComplete="new-password"
                    className="w-full bg-[#010409] border border-[#30363d] text-[#ffd700] rounded-xl pl-10 pr-4 py-2.5 focus:border-[#ff2244] focus:outline-none transition-colors"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs text-[#8b949e] mb-1.5">
                  // CONFIRM PASSWORD <span className="text-[#ff2244]">*</span>
                </label>
                <div className="relative">
                  <ShieldCheck className="w-4 h-4 text-[#8b949e] absolute left-3.5 top-3.5" />
                  <input
                    id="reg-password-confirm"
                    type="password"
                    required
                    value={regPassConfirm}
                    onChange={(e) => setRegPassConfirm(e.target.value)}
                    placeholder="Repeat password"
                    autoComplete="new-password"
                    className="w-full bg-[#010409] border border-[#30363d] text-[#ffd700] rounded-xl pl-10 pr-4 py-2.5 focus:border-[#ff2244] focus:outline-none transition-colors"
                  />
                </div>
              </div>

              <button
                id="reg-submit"
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-[#ff2244] to-[#d63031] text-white font-extrabold py-3.5 rounded-xl hover:opacity-90 disabled:opacity-50 transition-opacity shadow-[0_0_25px_rgba(255,34,68,0.4)] tracking-wider mt-2"
              >
                {loading ? 'CREATING ACCOUNT...' : '[ CREATE PILOT ACCOUNT ]'}
              </button>
            </motion.form>
          )}
        </AnimatePresence>

        {/* Footer */}
        <div className="mt-6 pt-4 border-t border-[#21262d] text-center text-[10px] text-[#6e7681]">
          STARK INDUSTRIES RESEARCH DIVISION // AUTHORIZED PERSONNEL ONLY
        </div>
      </motion.div>
    </div>
  );
};
