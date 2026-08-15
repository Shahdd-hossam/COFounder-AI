import { useParams } from "react-router-dom";
import PageShell from "../components/common/PageShell";
import FeatureRunPanel from "../components/common/FeatureRunPanel";
import { startSwotRun } from "../services/api";

function SWOTAnalysis() {
  const { startupId } = useParams();
  const columns = ["strengths", "weaknesses", "opportunities", "threats"];
  return (
    <PageShell title="SWOT Analysis" subtitle="Separate startup context, sourced evidence, hypotheses, and unknowns.">
      {!startupId ? <section className="panel"><h2>Create or open a startup</h2><p className="muted">SWOT analysis needs a startup context.</p></section> : <FeatureRunPanel
        startupId={startupId}
        title="Traceable SWOT"
        eyebrow="Evidence-backed strategy"
        description="Research-backed items retain source IDs. Context-derived items are labeled as context or hypothesis rather than presented as market facts."
        runFunction={startSwotRun}
        emptyText="Generate a SWOT from the current startup context and verified research."
        renderResult={(result) => <section className="swot-grid">{columns.map((column) => <article className="panel swot-column" key={column}><div className="section-heading"><h2>{column}</h2><span>{result?.[column]?.length || 0}</span></div>{(result?.[column] || []).map((item, index) => <div className="swot-item" key={`${column}-${index}`}><p>{item.text}</p><span>{item.evidence_status} · {item.source_ids?.length || 0} source(s)</span></div>)}</article>)}</section>}
      />}
    </PageShell>
  );
}

export default SWOTAnalysis;
