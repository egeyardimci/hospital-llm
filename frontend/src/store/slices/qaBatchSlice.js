import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { API_ENDPOINTS } from '../../constants';

export const fetchQABatches = createAsyncThunk(
  'qaBatches/fetchQABatches',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.FETCH_QA_BATCHES);
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

export const addQABatch = createAsyncThunk(
  'qaBatches/addQABatch',
  async (qaBatch, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.ADD_QA_BATCH, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(qaBatch),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const { _id } = await response.json();
      return { ...qaBatch, _id: _id };
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const updateQABatch = createAsyncThunk(
  'qaBatches/updateQABatch',
  async (qaBatch, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.UPDATE_QA_BATCH, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(qaBatch),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      await response.json();
      return qaBatch;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);


export const deleteQABatch = createAsyncThunk(
  'qaBatches/deleteQABatch',
  async (qaBatch, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.DELETE_QA_BATCH, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(qaBatch),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      await response.json();
      return qaBatch;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);


const qaBatchSlice = createSlice({
  name: 'qaBatches',
  initialState: {
    qaBatches: [],
    selectedQABatch: null,
    isLoading: false,
    error: null,
  },
  reducers: {
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchQABatches.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchQABatches.fulfilled, (state, action) => {
        state.isLoading = false;
        state.qaBatches = action.payload;
      })
      .addCase(fetchQABatches.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      .addCase(addQABatch.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(addQABatch.fulfilled, (state, action) => {
        state.isLoading = false;
        state.qaBatches.push(action.payload);
      })
      .addCase(addQABatch.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      .addCase(updateQABatch.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(updateQABatch.fulfilled, (state, action) => {
        state.isLoading = false;
        const index = state.qaBatches.findIndex((qa) => qa._id === action.payload._id);
        if (index !== -1) {
          state.qaBatches[index] = action.payload;
        }
      })
      .addCase(updateQABatch.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      .addCase(deleteQABatch.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(deleteQABatch.fulfilled, (state, action) => {
        state.isLoading = false;
        console.log(action.payload);
        state.qaBatches = state.qaBatches.filter((qa) => qa._id !== action.payload._id);
      })
      .addCase(deleteQABatch.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });
  },
});

export default qaBatchSlice.reducer;