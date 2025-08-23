import React, { useState, useRef, useEffect } from 'react';

function FiltersSection({ filterOptions, applyFilters, resetFilters }) {
  const [selectedLlm, setSelectedLlm] = useState('');
  const [selectedEmbedding, setSelectedEmbedding] = useState('');
  const [selectedChunkSize, setSelectedChunkSize] = useState('');
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [queryText, setQueryText] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [isOptionsDropdownOpen, setIsOptionsDropdownOpen] = useState(false);
  
  const dropdownRef = useRef(null);
  
  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOptionsDropdownOpen(false);
      }
    }
    
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const toggleOption = (optionName) => {
    setSelectedOptions(prev => 
      prev.includes(optionName)
        ? prev.filter(name => name !== optionName)
        : [...prev, optionName]
    );
  };
  
  const handleApplyFilters = () => {
    applyFilters({
      selectedLlm,
      selectedEmbedding,
      selectedChunkSize,
      selectedOptions,
      queryText,
      startDate,
      endDate
    });
  };

  const handleResetFilters = () => {
    setSelectedLlm('');
    setSelectedEmbedding('');
    setSelectedChunkSize('');
    setSelectedOptions([]);
    setQueryText('');
    setStartDate('');
    setEndDate('');
    resetFilters();
  };

  return (
    <div className="filters">
      <h3>Filters</h3>
      <div className="filters-grid">
        <div className="filter-group">
          <label className="filter-label">LLM Model</label>
          <select 
            value={selectedLlm}
            onChange={e => setSelectedLlm(e.target.value)}
          >
            <option value="">All LLMs</option>
            {filterOptions.llms.map(model => (
              <option key={model} value={model}>{model}</option>
            ))}
          </select>
        </div>
        
        <div className="filter-group">
          <label className="filter-label">Embedding Model</label>
          <select 
            value={selectedEmbedding}
            onChange={e => setSelectedEmbedding(e.target.value)}
          >
            <option value="">All Embedding Models</option>
            {filterOptions.embeddingModels.map(model => (
              <option key={model} value={model}>{model}</option>
            ))}
          </select>
        </div>
        
        <div className="filter-group">
          <label className="filter-label">Chunk Size</label>
          <select 
            value={selectedChunkSize}
            onChange={e => setSelectedChunkSize(e.target.value)}
          >
            <option value="">All Chunk Sizes</option>
            {filterOptions.chunkSizes.map(size => (
              <option key={size} value={size}>{size}</option>
            ))}
          </select>
        </div>
        
        <div className="filter-group" ref={dropdownRef}>
          <label className="filter-label">Options</label>
          <div className="custom-dropdown">
            <div 
              className="dropdown-header" 
              onClick={() => setIsOptionsDropdownOpen(!isOptionsDropdownOpen)}
            >
              {selectedOptions.length === 0 
                ? "All Options" 
                : `${selectedOptions.length} option(s) selected`}
              <span className="dropdown-arrow">▼</span>
            </div>
            
            {isOptionsDropdownOpen && (
              <div className="dropdown-options">
                {filterOptions.options.map(option => (
                  <div 
                    key={option} 
                    className="dropdown-option"
                    onClick={() => toggleOption(option)}
                  >
                    <input 
                      type="checkbox" 
                      checked={selectedOptions.includes(option)} 
                      onChange={() => {}} // Handled by div onClick
                    />
                    <span>{option}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
        
        <div className="filter-group">
          <label className="filter-label">Search Query</label>
          <input
            type="text"
            value={queryText}
            onChange={e => setQueryText(e.target.value)}
            placeholder="Search in queries..."
          />
        </div>
        
        <div className="filter-group">
          <label className="filter-label">Start Date</label>
          <input
            type="date"
            value={startDate}
            onChange={e => setStartDate(e.target.value)}
          />
        </div>
        
        <div className="filter-group">
          <label className="filter-label">End Date</label>
          <input
            type="date"
            value={endDate}
            onChange={e => setEndDate(e.target.value)}
          />
        </div>
      </div>
      
      <div className="filters-actions">
        <button onClick={handleApplyFilters}>Apply Filters</button>
        <button onClick={handleResetFilters}>Reset</button>
      </div>
      
    </div>
  );
}

export default FiltersSection;