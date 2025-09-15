import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { API_ENDPOINTS } from '../../constants';

export const fetchSystemPrompts = createAsyncThunk(
  'systemPrompts/fetchSystemPrompts',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.FETCH_SYSTEM_PROMPTS);
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

export const addSystemPrompt = createAsyncThunk(
  'systemPrompts/addSystemPrompt',
  async (systemPrompt, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.ADD_SYSTEM_PROMPT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(systemPrompt),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const { _id } = await response.json();
      return { ...systemPrompt, _id: _id };
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const updateSystemPrompt = createAsyncThunk(
  'systemPrompts/updateSystemPrompt',
  async (systemPrompt, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.UPDATE_SYSTEM_PROMPT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(systemPrompt),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      await response.json();
      return systemPrompt;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const deleteSystemPrompt = createAsyncThunk(
  'systemPrompts/deleteSystemPrompt',
  async (systemPrompt, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.DELETE_SYSTEM_PROMPT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(systemPrompt),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      await response.json();
      return systemPrompt;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

const systemPromptsSlice = createSlice({
  name: 'systemPrompts',
  initialState: {
    systemPrompts: [],
    selectedSystemPrompt: null,
    isLoading: false,
    error: null,
  },
  reducers: {
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchSystemPrompts.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchSystemPrompts.fulfilled, (state, action) => {
        state.isLoading = false;
        state.systemPrompts = action.payload;
      })
      .addCase(fetchSystemPrompts.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      .addCase(addSystemPrompt.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(addSystemPrompt.fulfilled, (state, action) => {
        state.isLoading = false;
        state.systemPrompts.push(action.payload);
      })
      .addCase(addSystemPrompt.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      .addCase(updateSystemPrompt.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(updateSystemPrompt.fulfilled, (state, action) => {
        state.isLoading = false;
        const index = state.systemPrompts.findIndex((prompt) => prompt._id === action.payload._id);
        if (index !== -1) {
          state.systemPrompts[index] = action.payload;
        }
      })
      .addCase(updateSystemPrompt.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      .addCase(deleteSystemPrompt.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(deleteSystemPrompt.fulfilled, (state, action) => {
        state.isLoading = false;
        state.systemPrompts = state.systemPrompts.filter((prompt) => prompt._id !== action.payload._id);
      })
      .addCase(deleteSystemPrompt.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });
  },
});

export default systemPromptsSlice.reducer;