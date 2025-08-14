import React from 'react';
import { Snackbar, Alert, Stack } from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../../store';
import { removeNotification } from '../../store/slices/uiSlice';

const NotificationSystem: React.FC = () => {
  const dispatch = useDispatch();
  const { notifications } = useSelector((state: RootState) => state.ui);

  const handleClose = (notificationId: string) => {
    dispatch(removeNotification(notificationId));
  };

  return (
    <Stack
      spacing={1}
      sx={{
        position: 'fixed',
        top: 80,
        right: 16,
        zIndex: 1400,
        maxWidth: 400,
      }}
    >
      {notifications.map((notification) => (
        <Snackbar
          key={notification.id}
          open={true}
          autoHideDuration={6000}
          onClose={() => handleClose(notification.id)}
          anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
        >
          <Alert
            onClose={() => handleClose(notification.id)}
            severity={notification.type}
            variant="filled"
            sx={{ width: '100%' }}
          >
            <strong>{notification.title}</strong>
            <br />
            {notification.message}
          </Alert>
        </Snackbar>
      ))}
    </Stack>
  );
};

export default NotificationSystem;