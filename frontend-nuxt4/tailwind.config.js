/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './components/**/*.{js,vue,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js,ts}',
    './app/**/*.{js,vue,ts}',
    './nuxt.config.{js,ts}',
  ],
  theme: {
    extend: {
      // Custom color palette based on existing CSS variables
      colors: {
        // Background colors - Gray/Slate Theme
        background: {
          DEFAULT: '#0f172a', // deep slate
          card: '#1e293b', // slate card
          elevated: '#334155', // elevated slate
          overlay: 'rgba(15, 23, 42, 0.9)', // slate overlay
        },

        // Surface colors
        surface: {
          1: '#0f172a', // deep slate
          2: '#1e293b', // slate
          3: '#334155', // light slate
        },

        // Forest color palette (now gray-based)
        forest: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155', // Main interactive elements
          800: '#1e293b', // Main containers
          900: '#0f172a', // Background
        },

        // Text colors
        text: {
          primary: '#ffffff',
          secondary: '#d1d5db', // gray-300
          tertiary: '#9ca3af', // gray-400
          muted: '#6b7280', // gray-500
        },

        // Forest + Orange brand colors
        brand: {
          primary: '#f97316', // Orange primary
          secondary: '#22c55e', // Forest green secondary
          50: '#fff7ed',
          100: '#ffedd5',
          200: '#fed7aa',
          300: '#fdba74',
          400: '#fb923c',
          500: '#f97316', // Orange primary
          600: '#ea580c',
          700: '#c2410c',
          800: '#9a3412',
          900: '#7c2d12',
        },

        // Gray color palette with custom 850
        gray: {
          50: '#f9fafb',
          100: '#f3f4f6',
          200: '#e5e7eb',
          300: '#d1d5db',
          400: '#9ca3af',
          500: '#6b7280',
          600: '#4b5563',
          700: '#374151',
          800: '#1f2937',
          850: '#1a202c', // Custom intermediate gray
          900: '#111827',
        },

        // Orange color palette (primary accent)
        orange: {
          50: '#fff7ed',
          100: '#ffedd5',
          200: '#fed7aa',
          300: '#fdba74',
          400: '#fb923c',
          500: '#f97316', // Main orange accent
          600: '#ea580c',
          700: '#c2410c',
          800: '#9a3412',
          900: '#7c2d12',
        },

        // Agent colors - matching correct agent mapping
        agent: {
          alex: '#f97316',  // Agent 1 - Alex - Orange
          levi: '#3b82f6',  // Agent 2 - Levi - Blue
          maya: '#a855f7',  // Agent 3 - Maya - Purple
          zara: '#eab308',  // Agent 4 - Zara - Yellow
          kai: '#16a34a',   // Agent 5 - Kai - Green
          boss: '#ef4444',  // Boss Agent - Red
          // Legacy numeric keys for backward compatibility
          1: '#f97316',     // Alex - Orange
          2: '#3b82f6',     // Levi - Blue
          3: '#a855f7',     // Maya - Purple
          4: '#eab308',     // Zara - Yellow
          5: '#16a34a',     // Kai - Green
        },

        // Accent colors (forest + orange theme)
        accent: {
          orange: '#f97316', // Primary accent
          yellow: '#FFEAA7', // Agent 2 (Levi)
          green: '#059669', // Agent 3
          amber: '#ea580c', // Agent 4
          red: '#ef4444',
          primary: '#f97316', // Orange as primary
        },

        // Status colors
        success: {
          50: '#ecfdf5',
          100: '#d1fae5',
          500: '#10b981',
          600: '#059669',
          700: '#047857',
        },

        warning: {
          50: '#fffbeb',
          100: '#fef3c7',
          500: '#f59e0b',
          600: '#d97706',
          700: '#b45309',
        },

        error: {
          50: '#fef2f2',
          100: '#fee2e2',
          500: '#ef4444',
          600: '#dc2626',
          700: '#b91c1c',
        },

        // Border colors
        border: {
          DEFAULT: '#374151', // gray-700
          light: '#4b5563', // gray-600
          dark: '#1f2937', // gray-800
        },
      },

      // Typography
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Menlo', 'Monaco', 'monospace'],
      },

      fontSize: {
        xs: ['0.75rem', { lineHeight: '1rem' }],
        sm: ['0.875rem', { lineHeight: '1.25rem' }],
        base: ['1rem', { lineHeight: '1.5rem' }],
        lg: ['1.125rem', { lineHeight: '1.75rem' }],
        xl: ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
      },

      // Spacing system
      spacing: {
        18: '4.5rem',
        88: '22rem',
        128: '32rem',
      },

      // Border radius
      borderRadius: {
        xl: '0.75rem',
        '2xl': '1rem',
        '3xl': '1.5rem',
      },

      // Box shadows
      boxShadow: {
        glass: '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
        glow: '0 0 20px rgba(228, 117, 163, 0.3)',
        'glow-blue': '0 0 20px rgba(112, 180, 255, 0.3)',
        card: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'card-hover': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      },

      // Backdrop blur
      backdropBlur: {
        glass: '16px',
      },

      // Forest + Orange gradients
      backgroundImage: {
        'gradient-brand': 'linear-gradient(135deg, #f97316 0%, #22c55e 100%)',
        'gradient-agent-1': 'linear-gradient(135deg, #f97316 0%, #ea580c 100%)',
        'gradient-agent-2': 'linear-gradient(135deg, #FFEAA7 0%, #eab308 100%)',
        'gradient-agent-3': 'linear-gradient(135deg, #059669 0%, #047857 100%)',
        'gradient-agent-4': 'linear-gradient(135deg, #ea580c 0%, #c2410c 100%)',
        'gradient-agent-5': 'linear-gradient(135deg, #db2777 0%, #be185d 100%)',
        'gradient-boss': 'linear-gradient(135deg, #7c2d12 0%, #991b1b 100%)',
        'gradient-forest-orange': 'linear-gradient(135deg, #0f1419 0%, #f97316 100%)',
        'gradient-multi-agent':
          'linear-gradient(135deg, #f97316 0%, #2563eb 25%, #059669 50%, #ea580c 75%, #db2777 100%)',
        'gradient-glass':
          'linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%)',
      },

      // Animation
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
        'pulse-glow': 'pulseGlow 2s ease-in-out infinite',
      },

      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        pulseGlow: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(228, 117, 163, 0.3)' },
          '50%': { boxShadow: '0 0 30px rgba(228, 117, 163, 0.5)' },
        },
      },

      // Transitions
      transitionDuration: {
        250: '250ms',
        350: '350ms',
      },
    },
  },
  plugins: [
    // Custom plugin for component classes
    function ({ addComponents, theme }) {
      addComponents({
        // Glass morphism effect
        '.glass': {
          background: 'rgba(255, 255, 255, 0.05)',
          backdropFilter: 'blur(16px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
        },

        // Card variants
        '.card': {
          backgroundColor: theme('colors.background.card'),
          borderRadius: theme('borderRadius.xl'),
          padding: theme('spacing.6'),
          boxShadow: theme('boxShadow.card'),
          transition: 'all 0.2s ease-in-out',
        },

        '.card-hover': {
          '&:hover': {
            boxShadow: theme('boxShadow.card-hover'),
            transform: 'translateY(-2px)',
          },
        },

        '.card-glass': {
          background: 'rgba(255, 255, 255, 0.05)',
          backdropFilter: 'blur(16px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          borderRadius: theme('borderRadius.xl'),
          padding: theme('spacing.6'),
        },
      })
    },
  ],
}
