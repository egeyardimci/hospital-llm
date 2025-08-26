import { Database, Plus, FolderOpen } from "lucide-react"
import Select from "react-select"
import { Terminal } from '@xterm/xterm';
import { FitAddon } from '@xterm/addon-fit';
import { useEffect, useRef, useState } from 'react';
import '@xterm/xterm/css/xterm.css';
import { customSelectTheme } from "../../constants";

// Mock data - replace with your actual hook
const mockEmbeddingModels = ['text-embedding-ada-002', 'text-embedding-3-small', 'text-embedding-3-large'];
const mockVectorDbs = ['ChromaDB-1', 'Pinecone-Production', 'Weaviate-Dev'];

// Create New Vector DB Component
const CreateVectorDB = ({ selectedModel, setSelectedModel }) => {
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
            options={mockEmbeddingModels.map(model => ({ value: model, label: model }))}
            value={selectedModel}
            onChange={setSelectedModel}
            placeholder="Choose an embedding model..."
            className="w-full"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Database Name
          </label>
          <input
            type="text"
            placeholder="Enter database name..."
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <button
          disabled={!selectedModel}
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
const LoadVectorDB = ({ selectedDb, setSelectedDb }) => {
  return (
    <div className="flex flex-col items-center space-y-6">
      <FolderOpen color="#002776" size={92} />
      <h3 className="text-xl font-semibold text-gray-800">Load Existing Vector Database</h3>

      <div className="w-full max-w-md space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Available Vector Databases
          </label>
          <Select
            theme={customSelectTheme}
            options={mockVectorDbs.map(db => ({ value: db, label: db }))}
            value={selectedDb}
            onChange={setSelectedDb}
            placeholder="Choose a vector database..."
            className="w-full"
          />
        </div>

        <button
          disabled={!selectedDb}
          className="w-full bg-primary hover:bg-primary-dark disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-md transition-colors duration-200 flex items-center justify-center space-x-2"
        >
          <Database size={16} />
          <span>Load Vector DB</span>
        </button>
      </div>
    </div>
  );
};

const VectorDB = ({ logs = [] }) => {
  const [selectedOption, setSelectedOption] = useState(null); // 'create' or 'load'
  const [selectedModel, setSelectedModel] = useState(null);
  const [selectedDb, setSelectedDb] = useState(null);

  const terminalRef = useRef();
  const terminal = useRef();

  useEffect(() => {
    terminal.current = new Terminal({
      cursorBlink: true,
      fontSize: 14,
      fontFamily: 'Consolas, Monaco, monospace',
      theme: {
        background: '#1e1e1e',
        foreground: '#ffffff'
      }
    });

    const fitAddon = new FitAddon();
    terminal.current.loadAddon(fitAddon);
    terminal.current.open(terminalRef.current);
    fitAddon.fit();

    return () => terminal.current?.dispose();
  }, []);

  useEffect(() => {
    if (terminal.current && logs.length > 0) {
      const latestLog = logs[logs.length - 1];
      terminal.current.write(latestLog + '\n');
    }
  }, [logs]);

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
        <CreateVectorDB
          selectedModel={selectedModel}
          setSelectedModel={setSelectedModel}
        />
      );
    }

    if (selectedOption === 'load') {
      return (
        <LoadVectorDB
          selectedDb={selectedDb}
          setSelectedDb={setSelectedDb}
        />
      );
    }
  };

  return (
    <div className="bg-white rounded-lg shadow flex flex-col">

      {/* Main content area */}
      <div className="flex-1 p-6">
        {renderContent()}
      </div>

      {/* Fixed terminal at bottom */}
      <div className="border-t border-gray-200 bg-gray-50 p-4">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Console Output</h4>
        <div
          ref={terminalRef}
          style={{ height: '200px', width: '100%', overflow: 'hidden' }}
        />
      </div>
    </div>
  );
};

export default VectorDB;