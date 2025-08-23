import React, { useRef, useEffect } from 'react';
import { useAppDispatch } from '../../../hooks/useAppDispatch';
import { useAppSelector } from '../../../hooks/useAppSelector';
import { 
  setSelectedLlm,
  setSelectedEmbedding,
  setSelectedChunkSize,
  setSelectedOptions,
  setQueryText,
  setStartDate,
  setEndDate,
  resetAllFilters
} from '../../../store/slices/filtersSlice';
import { setFilteredData, resetFilters as resetResultsFilters } from '../../../store/slices/resultsSlice';
import { applyResultsFilters } from '../../../utils/filterUtils';

function FiltersSection() {
  const dispatch = useAppDispatch();
  const filters = useAppSelector(state => state.filters);
  const { allData } = useAppSelector(state => state.results);
  
  const {
    selectedLlm,
    selectedEmbedding,
    selectedChunkSize,
    selectedOptions,
    queryText,
    startDate,
    endDate,
    filterOptions
  } = filters;
  
  const [isOptionsDropdownOpen, setIsOptionsDropdownOpen] = React.useState(false);
  
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
    const newOptions = selectedOptions.includes(optionName)
      ? selectedOptions.filter(name => name !== optionName)
      : [...selectedOptions, optionName];
    dispatch(setSelectedOptions(newOptions));
  };
  
  const handleApplyFilters = () => {
    const filteredData = applyResultsFilters(allData, filters);
    dispatch(setFilteredData(filteredData));
  };

  const handleResetFilters = () => {
    dispatch(resetAllFilters());
    dispatch(resetResultsFilters());
  };

  return (
    <div className="filters">
      <h3>Filters</h3>
      <div className="filters-grid">
        <div className="filter-group">
          <label className="filter-label">LLM Model</label>
          <select 
            value={selectedLlm}
            onChange={e => dispatch(setSelectedLlm(e.target.value))}
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
            onChange={e => dispatch(setSelectedEmbedding(e.target.value))}
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
            onChange={e => dispatch(setSelectedChunkSize(e.target.value))}
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
            onChange={e => dispatch(setQueryText(e.target.value))}
            placeholder="Search in queries..."
          />
        </div>
        
        <div className="filter-group">
          <label className="filter-label">Start Date</label>
          <input
            type="date"
            value={startDate}
            onChange={e => dispatch(setStartDate(e.target.value))}
          />
        </div>
        
        <div className="filter-group">
          <label className="filter-label">End Date</label>
          <input
            type="date"
            value={endDate}
            onChange={e => dispatch(setEndDate(e.target.value))}
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