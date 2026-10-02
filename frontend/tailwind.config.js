/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        stark: {
          dark: '#0a0a0f',
          card: '#0d1117',
          border: '#2a2f3a',
          red: '#d63031',
          'red-bright': '#ff2244',
          'red-dark': '#8b0000',
          gold: '#ffd700',
          'gold-dark': '#b8860b',
          cyan: '#00d4ff',
          'cyan-bright': '#00f2fe',
          green: '#00ff88',
          text: '#e6edf3',
          muted: '#8b949e'
        }
      },
      fontFamily: {
        mono: ['Fira Code', 'Courier New', 'monospace'],
        sans: ['Inter', 'sans-serif']
      },
      boxShadow: {
        'glow-red': '0 0 25px rgba(214, 48, 49, 0.35)',
        'glow-gold': '0 0 25px rgba(255, 215, 0, 0.35)',
        'glow-cyan': '0 0 25px rgba(0, 212, 255, 0.35)',
        'glow-green': '0 0 25px rgba(0, 255, 136, 0.35)',
      }
    },
  },
  plugins: [],
}
