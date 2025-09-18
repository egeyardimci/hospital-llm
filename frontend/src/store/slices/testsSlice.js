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


export const addTest = createAsyncThunk(
  'tests/addTest',
  async (testConfig, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.ADD_TEST, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(testConfig),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const { _id } = await response.json();
      return { ...testConfig, _id: _id };
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const updateTest = createAsyncThunk(
  'tests/updateTest',
  async (testData, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.UPDATE_TEST, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(testData),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      await response.json();
      return testData;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);


export const deleteTest = createAsyncThunk(
  'tests/deleteTest',
  async (testData, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.DELETE_TEST, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({"_id": testData._id}),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      await response.json();
      return testData;
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
      })
      .addCase(addTest.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(addTest.fulfilled, (state, action) => {
        state.isLoading = false;
        state.tests.push(action.payload);
      })
      .addCase(addTest.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      .addCase(updateTest.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(updateTest.fulfilled, (state, action) => {
        state.isLoading = false;
        const index = state.tests.findIndex((test) => test._id === action.payload._id);
        if (index !== -1) {
          state.tests[index] = action.payload;
        }
      })
      .addCase(updateTest.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      .addCase(deleteTest.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(deleteTest.fulfilled, (state, action) => {
        state.isLoading = false;
        console.log(action.payload);
        state.tests = state.tests.filter((test) => test._id !== action.payload._id);
      })
      .addCase(deleteTest.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });
  },
});

export default testsSlice.reducer;