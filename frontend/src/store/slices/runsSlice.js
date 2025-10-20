import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { API_ENDPOINTS } from '../../constants';

export const fetchRuns = createAsyncThunk(
  'runs/fetchRuns',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.FETCH_RUNS);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();

      return data;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

const runsSlice = createSlice({
  name: 'config',
  initialState: {
    runs: {},
    isLoading: false,
    error: null,
  },
  reducers: {
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchRuns.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchRuns.fulfilled, (state, action) => {
        state.isLoading = false;
        state.runs = action.payload;
      })
      .addCase(fetchRuns.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });
  },
});

export default runsSlice.reducer;