import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import PageShell from "../components/common/PageShell";
import { getStartup, getWorkflowRun, startMarketResearchRun } from "../services/api";

function QualityBadge({ value }) {
  return <span className={`quality-badge quality-${value || "unknown"}`}>{value || "unknown"}</span>;
}

function MarketResearch() {
  const { startupId } = useParams();
  const [startup, setStartup] = useState(null);
  const [run, setRun] = useState(null);
  const [loading, setLoading] = useState(Boolean(startupId));
  const [running, setRunning] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!startupId) {
      setLoading(false);
      return;
    }
    getStartup(startupId)
      .then(setStartup)
      .catch((requestError) => setError(requestError.message || "Could not load startup context."))
      .finally(() => setLoading(false));
  }, [startupId]);

  const result = run?.result_json || null;
  const quality = result?.data_quality || {};
  const sources = result?.sources || [];
  const numericClaims = result?.numeric_claims || [];
  const estimatedFindings = result?.estimated_findings || [];
  const unknownClaims = useMemo(
    () => numericClaims.filter((claim) => claim.number_type === "unknown"),
    [numericClaims],
  );
  const insightGroups = [
    ["Market trends", result?.market_trends || []],
    ["Customer pain points", result?.customer_pain_points || []],
    ["Opportunities", result?.opportunities || []],
    ["Threats", result?.threats || []],
  ];

  const startResearch = async () => {
    if (!startupId) return;
    setRunning(true);
    setError("");
    try {
      const createdRun = await startMarketResearchRun(startupId);
      setRun(createdRun);
      const completedRun = await getWorkflowRun(createdRun.id);
      setRun(completedRun);
    } catch (requestError) {
      setError(requestError.message || "Deep Search could not be started.");
    } finally {
      setRunning(false);
    }
  };

  return (
    <PageShell title="Market Research" subtitle="Deep Search returns source-backed evidence and clearly marks what remains unknown.">
      {!startupId ? (
        <section className="panel">
          <p className="eyebrow">Evidence workspace</p>
          <h2>Choose a startup first</h2>
          <p className="muted">Open Market Research from a startup overview so the research run is tied to a context revision.</p>
          <Link className="primary-link" to="/">Open overview</Link>
        </section>
      ) : null}

      {startupId && loading ? <p className="muted">Loading startup context...</p> : null}
      {error ? <p className="error">{error}</p> : null}

      {startup ? (
        <>
          <section className="panel research-header">
            <div>
              <p className="eyebrow">Deep Search workspace</p>
              <h2>{startup.name}</h2>
              <p className="muted">Research is pinned to context revision {startup.context_revision}. Unsupported market numbers are never shown as facts.</p>
            </div>
            <button className="primary-button" type="button" onClick={startResearch} disabled={running}>
              {running ? "Searching and cleaning..." : "Run Deep Search"}
            </button>
          </section>

          {!run ? (
            <section className="panel empty-state research-empty">
              <h3>No research run yet</h3>
              <p>Run Deep Search to collect sources. If the connector is unavailable, the result will say unknown instead of fabricating estimates.</p>
            </section>
          ) : (
            <>
              <section className="quality-grid">
                <article className="panel quality-card"><span>Workflow status</span><strong>{run.status}</strong></article>
                <article className="panel quality-card"><span>Evidence confidence</span><strong><QualityBadge value={quality.confidence} /></strong></article>
                <article className="panel quality-card"><span>Source coverage</span><strong>{sources.length ? `${Math.round((quality.coverage || 0) * 100)}%` : "No verified sources"}</strong></article>
                <article className="panel quality-card"><span>Numeric claims returned</span><strong>{numericClaims.length ? `${numericClaims.length} (${quality.unknown_numeric_claims || 0} unknown)` : "None returned"}</strong></article>
              </section>

              <section className="panel research-section">
                <p className="eyebrow">Market overview</p>
                <div className="row-title"><h2>{result.market_overview || "Unknown"}</h2><QualityBadge value={result.market_overview_status || (result.data_mode === "mock_seed" ? "mock_reference" : result.market_overview?.startsWith("Preliminary") ? "modeled_estimate" : "source_backed")} /></div>
                <p className="muted">Tool: {result.tool || "not configured"}. Data mode: {result.data_mode || "live"}. Profile: {result.mock_profile_name || "none"}. Fallback path: {(quality.fallback_chain || []).join(" → ") || "not configured"}. All claims below retain their evidence links and cleaning metadata.</p>
                {quality.fallback_errors?.length ? <p className="warning">Research connectors were unavailable. No unsupported result was substituted.</p> : null}
              </section>

              <section className="panel research-section">
                <div className="section-heading"><h2>Source-backed findings</h2><span>Uncited insights are removed</span></div>
                {insightGroups.every(([, items]) => items.length === 0) ? <p className="empty-state">No source-backed findings returned.</p> : null}
                <div className="insight-grid">
                  {insightGroups.map(([title, items]) => (
                    <article className="insight-group" key={title}>
                      <h3>{title}</h3>
                      {items.length === 0 ? <p className="muted">Unknown</p> : items.map((item, index) => <div className="insight-row" key={`${title}-${index}`}><p>{item.text}</p><span>{item.source_ids?.length || 0} source(s) · {item.confidence || "low"}</span></div>)}
                    </article>
                  ))}
                </div>
                            </section>
              <section className="panel research-section">
                <div className="section-heading"><h2>Model-assisted planning estimates</h2><span>{estimatedFindings.length} estimate(s)</span></div>
                <p className="warning">These values are planning hypotheses generated from startup context and explicit heuristics. They are not verified market facts.</p>
                {(estimatedFindings || []).map((item, index) => <article className="insight-row" key={`estimate-${index}`}><p>{item.text}</p><span>{item.number_type} · {item.confidence} confidence · {item.methodology}</span><small>{item.validation_plan}</small></article>)}
              </section>
              <section className="panel research-section">
                <div className="section-heading"><h2>Numeric claims</h2><span>Verified and modeled values are labeled</span></div>

                {numericClaims.length === 0 ? <p className="empty-state">No numeric claim was returned. This is safer than presenting an unsupported estimate.</p> : null}
                {numericClaims.map((claim, index) => (
                  <article className="claim-row" key={`${claim.label}-${index}`}>
                    <div><strong>{claim.label}</strong><p className="muted">{claim.value ?? "Unknown"} {claim.unit || ""} {claim.currency || ""}</p></div>
                    <div className="claim-meta"><QualityBadge value={claim.number_type} /><span>{claim.source_ids?.length || 0} source(s)</span></div>
                  </article>
                ))}
                {unknownClaims.length > 0 ? <p className="warning">Unknown claims are shown without values because they failed source or methodology checks.</p> : null}
              </section>

              <section className="research-two-column">
                <article className="panel research-section"><div className="section-heading"><h2>Sources</h2><span>{sources.length}</span></div>{sources.length === 0 ? <p className="empty-state">No verified sources returned.</p> : sources.map((source) => <div className="source-row" key={source.id}><a href={source.url} target="_blank" rel="noreferrer">{source.title}</a><span>{source.publisher || "Unknown publisher"} · {source.quality}</span></div>)}</article>
                <article className="panel research-section"><div className="section-heading"><h2>Data gaps</h2><span>{quality.missing_fields?.length || 0}</span></div>{quality.missing_fields?.length ? <ul className="data-list">{quality.missing_fields.map((field) => <li key={field}>{field}</li>)}</ul> : <p className="empty-state">No missing fields reported.</p>}{quality.cleaning_issues?.length ? <><h3>Cleaning notes</h3><ul className="data-list">{quality.cleaning_issues.map((issue) => <li key={issue}>{issue}</li>)}</ul></> : null}</article>
              </section>
            </>
          )}
        </>
      ) : null}
    </PageShell>
  );
}

export default MarketResearch;
