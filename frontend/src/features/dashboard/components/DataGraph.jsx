import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import Select from 'react-select';
import { customSelectTheme } from '../../../constants';

export default function EvaluationScoreChart(testData) {
  const [data, setData] = useState([]);
  const [groupBy, setGroupBy] = useState('test_id');
  const [viewMetric, setViewMetric] = useState('avgScore');

  // Options for React Select
  const groupByOptions = [
    { value: 'llm', label: 'LLM' },
    { value: 'embedding_model', label: 'Embedding Model' },
    { value: 'test_id', label: 'Test ID' },
    { value: 'chunk_size', label: 'Chunk Size' },
    { value: 'similar_vector_count', label: 'Similar Vector Count' },
    { value: 'chunk_evaluation', label: 'Chunk Evaluation' }
  ];

  const viewMetricOptions = [
    { value: 'avgScore', label: 'Average Score' },
    { value: 'avgChunkScore', label: 'Average Chunk Score' }
  ];

  useEffect(() => {
    // Parse the raw data - this would normally come from an API or props
    const rawData = testData.testData;

    calculateAverages(rawData, groupBy);
  }, [groupBy, testData.testData]);

  const calculateAverages = (rawData, groupField) => {
    const groups = {};

    // Group data by the selected field
    rawData.forEach(item => {
      const key = item[groupField];
      if (!groups[key]) {
        groups[key] = {
          name: key,
          totalScore: 0,
          totalChunkScore: 0, // Added for chunk_evaluation_score
          count: 0,
          options: item.options,
          chunk_size: item.chunk_size,
          similar_vector_count: item.similar_vector_count,
          llm: item.llm,
          embedding_model: item.embedding_model,
          chunk_evaluation: item.chunk_evaluation, // Added new field
        };
      }
      groups[key].totalScore += item.evaluation_score;
      // Add chunk_evaluation_score to the total
      groups[key].totalChunkScore += item.chunk_evaluation_score || 0; // Using || 0 to handle undefined values
      groups[key].count += 1;

      // For metrics that shouldn't be averaged, just use the last value
      // (assuming they're consistent within a group)
      groups[key].options = item.options;
      groups[key].chunk_size = item.chunk_size;
      groups[key].similar_vector_count = item.similar_vector_count;
      groups[key].llm = item.llm;
      groups[key].embedding_model = item.embedding_model;
      groups[key].chunk_evaluation = item.chunk_evaluation;
    });

    // Calculate average for each group
    const result = Object.values(groups).map(group => ({
      name: group.name,
      avgScore: parseFloat((group.totalScore / group.count).toFixed(2)),
      avgChunkScore: parseFloat((group.totalChunkScore / group.count).toFixed(2)), // Add average chunk score
      options: group.options,
      chunk_size: group.chunk_size,
      similar_vector_count: group.similar_vector_count,
      llm: group.llm,
      embedding_model: group.embedding_model,
      chunk_evaluation: group.chunk_evaluation,
    }));

    setData(result);
    console.log("res", result);
  };

  // Get display name for metrics
  const getMetricDisplayName = (metric) => {
    const displayNames = {
      'avgScore': 'Average Score',
      'avgChunkScore': 'Average Chunk Score', // Added display name for chunk score
      'chunk_size': 'Chunk Size',
      'similar_vector_count': 'Similar Vector Count',
      'options': 'Options',
      'llm': 'LLM',
      'embedding_model': 'Embedding Model',
      'chunk_evaluation': 'Chunk Evaluation' // Added display name for chunk evaluation
    };
    return displayNames[metric] || metric;
  };

  // Helper functions to find selected options
  const findSelectedOption = (value, options) => {
    return options.find(option => option.value === value) || null;
  };

  // Custom tooltip styles matching the provided CSS
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const item = payload[0].payload;

      return (
        <div className="section-content" style={{ backgroundColor: 'white', padding: '10px', boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)', borderRadius: '4px' }}>
          <p className="meta-label" style={{ fontWeight: 'bold', marginBottom: '5px' }}>{label}</p>
          <p className="meta-value">
            <span style={{ color: '#3498db', fontWeight: 'bold' }}>
              {getMetricDisplayName(viewMetric)}: {payload[0].value}
            </span>
          </p>
          <p className="meta-value">LLM: {item.llm}</p>
          <p className="meta-value">Embedding Model: {item.embedding_model}</p>
          <p className="meta-value">Chunk Size: {item.chunk_size}</p>
          <p className="meta-value">Similar Vector Count: {item.similar_vector_count}</p>
        </div>
      );
    }
    return null;
  };

  // Get the appropriate domain for the Y-axis based on the metric
  const getYAxisDomain = () => {
    if (viewMetric === 'avgScore' || viewMetric === 'avgChunkScore') return [0, 5];
    return 'auto';
  };

  // Get chart color based on metric
  const getChartColor = () => {
    const colors = {
      'avgScore': '#002776',
      'avgChunkScore': '#002776', // Added a color for avgChunkScore
      'chunk_size': '#002776',
      'similar_vector_count': '#002776',
      'options': '#002776',
      'llm': '#002776',
      'embedding_model': '#002776',
      'chunk_evaluation': '#002776' // Added a color for chunk_evaluation
    };
    return colors[viewMetric] || '#002776';
  };

  return (
    <div className="visualization-container">
      <div className="card-header rounded-t-[8px] h-[60px]">
        <span>Result Visualization</span>
        <span className="model-badge">{data.length} Groups</span>
      </div>
      <div className="card-body">
        <div className="section">
          <div className="section-title">
            <span>View Options</span>
          </div>
          <div className="filters-grid">
            <div className="filter-group">
              <label className="filter-label">Group by:</label>
              <Select
                theme={customSelectTheme}
                value={findSelectedOption(groupBy, groupByOptions)}
                onChange={(selectedOption) => setGroupBy(selectedOption ? selectedOption.value : 'test_id')}
                options={groupByOptions}
                placeholder="Select grouping..."
                isSearchable={false}
                isClearable
              />
            </div>

            <div className="filter-group">
              <label className="filter-label">View Metric:</label>
              <Select
                theme={customSelectTheme}
                value={findSelectedOption(viewMetric, viewMetricOptions)}
                onChange={(selectedOption) => setViewMetric(selectedOption ? selectedOption.value : 'avgScore')}
                options={viewMetricOptions}
                placeholder="Select metric..."
                isSearchable={false}
                isClearable
              />
            </div>
          </div>
        </div>

        <div className="section">
          <div className="section-title">
            <span>{getMetricDisplayName(viewMetric)} Distribution</span>
          </div>
          <div style={{ height: "400px" }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={data}
                margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
                <XAxis
                  dataKey="name"
                  tick={{ fill: '#2c3e50' }}
                />
                <YAxis
                  domain={getYAxisDomain()}
                  tick={{ fill: '#2c3e50' }}
                />
                <Tooltip content={<CustomTooltip />} />
                <Legend />
                <Bar
                  dataKey={viewMetric}
                  name={getMetricDisplayName(viewMetric)}
                  fill={getChartColor()}
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="section_without_border !mb-0 !pb-0">
          <div className="stats flex flex-wrap gap-4">
            {data.map((item) => (
              <div className="stat-card p-4 bg-white rounded shadow" key={item.name}>
                <div className="stat-label font-bold">{item.name}</div>
                <div className="stat-value text-2xl">{item.avgScore}</div>
                <div className="stat-label text-sm">Average Score</div>
                <div className="stat-value text-lg">{item.avgChunkScore}</div>
                <div className="stat-label text-sm">Average Chunk Score</div>
                <div className="mt-2 text-xs">
                  <div>Chunk Size: {item.chunk_size}</div>
                  <div>Vectors: {item.similar_vector_count}</div>
                  <div>LLM: {item.llm}</div>
                  <div>Embedding: {item.embedding_model}</div>
                  <div>
                    {item.options.map((option, index) => (
                      <p key={index} style={{ margin: 0 }}>{option.data}</p>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}