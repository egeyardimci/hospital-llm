import { useState } from 'react';
import { useAppSelector } from '../../../hooks/useAppSelector';

function ResultCard({ item, index }) {
  const [showSystem, setShowSystem] = useState(false);
  const [showChunks, setShowChunks] = useState(false);
  const [showOptions, setShowOptions] = useState(false);
  const [showError, setShowError] = useState(false);
  const [showEvaluation, setShowEvaluation] = useState(false);

  const tests = useAppSelector((state) => state.tests.tests);
  const test = tests.find((t) => t.test_id === item.test_id) || {};

  const qaBatches = useAppSelector((state) => state.qaBatches.qaBatches);
  const qaBatch =
    qaBatches.find((batch) => batch._id === test.qa_batch) || {}.title || 'N/A';

  // Detect language (simple heuristic)
  const isTurkish =
    /[çğıöşüÇĞİÖŞÜ]/.test(item.query) || /türk/i.test(item.query);
  const hasError =
    item.error !== undefined && item.error !== null && item.error !== '';

  return (
    <div className="card">
      <div className="card-header">
        <div>
          <span className="test-id">{`Test ID: ${
            item.test_id || `Test-${index + 1}`
          }`}</span>
          <span className="test-id">{`Run Count: ${
            item.run_count || 'N/A'
          }`}</span>
          {isTurkish && <span className="language-badge">Turkish</span>}
        </div>
        <span className="model-badge">{item.llm}</span>
      </div>

      <div className={`${hasError ? 'error-card-body' : 'card-body'}`}>
        <div className="section">
          <div className="section-title">
            <span>Query</span>
          </div>
          <div className="section-content">{item.query}</div>
        </div>

        <div className="expected-vs-actual">
          <div className="section-without-border">
            <div className="section-title">
              <span>Expected Answer</span>
            </div>
            <div className="section-content">
              {item.expected_answer || 'No expected answer provided'}
            </div>
          </div>

          <div className="section">
            <div className="section-title">
              <span>Actual Response</span>
            </div>
            <div
              className="section-content"
              dangerouslySetInnerHTML={{ __html: item.response }}
            ></div>
          </div>
        </div>

        {/* New Evaluation Section */}
        <div className="section">
          <div className="section-title">
            <span>Evaluation</span>
            <button
              className="button toggle-button"
              onClick={() => setShowEvaluation(!showEvaluation)}
            >
              Show/Hide
            </button>
          </div>
          <div className={`section-content ${showEvaluation ? '' : 'hidden'}`}>
            {'General evaluation: ' +
              item.evaluation +
              ' \nScore: ' +
              item.evaluation_score +
              '\nChunk evaluation: ' +
              item.chunk_evaluation +
              '\nScore: ' +
              item.chunk_evaluation_score || 'No evaluation data available'}
          </div>
        </div>

        <div className="section">
          <div className="section-title">
            <span>System Message</span>
            <button
              className="button toggle-button"
              onClick={() => setShowSystem(!showSystem)}
            >
              Show/Hide
            </button>
          </div>
          <div className={`section-content ${showSystem ? '' : 'hidden'}`}>
            {item.system_message}
          </div>
        </div>

        <div className="section">
          <div className="section-title">
            <span>Retrieved Chunks</span>
            <button
              className="button toggle-button"
              onClick={() => setShowChunks(!showChunks)}
            >
              Show/Hide
            </button>
          </div>
          <div className={`section-content ${showChunks ? '' : 'hidden'}`}>
            <ol>
              {item.retrieved_chunks &&
                item.retrieved_chunks.map((chunk, i) => (
                  <li key={i}>{chunk}</li>
                ))}
            </ol>
          </div>
        </div>

        {/* Options Section */}
        <div className="section">
          <div className="section-title">
            <span>Options</span>
            <button
              className="button toggle-button"
              onClick={() => setShowOptions(!showOptions)}
            >
              Show/Hide
            </button>
          </div>
          <div className={`section-content ${showOptions ? '' : 'hidden'}`}>
            {item.options && item.options.length > 0 ? (
              <ul>
                {item.options.map((option, i) => (
                  <li key={i}>
                    {option.name}: {option.data}
                  </li>
                ))}
              </ul>
            ) : (
              <span>No options available</span>
            )}
          </div>
        </div>

        {/* Options Section */}
        {hasError && (
          <div className="section">
            <div className="section-title">
              <span>Error</span>
              <button
                className="button toggle-button"
                onClick={() => setShowError(!showError)}
              >
                Show/Hide
              </button>
            </div>
            <div className={`section-content ${showError ? '' : 'hidden'}`}>
              {item.error}
            </div>
          </div>
        )}

        <div className="meta-info">
          <div className="meta-item">
            <span className="meta-label">Embedding Model</span>
            <span className="meta-value">{item.embedding_model}</span>
          </div>
          <div className="meta-item">
            <span className="meta-label">Chunk Size</span>
            <span className="meta-value">{item.chunk_size || 'N/A'}</span>
          </div>
          <div className="meta-item">
            <span className="meta-label">Chunk Overlap</span>
            <span className="meta-value">{item.chunk_overlap || 'N/A'}</span>
          </div>
          <div className="meta-item">
            <span className="meta-label">Similar Vector Count</span>
            <span className="meta-value">
              {item.similar_vector_count || 'N/A'}
            </span>
          </div>
          <div className="meta-item">
            <span className="meta-label">QA Batch</span>
            <span className="meta-value">{qaBatch.title || 'N/A'}</span>
          </div>
          <div className="meta-item">
            <span className="meta-label">Timestamp</span>
            <span className="meta-value">{item.time_stamp}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResultCard;
