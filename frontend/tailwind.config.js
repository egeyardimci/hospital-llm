/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#e3f2fd',
          100: '#bbdefb',
          500: '#3498db',
          600: '#2980b9',
          700: '#1976d2',
        },
        secondary: {
          50: '#ecf0f1',
          100: '#bdc3c7',
          500: '#7f8c8d',
          700: '#2c3e50',
        },
        success: '#2ecc71',
        danger: '#e74c3c',
        warning: '#f39c12',
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
  },
  plugins: [],
}