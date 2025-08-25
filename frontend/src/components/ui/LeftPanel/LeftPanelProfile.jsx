import { UserCircle } from "lucide-react";
import { TABS } from "../../../constants";

const LeftPanelProfile = ({activeTab,setActiveTab}) => {
  return (
    <div onClick={() => setActiveTab(TABS.SETTINGS)} className="flex px-2 py-2.5 border-t border-gray-200 items-center justify-start cursor-pointer">
      <div className={`flex items-center justify-start px-3 py-1.5 w-full ${activeTab === TABS.SETTINGS 
                  ? 'bg-primary rounded-lg text-white' 
                  : 'text-secondary-dark'
                }`}>
      <UserCircle />
      <div className="flex flex-col ml-3">
        <span className="font-medium text-m">Ege Yardımcı</span>
        <span className="text-xs">Domain Expert</span>
      </div>
      </div>
    </div>
  );
};

export default LeftPanelProfile;
