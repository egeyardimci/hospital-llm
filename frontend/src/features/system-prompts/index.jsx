import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Save, X, Settings, Search } from 'lucide-react';
import { useAppSelector } from '../../hooks/useAppSelector';
import { useDispatch } from 'react-redux';
import { addSystemPrompt, deleteSystemPrompt, updateSystemPrompt } from '../../store/slices/systemPromptsSlice';
import { toast } from '../../utils/toast';

const SystemPrompts = () => {
  const systemPrompts = useAppSelector(state => state.systemPrompts.systemPrompts);
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredSystemPrompts, setFilteredSystemPrompts] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [isCreating, setIsCreating] = useState(false);
  const [newSystemPrompt, setNewSystemPrompt] = useState({ title: '', content: '' });
  const dispatch = useDispatch();

  useEffect(() => {
    if (searchTerm.trim() === '') {
      setFilteredSystemPrompts(systemPrompts);
    } else {
      const filtered = systemPrompts.filter(prompt =>
        prompt.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        prompt.content.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredSystemPrompts(filtered);
    }
  }, [searchTerm, systemPrompts]);

  const handleCreateNew = () => {
    setIsCreating(true);
    setEditingId(null);
    setNewSystemPrompt({ title: '', content: '' });
  }

  const handleSave = async (data) => {
    try {
      if (editingId !== null) {
        await dispatch(updateSystemPrompt({ ...data, _id: editingId })).unwrap();
        toast.success('System prompt updated successfully');
      } else {
        await dispatch(addSystemPrompt({ ...data, _id: "" })).unwrap();
        toast.success('System prompt created successfully');
      }
      setIsCreating(false);
      setEditingId(null);
      setNewSystemPrompt({ title: '', content: '' });
    } catch (error) {
      toast.error(`Failed to save system prompt: ${error}`);
    }
  }

  const handleDelete = async (systemPrompt) => {
    try {
      await dispatch(deleteSystemPrompt(systemPrompt)).unwrap();
      toast.success('System prompt deleted successfully');
    } catch (error) {
      toast.error(`Failed to delete system prompt: ${error}`);
    }
  }

  const SystemPromptForm = ({ systemPrompt, onSave, onCancel }) => {
    const [formData, setFormData] = useState(systemPrompt);

    return (
      <div className="bg-white rounded-lg shadow p-6 mb-4 border-2 border-blue-200">
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Title
          </label>
          <input
            type="text"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter system prompt title..."
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            System Prompt Content
          </label>
          <textarea
            value={formData.content}
            onChange={(e) => setFormData({ ...formData, content: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={6}
            placeholder="Enter the system prompt content..."
          />
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => onSave(formData)}
            disabled={!formData.title.trim() || !formData.content.trim()}
            className="px-4 py-2 bg-success hover:bg-success-dark disabled:bg-gray-400 text-white rounded-md flex items-center gap-2"
          >
            <Save size={16} />
            Save
          </button>
          <button
            onClick={onCancel}
            className="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-md flex items-center gap-2"
          >
            <X size={16} />
            Cancel
          </button>
        </div>
      </div>
    );
  };

  const SystemPromptCard = ({ prompt }) => {

    return (
      <div className="bg-white rounded-lg shadow p-6 mb-4">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-800">
              {prompt.title} ({prompt._id})
            </h3>
          </div>
          <div className="flex">
            <button
              onClick={() => { setEditingId(prompt._id); setIsCreating(false); }}
              className="p-2 text-yellow-500 hover:text-yellow-700"
              title="Edit"
            >
              <Edit size={16} />
            </button>
            <button
              onClick={() => { handleDelete(prompt) }}
              className="p-2 text-danger-dark hover:text-danger"
              title="Delete"
            >
              <Trash2 size={16} />
            </button>
          </div>
        </div>

        <div className="space-y-4 text-sm">
          <div>
            <span className="font-medium text-gray-700">System Prompt:</span>
            <div className="ml-2 text-gray-600 mt-1 bg-gray-50 p-3 rounded-md">
              {prompt.content}
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="page">
      {/* Header */}
      <div className="flex flex-col items-center space-y-6 m-6">
        <Settings color="#002776" size={92} />
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-800 mb-2">System Prompts</h1>
          <p className="text-gray-600">Manage system prompts for AI conversations</p>
        </div>
        <button
          onClick={handleCreateNew}
          className="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-light flex items-center gap-2"
        >
          <Plus size={16} />
          New System Prompt
        </button>
      </div>

      {/* Search Bar */}
      <div className="bg-white rounded-lg shadow p-4 mb-6">
        <div className="flex items-center gap-2">
          <Search size={20} className="text-gray-500" />
          <input
            type="text"
            placeholder="Search system prompts..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="mt-2 text-sm text-gray-600">
          Showing {filteredSystemPrompts.length} of {systemPrompts.length} system prompts
        </div>
      </div>

      {/* New System Prompt Form */}
      {isCreating && (
        <SystemPromptForm
          systemPrompt={newSystemPrompt}
          onSave={handleSave}
          onCancel={() => setIsCreating(false)}
          isNew={true}
        />
      )}

      {/* System Prompts List */}
      <div className="space-y-4">
        {filteredSystemPrompts.map((prompt, index) => {
          const id = prompt._id;

          return editingId === id ? (
            <SystemPromptForm
              key={id}
              systemPrompt={prompt}
              onSave={handleSave}
              onCancel={() => setEditingId(null)}
            />
          ) : (
            <SystemPromptCard key={id} prompt={prompt} index={index} />
          );
        })}
      </div>

      {/* Empty State */}
      {filteredSystemPrompts.length === 0 && (
        <div className="text-center py-12 bg-white rounded-lg shadow">
          <Settings size={48} className="mx-auto text-gray-400 mb-4" />
          <p className="text-gray-500 text-lg mb-2">
            {searchTerm ? 'No system prompts match your search' : 'No system prompts found'}
          </p>
          <p className="text-gray-400 text-sm">
            {searchTerm ? 'Try a different search term' : 'Create your first system prompt to get started'}
          </p>
        </div>
      )}
    </div>
  );
};

export default SystemPrompts;