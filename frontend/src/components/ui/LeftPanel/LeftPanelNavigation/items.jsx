import { BarChart3, Database, HelpCircle, LineChart, MessageSquare, Settings } from "lucide-react";
import { TABS } from "../../../../constants";

export const navigationItems = [
    { key: TABS.CHATBOT, label: 'Chatbot', icon: <MessageSquare /> },
    { key: TABS.RESULTS, label: 'Test Results', icon: <BarChart3 /> },
    { key: TABS.DATA, label: 'Result Visualization', icon: <LineChart /> },
    { key: TABS.TEST_CONFIGURATOR, label: 'Test Configurator', icon: <Settings /> },
    { key: TABS.VECTORDB_EDITOR, label: 'VectorDB Editor', icon: <Database /> },
    { key: TABS.QA_EDITOR, label: 'QA Editor', icon: <HelpCircle /> },
  ];