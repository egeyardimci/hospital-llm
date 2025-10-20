import StatsSection from "./components/StatsSection";
import { useAppSelector } from "../../hooks/useAppSelector";
import FiltersSection from "./components/FiltersSection";
import ResultsContainer from "./components/ResultsContainer";

const ResultsTab = () => {

    const { filteredData, loading } = useAppSelector(state => state.results);

  return (
    <>
    <FiltersSection />
    <StatsSection data={filteredData} />
    {loading ? (
      <div className="loading">Loading results...</div>
    ) : (
      <ResultsContainer data={filteredData} />
    )}
  </>
  );
}

export default ResultsTab;