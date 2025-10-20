import LeftPanelNavigation from './components/LeftPanelNavigation';
import LeftPanelProfile from './components/LeftPanelProfile';

function LeftPanel({ activeTab, setActiveTab }) {
  return (
    <div className="w-[240px] bg-white border-r border-gray-200 pt-4 flex flex-col justify-between">
      <LeftPanelNavigation activeTab={activeTab} setActiveTab={setActiveTab} />
      <LeftPanelProfile activeTab={activeTab} setActiveTab={setActiveTab} />
    </div>
  );
}

export default LeftPanel;
