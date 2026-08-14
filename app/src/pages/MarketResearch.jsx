import PageShell from "../components/common/PageShell";
import MarketResearchForm from "../components/market-research/MarketResearchForm";

function MarketResearch() {
  return (
    <PageShell
      title="Market Research Assistant"
      subtitle="Get trends, competitor context, and market entry opportunities."
    >
      <MarketResearchForm />
    </PageShell>
  );
}

export default MarketResearch;
