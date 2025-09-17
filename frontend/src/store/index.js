import { configureStore } from '@reduxjs/toolkit';
import resultsReducer from './slices/resultsSlice';
import chatReducer from './slices/chatSlice';
import filtersReducer from './slices/filtersSlice';
import vectorDBReducer from './slices/vectordbSlice';
import qaReducer from './slices/qaSlice';
import qaBatchReducer from './slices/qaBatchSlice';
import systemPromptsReducer from './slices/systemPromptsSlice';
import testsReducer from './slices/testsSlice';
import configReducer from './slices/configSlice';

export const store = configureStore({
  reducer: {
    results: resultsReducer,
    chat: chatReducer,
    filters: filtersReducer,
    vectorDBs: vectorDBReducer,
    qa: qaReducer,
    qaBatches: qaBatchReducer,
    systemPrompts: systemPromptsReducer,
    tests: testsReducer,
    config: configReducer,
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