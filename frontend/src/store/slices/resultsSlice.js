import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { API_ENDPOINTS } from '../../constants';

export const fetchResults = createAsyncThunk(
  'results/fetchResults',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.RESULTS);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      
      const generateTestId = (index, llm) => {
        const llmPrefix = llm.split("-")[0].substring(0, 3).toUpperCase();
        return `${llmPrefix}-${String(index + 1).padStart(3, "0")}`;
      };

      const processedData = data.map((item, index) => ({
        ...item,
        testId: generateTestId(index, item.llm)
      }));

      return processedData;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

const resultsSlice = createSlice({
  name: 'results',
  initialState: {
    allData: [],
    filteredData: [],
    loading: false,
    error: null,
  },
  reducers: {
    setFilteredData: (state, action) => {
      state.filteredData = action.payload;
    },
    resetFilters: (state) => {
      state.filteredData = state.allData;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchResults.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchResults.fulfilled, (state, action) => {
        state.loading = false;
        state.allData = action.payload;
        state.filteredData = action.payload;
      })
      .addCase(fetchResults.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { setFilteredData, resetFilters } = resultsSlice.actions;
export default resultsSlice.reducer;