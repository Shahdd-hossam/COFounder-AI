import { useParams } from "react-router-dom";
import PageShell from "../components/common/PageShell";

function MarketResearch() {
  const { startupId } = useParams();
  return (
    <PageShell title="Market Research" subtitle="Deep search will return source-backed market evidence and identify data gaps.">
      <section className="panel">
        <p className="eyebrow">Phase 5 workspace</p>
        <h2>Research workspace</h2>
        <p className="muted">{startupId ? `Startup #${startupId} is active.` : "Create or open a startup to continue."}</p>
        <p className="empty-state">The shared startup context is now ready to feed the deep-search and data-quality pipeline.</p>
      </section>
    </PageShell>
  );
}

export default MarketResearch;
