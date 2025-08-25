import ResultCard from '../../../components/ui/ResultCard';

function ResultsContainer({ data }) {
  if (data.length === 0) {
    return (
      <div id="results-container">
        <div className="card">
          <div className="card-body">No results match your filters.</div>
        </div>
      </div>
    );
  }

  return (
    <div id="results-container">
      {data.map((item, index) => (
        <ResultCard key={item.testId || `test-${index}`} item={item} index={index} />
      ))}
    </div>
  );
}

export default ResultsContainer;