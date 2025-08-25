import { TABS } from '../../../constants';

function Tabs({ activeTab, setActiveTab }) {
  return (
    <div className="tabs-container">
      <button 
        className={`tab-button ${activeTab === TABS.RESULTS ? 'active' : ''}`}
        onClick={() => setActiveTab(TABS.RESULTS)}
      >
        Test Results
      </button>
      <button 
        className={`tab-button ${activeTab === TABS.CHATBOT ? 'active' : ''}`}
        onClick={() => setActiveTab(TABS.CHATBOT)}
      >
        Chatbot
      </button>
      <button 
        className={`tab-button ${activeTab === TABS.DATA ? 'active' : ''}`}
        onClick={() => setActiveTab(TABS.DATA)}
      >
        Result Visualization
      </button>
    </div>
  );
}

export default Tabs;