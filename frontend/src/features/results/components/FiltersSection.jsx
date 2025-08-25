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

  // Consistent select styling
  const selectClasses = "w-full px-3 py-2 text-sm border border-gray-300 rounded-md bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 appearance-none cursor-pointer";
  const inputClasses = "w-full px-3 py-2 text-sm border border-gray-300 rounded-md bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500";

  return (
    <div className="filters">
      <h3 className="text-lg font-semibold mb-4 text-gray-900">Filters</h3>
      <div className="filters-grid">
        <div className="filter-group">
          <label className="block text-sm font-medium text-gray-700 mb-2">LLM Model</label>
          <select 
            className={selectClasses}
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
          <label className="block text-sm font-medium text-gray-700 mb-2">Embedding Model</label>
          <select 
            className={selectClasses}
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
          <label className="block text-sm font-medium text-gray-700 mb-2">Chunk Size</label>
          <select 
            className={selectClasses}
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
          <label className="block text-sm font-medium text-gray-700 mb-2">Options</label>
          <div className="relative">
            <div 
              className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 cursor-pointer flex items-center justify-between"
              onClick={() => setIsOptionsDropdownOpen(!isOptionsDropdownOpen)}
            >
              <span className={selectedOptions.length === 0 ? 'text-gray-500' : 'text-gray-900'}>
                {selectedOptions.length === 0 
                  ? "All Options" 
                  : `${selectedOptions.length} option(s) selected`}
              </span>
              <svg 
                className={`w-4 h-4 text-gray-400 transition-transform duration-200 ${
                  isOptionsDropdownOpen ? 'transform rotate-180' : ''
                }`}
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </div>
            
            {isOptionsDropdownOpen && (
              <div className="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
                {filterOptions.options.map(option => (
                  <div 
                    key={option} 
                    className="px-3 py-2 text-sm cursor-pointer hover:bg-gray-50 flex items-center space-x-2"
                    onClick={() => toggleOption(option)}
                  >
                    <input 
                      type="checkbox" 
                      className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      checked={selectedOptions.includes(option)} 
                      onChange={() => {}} // Handled by div onClick
                    />
                    <span className="text-gray-700">{option}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
        
        <div className="filter-group">
          <label className="block text-sm font-medium text-gray-700 mb-2">Search Query</label>
          <input
            className={inputClasses}
            type="text"
            value={queryText}
            onChange={e => dispatch(setQueryText(e.target.value))}
            placeholder="Search in queries..."
          />
        </div>
        
        <div className="filter-group">
          <label className="block text-sm font-medium text-gray-700 mb-2">Start Date</label>
          <input
            className={inputClasses}
            type="date"
            value={startDate}
            onChange={e => dispatch(setStartDate(e.target.value))}
          />
        </div>
        
        <div className="filter-group">
          <label className="block text-sm font-medium text-gray-700 mb-2">End Date</label>
          <input
            className={inputClasses}
            type="date"
            value={endDate}
            onChange={e => dispatch(setEndDate(e.target.value))}
          />
        </div>
      </div>
      
      <div className="filters-actions mt-6 flex">
        <button 
          className="button px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
          onClick={handleApplyFilters}
        >
          Apply Filters
        </button>
        <button 
          className="button px-4 py-2 bg-gray-200 text-gray-700 text-sm font-medium rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors"
          onClick={handleResetFilters}
        >
          Reset
        </button>
      </div>
    </div>
  );
}

export default FiltersSection;