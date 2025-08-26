import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Save, X, HelpCircle, Search } from 'lucide-react';

const QaEditor = () => {
  const [qaPairs, setQaPairs] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredQaPairs, setFilteredQaPairs] = useState([]);
  const [editingIndex, setEditingIndex] = useState(null);
  const [isCreating, setIsCreating] = useState(false);
  const [newQaPair, setNewQaPair] = useState({ query: '', answer: '' });

  useEffect(() => {
    loadQaPairs();
  }, []);

  useEffect(() => {
    if (searchTerm.trim() === '') {
      setFilteredQaPairs(qaPairs);
    } else {
      const filtered = qaPairs.filter(pair =>
        pair.query.toLowerCase().includes(searchTerm.toLowerCase()) ||
        pair.answer.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredQaPairs(filtered);
    }
  }, [searchTerm, qaPairs]);

  const loadQaPairs = async () => {
    try {
      const response = await fetch('/queries_expected_answers.json');
      const data = await response.json();
      setQaPairs(data);
    } catch (error) {
      console.error('Error loading Q&A pairs:', error);
    }
  };

  const saveQaPairs = async (pairs) => {
    try {
      const blob = new Blob([JSON.stringify(pairs, null, 4)], { type: 'application/json' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = 'queries_expected_answers.json';
      link.click();
      URL.revokeObjectURL(link.href);
    } catch (error) {
      console.error('Error saving Q&A pairs:', error);
    }
  };

  const handleCreate = () => {
    setNewQaPair({ query: '', answer: '' });
    setIsCreating(true);
  };

  const handleSaveNew = () => {
    if (newQaPair.query.trim() && newQaPair.answer.trim()) {
      const updatedPairs = [...qaPairs, { ...newQaPair }];
      setQaPairs(updatedPairs);
      saveQaPairs(updatedPairs);
      setIsCreating(false);
      setNewQaPair({ query: '', answer: '' });
    }
  };

  const handleEdit = (index) => {
    setEditingIndex(index);
  };

  const handleSaveEdit = (index, updatedPair) => {
    const updatedPairs = qaPairs.map((pair, i) =>
      i === index ? updatedPair : pair
    );
    setQaPairs(updatedPairs);
    saveQaPairs(updatedPairs);
    setEditingIndex(null);
  };

  const handleDelete = (index) => {
    if (window.confirm('Are you sure you want to delete this Q&A pair?')) {
      const updatedPairs = qaPairs.filter((_, i) => i !== index);
      setQaPairs(updatedPairs);
      saveQaPairs(updatedPairs);
    }
  };

  const QaForm = ({ qaPair, onSave, onCancel }) => {
    const [formData, setFormData] = useState(qaPair);

    return (
      <div className="bg-white rounded-lg shadow p-6 mb-4 border-2 border-blue-200">
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Question
          </label>
          <textarea
            value={formData.query}
            onChange={(e) => setFormData({ ...formData, query: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={3}
            placeholder="Enter your question..."
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Expected Answer
          </label>
          <textarea
            value={formData.answer}
            onChange={(e) => setFormData({ ...formData, answer: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={4}
            placeholder="Enter the expected answer..."
          />
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => onSave(formData)}
            disabled={!formData.query.trim() || !formData.answer.trim()}
            className="px-4 py-2 bg-green-500 hover:bg-green-600 disabled:bg-gray-400 text-white rounded-md flex items-center gap-2"
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

  const QaCard = ({ pair, index }) => {
    const originalIndex = qaPairs.findIndex(p => p === pair);

    return (
      <div className="bg-white rounded-lg shadow p-6 mb-4">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-800">
              Q&A Pair #{index + 1}
            </h3>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => handleEdit(originalIndex)}
              className="p-2 text-yellow-500 hover:text-yellow-700"
              title="Edit"
            >
              <Edit size={16} />
            </button>
            <button
              onClick={() => handleDelete(originalIndex)}
              className="p-2 text-red-500 hover:text-red-700"
              title="Delete"
            >
              <Trash2 size={16} />
            </button>
          </div>
        </div>

        <div className="space-y-4 text-sm">
          <div>
            <span className="font-medium text-gray-700">Question:</span>
            <div className="ml-2 text-gray-600 mt-1 bg-gray-50 p-3 rounded-md">
              {pair.query}
            </div>
          </div>

          <div>
            <span className="font-medium text-gray-700">Expected Answer:</span>
            <div className="ml-2 text-gray-600 mt-1 bg-gray-50 p-3 rounded-md">
              {pair.answer}
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
        <HelpCircle color="#002776" size={92} />
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-800 mb-2">Q&A Editor</h1>
          <p className="text-gray-600">Manage question and answer pairs for testing</p>
        </div>
        <button
          onClick={handleCreate}
          className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 flex items-center gap-2"
        >
          <Plus size={16} />
          New Q&A Pair
        </button>
      </div>

      {/* Search Bar */}
      <div className="bg-white rounded-lg shadow p-4 mb-6">
        <div className="flex items-center gap-2">
          <Search size={20} className="text-gray-500" />
          <input
            type="text"
            placeholder="Search questions and answers..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="mt-2 text-sm text-gray-600">
          Showing {filteredQaPairs.length} of {qaPairs.length} Q&A pairs
        </div>
      </div>

      {/* New Q&A Form */}
      {isCreating && (
        <QaForm
          qaPair={newQaPair}
          onSave={() => handleSaveNew()}
          onCancel={() => setIsCreating(false)}
          isNew={true}
        />
      )}

      {/* Q&A Pairs List */}
      <div className="space-y-4">
        {filteredQaPairs.map((pair, index) => {
          const originalIndex = qaPairs.findIndex(p => p === pair);

          return editingIndex === originalIndex ? (
            <QaForm
              key={originalIndex}
              qaPair={pair}
              onSave={(updatedPair) => handleSaveEdit(originalIndex, updatedPair)}
              onCancel={() => setEditingIndex(null)}
            />
          ) : (
            <QaCard key={originalIndex} pair={pair} index={index} />
          );
        })}
      </div>

      {/* Empty State */}
      {filteredQaPairs.length === 0 && (
        <div className="text-center py-12 bg-white rounded-lg shadow">
          <HelpCircle size={48} className="mx-auto text-gray-400 mb-4" />
          <p className="text-gray-500 text-lg mb-2">
            {searchTerm ? 'No Q&A pairs match your search' : 'No Q&A pairs found'}
          </p>
          <p className="text-gray-400 text-sm">
            {searchTerm ? 'Try a different search term' : 'Create your first Q&A pair to get started'}
          </p>
        </div>
      )}

      {/* Stats */}
      {qaPairs.length > 0 && (
        <div className="mt-6 bg-blue-50 rounded-lg p-4">
          <div className="flex items-center justify-between text-sm text-blue-800">
            <span>Total Q&A Pairs: {qaPairs.length}</span>
            <span>Filtered Results: {filteredQaPairs.length}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default QaEditor;