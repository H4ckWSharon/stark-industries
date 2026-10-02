import React from 'react';

interface ArcReactorLogoProps {
  size?: number;
  showText?: boolean;
}

export const ArcReactorLogo: React.FC<ArcReactorLogoProps> = ({
  size = 40,
  showText = true,
}) => {
  return (
    <div className="flex items-center space-x-3 group cursor-pointer select-none">
      <div
        className="relative flex items-center justify-center rounded-full p-1 transition-transform group-hover:scale-105"
        style={{ width: size, height: size }}
      >
        {/* Arc Reactor Outer Glow */}
        <div className="absolute inset-0 rounded-full bg-[#00d4ff33] blur-md animate-pulse" />

        {/* Arc Reactor SVG */}
        <svg
          viewBox="0 0 100 100"
          className="w-full h-full relative z-10 drop-shadow-[0_0_10px_rgba(0,212,255,0.8)]"
        >
          {/* Outer Titanium Ring */}
          <circle cx="50" cy="50" r="46" fill="#0d1117" stroke="#ff2244" strokeWidth="2.5" />
          <circle cx="50" cy="50" r="42" fill="none" stroke="#ffd700" strokeWidth="1" strokeDasharray="4 2" />

          {/* Copper Coil Nodes (10 segments) */}
          {[0, 36, 72, 108, 144, 180, 216, 252, 288, 324].map((angle, i) => {
            const rad = (angle * Math.PI) / 180;
            const x = 50 + 33 * Math.cos(rad);
            const y = 50 + 33 * Math.sin(rad);
            return (
              <circle
                key={i}
                cx={x}
                cy={y}
                r="3.5"
                fill="#ffd700"
                stroke="#ff2244"
                strokeWidth="1"
              />
            );
          })}

          {/* Inner Energy Ring */}
          <circle
            cx="50"
            cy="50"
            r="24"
            fill="none"
            stroke="#00d4ff"
            strokeWidth="3.5"
            className="animate-pulse"
          />

          {/* Center Palladium Core */}
          <polygon
            points="50,30 67,40 67,60 50,70 33,60 33,40"
            fill="url(#coreGradient)"
            stroke="#00f2fe"
            strokeWidth="1.5"
            className="animate-core-glow"
          />

          {/* Core Gradients */}
          <defs>
            <radialGradient id="coreGradient" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#ffffff" />
              <stop offset="50%" stopColor="#00d4ff" />
              <stop offset="100%" stopColor="#0066cc" />
            </radialGradient>
          </defs>
        </svg>
      </div>

      {showText && (
        <div className="flex flex-col">
          <div className="flex items-center space-x-1.5 leading-none">
            <span className="font-extrabold tracking-widest text-[#ff2244] text-lg font-mono drop-shadow-[0_0_8px_rgba(255,34,68,0.4)]">
              STARK
            </span>
            <span className="font-bold tracking-widest text-[#ffd700] text-lg font-mono">
              INDUSTRIES
            </span>
          </div>
          <span className="text-[10px] text-[#00d4ff] font-mono tracking-widest mt-0.5">
            SQL CYBER RANGE // MARK VIII
          </span>
        </div>
      )}
    </div>
  );
};
