import React from 'react';
import { Provider } from 'react-redux';
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import { CacheProvider } from '@emotion/react';
import createCache from '@emotion/cache';
import { store } from './store';
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
      <Provider store={store}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <AppRouter />
        </ThemeProvider>
      </Provider>
    </CacheProvider>
  );
};

export default App;