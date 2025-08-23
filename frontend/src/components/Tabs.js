import React from 'react';

function Tabs({ activeTab, setActiveTab }) {
  return (
    <div className="tabs-container">
      <button 
        className={`tab-button ${activeTab === 'results' ? 'active' : ''}`}
        onClick={() => setActiveTab('results')}
      >
        Test Results
      </button>
      <button 
        className={`tab-button ${activeTab === 'chatbot' ? 'active' : ''}`}
        onClick={() => setActiveTab('chatbot')}
      >
        Chatbot
      </button>
      <button 
        className={`tab-button ${activeTab === 'data' ? 'active' : ''}`}
        onClick={() => setActiveTab('data')}
      >
        Result Visualization
      </button>
    </div>
  );
}

export default Tabs;