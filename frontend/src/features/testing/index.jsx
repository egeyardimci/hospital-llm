import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Save, X, Copy, Settings, Play, Search } from 'lucide-react';

const Testing = () => {
  const [selectedOption, setSelectedOption] = useState(null); // 'configure' or 'run'
  const [testConfigs, setTestConfigs] = useState([]);
  const [isCreating, setIsCreating] = useState(false);
  const [editingId, setEditingId] = useState(null);

  // Run tests states
  const [selectedConfigs, setSelectedConfigs] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredConfigs, setFilteredConfigs] = useState([]);
  const [runningTests, setRunningTests] = useState(false);

  const [newConfig, setNewConfig] = useState({
    test_id: '',
    test_description: '',
    llm_name: 'llama-3.3-70b-versatile',
    embedding_model_name: 'LaBSE',
    system_message: '',
    chunk_size: 500,
    chunk_overlap: 50,
    similar_vector_count: 10,
    options: []
  });

  const [newOption, setNewOption] = useState({ name: 'CE', is_enabled: true, data: '' });

  const defaultSystemMessage = "You are a highly precise document analysis assistant. Answer questions exclusively based on the provided context without using any external knowledge. Do not assume, infer, or extrapolate information beyond what is explicitly stated in the context. CONTEXT HANDLING: Analyze all context thoroughly before responding; Quote specific relevant phrases from the document using quotation marks; When information spans multiple pages, include all relevant page references; Clearly indicate when information appears contradictory across different pages; Handle tables, charts, or images mentioned in text by describing their purpose based on context; Assign confidence levels (Kesin/Muhtemel/Belirsiz) when information seems ambiguous; Flag when critical information appears to be missing. CITATION REQUIREMENTS: Include in-line citations immediately after each claim using: <a href='yourfile.pdf#page=PAGENUMBER' target='_blank'>Sayfa PAGENUMBER</a>; For direct quotes, place citation immediately after the quoted text; When information spans multiple pages, cite the full range: <a href='yourfile.pdf#page=START' target='_blank'>Sayfa START-END</a>; Always cite your sources, even for seemingly minor details. ANSWER STRUCTURE: Begin with a concise summary of the main findings; Prioritize information based on relevance to the specific question; Use bullet points for lists, numbered steps for processes, and short paragraphs for explanations; Include descriptive section headings for complex multi-part answers; End with a brief conclusion highlighting key points; Highlight key insights that directly address the core question. TURKISH LANGUAGE REQUIREMENTS: Communicate exclusively in Turkish using formal, grammatically correct language; Use informal language only when the user's tone clearly suggests informality; Adapt technical terminology appropriately for Turkish readers; Follow Turkish-specific sentence structure and syntax patterns; Use Turkish numerical formatting conventions. QUALITY CONTROL: Check for consistency between information cited from different pages; Explicitly state when numerical data is approximate or uncertain; Distinguish clearly between factual statements and organizational structure; When context does not contain sufficient information, clearly state: 'Sağlanan bağlamda bu soruya yanıt verecek yeterli bilgi bulunmamaktadır.' Remember that the context is formatted as: Page Number: [page number]: [content of that page]. Always analyze this format correctly to ensure proper page citation. CLARIFICATION PROTOCOL: If the user's query is ambiguous, incomplete, or appears to require additional context for a precise answer, ask a clear follow-up question before attempting to respond. Prioritize understanding the user's intent to ensure accurate and relevant analysis.";

  const llmOptions = [
    'llama-3.3-70b-versatile',
    'llama-3.2-90b-vision-preview',
    'meta-llama/llama-4-maverick-17b-128e-instruct',
    'mistral-saba-24b',
    'deepseek-r1-distill-llama-70b'
  ];

  const embeddingOptions = [
    'LaBSE',
    'emrecan/bert-base-turkish-cased-mean-nli-stsb-tr',
    'Snowflake/snowflake-arctic-embed-l-v2.0',
    'BAAI/bge-m3',
    'sentence-transformers/all-mpnet-base-v2'
  ];

  const crossEncoderOptions = [
    'mixedbread-ai/mxbai-rerank-base-v1',
    'cross-encoder/ms-marco-MiniLM-L6-v2',
    'BAAI/bge-reranker-v2-m3',
    'Alibaba-NLP/gte-multilingual-reranker-base'
  ];

  useEffect(() => {
    loadTestConfigs();
  }, []);

  useEffect(() => {
    if (searchTerm.trim() === '') {
      setFilteredConfigs(testConfigs);
    } else {
      const filtered = testConfigs.filter(config =>
        config.test_id.toString().toLowerCase().includes(searchTerm.toLowerCase()) ||
        config.test_description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        config.llm_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        config.embedding_model_name.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredConfigs(filtered);
    }
  }, [searchTerm, testConfigs]);

  const loadTestConfigs = async () => {
    try {
      const response = await fetch('/test_cases.json');
      const data = await response.json();
      setTestConfigs(data);
    } catch (error) {
      console.error('Error loading test configs:', error);
    }
  };

  const saveTestConfigs = async (configs) => {
    try {
      const formData = new FormData();
      const blob = new Blob([JSON.stringify(configs, null, 4)], { type: 'application/json' });
      formData.append('file', blob, 'test_cases.json');

      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = 'test_cases.json';
      link.click();
      URL.revokeObjectURL(link.href);
    } catch (error) {
      console.error('Error saving test configs:', error);
    }
  };

  const handleCreate = () => {
    const nextId = Math.max(...testConfigs.map(c => c.test_id), 0) + 1;
    setNewConfig({
      ...newConfig,
      test_id: nextId,
      system_message: defaultSystemMessage
    });
    setIsCreating(true);
  };

  const handleSaveNew = () => {
    const updatedConfigs = [...testConfigs, { ...newConfig }];
    setTestConfigs(updatedConfigs);
    saveTestConfigs(updatedConfigs);
    setIsCreating(false);
    setNewConfig({
      test_id: '',
      test_description: '',
      llm_name: 'llama-3.3-70b-versatile',
      embedding_model_name: 'LaBSE',
      system_message: '',
      chunk_size: 500,
      chunk_overlap: 50,
      similar_vector_count: 10,
      options: []
    });
  };

  const handleEdit = (config) => {
    setEditingId(config.test_id);
  };

  const handleSaveEdit = (config) => {
    const updatedConfigs = testConfigs.map(c =>
      c.test_id === config.test_id ? config : c
    );
    setTestConfigs(updatedConfigs);
    saveTestConfigs(updatedConfigs);
    setEditingId(null);
  };

  const handleDelete = (id) => {
    if (window.confirm('Are you sure you want to delete this test configuration?')) {
      const updatedConfigs = testConfigs.filter(c => c.test_id !== id);
      setTestConfigs(updatedConfigs);
      saveTestConfigs(updatedConfigs);
    }
  };

  const handleDuplicate = (config) => {
    const nextId = Math.max(...testConfigs.map(c => c.test_id), 0) + 1;
    const duplicated = {
      ...config,
      test_id: nextId,
      test_description: config.test_description + ' (Copy)'
    };
    const updatedConfigs = [...testConfigs, duplicated];
    setTestConfigs(updatedConfigs);
    saveTestConfigs(updatedConfigs);
  };

  const addOption = (configSetter, config) => {
    if (newOption.data.trim()) {
      const updatedOptions = [...(config.options || []), { ...newOption }];
      configSetter({ ...config, options: updatedOptions });
      setNewOption({ name: 'CE', is_enabled: true, data: '' });
    }
  };

  const removeOption = (configSetter, config, index) => {
    const updatedOptions = config.options.filter((_, i) => i !== index);
    configSetter({ ...config, options: updatedOptions });
  };

  const handleConfigSelect = (configId, isSelected) => {
    if (isSelected) {
      setSelectedConfigs([...selectedConfigs, configId]);
    } else {
      setSelectedConfigs(selectedConfigs.filter(id => id !== configId));
    }
  };

  const handleSelectAll = () => {
    if (selectedConfigs.length === filteredConfigs.length) {
      setSelectedConfigs([]);
    } else {
      setSelectedConfigs(filteredConfigs.map(config => config.test_id));
    }
  };

  const handleRunTests = async () => {
    setRunningTests(true);
    // Simulate running tests
    setTimeout(() => {
      setRunningTests(false);
      alert(`Running tests for ${selectedConfigs.length} configurations...`);
    }, 2000);
  };

  const ConfigForm = ({ config, onSave, onCancel, isEditing = false }) => {
    const [formConfig, setFormConfig] = useState(config);

    return (
      <div className="bg-white rounded-lg shadow p-6 mb-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Test ID
            </label>
            <input
              type="number"
              value={formConfig.test_id}
              onChange={(e) => setFormConfig({ ...formConfig, test_id: parseInt(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={isEditing}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Test Description
            </label>
            <input
              type="text"
              value={formConfig.test_description}
              onChange={(e) => setFormConfig({ ...formConfig, test_description: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Optional description"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              LLM Name
            </label>
            <select
              value={formConfig.llm_name}
              onChange={(e) => setFormConfig({ ...formConfig, llm_name: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {llmOptions.map(option => (
                <option key={option} value={option}>{option}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Embedding Model
            </label>
            <select
              value={formConfig.embedding_model_name}
              onChange={(e) => setFormConfig({ ...formConfig, embedding_model_name: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {embeddingOptions.map(option => (
                <option key={option} value={option}>{option}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Chunk Size
            </label>
            <input
              type="number"
              value={formConfig.chunk_size}
              onChange={(e) => setFormConfig({ ...formConfig, chunk_size: parseInt(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Chunk Overlap
            </label>
            <input
              type="number"
              value={formConfig.chunk_overlap}
              onChange={(e) => setFormConfig({ ...formConfig, chunk_overlap: parseInt(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Similar Vector Count
            </label>
            <input
              type="number"
              value={formConfig.similar_vector_count}
              onChange={(e) => setFormConfig({ ...formConfig, similar_vector_count: parseInt(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            System Message
          </label>
          <textarea
            value={formConfig.system_message}
            onChange={(e) => setFormConfig({ ...formConfig, system_message: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={8}
            placeholder="Enter system message..."
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Options
          </label>
          <div className="space-y-2">
            {formConfig.options && formConfig.options.map((option, index) => (
              <div key={index} className="flex items-center gap-2 p-2 bg-gray-50 rounded">
                <span className="text-sm font-medium">{option.name}:</span>
                <span className="text-sm">{option.data}</span>
                <span className={`text-xs px-2 py-1 rounded ${option.is_enabled ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                  {option.is_enabled ? 'Enabled' : 'Disabled'}
                </span>
                <button
                  onClick={() => removeOption(setFormConfig, formConfig, index)}
                  className="text-red-500 hover:text-red-700"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            ))}
          </div>
          <div className="mt-2 flex gap-2">
            <select
              value={newOption.name}
              onChange={(e) => setNewOption({ ...newOption, name: e.target.value })}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="CE">CE</option>
            </select>
            <select
              value={newOption.data}
              onChange={(e) => setNewOption({ ...newOption, data: e.target.value })}
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select Cross Encoder</option>
              {crossEncoderOptions.map(option => (
                <option key={option} value={option}>{option}</option>
              ))}
            </select>
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={newOption.is_enabled}
                onChange={(e) => setNewOption({ ...newOption, is_enabled: e.target.checked })}
                className="rounded"
              />
              <span className="text-sm">Enabled</span>
            </label>
            <button
              onClick={() => addOption(setFormConfig, formConfig)}
              className="px-3 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
            >
              Add
            </button>
          </div>
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => onSave(formConfig)}
            className="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 flex items-center gap-2"
          >
            <Save size={16} />
            Save
          </button>
          <button
            onClick={onCancel}
            className="px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600 flex items-center gap-2"
          >
            <X size={16} />
            Cancel
          </button>
        </div>
      </div>
    );
  };

  const ConfigCard = ({ config }) => (
    <div className="bg-white rounded-lg shadow p-6 mb-4">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-800">
            Test ID: {config.test_id}
          </h3>
          {config.test_description && (
            <p className="text-sm text-gray-600">{config.test_description}</p>
          )}
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => handleDuplicate(config)}
            className="p-2 text-blue-500 hover:text-blue-700"
            title="Duplicate"
          >
            <Copy size={16} />
          </button>
          <button
            onClick={() => handleEdit(config)}
            className="p-2 text-yellow-500 hover:text-yellow-700"
            title="Edit"
          >
            <Edit size={16} />
          </button>
          <button
            onClick={() => handleDelete(config.test_id)}
            className="p-2 text-red-500 hover:text-red-700"
            title="Delete"
          >
            <Trash2 size={16} />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
        <div>
          <span className="font-medium text-gray-700">LLM:</span>
          <span className="ml-2 text-gray-600">{config.llm_name}</span>
        </div>
        <div>
          <span className="font-medium text-gray-700">Embedding:</span>
          <span className="ml-2 text-gray-600">{config.embedding_model_name}</span>
        </div>
        <div>
          <span className="font-medium text-gray-700">Chunk Size:</span>
          <span className="ml-2 text-gray-600">{config.chunk_size}</span>
        </div>
        <div>
          <span className="font-medium text-gray-700">Chunk Overlap:</span>
          <span className="ml-2 text-gray-600">{config.chunk_overlap}</span>
        </div>
        <div>
          <span className="font-medium text-gray-700">Vector Count:</span>
          <span className="ml-2 text-gray-600">{config.similar_vector_count}</span>
        </div>
        <div>
          <span className="font-medium text-gray-700">Options:</span>
          <span className="ml-2 text-gray-600">
            {config.options?.length || 0} configured
          </span>
        </div>
      </div>

      {config.options && config.options.length > 0 && (
        <div className="mt-4">
          <div className="text-sm font-medium text-gray-700 mb-2">Options:</div>
          <div className="space-y-1">
            {config.options.map((option, index) => (
              <div key={index} className="text-xs bg-gray-50 p-2 rounded">
                <span className="font-medium">{option.name}:</span> {option.data}
                <span className={`ml-2 px-2 py-1 rounded ${option.is_enabled ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                  {option.is_enabled ? 'Enabled' : 'Disabled'}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  // Configure Tests Component
  const ConfigureTests = () => (
    <div className="flex flex-col items-center space-y-6">
      <Settings color="#002776" size={92} />
      <h3 className="text-xl font-semibold text-gray-800">Configure Test Settings</h3>
      <p className="text-gray-600 text-center max-w-md">
        Create and manage your AI test configurations
      </p>

      <div className="w-full max-w-6xl">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">Test Configurations</h2>
            <p className="text-gray-600">Manage your AI test configurations</p>
          </div>
          <button
            onClick={handleCreate}
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 flex items-center gap-2"
          >
            <Plus size={16} />
            New Configuration
          </button>
        </div>

        {isCreating && (
          <ConfigForm
            config={newConfig}
            onSave={handleSaveNew}
            onCancel={() => setIsCreating(false)}
          />
        )}

        <div className="space-y-4">
          {testConfigs.map((config) => (
            editingId === config.test_id ? (
              <ConfigForm
                key={config.test_id}
                config={config}
                onSave={handleSaveEdit}
                onCancel={() => setEditingId(null)}
                isEditing={true}
              />
            ) : (
              <ConfigCard key={config.test_id} config={config} />
            )
          ))}
        </div>

        {testConfigs.length === 0 && !isCreating && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No test configurations found</p>
            <p className="text-gray-400 text-sm">Create your first configuration to get started</p>
          </div>
        )}
      </div>
    </div>
  );

  // Run Tests Component
  const RunTests = () => (
    <div className="flex flex-col items-center space-y-6">
      <Play color="#002776" size={92} />
      <h3 className="text-xl font-semibold text-gray-800">Run Test Configurations</h3>
      <p className="text-gray-600 text-center max-w-md">
        Select and execute test configurations to evaluate your AI models
      </p>

      <div className="w-full max-w-6xl">
        {/* Search and Selection Controls */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="flex flex-col md:flex-row gap-4 items-center justify-between mb-4">
            <div className="flex items-center gap-2 flex-1">
              <Search size={20} className="text-gray-500" />
              <input
                type="text"
                placeholder="Search configurations by ID, description, model..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div className="flex items-center gap-4">
              <button
                onClick={handleSelectAll}
                className="px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-md"
              >
                {selectedConfigs.length === filteredConfigs.length ? 'Deselect All' : 'Select All'}
              </button>
              <span className="text-sm text-gray-600">
                {selectedConfigs.length} of {filteredConfigs.length} selected
              </span>
            </div>
          </div>

          {/* Run Tests Button */}
          <div className="flex justify-center">
            <button
              onClick={handleRunTests}
              disabled={selectedConfigs.length === 0 || runningTests}
              className="px-6 py-3 bg-green-500 hover:bg-green-600 disabled:bg-gray-400 text-white font-medium rounded-md transition-colors duration-200 flex items-center gap-2"
            >
              <Play size={16} />
              {runningTests ? 'Running Tests...' : `Run ${selectedConfigs.length} Configuration${selectedConfigs.length !== 1 ? 's' : ''}`}
            </button>
          </div>
        </div>

        {/* Configuration List */}
        <div className="space-y-4">
          {filteredConfigs.map((config) => (
            <div key={config.test_id} className="bg-white rounded-lg shadow p-6">
              <div className="flex items-start gap-4">
                <input
                  type="checkbox"
                  checked={selectedConfigs.includes(config.test_id)}
                  onChange={(e) => handleConfigSelect(config.test_id, e.target.checked)}
                  className="mt-2 w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                />
                <div className="flex-1">
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-800">
                        Test ID: {config.test_id}
                      </h3>
                      {config.test_description && (
                        <p className="text-sm text-gray-600">{config.test_description}</p>
                      )}
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                    <div>
                      <span className="font-medium text-gray-700">LLM:</span>
                      <span className="ml-2 text-gray-600">{config.llm_name}</span>
                    </div>
                    <div>
                      <span className="font-medium text-gray-700">Embedding:</span>
                      <span className="ml-2 text-gray-600">{config.embedding_model_name}</span>
                    </div>
                    <div>
                      <span className="font-medium text-gray-700">Options:</span>
                      <span className="ml-2 text-gray-600">
                        {config.options?.length || 0} configured
                      </span>
                    </div>
                    <div>
                      <span className="font-medium text-gray-700">Chunk Size:</span>
                      <span className="ml-2 text-gray-600">{config.chunk_size}</span>
                    </div>
                    <div>
                      <span className="font-medium text-gray-700">Chunk Overlap:</span>
                      <span className="ml-2 text-gray-600">{config.chunk_overlap}</span>
                    </div>
                    <div>
                      <span className="font-medium text-gray-700">Vector Count:</span>
                      <span className="ml-2 text-gray-600">{config.similar_vector_count}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredConfigs.length === 0 && (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <p className="text-gray-500 text-lg">
              {searchTerm ? 'No configurations match your search' : 'No test configurations available'}
            </p>
            <p className="text-gray-400 text-sm">
              {searchTerm ? 'Try a different search term' : 'Create configurations first to run tests'}
            </p>
          </div>
        )}
      </div>
    </div>
  );

  const renderContent = () => {
    if (!selectedOption) {
      return (
        <div className="flex flex-col items-center space-y-8">
          <Settings color="#002776" size={92} />
          <h2 className="text-2xl font-semibold text-gray-800">Test Configuration Manager</h2>
          <p className="text-gray-600 text-center max-w-md">
            Choose an option to get started with your test configurations
          </p>

          <div className="flex space-x-6">
            <button
              onClick={() => setSelectedOption('configure')}
              className="flex flex-col items-center p-6 bg-blue-50 hover:bg-blue-100 border-2 border-blue-200 hover:border-blue-300 rounded-lg transition-all duration-200 min-w-[200px]"
            >
              <Settings size={48} color="#002776" className="mb-3" />
              <h3 className="text-lg font-semibold text-gray-800 mb-2">Configure Tests</h3>
              <p className="text-sm text-gray-600 text-center">
                Create and manage AI test configurations
              </p>
            </button>

            <button
              onClick={() => setSelectedOption('run')}
              className="flex flex-col items-center p-6 bg-blue-50 hover:bg-blue-100 border-2 border-blue-200 hover:border-blue-300 rounded-lg transition-all duration-200 min-w-[200px]"
            >
              <Play size={48} color="#002776" className="mb-3" />
              <h3 className="text-lg font-semibold text-gray-800 mb-2">Run Tests</h3>
              <p className="text-sm text-gray-600 text-center">
                Execute test configurations and view results
              </p>
            </button>
          </div>
        </div>
      );
    }

    if (selectedOption === 'configure') {
      return <ConfigureTests />;
    }

    if (selectedOption === 'run') {
      return <RunTests />;
    }
  };
  const featureEnabled = false;
  if (!featureEnabled) {
    return (
      <div className="page">
        {/* Main content area */}
        <div className="flex flex-1 p-6 items-center justify-center flex-col">
          <Settings color="#002776" size={92} />
          <span className='font-bold'>Coming soon...</span>
        </div>
      </div>
    );
  }
  return (
    <div className="page">
      {/* Header with back button when option is selected */}
      {selectedOption && (
        <div className="border-b border-gray-200 p-4">
          <button
            onClick={() => setSelectedOption(null)}
            className="text-blue-500 hover:text-blue-700 flex items-center gap-2"
          >
            <X size={16} />
            Back to Main Menu
          </button>
        </div>
      )}

      {/* Main content area */}
      <div className="flex-1 p-6">
        {renderContent()}
      </div>
    </div>
  );
};

export default Testing;