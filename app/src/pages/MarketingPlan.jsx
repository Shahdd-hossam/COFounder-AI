import { useParams } from "react-router-dom";
import PageShell from "../components/common/PageShell";

function MarketingPlan() {
  const { startupId } = useParams();
  return (
    <PageShell title="Marketing Plan" subtitle="The strategy dashboard will consume the shared startup context, research, and SWOT.">
      <section className="panel">
        <p className="eyebrow">Phase 5 workspace</p>
        <h2>Marketing plan generation</h2>
        <p className="muted">{startupId ? `Startup #${startupId} is active.` : "Create or open a startup to continue."}</p>
        <p className="empty-state">The database-backed startup foundation is ready. The structured marketing workflow will be connected in the next feature phase.</p>
      </section>
    </PageShell>
  );
}

export default MarketingPlan;
