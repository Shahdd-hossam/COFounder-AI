import { useParams } from "react-router-dom";
import PageShell from "../components/common/PageShell";

function SWOTAnalysis() {
  const { startupId } = useParams();
  return (
    <PageShell title="SWOT Analysis" subtitle="Traceable strengths, weaknesses, opportunities, and threats from startup context and research.">
      <section className="panel">
        <p className="eyebrow">Phase 4 workspace</p>
        <h2>SWOT workspace</h2>
        <p className="muted">{startupId ? `Startup #${startupId} is active.` : "Create or open a startup to continue."}</p>
        <p className="empty-state">SWOT generation will use the shared context and optional cleaned research without blocking on research completion.</p>
      </section>
    </PageShell>
  );
}

export default SWOTAnalysis;
