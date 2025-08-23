import React, { useState, useEffect } from 'react';
import './App.css';
import StatsSection from './components/StatsSection';
import FiltersSection from './components/FiltersSection';
import ResultsContainer from './components/ResultsContainer';
import ChatbotTab from './components/ChatbotTab';
import Tabs from './components/Tabs';
import EvaluationScoreChart from './components/DataGraph';

function App() {
  const [allData, setAllData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('results'); // 'results' or 'chatbot'
  const [filterOptions, setFilterOptions] = useState({
    llms: [],
    embeddingModels: [],
    chunkSizes: [],
    options: []
  });

  // Generate unique test IDs
  const generateTestId = (index, llm) => {
    const llmPrefix = llm.split("-")[0].substring(0, 3).toUpperCase();
    return `${llmPrefix}-${String(index + 1).padStart(3, "0")}`;
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch the JSON data from the backend endpoint
        const response = await fetch('http://127.0.0.1:8000/results');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        // Add unique IDs to each test
        const processedData = data.map((item, index) => ({
          ...item,
          testId: generateTestId(index, item.llm)
        }));

        setAllData(processedData);
        setFilteredData(processedData);

        // Extract unique values for filters
        const llms = [...new Set(processedData.map(item => item.llm))];
        const embeddingModels = [...new Set(processedData.map(item => item.embedding_model))];
        const chunkSizes = [...new Set(processedData.map(item => item.chunk_size))];
        const options = [...new Set(processedData.flatMap(item => item.options.map(opt => opt.name)))];


        setFilterOptions({
          llms: llms.sort(),
          embeddingModels: embeddingModels.sort(),
          chunkSizes: chunkSizes.sort((a, b) => a - b),
          options: options.sort()
        });
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);
  const applyFilters = (filters) => {
    const {
      selectedLlm,
      selectedEmbedding,
      selectedChunkSize,
      selectedOptions,
      queryText,
      startDate,
      endDate,
    } = filters;
  
    const newFilteredData = allData.filter((item) => {
      const llmMatch = selectedLlm ? item.llm === selectedLlm : true;
      const embeddingMatch = selectedEmbedding
        ? item.embedding_model === selectedEmbedding
        : true;
      const chunkSizeMatch = selectedChunkSize
        ? item.chunk_size === parseInt(selectedChunkSize, 10)
        : true;
      const queryMatch = queryText
        ? item.query?.toLowerCase().includes(queryText.toLowerCase())
        : true;
      const startDateMatch = startDate
        ? new Date(item.time_stamp) >= new Date(startDate)
        : true;
      const endDateMatch = endDate
        ? new Date(item.time_stamp) <= new Date(endDate)
        : true;
      
        const optionsMatch = selectedOptions.length > 0
        ? selectedOptions.every(option => 
            item.options?.some(opt => opt.name === option)
          )
        : true;
      
      
      return (
        llmMatch &&
        embeddingMatch &&
        chunkSizeMatch &&
        queryMatch &&
        startDateMatch &&
        endDateMatch &&
        optionsMatch
      );
    });
  
    setFilteredData(newFilteredData);
  };
  

  const resetFilters = () => {
    setFilteredData(allData);
  };

  return (
    <div className="container">
      <h1>LLM Question-Answer Testing Visualizer</h1>

      <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />

      {activeTab === 'results' ? (
        <>
          <FiltersSection 
            filterOptions={filterOptions}
            applyFilters={applyFilters}
            resetFilters={resetFilters}
          />

          <StatsSection data={filteredData} />

          {loading ? (
            <div className="loading">Loading results...</div>
          ) : (
            <ResultsContainer data={filteredData} />
          )}
        </>
      ) : activeTab === 'chatbot' ? (
        <ChatbotTab 
          availableModels={filterOptions.llms} 
          embeddingModels={filterOptions.embeddingModels} 
        />
      ) : activeTab === 'data' ? (

        <EvaluationScoreChart testData={filteredData}>
        </EvaluationScoreChart>
        ) : null}
    </div>
  );
}

export default App;
