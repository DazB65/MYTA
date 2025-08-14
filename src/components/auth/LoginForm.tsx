import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Stack,
  Alert,
  CircularProgress,
} from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../store';
import { loginStart, loginSuccess, loginFailure } from '../../store/slices/authSlice';
import { User } from '../../types';

const LoginForm: React.FC = () => {
  const dispatch = useDispatch();
  const { loading, error } = useSelector((state: RootState) => state.auth);
  const [credentials, setCredentials] = useState({
    email: '',
    password: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    dispatch(loginStart());

    try {
      // Mock login - replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const mockUser: User = {
        id: '1',
        email: credentials.email,
        name: 'Demo User',
        subscription_tier: 'pro',
        youtube_connected: true,
        created_at: new Date(),
      };

      dispatch(loginSuccess({ user: mockUser, token: 'demo-token' }));
    } catch (err: any) {
      dispatch(loginFailure(err.message || 'Login failed'));
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        bgcolor: 'background.default',
        p: 2,
      }}
    >
      <Card sx={{ maxWidth: 400, width: '100%' }}>
        <CardContent sx={{ p: 4 }}>
          <Stack spacing={3}>
            <Box textAlign="center">
              <Typography variant="h4" sx={{ fontWeight: 700, color: 'primary.main', mb: 1 }}>
                Vidalytics
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Sign in to your account
              </Typography>
            </Box>

            {error && (
              <Alert severity="error" sx={{ borderRadius: 2 }}>
                {error}
              </Alert>
            )}

            <form onSubmit={handleSubmit}>
              <Stack spacing={3}>
                <TextField
                  name="email"
                  type="email"
                  label="Email"
                  value={credentials.email}
                  onChange={handleChange}
                  required
                  fullWidth
                  variant="outlined"
                />
                
                <TextField
                  name="password"
                  type="password"
                  label="Password"
                  value={credentials.password}
                  onChange={handleChange}
                  required
                  fullWidth
                  variant="outlined"
                />

                <Button
                  type="submit"
                  variant="contained"
                  size="large"
                  fullWidth
                  disabled={loading}
                  sx={{ 
                    py: 1.5,
                    borderRadius: 2,
                    textTransform: 'none',
                    fontSize: '1rem',
                    fontWeight: 600,
                  }}
                >
                  {loading ? (
                    <CircularProgress size={24} color="inherit" />
                  ) : (
                    'Sign In'
                  )}
                </Button>
              </Stack>
            </form>

            <Typography variant="body2" color="text.secondary" textAlign="center">
              Demo credentials: any email/password combination
            </Typography>
          </Stack>
        </CardContent>
      </Card>
    </Box>
  );
};

export default LoginForm;