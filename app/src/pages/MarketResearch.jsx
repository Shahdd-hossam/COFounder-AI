import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import PageShell from "../components/common/PageShell";
import { getStartup, getWorkflowRun, startMarketResearchRun } from "../services/api";
import { claimValueLabel, resultLabel, sourceCountLabel, sourceModeLabel } from "../components/common/resultLanguage";

function QualityBadge({ value }) {
  const label = resultLabel(value);
  const tone = String(value || "").includes("estimate") ? "estimate" : String(value || "").includes("mock") ? "mock" : value === "unknown" ? "warning" : "";
  return <span className={`quality-badge quality-${value || "review"}`} data-tone={tone}>{label}</span>;
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
          <PageShell title="Market Research" subtitle="Build a practical research baseline, see where it comes from, and turn missing evidence into validation tasks.">

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
              <p className="muted">Research is pinned to context revision {startup.context_revision}. The description and target market drive profile matching and planning recommendations.</p>
            </div>
            <button className="primary-button" type="button" onClick={startResearch} disabled={running}>
              {running ? "Searching and cleaning..." : "Run Deep Search"}
            </button>
          </section>

          {!run ? (
            <section className="panel empty-state research-empty">
              <h3>No research run yet</h3>
              <p>Run research to build a coherent baseline. If live sources are unavailable, the workspace uses a reference profile and clearly separates planning ranges from research-backed findings.</p>
            </section>
          ) : (
            <>
              <section className="quality-grid">
                <article className="panel quality-card"><span>Workflow</span><strong>{resultLabel(run.status)}</strong></article>
                <article className="panel quality-card"><span>Research basis</span><strong><QualityBadge value={result.data_mode === "mock_seed" ? "mock_reference" : sourceModeLabel(result)} /></strong></article>
                <article className="panel quality-card"><span>Research references</span><strong>{sourceCountLabel(sources.length)}</strong></article>
                <article className="panel quality-card"><span>Planning values</span><strong>{numericClaims.length ? `${numericClaims.length} values to review` : "Add values during validation"}</strong></article>
              </section>

              <section className="panel research-section">
                <p className="eyebrow">Market overview</p>
                <div className="row-title"><h2>{result.market_overview || "Unknown"}</h2><QualityBadge value={result.market_overview_status || (result.data_mode === "mock_seed" ? "mock_reference" : result.market_overview?.startsWith("Preliminary") ? "modeled_estimate" : "source_backed")} /></div>
                <p className="muted">Tool: {result.tool || "not configured"}. Data mode: {result.data_mode || "live"}. Profile: {result.mock_profile_name || "none"}. Fallback path: {(quality.fallback_chain || []).join(" → ") || "not configured"}. All claims below retain their evidence links and cleaning metadata.</p>
                {quality.fallback_errors?.length ? <p className="warning">Research connectors were unavailable. No unsupported result was substituted.</p> : null}
              </section>

              <section className="panel research-section">
                <div className="section-heading"><h2>Source-backed findings</h2><span>Uncited insights are removed</span></div>
                {insightGroups.every(([, items]) => items.length === 0) ? <p className="empty-state">No findings in this category yet. Use the validation tasks below to collect evidence.</p> : null}
                <div className="insight-grid">
                  {insightGroups.map(([title, items]) => (
                    <article className="insight-group" key={title}>
                      <h3>{title}</h3>
                      {items.length === 0 ? <p className="muted">Needs validation</p> : items.map((item, index) => <div className="insight-row" key={`${title}-${index}`}><p>{item.text}</p><span>{sourceCountLabel(item.source_ids?.length || 0)} · {resultLabel(item.evidence_status || item.confidence)}</span></div>)}
                    </article>
                  ))}
                </div>
                            </section>
              <section className="panel research-section">
                <div className="section-heading"><h2>Planning ranges</h2><span>{estimatedFindings.length ? `${estimatedFindings.length} planning views` : "Add through validation"}</span></div>
                <p className="warning">These are decision-support ranges from startup context and reasoning. Confirm them with interviews, pilots, and measured experiments before treating them as operating targets.</p>
                {(estimatedFindings || []).map((item, index) => <article className="insight-row" key={`estimate-${index}`}><p>{item.text}</p><span>{resultLabel(item.number_type)} · {resultLabel(item.confidence)} · {item.methodology}</span><small>Next check: {item.validation_plan}</small></article>)}
              </section>
              <section className="panel research-section">
                <div className="section-heading"><h2>Decision values</h2><span>Each value has a review basis</span></div>

                {numericClaims.length === 0 ? <p className="empty-state">No decision values yet. Add a pilot result or planning assumption to make this section actionable.</p> : null}
                {numericClaims.map((claim, index) => (
                  <article className="claim-row" key={`${claim.label}-${index}`}>
                    <div><strong>{claim.label}</strong><p className="muted">{claimValueLabel(claim)}</p></div>
                    <div className="claim-meta"><QualityBadge value={claim.number_type} /><span>{sourceCountLabel(claim.source_ids?.length || 0)}</span></div>
                  </article>
                ))}
                {unknownClaims.length > 0 ? <p className="warning">Some values need validation before they can guide a decision. Use the source and pilot tasks rather than treating them as facts.</p> : null}
              </section>

              <section className="research-two-column">
                <article className="panel research-section"><div className="section-heading"><h2>Research references</h2><span>{sources.length ? `${sources.length} available` : "Build reference set"}</span></div>{sources.length === 0 ? <p className="empty-state">Research references will appear after a live or reference-profile run.</p> : sources.map((source) => <div className="source-row" key={source.id}><a href={source.url} target="_blank" rel="noreferrer">{source.title}</a><span>{source.publisher || "Reference source"} · {resultLabel(source.quality)}</span></div>)}</article>
                <article className="panel research-section"><div className="section-heading"><h2>Validation queue</h2><span>{quality.missing_fields?.length ? `${quality.missing_fields.length} items` : "Ready"}</span></div>{quality.missing_fields?.length ? <ul className="data-list">{quality.missing_fields.map((field) => <li key={field}>{field}</li>)}</ul> : <p className="empty-state">No validation items were raised by this run.</p>}{quality.cleaning_issues?.length ? <><h3>Review notes</h3><ul className="data-list">{quality.cleaning_issues.map((issue) => <li key={issue}>{issue}</li>)}</ul></> : null}</article>
              </section>
            </>
          )}
        </>
      ) : null}
    </PageShell>
  );
}

export default MarketResearch;
