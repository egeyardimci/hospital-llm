import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { API_ENDPOINTS } from '../../constants';

export const fetchQA = createAsyncThunk(
  'qa/fetchQA',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.FETCH_QA);
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

const qaSlice = createSlice({
  name: 'qa',
  initialState: {
    qaPairs: [],
    selectedQaPair: null,
    isLoading: false,
    error: null,
  },
  reducers: {
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchQA.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchQA.fulfilled, (state, action) => {
        state.isLoading = false;
        state.qaPairs = action.payload;
      })
      .addCase(fetchQA.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });
  },
});

export default qaSlice.reducer;