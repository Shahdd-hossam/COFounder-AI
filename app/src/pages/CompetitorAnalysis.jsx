import { useParams } from "react-router-dom";
import PageShell from "../components/common/PageShell";
import FeatureRunPanel from "../components/common/FeatureRunPanel";
import { startCompetitorAnalysisRun } from "../services/api";
import { resultLabel, sourceCountLabel } from "../components/common/resultLanguage";

function CompetitorAnalysis() {
  const { startupId } = useParams();
  return (
    <PageShell title="Competitor Analysis" subtitle="Compare alternatives, understand the reason for each match, and turn pricing gaps into validation tasks.">
      {!startupId ? <section className="panel"><h2>Create or open a startup</h2><p className="muted">Competitor analysis needs a startup context.</p></section> : <FeatureRunPanel
        startupId={startupId}
        title="Competitive landscape"
        eyebrow="Evidence-backed comparison"
        description="Direct and indirect alternatives are separated. Each row shows its evidence basis and what still needs validation."
        runFunction={startCompetitorAnalysisRun}
        emptyText="Generate a competitor landscape from the startup description and matched research profile."
        renderResult={(result) => (
          <>
            <section className="panel research-section"><div className="section-heading"><h2>Matched alternatives</h2><span>{result?.competitors?.length ? `${result.competitors.length} comparisons` : "Build comparison set"}</span></div>
              {!result?.competitors?.length ? <p className="empty-state">No comparison candidates yet. Add a more specific customer, market, and problem description.</p> : result.competitors.map((competitor) => <article className="competitor-row" key={competitor.name}><div><div className="row-title"><h3>{competitor.name}</h3><span className="quality-badge">{resultLabel(competitor.evidence_status || competitor.classification)}</span></div><p>{competitor.strength}</p><p className="muted">Trade-off: {competitor.weakness}</p></div><div className="competitor-meta"><strong>{competitor.pricing || "Pricing to validate"}</strong><span>{sourceCountLabel(competitor.source_ids?.length || 0)}</span></div></article>)}
            </section>
            <section className="panel research-section"><div className="section-heading"><h2>Strategic gaps</h2><span>Use these as research questions</span></div>{(result?.strategic_gaps || []).map((gap, index) => <article className="insight-row" key={`${gap.text}-${index}`}><p>{gap.text}</p><span>{resultLabel(gap.evidence_status)} · {sourceCountLabel(gap.source_ids?.length || 0)}</span></article>)}</section>
            <section className="panel research-section"><div className="section-heading"><h2>Research references</h2><span>{result?.sources?.length ? `${result.sources.length} available` : "Build reference set"}</span></div>{(result?.sources || []).map((source) => <div className="source-row" key={source.id}><a href={source.url} target="_blank" rel="noreferrer">{source.title}</a><span>{source.publisher || "Reference source"} · {resultLabel(source.quality)}</span></div>)}</section>
          </>
        )}
      />}
    </PageShell>
  );
}

export default CompetitorAnalysis;
