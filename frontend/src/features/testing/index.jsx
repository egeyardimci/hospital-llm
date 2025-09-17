import { useState } from 'react';
import { Plus, Settings } from 'lucide-react';
import { useAppSelector } from '../../hooks/useAppSelector';
import ConfigCard from './ConfigCard';
import ConfigForm from './ConfigForm';
import { useDispatch } from 'react-redux';
import { addTest, deleteTest, updateTest } from '../../store/slices/testsSlice';

const Testing = () => {
  const testConfigs = useAppSelector(state => state.tests.tests)
  const [isCreating, setIsCreating] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const dispatch = useDispatch();

  const [newConfig, setNewConfig] = useState();

  const handleCreate = () => {
    const nextId = Math.max(...testConfigs.map(c => c.test_id), 0) + 1;
    setNewConfig({
      _id: '',
      test_description: '',
      llm_name: '',
      embedding_model_name: '',
      system_message: '',
      chunk_size: 0,
      chunk_overlap: 0,
      similar_vector_count: 10,
      qa_batch: '',
      options: [],
      test_id: nextId,
    });
    setIsCreating(true);
  };

  const handleSaveNew = () => {
    dispatch(addTest(newConfig));
    setIsCreating(false);
    setNewConfig(null);
  };

  const handleEdit = (config) => {
    setEditingId(config.test_id);
    setNewConfig(config);
    console.log(config);
    setIsCreating(false);
  };

  const handleSaveEdit = (config) => {
    dispatch(updateTest(config));
    setEditingId(null);
    setNewConfig(null);
  };

  const handleDelete = (config) => {
    dispatch(deleteTest(config));
  };

  return (
    <div className="page relative">
      {/* Main content area */}
      <div className="flex-1 p-6">
        <div className="flex flex-col items-center space-y-6">
          <Settings color="#002776" size={92} />
          <h3 className="text-xl font-semibold text-gray-800">Configure Test Settings</h3>
          <p className="text-gray-600 text-center max-w-md">
            Create and manage your AI test configurations
          </p>

          <div className="w-full">
            <div className="flex justify-between items-center mb-6">
              <div>
                <h2 className="text-2xl font-bold text-gray-800">Test Configurations</h2>
                <p className="text-gray-600">Manage your AI test configurations</p>
              </div>
              <button
                onClick={handleCreate}
                className="px-4 py-2 bg-primary-light text-white rounded-md hover:bg-primary flex items-center gap-2"
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
                formConfig={newConfig}
                setFormConfig={setNewConfig}
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
                    formConfig={newConfig}
                    setFormConfig={setNewConfig}
                  />
                ) : (
                  <ConfigCard key={config.test_id} config={config} handleDelete={handleDelete} handleEdit={handleEdit} />
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
      </div>
    </div>
  );
};

export default Testing;