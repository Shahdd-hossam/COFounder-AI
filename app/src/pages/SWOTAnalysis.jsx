import { useParams } from "react-router-dom";
import PageShell from "../components/common/PageShell";
import FeatureRunPanel from "../components/common/FeatureRunPanel";
import { startSwotRun } from "../services/api";
import { resultLabel, sourceCountLabel } from "../components/common/resultLanguage";

function SWOTAnalysis() {
  const { startupId } = useParams();
  const columns = ["strengths", "weaknesses", "opportunities", "threats"];
  return (
    <PageShell title="SWOT Analysis" subtitle="Turn the startup context and research baseline into clear strategic signals and validation questions.">
      {!startupId ? <section className="panel"><h2>Create or open a startup</h2><p className="muted">SWOT analysis needs a startup context.</p></section> : <FeatureRunPanel
        startupId={startupId}
        title="Traceable SWOT"
        eyebrow="Evidence-backed strategy"
        description="Each signal shows its review basis. Use the planning signals to choose what to validate next."
        runFunction={startSwotRun}
        emptyText="Generate a SWOT from the startup context and matched research profile."
        renderResult={(result) => <section className="swot-grid">{columns.map((column) => <article className="panel swot-column" key={column}><div className="section-heading"><h2>{column}</h2><span>{result?.[column]?.length ? `${result[column].length} signals` : "Add signal"}</span></div>{(result?.[column] || []).map((item, index) => <div className="swot-item" key={`${column}-${index}`}><p>{item.text}</p><span>{resultLabel(item.evidence_status)} · {sourceCountLabel(item.source_ids?.length || 0)}</span></div>)}</article>)}</section>}
      />}
    </PageShell>
  );
}

export default SWOTAnalysis;
