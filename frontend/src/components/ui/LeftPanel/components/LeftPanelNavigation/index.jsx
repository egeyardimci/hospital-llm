import { navigationItems } from './items';

const LeftPanelNavigation = ({ activeTab, setActiveTab }) => {
  return (
    <div className="mb-6 w-full">
      <nav className="space-y-2 w-full p-2">
        {navigationItems.map((item) => (
          <button
            key={item.key}
            onClick={() => setActiveTab(item.key)}
            className={`
               w-full flex items-center gap-3 px-3 py-2.5 text-left rounded-[8px] text-primary font-medium cursor-pointer
                ${
                  activeTab === item.key
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
  );
};

export default LeftPanelNavigation;
