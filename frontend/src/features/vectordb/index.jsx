import { Database, Plus, FolderOpen, ArrowLeft } from "lucide-react"
import Select from "react-select"
import { useEffect, useState } from 'react';
import '@xterm/xterm/css/xterm.css';
import { customSelectTheme } from "../../constants";
import { useAppDispatch } from "../../hooks/useAppDispatch";
import { createVectorDB, fetchEmbeddingModels, fetchVectorDBs, loadVectorDB, setSelectedVectorDB } from "../../store/slices/vectordbSlice";
import { useAppSelector } from "../../hooks/useAppSelector";
import { toast } from "../../utils/toast";

// Create New Vector DB Component
const CreateVectorDB = () => {
  const embeddingModels = useAppSelector(state => state.vectorDBs.embeddingModels);
  const isLoading = useAppSelector(state => state.vectorDBs.loading);
  const dispatch = useAppDispatch();
  const [selectedModel, setSelectedModel] = useState(null);
  const [chunkSize, setChunkSize] = useState('');
  const [chunkOverlap, setChunkOverlap] = useState('');

  return (
    <div className="flex flex-col items-center space-y-6">
      <Database color="#002776" size={92} />
      <h3 className="text-xl font-semibold text-gray-800">Create New Vector Database</h3>

      <div className="w-full max-w-md space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Embedding Model
          </label>
          <Select
            theme={customSelectTheme}
            options={embeddingModels.map(model => ({ value: model, label: model }))}
            value={selectedModel}
            onChange={setSelectedModel}
            placeholder="Choose an embedding model..."
            className="w-full"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Chunk Size
          </label>
          <input
            type="number"
            placeholder="Enter chunk size..."
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={chunkSize}
            onChange={e => setChunkSize(e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Chunk Overlap
          </label>
          <input
            type="number"
            placeholder="Enter chunk overlap..."
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={chunkOverlap}
            onChange={e => setChunkOverlap(e.target.value)}
          />
        </div>

        <button
          disabled={isLoading}
          onClick={async () => {
            try {
              await dispatch(createVectorDB({
                embedding_model: selectedModel.value,
                chunk_size: chunkSize,
                chunk_overlap: chunkOverlap
              })).unwrap();
              toast.success('Vector database created successfully');
            } catch (error) {
              toast.error(`Failed to create vector database: ${error}`);
            }
          }}
          className="w-full bg-primary hover:bg-primary-dark disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-md transition-colors duration-200 flex items-center justify-center space-x-2"
        >
          <Plus size={16} />
          <span>Create Vector DB</span>
        </button>
      </div>
    </div>
  );
};

// Load Existing Vector DB Component
const LoadVectorDB = () => {
  const dispatch = useAppDispatch();
  const selectedDB = useAppSelector(state => state.vectorDBs.selectedVectorDB);
  const vectorDbs = useAppSelector(state => state.vectorDBs.vectorDBs);
  const isLoading = useAppSelector(state => state.vectorDBs.loading);

  return (
    <div className="flex flex-col items-center space-y-6">
      <Database color="#002776" size={92} />
      <h3 className="text-xl font-semibold text-gray-800">Load Existing Vector Database</h3>

      <div className="w-full max-w-md space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Available Vector Databases
          </label>
          <Select
            theme={customSelectTheme}
            options={vectorDbs.map(db => ({ value: `${db.name}_${db.chunk_size}_${db.chunk_overlap}`, label: `${db.name}_${db.chunk_size}_${db.chunk_overlap}` }))}
            value={{ value: selectedDB, label: selectedDB }}
            onChange={option => dispatch(setSelectedVectorDB(option.value))}
            placeholder="Choose a vector database..."
            className="w-full"
          />
        </div>

        <button
          disabled={isLoading}
          onClick={async () => {
            try {
              await dispatch(loadVectorDB({ value: selectedDB })).unwrap();
              toast.success('Vector database loaded successfully');
            } catch (error) {
              toast.error(`Failed to load vector database: ${error}`);
            }
          }}
          className="w-full bg-primary hover:bg-primary-dark disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-md transition-colors duration-200 flex items-center justify-center space-x-2"
        >
          <Database size={16} />
          <span>Load Vector DB</span>
        </button>
      </div>
    </div>
  );
};

const VectorDB = () => {
  const [selectedOption, setSelectedOption] = useState(null); // 'create' or 'load'
  const [selectedModel, setSelectedModel] = useState(null);
  const [selectedDb, setSelectedDb] = useState(null);
  const dispatch = useAppDispatch();


  useEffect(() => {
    dispatch(fetchVectorDBs());
    dispatch(fetchEmbeddingModels());
  }, [dispatch]);

  const renderContent = () => {
    if (!selectedOption) {
      return (
        <div className="flex flex-col items-center space-y-8">
          <Database color="#002776" size={92} />
          <h2 className="text-2xl font-semibold text-gray-800">Vector Database Manager</h2>
          <p className="text-gray-600 text-center max-w-md">
            Choose an option to get started with your vector database
          </p>

          <div className="flex space-x-6">
            <button
              onClick={() => setSelectedOption('create')}
              className="flex flex-col items-center p-6 bg-blue-50 hover:bg-blue-100 border-2 border-blue-200 hover:border-blue-300 rounded-lg transition-all duration-200 min-w-[200px]"
            >
              <Plus size={48} color="#002776" className="mb-3" />
              <h3 className="text-lg font-semibold text-gray-800 mb-2">Create New</h3>
              <p className="text-sm text-gray-600 text-center">
                Create a new vector database with custom settings
              </p>
            </button>

            <button
              onClick={() => setSelectedOption('load')}
              className="flex flex-col items-center p-6 bg-blue-50 hover:bg-blue-100 border-2 border-blue-200 hover:border-blue-300 rounded-lg transition-all duration-200 min-w-[200px]"
            >
              <FolderOpen size={48} color="#002776" className="mb-3" />
              <h3 className="text-lg font-semibold text-gray-800 mb-2">Load Existing</h3>
              <p className="text-sm text-gray-600 text-center">
                Load an existing vector database from your collection
              </p>
            </button>
          </div>
        </div>
      );
    }

    if (selectedOption === 'create') {
      return (
        <>
          <div className="absolute top-4 left-4">
            <div className="space-y-2">
              <button onClick={() => setSelectedOption(null)} className="flex items-center justify-center w-11 h-11 bg-white rounded-xl shadow-md border border-gray-100 hover:shadow-lg transition-all duration-200 group" > <ArrowLeft size={20} style={{ color: '#002776' }} className="group-hover:scale-110 transition-transform" /> </button>
            </div>

          </div>
          <CreateVectorDB
            selectedModel={selectedModel}
            setSelectedModel={setSelectedModel}
          />
        </>
      );
    }

    if (selectedOption === 'load') {
      return (
        <>
          <div className="absolute top-4 left-4">
            <div className="space-y-2">
              <button onClick={() => setSelectedOption(null)} className="flex items-center justify-center w-11 h-11 bg-white rounded-xl shadow-md border border-gray-100 hover:shadow-lg transition-all duration-200 group" > <ArrowLeft size={20} style={{ color: '#002776' }} className="group-hover:scale-110 transition-transform" /> </button>
            </div>

          </div>
          <LoadVectorDB
            selectedDb={selectedDb}
            setSelectedDb={setSelectedDb}
          />

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

export default VectorDB;