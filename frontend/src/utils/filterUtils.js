export const applyResultsFilters = (allData, filters) => {
  const {
    selectedLlm,
    selectedEmbedding,
    selectedChunkSize,
    selectedOptions,
    queryText,
    selectedTestId,
    selectedRunCount,
    startDate,
    endDate,
  } = filters;

  return allData.filter((item) => {
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
    const testIdMatch = selectedTestId
      ? item.test_id === parseInt(selectedTestId, 10)
      : true;
    const runCountMatch = selectedRunCount
      ? item.run_count === parseInt(selectedRunCount, 10)
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
      testIdMatch &&
      runCountMatch &&
      startDateMatch &&
      endDateMatch &&
      optionsMatch
    );
  });
};

export const extractFilterOptions = (data) => {
  const llms = [...new Set(data.map(item => item.llm))];
  const embeddingModels = [...new Set(data.map(item => item.embedding_model))];
  const chunkSizes = [...new Set(data.map(item => item.chunk_size))];
  const testIds = [...new Set(data.map(item => item.test_id))];
  const runCounts = [...new Set(data.map(item => item.run_count).filter(count => count !== undefined && count !== null))];
  const options = [...new Set(data.flatMap(item => item.options.map(opt => opt.name)))];

  return {
    llms: llms.sort(),
    embeddingModels: embeddingModels.sort(),
    chunkSizes: chunkSizes.sort((a, b) => a - b),
    testIds: testIds.sort((a, b) => a - b),
    runCounts: runCounts.sort((a, b) => a - b),
    options: options.sort()
  };
};