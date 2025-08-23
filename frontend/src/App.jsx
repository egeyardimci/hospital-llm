import React, { useEffect, useState } from 'react';
import { Provider } from 'react-redux';
import { store } from './store';
import { useAppDispatch } from './hooks/useAppDispatch';
import { useAppSelector } from './hooks/useAppSelector';
import { fetchResults } from './store/slices/resultsSlice';
import { setFilterOptions } from './store/slices/filtersSlice';
import { extractFilterOptions } from './utils/filterUtils';
import { TABS } from './constants';
import './App.css';
import StatsSection from './features/dashboard/components/StatsSection';
import FiltersSection from './features/results/components/FiltersSection';
import ResultsContainer from './features/results/components/ResultsContainer';
import ChatbotTab from './features/chat/components/ChatbotTab';
import Tabs from './components/ui/Tabs';
import EvaluationScoreChart from './features/dashboard/components/DataGraph';

function AppContent() {
  const dispatch = useAppDispatch();
  const { filteredData, loading } = useAppSelector(state => state.results);
  const { filterOptions } = useAppSelector(state => state.filters);
  const [activeTab, setActiveTab] = useState(TABS.RESULTS);

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
    <div className="container">
      <h1>LLM Question-Answer Testing Visualizer</h1>

      <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />

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
      ) : null}
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
