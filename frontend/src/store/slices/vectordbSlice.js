import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { API_ENDPOINTS } from '../../constants';

export const fetchVectorDBs = createAsyncThunk(
  'results/fetchVectorDBs',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.VECTOR_DB_LIST);
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


export const fetchEmbeddingModels = createAsyncThunk(
  'results/fetchEmbeddingModels',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.VECTOR_DB_MODELS);
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

export const fetchCurrentVectorDB = createAsyncThunk(
  'results/fetchCurrentVectorDB',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.VECTOR_DB_CURRENT);
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

export const loadVectorDB = createAsyncThunk(
  'results/loadVectorDB',
  async ({value}, { rejectWithValue }) => {
    try {
      const selectedDBParts = value.split('_');
      const [name, chunk_size, chunk_overlap] = selectedDBParts;
      const response = await fetch(`${API_ENDPOINTS.VECTOR_DB_LOAD}`, {
        method: 'POST',
        body: JSON.stringify({
          name: name,
          chunk_size: chunk_size,
          chunk_overlap: chunk_overlap
        }),
        headers: { 'Content-Type': 'application/json' }
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      await response.json();

      return `${name}_${chunk_size}_${chunk_overlap}`;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const createVectorDB = createAsyncThunk(
  'results/createVectorDB',
  async ({embedding_model, chunk_size, chunk_overlap}, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.VECTOR_DB_CREATE, {
        method: 'POST',
        body: JSON.stringify({
          name: embedding_model,
          chunk_size: chunk_size,
          chunk_overlap: chunk_overlap
        }),
        headers: { 'Content-Type': 'application/json' }
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      console.log(embedding_model)
      await response.json();

      return {name: embedding_model, chunk_size: chunk_size, chunk_overlap: chunk_overlap};
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
)

const vectordbSlice = createSlice({
  name: 'vectorDBs',
  initialState: {
    vectorDBs: [],
    embeddingModels: [],
    selectedVectorDB: null,
    currentVectorDB: null,
    loading: false,
    error: null,
  },
  reducers: {
    setVectordbData: (state, action) => {
      state.vectorDBs = action.payload;
    },
    setSelectedVectorDB: (state, action) => {
      state.selectedVectorDB = action.payload;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchVectorDBs.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchVectorDBs.fulfilled, (state, action) => {
        state.loading = false;
        state.vectorDBs = action.payload;
      })
      .addCase(fetchVectorDBs.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(fetchEmbeddingModels.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchEmbeddingModels.fulfilled, (state, action) => {
        state.loading = false;
        state.embeddingModels = action.payload;
      })
      .addCase(fetchEmbeddingModels.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(fetchCurrentVectorDB.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchCurrentVectorDB.fulfilled, (state, action) => {
        state.loading = false;
        state.currentVectorDB = action.payload;
        state.selectedVectorDB = action.payload;
      })
      .addCase(fetchCurrentVectorDB.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(loadVectorDB.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(loadVectorDB.fulfilled, (state, action) => {
        state.loading = false;
        state.currentVectorDB = action.payload;
      })
      .addCase(loadVectorDB.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(createVectorDB.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createVectorDB.fulfilled, (state, action) => {
        state.loading = false;
        console.log(action.payload);
        state.vectorDBs.push({
          name: action.payload.name,
          chunk_size: action.payload.chunk_size,
          chunk_overlap: action.payload.chunk_overlap
        });
      })
      .addCase(createVectorDB.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
    }
});

export const { setVectordbData, setSelectedVectorDB } = vectordbSlice.actions;
export default vectordbSlice.reducer;