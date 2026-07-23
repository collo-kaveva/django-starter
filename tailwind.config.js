/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    "./templates/**/*.html",
    "./assets/javascript/**/*.js",
    "./assets/styles/**/*.css",
  ],
  safelist: [
    'alert-success',
    'alert-info',
    'alert-error',
    'alert-warning',
    'pg-bg-danger',
    'pg-bg-success',
  ],
  theme: {
    extend: {
      aspectRatio: {
        '3/2': '3 / 2',
      },
      colors: {
        navy: {
          DEFAULT: '#0B1020',
          light: '#1A1F35',
          dark: '#0B1020',
        },
        indigo: {
          DEFAULT: '#4F46E5',
          light: '#6366F1',
          dark: '#4F46E5',
        },
        electric: {
          DEFAULT: '#3B82F6',
          light: '#60A5FA',
          dark: '#3B82F6',
        },
        emerald: {
          DEFAULT: '#10B981',
          light: '#34D399',
          dark: '#10B981',
        },
        orange: {
          DEFAULT: '#F59E0B',
          light: '#FBBF24',
          dark: '#F59E0B',
        },
        rose: {
          DEFAULT: '#F43F5E',
          light: '#FB7185',
          dark: '#F43F5E',
        },
        purple: {
          DEFAULT: '#8B5CF6',
          light: '#A78BFA',
          dark: '#8B5CF6',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['IBM Plex Mono', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'spin-slow': 'spin 8s linear infinite',
        'float': 'float 3s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(59, 130, 246, 0.5)' },
          '100%': { boxShadow: '0 0 20px rgba(59, 130, 246, 0.8), 0 0 30px rgba(59, 130, 246, 0.4)' },
        },
      },
    },
    container: {
      center: true,
    },
  },
  plugins: [],
}
