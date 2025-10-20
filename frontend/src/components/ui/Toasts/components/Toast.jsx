import { useEffect } from 'react';
import { CheckCircle, XCircle, Info, X } from 'lucide-react';
import { useDispatch } from 'react-redux';
import { removeToast } from '../../../../store/slices/toastSlice';

const Toast = ({ toast }) => {
  const dispatch = useDispatch();

  useEffect(() => {
    const timer = setTimeout(() => {
      dispatch(removeToast(toast.id));
    }, toast.duration);

    return () => clearTimeout(timer);
  }, [dispatch, toast.id, toast.duration]);

  const handleClose = () => {
    dispatch(removeToast(toast.id));
  };

  const getToastStyles = () => {
    const baseStyles =
      'flex items-center p-4 mb-3 rounded-lg shadow-lg max-w-sm w-full transform transition-all duration-300 ease-in-out';

    switch (toast.type) {
      case 'success':
        return `${baseStyles} bg-green-50 border border-green-200 text-green-800`;
      case 'error':
        return `${baseStyles} bg-red-50 border border-red-200 text-red-800`;
      case 'info':
      default:
        return `${baseStyles} bg-blue-50 border border-blue-200 text-blue-800`;
    }
  };

  const getIcon = () => {
    const iconSize = 20;
    switch (toast.type) {
      case 'success':
        return <CheckCircle size={iconSize} className="text-green-600" />;
      case 'error':
        return <XCircle size={iconSize} className="text-red-600" />;
      case 'info':
      default:
        return <Info size={iconSize} className="text-blue-600" />;
    }
  };

  return (
    <div className={getToastStyles()}>
      <div className="flex-shrink-0 mr-3">{getIcon()}</div>
      <div className="flex-1 text-sm font-medium">{toast.message}</div>
      <button
        onClick={handleClose}
        className="flex-shrink-0 ml-3 p-1 rounded-full hover:bg-gray-200 transition-colors duration-200"
      >
        <X size={16} className="text-gray-500" />
      </button>
    </div>
  );
};

export default Toast;
