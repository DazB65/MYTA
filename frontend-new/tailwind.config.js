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
          50: '#f0f4ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          300: '#a5b4fc',
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81',
          950: '#1e1b4b',
        },
        dark: {
          50: '#1a202c',
          100: '#2d3748',
          200: '#4a5568',
          300: '#718096',
          400: '#a0aec0',
          500: '#cbd5e1',
          600: '#e2e8f0',
          700: '#edf2f7',
          800: '#f7fafc',
          900: '#ffffff',
          950: '#ffffff',
        },
        background: {
          primary: '#f4f7fa',
          secondary: '#ffffff',
          tertiary: '#f8fafc',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'thinking-pulse': 'thinking-pulse 1.4s infinite',
      },
      keyframes: {
        'thinking-pulse': {
          '0%, 20%': { opacity: '0.3', transform: 'scale(0.8)' },
          '50%': { opacity: '1', transform: 'scale(1)' },
          '80%, 100%': { opacity: '0.3', transform: 'scale(0.8)' },
        },
      },
    },
  },
  plugins: [],
}