export const API_BASE_URL = 'http://127.0.0.1:8000';

export const API_ENDPOINTS = {
  RESULTS: `${API_BASE_URL}/results`,
  CHAT: `${API_BASE_URL}/chat`,
};

export const TABS = {
  RESULTS: 'results',
  CHATBOT: 'chatbot', 
  DATA: 'data',
  TEST_CONFIGURATOR: 'test-configurator',
  VECTORDB_EDITOR: 'vectordb-editor',
  QA_EDITOR: 'qa-editor',
};

export const DEFAULT_MODELS = ['gpt-4', 'gpt-3.5-turbo', 'claude-2'];
export const DEFAULT_EMBEDDINGS = ['text-embedding-ada-002', 'text-embedding-3-small'];