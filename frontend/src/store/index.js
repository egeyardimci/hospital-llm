import { configureStore } from '@reduxjs/toolkit';
import resultsReducer from './slices/resultsSlice';
import chatReducer from './slices/chatSlice';
import filtersReducer from './slices/filtersSlice';

export const store = configureStore({
  reducer: {
    results: resultsReducer,
    chat: chatReducer,
    filters: filtersReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
      },
    }),
});

// TypeScript would use these types:
// export type RootState = ReturnType<typeof store.getState>;
// export type AppDispatch = typeof store.dispatch;