import { useState } from 'react';
import { User, Save, LogOut, Edit, X, UserCircle } from 'lucide-react';

const Settings = () => {
  const [isEditingProfile, setIsEditingProfile] = useState(false);
  const [userInfo, setUserInfo] = useState({
    name: 'John Doe',
    email: 'john.doe@example.com',
    role: 'Researcher',
    department: 'AI Research Lab',
    joinDate: '2024-01-15',
  });
  const [editedInfo, setEditedInfo] = useState({ ...userInfo });

  const handleEditProfile = () => {
    setEditedInfo({ ...userInfo });
    setIsEditingProfile(true);
  };

  const handleSaveProfile = () => {
    setUserInfo({ ...editedInfo });
    setIsEditingProfile(false);
  };

  const handleCancelEdit = () => {
    setEditedInfo({ ...userInfo });
    setIsEditingProfile(false);
  };

  const handleLogout = () => {
    if (window.confirm('Are you sure you want to log out?')) {
      // Add logout logic here
      alert('Logging out...');
    }
  };

  const ProfileForm = () => (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Full Name
          </label>
          <input
            type="text"
            value={editedInfo.name}
            onChange={(e) =>
              setEditedInfo({ ...editedInfo, name: e.target.value })
            }
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Email Address
          </label>
          <input
            type="email"
            value={editedInfo.email}
            onChange={(e) =>
              setEditedInfo({ ...editedInfo, email: e.target.value })
            }
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Role
          </label>
          <input
            type="text"
            value={editedInfo.role}
            onChange={(e) =>
              setEditedInfo({ ...editedInfo, role: e.target.value })
            }
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Department
          </label>
          <input
            type="text"
            value={editedInfo.department}
            onChange={(e) =>
              setEditedInfo({ ...editedInfo, department: e.target.value })
            }
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <div className="flex gap-2 pt-4">
        <button
          onClick={handleSaveProfile}
          className="px-4 py-2 bg-success hover:bg-success-dark text-white rounded-md flex items-center gap-2"
        >
          <Save size={16} />
          Save Changes
        </button>
        <button
          onClick={handleCancelEdit}
          className="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-md flex items-center gap-2"
        >
          <X size={16} />
          Cancel
        </button>
      </div>
    </div>
  );

  const ProfileDisplay = () => (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
        <div>
          <span className="font-medium text-gray-700">Full Name:</span>
          <span className="ml-2 text-gray-600">{userInfo.name}</span>
        </div>
        <div>
          <span className="font-medium text-gray-700">Email:</span>
          <span className="ml-2 text-gray-600">{userInfo.email}</span>
        </div>
        <div>
          <span className="font-medium text-gray-700">Role:</span>
          <span className="ml-2 text-gray-600">{userInfo.role}</span>
        </div>
        <div>
          <span className="font-medium text-gray-700">Department:</span>
          <span className="ml-2 text-gray-600">{userInfo.department}</span>
        </div>
        <div>
          <span className="font-medium text-gray-700">Member Since:</span>
          <span className="ml-2 text-gray-600">
            {new Date(userInfo.joinDate).toLocaleDateString()}
          </span>
        </div>
      </div>

      <div className="pt-4">
        <button
          onClick={handleEditProfile}
          className="px-4 py-2 bg-primary hover:bg-primary-dark text-white rounded-md flex items-center gap-2"
        >
          <Edit size={16} />
          Edit Profile
        </button>
      </div>
    </div>
  );

  return (
    <div className="page">
      {/* Header */}
      <div className="flex flex-col items-center space-y-6 mb-8 p-6">
        <UserCircle color="#002776" size={92} />
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-800 mb-2">Settings</h1>
          <p className="text-gray-600">
            Manage your account and application preferences
          </p>
        </div>
      </div>

      <div className="space-y-6">
        {/* User Profile Section */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-2 mb-6">
            <User size={20} className="text-primary" />
            <h2 className="text-lg font-semibold text-gray-800">
              Profile Information
            </h2>
          </div>

          {isEditingProfile ? <ProfileForm /> : <ProfileDisplay />}
        </div>

        {/* Account Actions Section */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-6">
            Account Actions
          </h2>

          <div className="space-y-4">
            <div className="bg-gray-50 rounded-md">
              <h3 className="font-medium text-gray-800 mb-2">
                Session Management
              </h3>
              <p className="text-sm text-gray-600 mb-4">
                Log out from your current session. You will need to sign in
                again to access the application.
              </p>
              <button
                onClick={handleLogout}
                className="px-4 py-2 bg-danger hover:bg-danger-dark text-white rounded-md flex items-center gap-2"
              >
                <LogOut size={16} />
                Logout
              </button>
            </div>
          </div>
        </div>

        {/* Application Info Section */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-6">
            Application Information
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <span className="font-medium text-gray-700">Version:</span>
              <span className="ml-2 text-gray-600">1.0.0</span>
            </div>
            <div>
              <span className="font-medium text-gray-700">Last Updated:</span>
              <span className="ml-2 text-gray-600">August 2024</span>
            </div>
            <div>
              <span className="font-medium text-gray-700">Environment:</span>
              <span className="ml-2 text-gray-600">Development</span>
            </div>
            <div>
              <span className="font-medium text-gray-700">Build:</span>
              <span className="ml-2 text-gray-600">main-2024.08.26</span>
            </div>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="bg-blue-50 rounded-lg p-4">
          <div className="flex items-center justify-between text-sm text-blue-800">
            <span>Session Status: Active</span>
            <span>Last Login: {new Date().toLocaleDateString()}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
