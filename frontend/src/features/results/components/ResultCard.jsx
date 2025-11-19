import { useState } from 'react';
import { useAppSelector } from '../../../hooks/useAppSelector';

function ResultCard({ item, index }) {
  const [showSystem, setShowSystem] = useState(false);
  const [showChunks, setShowChunks] = useState(false);
  const [showOptions, setShowOptions] = useState(false);
  const [showError, setShowError] = useState(false);
  const [showEvaluation, setShowEvaluation] = useState(false);
  const [showMetrics, setShowMetrics] = useState(false);

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

        {/* Advanced Metrics Section */}
        {(item.retrieval_metrics || item.generation_metrics) && (
          <div className="section">
            <div className="section-title">
              <span>Advanced Metrics</span>
              <button
                className="button toggle-button"
                onClick={() => setShowMetrics(!showMetrics)}
              >
                Show/Hide
              </button>
            </div>
            <div className={`section-content ${showMetrics ? '' : 'hidden'}`}>
              {/* Retrieval Metrics */}
              {item.retrieval_metrics && Object.keys(item.retrieval_metrics).length > 0 && (
                <div className="metrics-subsection">
                  <h4 style={{ fontWeight: 'bold', marginBottom: '8px', color: '#002776' }}>
                    Retrieval Quality Metrics
                  </h4>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '12px', marginBottom: '16px' }}>
                    {item.retrieval_metrics.context_relevancy !== undefined && item.retrieval_metrics.context_relevancy !== null && (
                      <div className="metric-item" style={{ padding: '8px', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
                        <div style={{ fontSize: '0.85em', color: '#666' }}>Context Relevancy</div>
                        <div style={{ fontSize: '1.2em', fontWeight: 'bold', color: '#002776' }}>
                          {item.retrieval_metrics.context_relevancy.toFixed(3)}
                        </div>
                      </div>
                    )}
                    {item.retrieval_metrics.context_precision !== undefined && item.retrieval_metrics.context_precision !== null && (
                      <div className="metric-item" style={{ padding: '8px', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
                        <div style={{ fontSize: '0.85em', color: '#666' }}>Context Precision</div>
                        <div style={{ fontSize: '1.2em', fontWeight: 'bold', color: '#002776' }}>
                          {item.retrieval_metrics.context_precision.toFixed(3)}
                        </div>
                      </div>
                    )}
                    {item.retrieval_metrics.context_recall !== undefined && item.retrieval_metrics.context_recall !== null && (
                      <div className="metric-item" style={{ padding: '8px', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
                        <div style={{ fontSize: '0.85em', color: '#666' }}>Context Recall</div>
                        <div style={{ fontSize: '1.2em', fontWeight: 'bold', color: '#002776' }}>
                          {item.retrieval_metrics.context_recall.toFixed(3)}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Generation Metrics */}
              {item.generation_metrics && Object.keys(item.generation_metrics).length > 0 && (
                <div className="metrics-subsection">
                  <h4 style={{ fontWeight: 'bold', marginBottom: '8px', color: '#002776' }}>
                    Generation Quality Metrics
                  </h4>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '12px' }}>
                    {item.generation_metrics.faithfulness !== undefined && item.generation_metrics.faithfulness !== null && (
                      <div className="metric-item" style={{ padding: '8px', backgroundColor: '#f0f8ff', borderRadius: '4px' }}>
                        <div style={{ fontSize: '0.85em', color: '#666' }}>Faithfulness</div>
                        <div style={{ fontSize: '1.2em', fontWeight: 'bold', color: '#002776' }}>
                          {item.generation_metrics.faithfulness.toFixed(3)}
                        </div>
                      </div>
                    )}
                    {item.generation_metrics.answer_relevancy !== undefined && item.generation_metrics.answer_relevancy !== null && (
                      <div className="metric-item" style={{ padding: '8px', backgroundColor: '#f0f8ff', borderRadius: '4px' }}>
                        <div style={{ fontSize: '0.85em', color: '#666' }}>Answer Relevancy</div>
                        <div style={{ fontSize: '1.2em', fontWeight: 'bold', color: '#002776' }}>
                          {item.generation_metrics.answer_relevancy.toFixed(3)}
                        </div>
                      </div>
                    )}
                    {item.generation_metrics.answer_correctness !== undefined && item.generation_metrics.answer_correctness !== null && (
                      <div className="metric-item" style={{ padding: '8px', backgroundColor: '#f0f8ff', borderRadius: '4px' }}>
                        <div style={{ fontSize: '0.85em', color: '#666' }}>Answer Correctness</div>
                        <div style={{ fontSize: '1.2em', fontWeight: 'bold', color: '#002776' }}>
                          {item.generation_metrics.answer_correctness.toFixed(3)}
                        </div>
                      </div>
                    )}
                    {item.generation_metrics.answer_similarity !== undefined && item.generation_metrics.answer_similarity !== null && (
                      <div className="metric-item" style={{ padding: '8px', backgroundColor: '#f0f8ff', borderRadius: '4px' }}>
                        <div style={{ fontSize: '0.85em', color: '#666' }}>Answer Similarity</div>
                        <div style={{ fontSize: '1.2em', fontWeight: 'bold', color: '#002776' }}>
                          {item.generation_metrics.answer_similarity.toFixed(3)}
                        </div>
                      </div>
                    )}
                    {item.generation_metrics.rouge1 !== undefined && item.generation_metrics.rouge1 !== null && (
                      <div className="metric-item" style={{ padding: '8px', backgroundColor: '#fff8f0', borderRadius: '4px' }}>
                        <div style={{ fontSize: '0.85em', color: '#666' }}>ROUGE-1</div>
                        <div style={{ fontSize: '1.2em', fontWeight: 'bold', color: '#002776' }}>
                          {item.generation_metrics.rouge1.toFixed(3)}
                        </div>
                      </div>
                    )}
                    {item.generation_metrics.rouge2 !== undefined && item.generation_metrics.rouge2 !== null && (
                      <div className="metric-item" style={{ padding: '8px', backgroundColor: '#fff8f0', borderRadius: '4px' }}>
                        <div style={{ fontSize: '0.85em', color: '#666' }}>ROUGE-2</div>
                        <div style={{ fontSize: '1.2em', fontWeight: 'bold', color: '#002776' }}>
                          {item.generation_metrics.rouge2.toFixed(3)}
                        </div>
                      </div>
                    )}
                    {item.generation_metrics.rougeL !== undefined && item.generation_metrics.rougeL !== null && (
                      <div className="metric-item" style={{ padding: '8px', backgroundColor: '#fff8f0', borderRadius: '4px' }}>
                        <div style={{ fontSize: '0.85em', color: '#666' }}>ROUGE-L</div>
                        <div style={{ fontSize: '1.2em', fontWeight: 'bold', color: '#002776' }}>
                          {item.generation_metrics.rougeL.toFixed(3)}
                        </div>
                      </div>
                    )}
                    {item.generation_metrics.bleu !== undefined && item.generation_metrics.bleu !== null && (
                      <div className="metric-item" style={{ padding: '8px', backgroundColor: '#fff8f0', borderRadius: '4px' }}>
                        <div style={{ fontSize: '0.85em', color: '#666' }}>BLEU</div>
                        <div style={{ fontSize: '1.2em', fontWeight: 'bold', color: '#002776' }}>
                          {item.generation_metrics.bleu.toFixed(3)}
                        </div>
                      </div>
                    )}
                    {item.generation_metrics.meteor !== undefined && item.generation_metrics.meteor !== null && (
                      <div className="metric-item" style={{ padding: '8px', backgroundColor: '#fff0f8', borderRadius: '4px' }}>
                        <div style={{ fontSize: '0.85em', color: '#666' }}>METEOR</div>
                        <div style={{ fontSize: '1.2em', fontWeight: 'bold', color: '#002776' }}>
                          {item.generation_metrics.meteor.toFixed(3)}
                        </div>
                      </div>
                    )}
                    {item.generation_metrics.bert_f1 !== undefined && item.generation_metrics.bert_f1 !== null && (
                      <div className="metric-item" style={{ padding: '8px', backgroundColor: '#f8f0ff', borderRadius: '4px' }}>
                        <div style={{ fontSize: '0.85em', color: '#666' }}>BERTScore F1</div>
                        <div style={{ fontSize: '1.2em', fontWeight: 'bold', color: '#002776' }}>
                          {item.generation_metrics.bert_f1.toFixed(3)}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

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
