import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  colorSchemes: {
    dark: {
      palette: {
        primary: {
          main: '#E475A3',
          light: '#E784A1',
          dark: '#D06B9E',
          contrastText: '#FFFFFF'
        },
        secondary: {
          main: '#70B4FF',
          light: '#A0C3FF',
          dark: '#6F72D1',
          contrastText: '#FFFFFF'
        },
        background: {
          default: '#1A1A1A',
          paper: '#212121'
        },
        text: {
          primary: '#FFFFFF',
          secondary: '#A0A0A0',
          disabled: '#6E6E6E'
        },
        divider: '#363636',
        grey: {
          50: '#FAFAFA',
          100: '#F5F5F5',
          200: '#EEEEEE',
          300: '#E0E0E0',
          400: '#BDBDBD',
          500: '#9E9E9E',
          600: '#757575',
          700: '#616161',
          800: '#424242',
          900: '#212121'
        }
      }
    }
  },
  typography: {
    fontFamily: 'Inter, sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 700,
      lineHeight: 1.2
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
      lineHeight: 1.3
    },
    h3: {
      fontSize: '1.5rem',
      fontWeight: 600,
      lineHeight: 1.4
    },
    h4: {
      fontSize: '1.25rem',
      fontWeight: 600,
      lineHeight: 1.4
    },
    h5: {
      fontSize: '1.125rem',
      fontWeight: 600,
      lineHeight: 1.4
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 600,
      lineHeight: 1.4
    },
    body1: {
      fontSize: '1rem',
      fontWeight: 400,
      lineHeight: 1.5
    },
    body2: {
      fontSize: '0.875rem',
      fontWeight: 400,
      lineHeight: 1.5
    }
  },
  shape: {
    borderRadius: 8
  }
});

export default theme;