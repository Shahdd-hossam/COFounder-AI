import PageShell from "../components/common/PageShell";
import MarketingPlanForm from "../components/marketing-plan/MarketingPlanForm";

function MarketingPlan() {
  return (
    <PageShell
      title="Marketing Plan Generator"
      subtitle="Turn a product concept into an actionable launch blueprint."
    >
      <MarketingPlanForm />
    </PageShell>
  );
}

export default MarketingPlan;
