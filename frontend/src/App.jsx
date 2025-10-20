import { useEffect, useState } from 'react';
import { Provider } from 'react-redux';
import { store } from './store';
import { useAppDispatch } from './hooks/useAppDispatch';
import { fetchResults } from './store/slices/resultsSlice';
import { setFilterOptions } from './store/slices/filtersSlice';
import { extractFilterOptions } from './utils/filterUtils';
import { TABS } from './constants';
import './styles/tailwind.css';
import ChatbotTab from './features/chat';
import Header from './components/ui/Header';
import LeftPanel from './components/ui/LeftPanel';
import Testing from './features/testing';
import VectorDB from './features/vectordb';
import QaEditor from './features/qa-editor';
import SystemPrompts from './features/system-prompts';
import Settings from './features/settings';
import { fetchQA } from './store/slices/qaSlice';
import { fetchTests } from './store/slices/testsSlice';
import { fetchSystemPrompts } from './store/slices/systemPromptsSlice';
import { fetchQABatches } from './store/slices/qaBatchSlice';
import { fetchConfig } from './store/slices/configSlice';
import { fetchVectorDBs } from './store/slices/vectordbSlice';
import { fetchRuns } from './store/slices/runsSlice';
import ResultsTab from './features/results';
import VisualizationDashboard from './features/visualization-dashboard';
import ToastContainer from './components/ui/Toasts';

function AppContent() {
  const dispatch = useAppDispatch();
  const [activeTab, setActiveTab] = useState(TABS.CHATBOT);

  useEffect(() => {
    const fetchData = async () => {
      const resultAction = await dispatch(fetchResults());
      if (fetchResults.fulfilled.match(resultAction)) {
        const filterOpts = extractFilterOptions(resultAction.payload);
        dispatch(setFilterOptions(filterOpts));
      }
    };

    fetchData();
  }, [dispatch]);

  useEffect(() => {
    dispatch(fetchTests());
    dispatch(fetchQA());
    dispatch(fetchSystemPrompts());
    dispatch(fetchQABatches());
    dispatch(fetchConfig());
    dispatch(fetchVectorDBs());
    dispatch(fetchRuns());
  }, [dispatch]);

  return (
    <div className="h-screen flex flex-col">
      {' '}
      {/* Full viewport height container */}
      <Header />
      <div className="flex flex-1 min-h-0">
        {' '}
        {/* Remaining space after header */}
        <LeftPanel activeTab={activeTab} setActiveTab={setActiveTab} />
        <div className="flex-1 p-4 overflow-y-scroll">
          {activeTab === TABS.RESULTS ? (
            <ResultsTab />
          ) : activeTab === TABS.CHATBOT ? (
            <ChatbotTab />
          ) : activeTab === TABS.DATA ? (
            <VisualizationDashboard />
          ) : activeTab === TABS.TEST_CONFIGURATOR ? (
            <Testing />
          ) : activeTab === TABS.VECTORDB_EDITOR ? (
            <VectorDB />
          ) : activeTab === TABS.QA_EDITOR ? (
            <QaEditor />
          ) : activeTab === TABS.SYSTEM_PROMPTS ? (
            <SystemPrompts />
          ) : activeTab === TABS.SETTINGS ? (
            <Settings />
          ) : null}
        </div>
      </div>
      <ToastContainer />
    </div>
  );
}

function App() {
  return (
    <Provider store={store}>
      <AppContent />
    </Provider>
  );
}

export default App;
