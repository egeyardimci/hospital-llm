import { createSlice } from '@reduxjs/toolkit';

const toastSlice = createSlice({
  name: 'toast',
  initialState: {
    toasts: []
  },
  reducers: {
    addToast: (state, action) => {
      const toast = {
        id: Date.now() + Math.random(),
        type: action.payload.type || 'info',
        message: action.payload.message,
        duration: action.payload.duration || 3000,
        timestamp: Date.now()
      };
      state.toasts.push(toast);
    },
    removeToast: (state, action) => {
      state.toasts = state.toasts.filter(toast => toast.id !== action.payload);
    },
    clearAllToasts: (state) => {
      state.toasts = [];
    }
  }
});

export const { addToast, removeToast, clearAllToasts } = toastSlice.actions;

// Helper action creators for different toast types
export const showSuccess = (message, duration) => addToast({ type: 'success', message, duration });
export const showError = (message, duration) => addToast({ type: 'error', message, duration });
export const showInfo = (message, duration) => addToast({ type: 'info', message, duration });

export default toastSlice.reducer;