export const API_BASE_URL = 'http://127.0.0.1:8000';

export const API_ENDPOINTS = {
  RESULTS: `${API_BASE_URL}/results`,
  CHAT: `${API_BASE_URL}/chat`,
  VECTOR_DB_LIST: `${API_BASE_URL}/vectordb/list`,
  VECTOR_DB_MODELS: `${API_BASE_URL}/vectordb/models`,
  VECTOR_DB_CURRENT: `${API_BASE_URL}/vectordb/current`,
  VECTOR_DB_LOAD: `${API_BASE_URL}/vectordb/load`,
  VECTOR_DB_CREATE: `${API_BASE_URL}/vectordb/create`,
  FETCH_QA: `${API_BASE_URL}/qa`,
  ADD_QA: `${API_BASE_URL}/qa/add`,
  DELETE_QA: `${API_BASE_URL}/qa/delete`,
  UPDATE_QA: `${API_BASE_URL}/qa/update`,
  FETCH_TESTS: `${API_BASE_URL}/tests`,

};

export const TABS = {
  RESULTS: 'results',
  CHATBOT: 'chatbot', 
  DATA: 'data',
  TEST_CONFIGURATOR: 'test-configurator',
  VECTORDB_EDITOR: 'vectordb-editor',
  QA_EDITOR: 'qa-editor',
  SETTINGS: 'settings',
};

export const DEFAULT_MODELS = ['gpt-4', 'gpt-3.5-turbo', 'claude-2'];
export const DEFAULT_EMBEDDINGS = ['text-embedding-ada-002', 'text-embedding-3-small'];

export const customSelectTheme = (theme) => ({
    ...theme,
    colors: {
      ...theme.colors,
      primary: '#002776',        // Your primary color for selected items and focus
      primary75: '#002776bf',    // 75% opacity
      primary50: '#00277680',    // 50% opacity  
      primary25: '#00277640',    // 25% opacity for hover states
    },
  });