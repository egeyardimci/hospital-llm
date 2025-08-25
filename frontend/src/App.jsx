import React, { useEffect, useState } from 'react';
import { Provider } from 'react-redux';
import { store } from './store';
import { useAppDispatch } from './hooks/useAppDispatch';
import { useAppSelector } from './hooks/useAppSelector';
import { fetchResults } from './store/slices/resultsSlice';
import { setFilterOptions } from './store/slices/filtersSlice';
import { extractFilterOptions } from './utils/filterUtils';
import { TABS } from './constants';
import './styles/tailwind.css';
import StatsSection from './features/dashboard/components/StatsSection';
import FiltersSection from './features/results/components/FiltersSection';
import ResultsContainer from './features/results/components/ResultsContainer';
import ChatbotTab from './features/chat/components/ChatbotTab';
import EvaluationScoreChart from './features/dashboard/components/DataGraph';
import Header from './components/ui/Header';
import LeftPanel from './components/ui/LeftPanel';

function AppContent() {
  const dispatch = useAppDispatch();
  const { filteredData, loading } = useAppSelector(state => state.results);
  const { filterOptions } = useAppSelector(state => state.filters);
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

  return (
    <div className="h-screen flex flex-col"> {/* Full viewport height container */}
      <Header />
      <div className="flex flex-1 min-h-0"> {/* Remaining space after header */}
        <LeftPanel activeTab={activeTab} setActiveTab={setActiveTab} />
        <div className="flex-1 p-4 overflow-y-scroll">

          {activeTab === TABS.RESULTS ? (
            <>
              <FiltersSection />
              <StatsSection data={filteredData} />
              {loading ? (
                <div className="loading">Loading results...</div>
              ) : (
                <ResultsContainer data={filteredData} />
              )}
            </>
          ) : activeTab === TABS.CHATBOT ? (
            <ChatbotTab 
              availableModels={filterOptions.llms} 
              embeddingModels={filterOptions.embeddingModels} 
            />
          ) : activeTab === TABS.DATA ? (
            <EvaluationScoreChart testData={filteredData} />
          ) : activeTab === TABS.TEST_CONFIGURATOR ? (
            <div className="p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Test Configurator</h2>
              <div className="bg-white rounded-lg shadow p-6">
                <p className="text-gray-600">Configure your test settings here.</p>
                <div className="mt-4">
                  <p className="text-sm text-gray-500">This feature is coming soon...</p>
                </div>
              </div>
            </div>
          ) : activeTab === TABS.VECTORDB_EDITOR ? (
            <div className="p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">VectorDB Editor</h2>
              <div className="bg-white rounded-lg shadow p-6">
                <p className="text-gray-600">Manage your vector database here.</p>
                <div className="mt-4">
                  <p className="text-sm text-gray-500">This feature is coming soon...</p>
                </div>
              </div>
            </div>
          ) : activeTab === TABS.QA_EDITOR ? (
            <div className="p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">QA Editor</h2>
              <div className="bg-white rounded-lg shadow p-6">
                <p className="text-gray-600">Edit questions and answers here.</p>
                <div className="mt-4">
                  <p className="text-sm text-gray-500">This feature is coming soon...</p>
                </div>
              </div>
            </div>
          ) : activeTab === TABS.SETTINGS ? (
            <div className="p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Settings</h2>
              <div className="bg-white rounded-lg shadow p-6">
                <p className="text-gray-600">Manage your settings here.</p>
                <div className="mt-4">
                  <p className="text-sm text-gray-500">This feature is coming soon...</p>
                </div>
              </div>
            </div>
          ) : null}
        </div>
      </div>
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
