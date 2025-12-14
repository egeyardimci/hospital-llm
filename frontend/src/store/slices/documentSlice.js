import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { API_ENDPOINTS } from '../../constants';

export const fetchDocument = createAsyncThunk(
  'document/fetchDocument',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.FETCH_DOCUMENT);
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

// Helper to recursively find a section by ID
const findSectionById = (sections, targetId) => {
  for (const section of sections) {
    if (section.id === targetId) {
      return section;
    }
    if (section.subsections) {
      const found = findSectionById(section.subsections, targetId);
      if (found) return found;
    }
  }
  return null;
};

const documentSlice = createSlice({
  name: 'document',
  initialState: {
    document: null,
    isLoading: false,
    error: null,
    modalOpen: false,
    focusSectionId: null,
  },
  reducers: {
    openDocumentModal: (state, action) => {
      state.modalOpen = true;
      state.focusSectionId = action.payload;
    },
    closeDocumentModal: (state) => {
      state.modalOpen = false;
      state.focusSectionId = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchDocument.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchDocument.fulfilled, (state, action) => {
        state.isLoading = false;
        state.document = action.payload;
      })
      .addCase(fetchDocument.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });
  },
});

export const { openDocumentModal, closeDocumentModal } = documentSlice.actions;
export { findSectionById };
export default documentSlice.reducer;
