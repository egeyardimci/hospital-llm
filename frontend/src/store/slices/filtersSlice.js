import { createSlice } from '@reduxjs/toolkit';

const filtersSlice = createSlice({
  name: 'filters',
  initialState: {
    selectedLlm: '',
    selectedEmbedding: '',
    selectedChunkSize: '',
    selectedOptions: [],
    queryText: '',
    selectedTestId: '',
    selectedRunCount: '',
    startDate: '',
    endDate: '',
    filterOptions: {
      llms: [],
      embeddingModels: [],
      chunkSizes: [],
      testIds: [],
      runCounts: [],
      options: []
    },
  },
  reducers: {
    setSelectedLlm: (state, action) => {
      state.selectedLlm = action.payload;
    },
    setSelectedEmbedding: (state, action) => {
      state.selectedEmbedding = action.payload;
    },
    setSelectedChunkSize: (state, action) => {
      state.selectedChunkSize = action.payload;
    },
    setSelectedOptions: (state, action) => {
      state.selectedOptions = action.payload;
    },
    setQueryText: (state, action) => {
      state.queryText = action.payload;
    },
    setStartDate: (state, action) => {
      state.startDate = action.payload;
    },
    setEndDate: (state, action) => {
      state.endDate = action.payload;
    },
    setSelectedTestId: (state, action) => {
      state.selectedTestId = action.payload;
    },
    setSelectedRunCount: (state, action) => {
      state.selectedRunCount = action.payload;
    },
    setFilterOptions: (state, action) => {
      state.filterOptions = action.payload;
    },
    resetAllFilters: (state) => {
      state.selectedLlm = '';
      state.selectedEmbedding = '';
      state.selectedChunkSize = '';
      state.selectedOptions = [];
      state.queryText = '';
      state.selectedTestId = '';
      state.selectedRunCount = '';
      state.startDate = '';
      state.endDate = '';
    },
  },
});

export const {
  setSelectedLlm,
  setSelectedEmbedding,
  setSelectedChunkSize,
  setSelectedOptions,
  setQueryText,
  setSelectedTestId,
  setSelectedRunCount,
  setStartDate,
  setEndDate,
  setFilterOptions,
  resetAllFilters,
} = filtersSlice.actions;

export default filtersSlice.reducer;