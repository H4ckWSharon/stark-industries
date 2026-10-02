export interface User {
  id: number;
  username: string;
  is_admin: boolean;
  xp: number;
  level: number;
  rank: string;
}

export interface Challenge {
  challenge_id: number;
  title: string;
  subtitle: string;
  description: string;
  objective: string;
  scenario: string;
  difficulty: 'easy' | 'medium' | 'hard' | 'expert';
  category: string;
  points: number;
  estimated_minutes: number;
  db_type: string;
  vulnerability_type: string;
  port: number;
  hint_1: string;
  hint_2: string;
  hint_3: string;
  completed?: boolean;
  hints_used?: number;
  attempts?: number;
  xp_earned?: number;
  solution_explanation?: string | null;
  vulnerable_code?: string | null;
  secure_code?: string | null;
  defensive_tips?: string[];
  container_name?: string;
  tags?: string[];
}

export interface LeaderboardEntry {
  rank: number;
  username: string;
  xp: number;
  level: number;
  rank_title: string;
  completed: number;
}

export interface AttackLogEntry {
  id: number;
  challenge_id: number;
  event_type: string;
  message: string;
  timestamp: string;
}

export interface UserStats {
  user_id: number;
  username: string;
  xp: number;
  level: number;
  rank: string;
  total_challenges: number;
  completed: number;
  remaining: number;
  success_rate: number;
  achievements: { id: string; name: string }[];
  progress: {
    challenge_id: number;
    completed: boolean;
    hints_used: number;
    attempts: number;
    xp_earned: number;
  }[];
}
