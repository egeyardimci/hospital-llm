import { useState, useEffect } from "react";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";
import Select from "react-select";
import { useAppSelector } from "../../../hooks/useAppSelector";
import { customSelectTheme } from "../../../constants";

export default function MetricsComparisonChart() {
  const { filteredData: testData } = useAppSelector((state) => state.results);
  const [chartType, setChartType] = useState("bar");
  const [groupBy, setGroupBy] = useState("run_count");
  const [metricsData, setMetricsData] = useState([]);


  const chartTypeOptions = [
    { value: "bar", label: "Bar Chart" },
    { value: "radar", label: "Radar Chart" },
  ];

  const groupByOptions = [
    { value: "run_count", label: "Run Count" },
    { value: "llm", label: "LLM" },
    { value: "embedding_model", label: "Embedding Model" },
    { value: "rag_database", label: "RAG Database" },
  ];

  useEffect(() => {
    // Only include items that have BOTH run_count AND generation_metrics
    // This filters out old runs that don't have the new metrics
    const filteredData = testData.filter(
      (item) =>
        item.run_count !== undefined &&
        item.run_count !== null &&
        item.generation_metrics !== undefined &&
        item.generation_metrics !== null &&
        Object.keys(item.generation_metrics).length > 0
    );

    calculateMetricsAverages(filteredData, groupBy);
  }, [groupBy, testData]);

  const calculateMetricsAverages = (rawData, groupField) => {
    const groups = {};

    rawData.forEach((item) => {
      const key = item[groupField];
      if (!groups[key]) {
        groups[key] = {
          name: key,
          // Retrieval metrics
          context_relevancy_total: 0,
          context_precision_total: 0,
          context_recall_total: 0,
          // Generation metrics - RAGAs
          faithfulness_total: 0,
          answer_relevancy_total: 0,
          answer_correctness_total: 0,
          answer_similarity_total: 0,
          // Generation metrics - Traditional
          rouge1_total: 0,
          rouge2_total: 0,
          rougeL_total: 0,
          bleu_total: 0,
          meteor_total: 0,
          bert_f1_total: 0,
          // Counts for averaging
          retrieval_count: 0,
          generation_ragas_count: 0,
          generation_traditional_count: 0,
          // Metadata
          llm: item.llm,
          embedding_model: item.embedding_model,
          rag_database: item.rag_database,
        };
      }

      // Aggregate retrieval metrics
      if (item.retrieval_metrics) {
        if (item.retrieval_metrics.context_relevancy !== null && item.retrieval_metrics.context_relevancy !== undefined) {
          groups[key].context_relevancy_total += item.retrieval_metrics.context_relevancy;
          groups[key].retrieval_count++;
        }
        if (item.retrieval_metrics.context_precision !== null && item.retrieval_metrics.context_precision !== undefined) {
          groups[key].context_precision_total += item.retrieval_metrics.context_precision;
        }
        if (item.retrieval_metrics.context_recall !== null && item.retrieval_metrics.context_recall !== undefined) {
          groups[key].context_recall_total += item.retrieval_metrics.context_recall;
        }
      }

      // Aggregate generation metrics
      if (item.generation_metrics) {
        // RAGAs metrics
        if (item.generation_metrics.faithfulness !== null && item.generation_metrics.faithfulness !== undefined) {
          groups[key].faithfulness_total += item.generation_metrics.faithfulness;
          groups[key].generation_ragas_count++;
        }
        if (item.generation_metrics.answer_relevancy !== null && item.generation_metrics.answer_relevancy !== undefined) {
          groups[key].answer_relevancy_total += item.generation_metrics.answer_relevancy;
        }
        if (item.generation_metrics.answer_correctness !== null && item.generation_metrics.answer_correctness !== undefined) {
          groups[key].answer_correctness_total += item.generation_metrics.answer_correctness;
        }
        if (item.generation_metrics.answer_similarity !== null && item.generation_metrics.answer_similarity !== undefined) {
          groups[key].answer_similarity_total += item.generation_metrics.answer_similarity;
        }

        // Traditional metrics
        if (item.generation_metrics.rouge1 !== null && item.generation_metrics.rouge1 !== undefined) {
          groups[key].rouge1_total += item.generation_metrics.rouge1;
          groups[key].generation_traditional_count++;
        }
        if (item.generation_metrics.rouge2 !== null && item.generation_metrics.rouge2 !== undefined) {
          groups[key].rouge2_total += item.generation_metrics.rouge2;
        }
        if (item.generation_metrics.rougeL !== null && item.generation_metrics.rougeL !== undefined) {
          groups[key].rougeL_total += item.generation_metrics.rougeL;
        }
        if (item.generation_metrics.bleu !== null && item.generation_metrics.bleu !== undefined) {
          groups[key].bleu_total += item.generation_metrics.bleu;
        }
        if (item.generation_metrics.meteor !== null && item.generation_metrics.meteor !== undefined) {
          groups[key].meteor_total += item.generation_metrics.meteor;
        }
        if (item.generation_metrics.bert_f1 !== null && item.generation_metrics.bert_f1 !== undefined) {
          groups[key].bert_f1_total += item.generation_metrics.bert_f1;
        }
      }
    });

    // Calculate averages
    const result = Object.values(groups).map((group) => {
      const retrieval_count = group.retrieval_count || 1;
      const ragas_count = group.generation_ragas_count || 1;
      const traditional_count = group.generation_traditional_count || 1;

      return {
        name: String(group.name),
        // Retrieval metrics (0-1 scale)
        "Context Relevancy": parseFloat((group.context_relevancy_total / retrieval_count).toFixed(3)),
        "Context Precision": parseFloat((group.context_precision_total / retrieval_count).toFixed(3)),
        "Context Recall": parseFloat((group.context_recall_total / retrieval_count).toFixed(3)),
        // Generation metrics - RAGAs (0-1 scale)
        "Faithfulness": parseFloat((group.faithfulness_total / ragas_count).toFixed(3)),
        "Answer Relevancy": parseFloat((group.answer_relevancy_total / ragas_count).toFixed(3)),
        "Answer Correctness": parseFloat((group.answer_correctness_total / ragas_count).toFixed(3)),
        "Answer Similarity": parseFloat((group.answer_similarity_total / ragas_count).toFixed(3)),
        // Generation metrics - Traditional (0-1 scale)
        "ROUGE-1": parseFloat((group.rouge1_total / traditional_count).toFixed(3)),
        "ROUGE-2": parseFloat((group.rouge2_total / traditional_count).toFixed(3)),
        "ROUGE-L": parseFloat((group.rougeL_total / traditional_count).toFixed(3)),
        "BLEU": parseFloat((group.bleu_total / traditional_count).toFixed(3)),
        "METEOR": parseFloat((group.meteor_total / traditional_count).toFixed(3)),
        "BERTScore F1": parseFloat((group.bert_f1_total / traditional_count).toFixed(3)),
        // Metadata
        llm: group.llm,
        embedding_model: group.embedding_model,
        rag_database: group.rag_database,
      };
    });

    setMetricsData(result);
  };

  const findSelectedOption = (value, options) => {
    return options.find((option) => option.value === value) || null;
  };

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div
          className="section-content"
          style={{
            backgroundColor: "white",
            padding: "12px",
            boxShadow: "0 2px 10px rgba(0, 0, 0, 0.1)",
            borderRadius: "4px",
            maxWidth: "300px",
          }}
        >
          <p style={{ fontWeight: "bold", marginBottom: "8px" }}>
            {data.name}
          </p>
          {payload.map((entry, index) => (
            <p
              key={index}
              style={{
                color: entry.color,
                margin: "4px 0",
                fontSize: "0.9em",
              }}
            >
              {entry.name}: {entry.value}
            </p>
          ))}
          <div style={{ marginTop: "8px", fontSize: "0.85em", color: "#666" }}>
            <div>LLM: {data.llm}</div>
            <div>Embedding: {data.embedding_model}</div>
            <div>RAG DB: {data.rag_database}</div>
          </div>
        </div>
      );
    }
    return null;
  };

  // Prepare data for radar chart (select first group for radar view)
  const radarData = metricsData.length > 0 ? [
    { metric: "Context Relevancy", value: metricsData[0]["Context Relevancy"] || 0 },
    { metric: "Context Precision", value: metricsData[0]["Context Precision"] || 0 },
    { metric: "Context Recall", value: metricsData[0]["Context Recall"] || 0 },
    { metric: "Faithfulness", value: metricsData[0]["Faithfulness"] || 0 },
    { metric: "Answer Relevancy", value: metricsData[0]["Answer Relevancy"] || 0 },
    { metric: "Answer Correctness", value: metricsData[0]["Answer Correctness"] || 0 },
    { metric: "ROUGE-1", value: metricsData[0]["ROUGE-1"] || 0 },
    { metric: "BLEU", value: metricsData[0]["BLEU"] || 0 },
    { metric: "METEOR", value: metricsData[0]["METEOR"] || 0 },
    { metric: "BERTScore F1", value: metricsData[0]["BERTScore F1"] || 0 },
  ] : [];

  const metricColors = {
    "Context Relevancy": "#8884d8",
    "Context Precision": "#82ca9d",
    "Context Recall": "#ffc658",
    "Faithfulness": "#ff7c7c",
    "Answer Relevancy": "#8dd1e1",
    "Answer Correctness": "#d084d0",
    "Answer Similarity": "#a4de6c",
    "ROUGE-1": "#ffbb28",
    "ROUGE-2": "#ff8042",
    "ROUGE-L": "#0088fe",
    "BLEU": "#00c49f",
    "METEOR": "#ff69b4",
    "BERTScore F1": "#9370db",
  };

  return (
    <div className="visualization-container">
      <div className="card-body">
        <div className="section">
          <div className="section-title">
            <span>Advanced Metrics Visualization</span>
          </div>
          <div className="filters-grid">
            <div className="filter-group">
              <label className="filter-label">Chart Type:</label>
              <Select
                theme={customSelectTheme}
                value={findSelectedOption(chartType, chartTypeOptions)}
                onChange={(selectedOption) =>
                  setChartType(selectedOption ? selectedOption.value : "bar")
                }
                options={chartTypeOptions}
                placeholder="Select chart type..."
                isSearchable={false}
              />
            </div>

            <div className="filter-group">
              <label className="filter-label">Group by:</label>
              <Select
                theme={customSelectTheme}
                value={findSelectedOption(groupBy, groupByOptions)}
                onChange={(selectedOption) =>
                  setGroupBy(selectedOption ? selectedOption.value : "run_count")
                }
                options={groupByOptions}
                placeholder="Select grouping..."
                isSearchable={false}
              />
            </div>
          </div>
        </div>

        {metricsData.length === 0 ? (
          <div className="section">
            <div className="section-content" style={{ textAlign: "center", padding: "40px", color: "#666" }}>
              No metrics data available. Run tests with metrics enabled to see visualizations.
            </div>
          </div>
        ) : (
          <>
            {chartType === "bar" && (
              <div className="section">
                <div className="section-title">
                  <span>Metrics Comparison (All Groups)</span>
                </div>
                <div style={{ height: "500px", overflowX: "auto" }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={metricsData}
                      margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
                      <XAxis
                        dataKey="name"
                        angle={-45}
                        textAnchor="end"
                        height={100}
                        tick={{ fill: "#2c3e50", fontSize: 12 }}
                      />
                      <YAxis domain={[0, 1]} tick={{ fill: "#2c3e50" }} />
                      <Tooltip content={<CustomTooltip />} />
                      <Legend wrapperStyle={{ paddingTop: "20px" }} />
                      {/* Retrieval Metrics */}
                      <Bar dataKey="Context Relevancy" fill={metricColors["Context Relevancy"]} />
                      <Bar dataKey="Context Precision" fill={metricColors["Context Precision"]} />
                      <Bar dataKey="Context Recall" fill={metricColors["Context Recall"]} />
                      {/* RAGAs Generation Metrics */}
                      <Bar dataKey="Faithfulness" fill={metricColors["Faithfulness"]} />
                      <Bar dataKey="Answer Relevancy" fill={metricColors["Answer Relevancy"]} />
                      <Bar dataKey="Answer Correctness" fill={metricColors["Answer Correctness"]} />
                      {/* Traditional Metrics */}
                      <Bar dataKey="ROUGE-1" fill={metricColors["ROUGE-1"]} />
                      <Bar dataKey="BLEU" fill={metricColors["BLEU"]} />
                      <Bar dataKey="METEOR" fill={metricColors["METEOR"]} />
                      <Bar dataKey="BERTScore F1" fill={metricColors["BERTScore F1"]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}

            {chartType === "radar" && metricsData.length > 0 && (
              <div className="section">
                <div className="section-title">
                  <span>Metrics Profile: {metricsData[0].name}</span>
                </div>
                <div style={{ height: "500px" }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart data={radarData}>
                      <PolarGrid />
                      <PolarAngleAxis dataKey="metric" />
                      <PolarRadiusAxis domain={[0, 1]} />
                      <Radar
                        name="Metrics"
                        dataKey="value"
                        stroke="#002776"
                        fill="#002776"
                        fillOpacity={0.6}
                      />
                      <Legend />
                      <Tooltip />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>
                <div style={{ textAlign: "center", marginTop: "16px", fontSize: "0.9em", color: "#666" }}>
                  Showing first group. Use bar chart to compare all groups.
                </div>
              </div>
            )}

            {/* Metrics Summary Cards */}
            <div className="section">
              <div className="section-title">
                <span>Metrics Summary</span>
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))", gap: "16px" }}>
                {metricsData.map((item) => (
                  <div
                    key={item.name}
                    style={{
                      backgroundColor: "#f8f9fa",
                      padding: "16px",
                      borderRadius: "8px",
                      boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
                    }}
                  >
                    <div style={{ fontWeight: "bold", fontSize: "1.1em", marginBottom: "12px", color: "#002776" }}>
                      {item.name}
                    </div>

                    <div style={{ fontSize: "0.85em", marginBottom: "8px", color: "#666" }}>
                      <strong>Retrieval Quality:</strong>
                      <div style={{ marginTop: "4px", paddingLeft: "8px" }}>
                        <div>Relevancy: {item["Context Relevancy"]}</div>
                        <div>Precision: {item["Context Precision"]}</div>
                        <div>Recall: {item["Context Recall"]}</div>
                      </div>
                    </div>

                    <div style={{ fontSize: "0.85em", marginBottom: "8px", color: "#666" }}>
                      <strong>Generation Quality:</strong>
                      <div style={{ marginTop: "4px", paddingLeft: "8px" }}>
                        <div>Faithfulness: {item["Faithfulness"]}</div>
                        <div>Relevancy: {item["Answer Relevancy"]}</div>
                        <div>Correctness: {item["Answer Correctness"]}</div>
                      </div>
                    </div>

                    <div style={{ fontSize: "0.85em", color: "#666" }}>
                      <strong>Traditional Metrics:</strong>
                      <div style={{ marginTop: "4px", paddingLeft: "8px" }}>
                        <div>ROUGE-1: {item["ROUGE-1"]}</div>
                        <div>BLEU: {item["BLEU"]}</div>
                        <div>METEOR: {item["METEOR"]}</div>
                        <div>BERTScore F1: {item["BERTScore F1"]}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
