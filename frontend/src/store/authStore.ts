import { create } from 'zustand';
import { User } from '../types';
import { apiClient } from '../api/client';

interface AuthState {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string) => Promise<void>;
  logout: () => void;
  fetchMe: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem('stark_token'),
  user: JSON.parse(localStorage.getItem('stark_user') || 'null'),
  isAuthenticated: !!localStorage.getItem('stark_token'),

  login: async (username, password) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await apiClient.post('/auth/token', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });

    const { access_token, user } = response.data;
    localStorage.setItem('stark_token', access_token);
    localStorage.setItem('stark_user', JSON.stringify(user));
    set({ token: access_token, user, isAuthenticated: true });
  },

  register: async (username, password) => {
    const response = await apiClient.post('/auth/register', { username, password });
    const { access_token, user } = response.data;
    localStorage.setItem('stark_token', access_token);
    localStorage.setItem('stark_user', JSON.stringify(user));
    set({ token: access_token, user, isAuthenticated: true });
  },

  logout: () => {
    localStorage.removeItem('stark_token');
    localStorage.removeItem('stark_user');
    set({ token: null, user: null, isAuthenticated: false });
  },

  fetchMe: async () => {
    try {
      const response = await apiClient.get('/auth/me');
      const user = response.data;
      localStorage.setItem('stark_user', JSON.stringify(user));
      set({ user });
    } catch {
      localStorage.removeItem('stark_token');
      localStorage.removeItem('stark_user');
      set({ token: null, user: null, isAuthenticated: false });
    }
  },
}));
