import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#EC4899', // Pink-500
      light: '#F472B6', // Pink-400
      dark: '#BE185D', // Pink-700
      contrastText: '#FFFFFF'
    },
    secondary: {
      main: '#3B82F6', // Blue-500
      light: '#60A5FA', // Blue-400
      dark: '#1D4ED8', // Blue-700
      contrastText: '#FFFFFF'
    },
    background: {
      default: '#111827', // Gray-900
      paper: '#1F2937' // Gray-800
    },
    text: {
      primary: '#FFFFFF',
      secondary: '#9CA3AF', // Gray-400
      disabled: '#6B7280' // Gray-500
    },
    grey: {
      50: '#F9FAFB',
      100: '#F3F4F6',
      200: '#E5E7EB',
      300: '#D1D5DB',
      400: '#9CA3AF',
      500: '#6B7280',
      600: '#4B5563',
      700: '#374151',
      800: '#1F2937',
      900: '#111827'
    },
    success: {
      main: '#10B981', // Green-500
      light: '#34D399', // Green-400
      dark: '#059669', // Green-600
      contrastText: '#FFFFFF'
    },
    warning: {
      main: '#F59E0B', // Yellow-500
      light: '#FBBF24', // Yellow-400
      dark: '#D97706', // Yellow-600
      contrastText: '#FFFFFF'
    },
    error: {
      main: '#EF4444', // Red-500
      light: '#F87171', // Red-400
      dark: '#DC2626', // Red-600
      contrastText: '#FFFFFF'
    },
    info: {
      main: '#3B82F6', // Blue-500
      light: '#60A5FA', // Blue-400
      dark: '#1D4ED8', // Blue-700
      contrastText: '#FFFFFF'
    }
  },
  typography: {
    fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    h1: {
      fontSize: '2rem',
      fontWeight: 700,
      color: '#FFFFFF'
    },
    h2: {
      fontSize: '1.5rem',
      fontWeight: 700,
      color: '#FFFFFF'
    },
    h3: {
      fontSize: '1.125rem',
      fontWeight: 600,
      color: '#FFFFFF'
    },
    body1: {
      fontSize: '0.875rem',
      color: '#FFFFFF'
    },
    body2: {
      fontSize: '0.75rem',
      color: '#9CA3AF'
    },
    caption: {
      fontSize: '0.75rem',
      color: '#6B7280'
    }
  },
  shape: {
    borderRadius: 8
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: '8px',
          fontWeight: 600
        }
      }
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: '#1F2937',
          borderRadius: '12px'
        }
      }
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            backgroundColor: '#374151',
            borderRadius: '8px',
            '& fieldset': {
              borderColor: '#4B5563'
            },
            '&:hover fieldset': {
              borderColor: '#6B7280'
            },
            '&.Mui-focused fieldset': {
              borderColor: '#EC4899'
            }
          }
        }
      }
    }
  }
});

export default theme;