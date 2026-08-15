import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import PageShell from "../components/common/PageShell";
import { getStartup } from "../services/api";

const MODULES = [
  { title: "Market Research", description: "Use source-backed evidence and show what remains unknown.", path: "market-research" },
  { title: "Competitor Analysis", description: "Compare direct and indirect alternatives with source links and pricing uncertainty.", path: "competitor-analysis" },
  { title: "SWOT Analysis", description: "Turn context and evidence into traceable strategic dimensions.", path: "swot-analysis" },
  { title: "Marketing Plan", description: "Build channels, experiments, KPIs, and budget guardrails without invented forecasts.", path: "marketing-plan" },
  { title: "Action Plan", description: "Create execution tasks while keeping ad launch and spending disabled.", path: "action-plan" },
];

function StartupOverview() {
  const { startupId } = useParams();
  const [startup, setStartup] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getStartup(startupId).then(setStartup).catch((requestError) => setError(requestError.message || "Could not load startup."));
  }, [startupId]);

  return (
    <PageShell title={startup?.name || "Startup overview"} subtitle={startup?.goal || "Loading the shared startup context..."}>
      {error ? <p className="error">{error}</p> : null}
      {!startup && !error ? <p className="muted">Loading startup context...</p> : null}
      {startup ? (
        <>
          <section className="context-grid">
            <article className="panel context-card"><span>Description</span><strong>{startup.description}</strong></article>
            <article className="panel context-card"><span>Target customer</span><strong>{startup.target_customer}</strong></article>
            <article className="panel context-card"><span>Target market</span><strong>{startup.target_market}</strong></article>
            <article className="panel context-card"><span>Budget</span><strong>{startup.budget} {startup.currency}</strong></article>
            <article className="panel context-card"><span>Timeline</span><strong>{startup.time_horizon_days} days</strong></article>
            <article className="panel context-card"><span>Context revision</span><strong>{startup.context_revision}</strong></article>
          </section>
          <section className="module-grid">
            {MODULES.map((module) => (
              <article className="startup-card" key={module.path}>
                <div><p className="status-label">Ready to generate</p><h2>{module.title}</h2><p>{module.description}</p></div>
                <Link className="primary-link" to={`/startups/${startup.id}/${module.path}`}>Open module</Link>
              </article>
            ))}
          </section>
        </>
      ) : null}
    </PageShell>
  );
}

export default StartupOverview;
