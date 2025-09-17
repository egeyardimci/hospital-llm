import { Save, Trash2, X } from "lucide-react";
import { useEffect, useState } from "react";
import { useAppSelector } from "../../hooks/useAppSelector";
import Select from 'react-select'
import { customSelectTheme } from "../../constants";

const ConfigForm = ({ formConfig, setFormConfig, onSave, onCancel }) => {
  const [newOption, setNewOption] = useState({ name: null, is_enabled: true, data: null });

  const llmModels = useAppSelector(state => state.config.config.LLM_MODELS)
  const systemPrompts = useAppSelector(state => state.systemPrompts.systemPrompts)
  const vectorDBs = useAppSelector(state => state.vectorDBs.vectorDBs)
  const ragOptionsState = useAppSelector(state => state.config.config.RAG_OPTIONS)
  const qaBatches = useAppSelector(state => state.qaBatches.qaBatches)

  const llmOptions = llmModels.map(option => ({ value: option, label: option }))
  const systemPromptOptions = systemPrompts.map(option => ({ value: option._id, label: option.title }))
  const vectorDBOptions = vectorDBs.map(option => ({ value: option.name + '_' + option.chunk_size + '_' + option.chunk_overlap, label: option.name + '_' + option.chunk_size + '_' + option.chunk_overlap }))
  const ragOptions = Object.entries(ragOptionsState).map(option => ({ value: option[0], label: option[0] }))
  const qaBatchOptions = qaBatches.map(option => ({ value: option._id, label: option.title }))

  const [ragOptionsDataOptions, setRagOptionsDataOptions] = useState([]);


  useEffect(() => {
    const options = newOption.name ? ragOptionsState[newOption.name].map(option => ({ value: option, label: option })) : [];
    setRagOptionsDataOptions(options);
  }, [newOption.name, ragOptionsState]);

  const findSelectedOption = (value, options) => {
    return options.find(option => option.value === value) || null;
  };

  const handleSelectVectorDB = (e) => {
    const [name, chunk_size, chunk_overlap] = e.value.split('_');
    setFormConfig({ ...formConfig, embedding_model_name: name, chunk_size: parseInt(chunk_size), chunk_overlap: parseInt(chunk_overlap) });
  }

  const findSelectedVectorDB = (name, chunk_size, chunk_overlap, options) => {
    const value = name && chunk_size && chunk_overlap ? name + '_' + chunk_size + '_' + chunk_overlap : null;
    return options.find(option => option.value === value) || null;
  }

  const addOption = (configSetter, config) => {
    if (newOption.data.trim()) {
      const updatedOptions = [...(config.options || []), { ...newOption }];
      configSetter({ ...config, options: updatedOptions });
      setNewOption({ name: 'CE', is_enabled: true, data: '' });
    }
    console.log(config)
  };

  const removeOption = (configSetter, config, index) => {
    const updatedOptions = config.options.filter((_, i) => i !== index);
    configSetter({ ...config, options: updatedOptions });
  };

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
            className="w-full h-[38px] px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled
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
            className="w-full h-[38px] px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Optional description"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            LLM Name
          </label>
          <Select
            theme={customSelectTheme}
            value={findSelectedOption(formConfig.llm_name, llmOptions)}
            onChange={(e) => { setFormConfig({ ...formConfig, llm_name: e.value }); console.log(e.value) }}
            options={llmOptions}
            placeholder="Select..."
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Vector DB
          </label>
          <Select
            theme={customSelectTheme}
            value={findSelectedVectorDB(formConfig.embedding_model_name, formConfig.chunk_size, formConfig.chunk_overlap, vectorDBOptions)}
            onChange={(e) => handleSelectVectorDB(e)}
            options={vectorDBOptions}
            placeholder="Select..."
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Question Batch
          </label>
          <Select
            theme={customSelectTheme}
            value={findSelectedOption(formConfig.qa_batch, qaBatchOptions)}
            onChange={(e) => setFormConfig({ ...formConfig, qa_batch: e.value })}
            options={qaBatchOptions}
            placeholder="Select..."
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
            className="w-full h-[38px] px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          System Message
        </label>
        <Select
          theme={customSelectTheme}
          value={findSelectedOption(formConfig.system_message, systemPromptOptions)}
          onChange={(e) => setFormConfig({ ...formConfig, system_message: e.value })}
          options={systemPromptOptions}
          placeholder="Select..."
        />
      </div>

      <div className="mb-4 mt-4">
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
        <div className="w-full mt-2 flex gap-2">
          <Select
            className="flex-1"
            theme={customSelectTheme}
            value={findSelectedOption(newOption.name, ragOptions)}
            onChange={(e) => { setNewOption({ ...newOption, name: e.value }); console.log(newOption) }}
            options={ragOptions}
            placeholder="Select..."
          />
          <Select
            className="flex-3"
            theme={customSelectTheme}
            value={findSelectedOption(newOption.data, ragOptionsDataOptions)}
            onChange={(e) => setNewOption({ ...newOption, data: e.value })}
            options={ragOptionsDataOptions}
            placeholder="Select..."
          />
          <button
            onClick={() => addOption(setFormConfig, formConfig)}
            className="h-[38px] px-3 py-2 bg-primary-light text-white rounded-md hover:bg-primary"
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

export default ConfigForm;