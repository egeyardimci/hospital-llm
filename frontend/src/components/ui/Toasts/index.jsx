import { useSelector } from 'react-redux';
import Toast from './components/Toast';

const ToastContainer = () => {
  const toasts = useSelector((state) => state.toast.toasts);

  if (toasts.length === 0) {
    return null;
  }

  return (
    <div className="fixed bottom-4 right-4 z-50 space-y-2">
      {toasts.map((toast) => (
        <Toast key={toast.id} toast={toast} />
      ))}
    </div>
  );
};

export default ToastContainer;
