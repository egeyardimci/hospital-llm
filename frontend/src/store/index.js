import { configureStore } from '@reduxjs/toolkit';
import resultsReducer from './slices/resultsSlice';
import chatReducer from './slices/chatSlice';
import filtersReducer from './slices/filtersSlice';
import vectorDBReducer from './slices/vectordbSlice';
import qaReducer from './slices/qaSlice';
import testsReducer from './slices/testsSlice';

export const store = configureStore({
  reducer: {
    results: resultsReducer,
    chat: chatReducer,
    filters: filtersReducer,
    vectorDBs: vectorDBReducer,
    qa: qaReducer,
    tests: testsReducer,
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