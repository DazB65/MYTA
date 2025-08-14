import React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import { CacheProvider } from '@emotion/react';
import createCache from '@emotion/cache';
import theme from './theme';
import AppRouter from './AppRouter';

const createEmotionCache = () => {
  return createCache({
    key: 'mui',
    prepend: true,
  });
};

const emotionCache = createEmotionCache();

const App: React.FC = () => {
  return (
    <CacheProvider value={emotionCache}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <AppRouter />
      </ThemeProvider>
    </CacheProvider>
  );
};

export default App;