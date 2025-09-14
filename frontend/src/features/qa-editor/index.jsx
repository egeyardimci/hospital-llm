import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Save, X, HelpCircle, Search } from 'lucide-react';
import { useAppSelector } from '../../hooks/useAppSelector';

const QaEditor = () => {
  const qaPairs = useAppSelector(state => state.qa.qaPairs);
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredQaPairs, setFilteredQaPairs] = useState([]);
  const [editingIndex, setEditingIndex] = useState(null);
  const [isCreating, setIsCreating] = useState(false);
  const [newQaPair] = useState({ query: '', answer: '' });

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
            className="px-4 py-2 bg-success hover:bg-success-light disabled:bg-gray-400 text-white rounded-md flex items-center gap-2"
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

  const QaCard = ({ pair }) => {

    return (
      <div className="bg-white rounded-lg shadow p-6 mb-4">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-800">
              Q&A Pair ({pair._id})
            </h3>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => { }}
              className="p-2 text-yellow-500 hover:text-yellow-700"
              title="Edit"
            >
              <Edit size={16} />
            </button>
            <button
              onClick={() => { }}
              className="p-2 text-danger-dark hover:text-danger"
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
          onClick={() => { }}
          className="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-light flex items-center gap-2"
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
          onSave={() => { }}
          onCancel={() => setIsCreating(false)}
          isNew={true}
        />
      )}

      {/* Q&A Pairs List */}
      <div className="space-y-4">
        {filteredQaPairs.map((pair, index) => {
          const originalIndex = index

          return editingIndex === originalIndex ? (
            <QaForm
              key={originalIndex}
              qaPair={pair}
              onSave={() => { }}
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