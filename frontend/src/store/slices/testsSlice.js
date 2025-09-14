import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { API_ENDPOINTS } from '../../constants';

export const fetchTests = createAsyncThunk(
  'tests/fetchTests',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.FETCH_TESTS);
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

const testsSlice = createSlice({
  name: 'tests',
  initialState: {
    tests: [],
    selectedTest: null,
    isLoading: false,
    error: null,
  },
  reducers: {
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTests.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchTests.fulfilled, (state, action) => {
        state.isLoading = false;
        state.tests = action.payload;
      })
      .addCase(fetchTests.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });
  },
});

export default testsSlice.reducer;