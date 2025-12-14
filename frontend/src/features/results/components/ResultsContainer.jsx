import ResultCard from './ResultCard';
import DocumentModal from './DocumentModal';

function ResultsContainer({ data }) {
  if (data.length === 0) {
    return (
      <div id="results-container">
        <DocumentModal />
        <div className="card">
          <div className="card-body">No results match your filters.</div>
        </div>
      </div>
    );
  }

  return (
    <div id="results-container">
      <DocumentModal />
      {data.map((item, index) => (
        <ResultCard
          key={item.testId || `test-${index}`}
          item={item}
          index={index}
        />
      ))}
    </div>
  );
}

export default ResultsContainer;
