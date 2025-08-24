import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { API_ENDPOINTS } from '../../constants';

export const sendMessage = createAsyncThunk(
  'chat/sendMessage',
  async ({ selectedModel, selectedEmbedding, systemPrompt, query }, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.CHAT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          llm: selectedModel,
          query: query,
          options: []
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      return result;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

const chatSlice = createSlice({
  name: 'chat',
  initialState: {
    conversation: [],
    selectedModel: '',
    selectedEmbedding: '',
    systemPrompt: "You are a helpful assistant specializing in document analysis. Answer questions strictly based on the provided context and DO NOT use any external knowledge. Do not assume or infer information that is not explicitly stated in the context. If the context does not contain enough information, clearly state that you cannot provide an answer based on the available context. Always cite your sources by referencing the exact page numbers using this format: <a href='yourfile.pdf#page=PAGENUMBER' target='_blank'>Sayfa PAGENUMBER</a>. When multiple references exist across different pages, summarize the collective information before providing your answer. Structure your responses with bullet points, numbered lists, or short paragraphs as appropriate to the question. Communicate exclusively in Turkish, using formal and grammatically correct language unless the user's tone suggests informality is appropriate. Remember that the context is formatted as: Page Number: [page number]: [content of that page].",
    isLoading: false,
    error: null,
  },
  reducers: {
    setSelectedModel: (state, action) => {
      state.selectedModel = action.payload;
    },
    setSelectedEmbedding: (state, action) => {
      state.selectedEmbedding = action.payload;
    },
    setSystemPrompt: (state, action) => {
      state.systemPrompt = action.payload;
    },
    addUserMessage: (state, action) => {
      state.conversation.push({
        role: 'user',
        content: action.payload
      });
    },
    clearConversation: (state) => {
      state.conversation = [];
    },
    setError: (state, action) => {
      state.error = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendMessage.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(sendMessage.fulfilled, (state, action) => {
        state.isLoading = false;
        state.conversation.push(action.payload);
      })
      .addCase(sendMessage.rejected, (state, action) => {
        state.isLoading = false;
        state.conversation.push({
          role: 'system',
          content: 'Error: Failed to get response from the model. Please try again.'
        });
        state.error = action.payload;
      });
  },
});

export const {
  setSelectedModel,
  setSelectedEmbedding,
  setSystemPrompt,
  addUserMessage,
  clearConversation,
  setError,
} = chatSlice.actions;

export default chatSlice.reducer;