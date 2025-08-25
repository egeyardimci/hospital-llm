import React from 'react';
import { TABS } from '../../../constants';
import {
  BarChart3,
  MessageSquare,
  LineChart,
  Settings,
  Database,
  HelpCircle,
} from "lucide-react";

function LeftPanel({ activeTab, setActiveTab }) {
  const navigationItems = [
    { key: TABS.CHATBOT, label: 'Chatbot', icon: <MessageSquare /> },
    { key: TABS.RESULTS, label: 'Test Results', icon: <BarChart3/> },
    { key: TABS.DATA, label: 'Result Visualization', icon: <LineChart /> },
    { key: TABS.TEST_CONFIGURATOR, label: 'Test Configurator', icon: <Settings /> },
    { key: TABS.VECTORDB_EDITOR, label: 'VectorDB Editor', icon: <Database /> },
    { key: TABS.QA_EDITOR, label: 'QA Editor', icon: <HelpCircle /> },
  ];

  return (
    <div className="w-[240px] bg-white border-r border-gray-200 pt-4 flex flex-col">
      <div className="mb-6 w-full">
        <nav className="space-y-2 w-full p-2">
          {navigationItems.map((item) => (
            <button
              key={item.key}
              onClick={() => setActiveTab(item.key)}
              className={`
               w-full flex items-center gap-3 px-3 py-2.5 text-left rounded-[8px] text-primary font-medium cursor-pointer
                ${activeTab === item.key 
                  ? 'bg-primary text-white ' 
                  : 'bg-white text-secondary-dark hover:bg-primary hover:text-white'
                }
              `}
            >
              <span className="text-lg">{item.icon}</span>
              <span className="text-sm">{item.label}</span>
            </button>
          ))}
        </nav>
      </div>
    </div>
  );
}

export default LeftPanel;