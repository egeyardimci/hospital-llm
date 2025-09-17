import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Save, X, HelpCircle, Search, ArrowLeft, Layers } from 'lucide-react';
import Select from 'react-select';
import { useAppSelector } from '../../hooks/useAppSelector';
import { useDispatch } from 'react-redux';
import { addQA, deleteQA, updateQA, fetchQA } from '../../store/slices/qaSlice';
import { addQABatch, deleteQABatch, updateQABatch, fetchQABatches } from '../../store/slices/qaBatchSlice';
import { customSelectTheme } from '../../constants';

// Q&A Pairs Component
const QAPairsEditor = () => {
  const qaPairs = useAppSelector(state => state.qa.qaPairs);
  const qaBatches = useAppSelector(state => state.qaBatches.qaBatches);
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredQaPairs, setFilteredQaPairs] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [isCreating, setIsCreating] = useState(false);
  const [newQaPair, setNewQaPair] = useState({ query: '', answer: '', batch_id: '' });
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(fetchQA());
    dispatch(fetchQABatches());
  }, [dispatch]);

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

  const handleCreateNew = () => {
    setIsCreating(true);
    setEditingId(null);
    setNewQaPair({ query: '', answer: '', batch_id: '' });
  }

  const handleSave = (data) => {
    if (editingId !== null) {
      // Update existing Q&A pair
      dispatch(updateQA({ ...data, _id: editingId }));
    } else {
      // Create new Q&A pair
      dispatch(addQA({ ...data, _id: "" }));
    }
    setIsCreating(false);
    setEditingId(null);
    setNewQaPair({ query: '', answer: '', batch_id: '' });
  }

  const handleDelete = (qaPair) => {
    //dispatch action
    dispatch(deleteQA(qaPair));
  }

  const QaForm = ({ qaPair, onSave, onCancel }) => {
    const [formData, setFormData] = useState(qaPair);

    // Create options for batch selector
    const batchOptions = [
      { value: '', label: 'No batch selected' },
      ...qaBatches.map(batch => ({
        value: batch._id,
        label: batch.title
      }))
    ];

    // Find selected batch option
    const selectedBatch = batchOptions.find(option => option.value === formData.batch_id) || batchOptions[0];

    return (
      <div className="bg-white rounded-lg shadow p-6 mb-4 border-2 border-blue-200">
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            QA Batch
          </label>
          <Select
            theme={customSelectTheme}
            options={batchOptions}
            value={selectedBatch}
            onChange={(option) => setFormData({ ...formData, batch_id: option.value })}
            placeholder="Select a batch (optional)..."
            className="w-full"
            isClearable
            isSearchable
          />
        </div>

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

  const QaCard = ({ pair }) => {
    // Find the batch for this Q&A pair
    const associatedBatch = qaBatches.find(batch => batch._id === pair.batch_id);

    return (
      <div className="bg-white rounded-lg shadow p-6 mb-4">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-800">
              Q&A Pair ({pair._id})
            </h3>
            {associatedBatch && (
              <div className="mt-2">
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  <Layers size={12} className="mr-1" />
                  {associatedBatch.title}
                </span>
              </div>
            )}
          </div>
          <div className="flex">
            <button
              onClick={() => { setEditingId(pair._id); setIsCreating(false); }}
              className="p-2 text-yellow-500 hover:text-yellow-700"
              title="Edit"
            >
              <Edit size={16} />
            </button>
            <button
              onClick={() => { handleDelete(pair) }}
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

          {associatedBatch && (
            <div>
              <span className="font-medium text-gray-700">Batch Description:</span>
              <div className="ml-2 text-gray-600 mt-1 bg-gray-50 p-3 rounded-md">
                {associatedBatch.description}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };
  return (
    <div className="flex flex-col items-center space-y-6">
      <HelpCircle color="#002776" size={92} />
      <h3 className="text-xl font-semibold text-gray-800">Q&A Pairs Editor</h3>

      <div className="w-full">
        <div className="flex justify-center mb-6">
          <button
            onClick={handleCreateNew}
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
            onSave={handleSave}
            onCancel={() => setIsCreating(false)}
            isNew={true}
          />
        )}

        {/* Q&A Pairs List */}
        <div className="space-y-4">
          {filteredQaPairs.map((pair, index) => {
            const id = pair._id;

            return editingId === id ? (
              <QaForm
                key={id}
                qaPair={pair}
                onSave={handleSave}
                onCancel={() => setEditingId(null)}
              />
            ) : (
              <QaCard key={id} pair={pair} index={index} />
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
      </div>
    </div>
  );
};

// QA Batches Component
const QABatchesEditor = () => {
  const qaBatches = useAppSelector(state => state.qaBatches.qaBatches);
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredQABatches, setFilteredQABatches] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [isCreating, setIsCreating] = useState(false);
  const [newQABatch, setNewQABatch] = useState({ title: '', description: '' });
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(fetchQABatches());
  }, [dispatch]);

  useEffect(() => {
    if (searchTerm.trim() === '') {
      setFilteredQABatches(qaBatches);
    } else {
      const filtered = qaBatches.filter(batch =>
        batch.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        batch.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredQABatches(filtered);
    }
  }, [searchTerm, qaBatches]);

  const handleCreateNew = () => {
    setIsCreating(true);
    setEditingId(null);
    setNewQABatch({ title: '', description: '' });
  }

  const handleSave = (data) => {
    if (editingId !== null) {
      // Update existing QA Batch
      dispatch(updateQABatch({ ...data, _id: editingId }));
    } else {
      // Create new QA Batch
      dispatch(addQABatch({ ...data, _id: "" }));
    }
    setIsCreating(false);
    setEditingId(null);
    setNewQABatch({ title: '', description: '' });
  }

  const handleDelete = (qaBatch) => {
    dispatch(deleteQABatch(qaBatch));
  }

  const QABatchForm = ({ qaBatch, onSave, onCancel }) => {
    const [formData, setFormData] = useState(qaBatch);

    return (
      <div className="bg-white rounded-lg shadow p-6 mb-4 border-2 border-blue-200">
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Title
          </label>
          <input
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter batch title..."
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Description
          </label>
          <textarea
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={4}
            placeholder="Enter batch description..."
          />
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => onSave(formData)}
            disabled={!formData.title.trim() || !formData.description.trim()}
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

  const QABatchCard = ({ batch }) => {
    return (
      <div className="bg-white rounded-lg shadow p-6 mb-4">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-800">
              QA Batch ({batch._id})
            </h3>
          </div>
          <div className="flex">
            <button
              onClick={() => { setEditingId(batch._id); setIsCreating(false); }}
              className="p-2 text-yellow-500 hover:text-yellow-700"
              title="Edit"
            >
              <Edit size={16} />
            </button>
            <button
              onClick={() => { handleDelete(batch) }}
              className="p-2 text-danger-dark hover:text-danger"
              title="Delete"
            >
              <Trash2 size={16} />
            </button>
          </div>
        </div>

        <div className="space-y-4 text-sm">
          <div>
            <span className="font-medium text-gray-700">Title:</span>
            <div className="ml-2 text-gray-600 mt-1 bg-gray-50 p-3 rounded-md">
              {batch.title}
            </div>
          </div>

          <div>
            <span className="font-medium text-gray-700">Description:</span>
            <div className="ml-2 text-gray-600 mt-1 bg-gray-50 p-3 rounded-md">
              {batch.description}
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="flex flex-col items-center space-y-6">
      <Layers color="#002776" size={92} />
      <h3 className="text-xl font-semibold text-gray-800">QA Batches Editor</h3>

      <div className="w-full">
        <div className="flex justify-center mb-6">
          <button
            onClick={handleCreateNew}
            className="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-light flex items-center gap-2"
          >
            <Plus size={16} />
            New QA Batch
          </button>
        </div>

        {/* Search Bar */}
        <div className="bg-white rounded-lg shadow p-4 mb-6">
          <div className="flex items-center gap-2">
            <Search size={20} className="text-gray-500" />
            <input
              type="text"
              placeholder="Search batch titles and descriptions..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="mt-2 text-sm text-gray-600">
            Showing {filteredQABatches.length} of {qaBatches.length} QA batches
          </div>
        </div>

        {/* New QA Batch Form */}
        {isCreating && (
          <QABatchForm
            qaBatch={newQABatch}
            onSave={handleSave}
            onCancel={() => setIsCreating(false)}
            isNew={true}
          />
        )}

        {/* QA Batches List */}
        <div className="space-y-4">
          {filteredQABatches.map((batch, index) => {
            const id = batch._id;

            return editingId === id ? (
              <QABatchForm
                key={id}
                qaBatch={batch}
                onSave={handleSave}
                onCancel={() => setEditingId(null)}
              />
            ) : (
              <QABatchCard key={id} batch={batch} index={index} />
            );
          })}
        </div>

        {/* Empty State */}
        {filteredQABatches.length === 0 && (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <Layers size={48} className="mx-auto text-gray-400 mb-4" />
            <p className="text-gray-500 text-lg mb-2">
              {searchTerm ? 'No QA batches match your search' : 'No QA batches found'}
            </p>
            <p className="text-gray-400 text-sm">
              {searchTerm ? 'Try a different search term' : 'Create your first QA batch to get started'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

// Main QA Editor Component with selectedOption structure
const QaEditor = () => {
  const [selectedOption, setSelectedOption] = useState(null); // 'qa-pairs' or 'qa-batches'

  const renderContent = () => {
    if (!selectedOption) {
      return (
        <div className="flex flex-col items-center space-y-8">
          <HelpCircle color="#002776" size={92} />
          <h2 className="text-2xl font-semibold text-gray-800">Q&A Editor</h2>
          <p className="text-gray-600 text-center max-w-md">
            Choose an option to manage your Q&A content
          </p>

          <div className="flex space-x-6">
            <button
              onClick={() => setSelectedOption('qa-pairs')}
              className="flex flex-col items-center p-6 bg-blue-50 hover:bg-blue-100 border-2 border-blue-200 hover:border-blue-300 rounded-lg transition-all duration-200 min-w-[200px]"
            >
              <HelpCircle size={48} color="#002776" className="mb-3" />
              <h3 className="text-lg font-semibold text-gray-800 mb-2">Q&A Pairs</h3>
              <p className="text-sm text-gray-600 text-center">
                Manage individual question and answer pairs for testing
              </p>
            </button>

            <button
              onClick={() => setSelectedOption('qa-batches')}
              className="flex flex-col items-center p-6 bg-blue-50 hover:bg-blue-100 border-2 border-blue-200 hover:border-blue-300 rounded-lg transition-all duration-200 min-w-[200px]"
            >
              <Layers size={48} color="#002776" className="mb-3" />
              <h3 className="text-lg font-semibold text-gray-800 mb-2">QA Batches</h3>
              <p className="text-sm text-gray-600 text-center">
                Organize Q&A content into batches with titles and descriptions
              </p>
            </button>
          </div>
        </div>
      );
    }

    if (selectedOption === 'qa-pairs') {
      return (
        <>
          <div className="absolute top-4 left-4">
            <div className="space-y-2">
              <button onClick={() => setSelectedOption(null)} className="flex items-center justify-center w-11 h-11 bg-white rounded-xl shadow-md border border-gray-100 hover:shadow-lg transition-all duration-200 group" > <ArrowLeft size={20} style={{ color: '#002776' }} className="group-hover:scale-110 transition-transform" /> </button>
            </div>
          </div>
          <QAPairsEditor />
        </>
      );
    }

    if (selectedOption === 'qa-batches') {
      return (
        <>
          <div className="absolute top-4 left-4">
            <div className="space-y-2">
              <button onClick={() => setSelectedOption(null)} className="flex items-center justify-center w-11 h-11 bg-white rounded-xl shadow-md border border-gray-100 hover:shadow-lg transition-all duration-200 group" > <ArrowLeft size={20} style={{ color: '#002776' }} className="group-hover:scale-110 transition-transform" /> </button>
            </div>
          </div>
          <QABatchesEditor />
        </>
      );
    }
  };

  return (
    <div className="page flex flex-col relative">
      {/* Main content area */}
      <div className="flex-1 p-6">
        {renderContent()}
      </div>
    </div>
  );
};

export default QaEditor;