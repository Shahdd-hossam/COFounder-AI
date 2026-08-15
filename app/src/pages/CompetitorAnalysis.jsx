import { useParams } from "react-router-dom";
import PageShell from "../components/common/PageShell";
import FeatureRunPanel from "../components/common/FeatureRunPanel";
import { startCompetitorAnalysisRun } from "../services/api";

function CompetitorAnalysis() {
  const { startupId } = useParams();
  return (
    <PageShell title="Competitor Analysis" subtitle="Compare alternatives using cited evidence and preserve unknown pricing or capability data.">
      {!startupId ? <section className="panel"><h2>Create or open a startup</h2><p className="muted">Competitor analysis needs a startup context.</p></section> : <FeatureRunPanel
        startupId={startupId}
        title="Competitive landscape"
        eyebrow="Evidence-backed comparison"
        description="Direct and indirect competitors are separated, while uncited pricing and claims remain unknown."
        runFunction={startCompetitorAnalysisRun}
        emptyText="Generate a competitor analysis from the verified research snapshot."
        renderResult={(result) => (
          <>
            <section className="panel research-section"><div className="section-heading"><h2>Competitors</h2><span>{result?.competitors?.length || 0}</span></div>
              {!result?.competitors?.length ? <p className="empty-state">No cited competitors were returned.</p> : result.competitors.map((competitor) => <article className="competitor-row" key={competitor.name}><div><div className="row-title"><h3>{competitor.name}</h3><span className="quality-badge">{competitor.classification}</span></div><p>{competitor.strength}</p><p className="muted">Weakness: {competitor.weakness}</p></div><div className="competitor-meta"><strong>{competitor.pricing || "Unknown"}</strong><span>{competitor.source_ids?.length || 0} source(s)</span></div></article>)}
            </section>
            <section className="panel research-section"><div className="section-heading"><h2>Strategic gaps</h2><span>Hypotheses, not facts</span></div>{(result?.strategic_gaps || []).map((gap, index) => <article className="insight-row" key={`${gap.text}-${index}`}><p>{gap.text}</p><span>{gap.evidence_status} · {gap.source_ids?.length || 0} source(s)</span></article>)}</section>
            <section className="panel research-section"><div className="section-heading"><h2>Sources</h2><span>{result?.sources?.length || 0}</span></div>{(result?.sources || []).map((source) => <div className="source-row" key={source.id}><a href={source.url} target="_blank" rel="noreferrer">{source.title}</a><span>{source.publisher || "Unknown publisher"} · {source.quality}</span></div>)}</section>
          </>
        )}
      />}
    </PageShell>
  );
}

export default CompetitorAnalysis;
