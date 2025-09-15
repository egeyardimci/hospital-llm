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

export const addQA = createAsyncThunk(
  'qa/addQA',
  async (qaPair, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.ADD_QA, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(qaPair),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const { _id } = await response.json();
      return { ...qaPair, _id: _id };
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const updateQA = createAsyncThunk(
  'qa/updateQA',
  async (qaPair, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.UPDATE_QA, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(qaPair),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      await response.json();
      return qaPair;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);


export const deleteQA = createAsyncThunk(
  'qa/deleteQA',
  async (qaPair, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.DELETE_QA, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(qaPair),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      await response.json();
      return qaPair;
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
      })
      .addCase(addQA.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(addQA.fulfilled, (state, action) => {
        state.isLoading = false;
        state.qaPairs.push(action.payload);
      })
      .addCase(addQA.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      .addCase(updateQA.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(updateQA.fulfilled, (state, action) => {
        state.isLoading = false;
        const index = state.qaPairs.findIndex((qa) => qa._id === action.payload._id);
        if (index !== -1) {
          state.qaPairs[index] = action.payload;
        }
      })
      .addCase(updateQA.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      .addCase(deleteQA.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(deleteQA.fulfilled, (state, action) => {
        state.isLoading = false;
        console.log(action.payload);
        state.qaPairs = state.qaPairs.filter((qa) => qa._id !== action.payload._id);
      })
      .addCase(deleteQA.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });
  },
});

export default qaSlice.reducer;