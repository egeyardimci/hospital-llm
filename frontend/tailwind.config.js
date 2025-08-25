/** @type {import('tailwindcss').Config} */
export const content = [
  "./index.html",
  "./src/**/*.{js,ts,jsx,tsx}",
];
export const theme = {
  extend: {
    colors: {
      primary: {
        50: '#f0f4ff',
        100: '#e0eaff',
        200: '#c7d2fe',
        300: '#a5b4fc',
        400: '#818cf8',
        500: '#6366f1',
        600: '#4f46e5',
        700: '#4338ca',
        800: '#3730a3',
        900: '#002776', // Your main color
        950: '#001a5c',
      },
      secondary: {
        50: '#f8fafc',
        100: '#f1f5f9',
        200: '#e2e8f0',
        300: '#cbd5e1',
        400: '#94a3b8',
        500: '#64748b',
        600: '#475569',
        700: '#334155',
        800: '#1e293b',
        900: '#0f172a',
      },
      success: '#10b981',
      danger: '#ef4444',
      warning: '#f59e0b',
    },
    fontFamily: {
      sans: ['-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', '"Open Sans"', '"Helvetica Neue"', 'sans-serif'],
      mono: ['source-code-pro', 'Menlo', 'Monaco', 'Consolas', '"Courier New"', 'monospace'],
    },
    boxShadow: {
      'card': '0 2px 10px rgba(0, 0, 0, 0.1)',
      'card-hover': '0 5px 15px rgba(0, 0, 0, 0.1)',
    },
    animation: {
      'typing': 'typing 1s infinite',
    },
    keyframes: {
      typing: {
        '0%': { transform: 'translateY(0px)' },
        '50%': { transform: 'translateY(-5px)' },
        '100%': { transform: 'translateY(0px)' },
      },
    },
  },
};
export const plugins = [];