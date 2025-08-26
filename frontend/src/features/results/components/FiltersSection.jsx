import { useAppDispatch } from '../../../hooks/useAppDispatch';
import { useAppSelector } from '../../../hooks/useAppSelector';
import Select from 'react-select'
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
import { customSelectTheme } from '../../../constants';

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

  const handleApplyFilters = () => {
    const filteredData = applyResultsFilters(allData, filters);
    dispatch(setFilteredData(filteredData));
  };

  const handleResetFilters = () => {
    dispatch(resetAllFilters());
    dispatch(resetResultsFilters());
  };

  console.log(filters);

  // Consistent select styling
  const inputClasses = "w-full px-3 py-2 text-sm border border-gray-300 rounded-md bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500";

  // Helper function to find selected option object
  const findSelectedOption = (value, options) => {
    return options.find(option => option.value === value) || null;
  };

  // Helper function to find multiple selected options
  const findSelectedOptions = (values, options) => {
    if (!Array.isArray(values)) return [];
    return options.filter(option => values.includes(option.value));
  };

  // Prepare options
  const llmOptions = filterOptions.llms.map(model => ({ value: model, label: model }));
  const embeddingOptions = filterOptions.embeddingModels.map(model => ({ value: model, label: model }));
  const chunkSizeOptions = filterOptions.chunkSizes.map(size => ({ value: size, label: size }));
  const optionsOptions = filterOptions.options.map(option => ({ value: option, label: option }));

  return (
    <div className="filters">
      <div className="card-header rounded-t-[8px] h-[60px] m-0">
        <span>Test Results</span>
      </div>
      <div className='p-[15px]'>
        <h3 className="text-lg font-semibold mb-4 text-gray-900">Filters</h3>
        <div className="filters-grid">
          <div className="filter-group">
            <label className="block text-sm font-medium text-gray-700 mb-2">LLM Model</label>
            <Select
              theme={customSelectTheme}
              value={findSelectedOption(selectedLlm, llmOptions)}
              onChange={e => dispatch(setSelectedLlm(e ? e.value : null))}
              options={llmOptions}
              placeholder="Select..."
              isClearable
            />
          </div>

          <div className="filter-group">
            <label className="block text-sm font-medium text-gray-700 mb-2">Embedding Model</label>
            <Select
              theme={customSelectTheme}
              value={findSelectedOption(selectedEmbedding, embeddingOptions)}
              onChange={e => dispatch(setSelectedEmbedding(e ? e.value : null))}
              options={embeddingOptions}
              placeholder="Select..."
              isClearable
            />
          </div>

          <div className="filter-group">
            <label className="block text-sm font-medium text-gray-700 mb-2">Chunk Size</label>
            <Select
              theme={customSelectTheme}
              value={findSelectedOption(selectedChunkSize, chunkSizeOptions)}
              onChange={e => dispatch(setSelectedChunkSize(e ? e.value : null))}
              options={chunkSizeOptions}
              placeholder="Select..."
              isClearable
            />
          </div>

          <div className="filter-group">
            <label className="block text-sm font-medium text-gray-700 mb-2">Options</label>
            <Select
              theme={customSelectTheme}
              name="options"
              isMulti
              className="basic-multi-select"
              classNamePrefix="select"
              value={findSelectedOptions(selectedOptions, optionsOptions)}
              onChange={e => dispatch(setSelectedOptions(e ? e.map(option => option.value) : []))}
              options={optionsOptions}
              placeholder="Select..."
            />
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
    </div>
  );
}

export default FiltersSection;