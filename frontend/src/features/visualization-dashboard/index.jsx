import { useState } from 'react';
import EvaluationScoreChart from './components/EvaluationScoreChart';
import MetricsComparisonChart from './components/MetricsComparisonChart';

const VisualizationDashboard = () => {
  const [activeView, setActiveView] = useState('evaluation');

  return (
    <div style={{ padding: '20px' }}>
      {/* Navigation Tabs */}
      <div
        style={{
          display: 'flex',
          gap: '8px',
          marginBottom: '20px',
          borderBottom: '2px solid #e0e0e0',
          paddingBottom: '8px',
        }}
      >
        <button
          onClick={() => setActiveView('evaluation')}
          style={{
            padding: '12px 24px',
            backgroundColor: activeView === 'evaluation' ? '#002776' : '#f0f0f0',
            color: activeView === 'evaluation' ? 'white' : '#333',
            border: 'none',
            borderRadius: '4px 4px 0 0',
            cursor: 'pointer',
            fontWeight: activeView === 'evaluation' ? 'bold' : 'normal',
            transition: 'all 0.2s',
          }}
        >
          Evaluation Scores
        </button>
        <button
          onClick={() => setActiveView('metrics')}
          style={{
            padding: '12px 24px',
            backgroundColor: activeView === 'metrics' ? '#002776' : '#f0f0f0',
            color: activeView === 'metrics' ? 'white' : '#333',
            border: 'none',
            borderRadius: '4px 4px 0 0',
            cursor: 'pointer',
            fontWeight: activeView === 'metrics' ? 'bold' : 'normal',
            transition: 'all 0.2s',
          }}
        >
          Advanced Metrics
        </button>
      </div>

      {/* Content */}
      {activeView === 'evaluation' && <EvaluationScoreChart />}
      {activeView === 'metrics' && <MetricsComparisonChart />}
    </div>
  );
};

export default VisualizationDashboard;
