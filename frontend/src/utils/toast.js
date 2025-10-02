import { store } from '../store';
import { addToast, showSuccess, showError, showInfo } from '../store/slices/toastSlice';

// Helper functions that can be used anywhere in the app without requiring useDispatch hook
export const toast = {
  success: (message, duration = 3000) => {
    store.dispatch(showSuccess(message, duration));
  },
  error: (message, duration = 3000) => {
    store.dispatch(showError(message, duration));
  },
  info: (message, duration = 3000) => {
    store.dispatch(showInfo(message, duration));
  },
  custom: (type, message, duration = 3000) => {
    store.dispatch(addToast({ type, message, duration }));
  }
};

// Export individual functions for flexibility
export { showSuccess, showError, showInfo, addToast } from '../store/slices/toastSlice';