import { Edit, Play, Trash2 } from "lucide-react";
import { useState } from "react";

const ConfigCard = ({ config, handleDelete, handleEdit, handleRun }) => {
  const [isRunning, setIsRunning] = useState(false);

  const onRunClick = async (config) => {
    setIsRunning(true);
    await handleRun(config);
    // Reset after a delay (optional - adjust timing as needed)
    setTimeout(() => setIsRunning(false), 2000);
  };

  return (
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
        <div className="flex">
          <button
            onClick={() => onRunClick(config)}
            className={`p-2 rounded transition-colors ${
              isRunning
                ? 'bg-green-500 text-white'
                : 'text-green-600 hover:text-green-700 hover:bg-green-50'
            }`}
            title="Run"
            disabled={isRunning}
          >
            <Play size={16} />
          </button>
          <button
            onClick={() => handleEdit(config)}
            className="p-2 text-yellow-500 hover:text-yellow-700 hover:bg-yellow-50 rounded transition-colors"
            title="Edit"
          >
            <Edit size={16} />
          </button>
          <button
            onClick={() => handleDelete(config)}
            className="p-2 text-red-500 hover:text-red-700 hover:bg-red-50 rounded transition-colors"
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
          <span className="font-medium text-gray-700">System Prompt:</span>
          <span className="ml-2 text-gray-600">{config.system_message}</span>
        </div>
        <div>
          <span className="font-medium text-gray-700">QA Batch:</span>
          <span className="ml-2 text-gray-600">{config.qa_batch}</span>
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
                <span className={`ml-2 px-2 py-1 rounded ${
                  option.is_enabled ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
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
};

export default ConfigCard;