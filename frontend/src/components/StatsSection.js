import React from 'react';

function StatsSection({ data }) {
  // Calculate stats
  const totalTests = data.length;
  const uniqueModels = [...new Set(data.map(item => item.llm))].length;
  
  const avgChunkSize = data.length 
    ? Math.round(data.reduce((sum, item) => sum + (item.chunk_size || 0), 0) / data.length)
    : 0;
    
  const avgVectorCount = data.length
    ? Math.round(data.reduce((sum, item) => sum + (item.similar_vector_count || 0), 0) / data.length)
    : 0;

  return (
    <div className="stats">
      <div className="stat-card">
        <div className="stat-label">Total Tests</div>
        <div className="stat-value">{totalTests}</div>
      </div>
      <div className="stat-card">
        <div className="stat-label">LLM Models</div>
        <div className="stat-value">{uniqueModels}</div>
      </div>
      <div className="stat-card">
        <div className="stat-label">Avg. Chunk Size</div>
        <div className="stat-value">{avgChunkSize}</div>
      </div>
      <div className="stat-card">
        <div className="stat-label">Avg. Similar Vectors</div>
        <div className="stat-value">{avgVectorCount}</div>
      </div>
    </div>
  );
}

export default StatsSection;