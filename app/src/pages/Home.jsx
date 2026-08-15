import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import PageShell from "../components/common/PageShell";
import { listStartups } from "../services/api";

function Home() {
  const [startups, setStartups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    listStartups()
      .then((data) => {
        if (active) setStartups(data);
      })
      .catch((requestError) => {
        if (active) setError(requestError.message || "Could not load startups.");
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  return (
    <PageShell
      title="CoFounder AI"
      subtitle="Turn startup information into evidence-backed decisions and actionable next steps."
    >
      <section className="hero-panel">
        <div>
          <p className="eyebrow">Founder operating system</p>
          <h2>Choose a startup workspace</h2>
          <p>Start with one shared context, then move through research, SWOT, marketing, and actions.</p>
        </div>
        <Link className="primary-link" to="/startups/new">Create startup</Link>
      </section>

      <section className="startup-list" aria-label="Saved startups">
        <div className="section-heading">
          <h2>Saved startups</h2>
          <span>{startups.length} workspace{startups.length === 1 ? "" : "s"}</span>
        </div>
        {loading ? <p className="muted">Loading startup workspaces...</p> : null}
        {error ? <p className="error">{error}</p> : null}
        {!loading && !error && startups.length === 0 ? (
          <p className="empty-state">No startup yet. Create one or seed the CareerLaunch Egypt demo.</p>
        ) : null}
        <div className="startup-grid">
          {startups.map((startup) => (
            <article className="startup-card" key={startup.id}>
              <div>
                <p className="status-label">Revision {startup.context_revision}</p>
                <h3>{startup.name}</h3>
                <p>{startup.description}</p>
                <p className="muted">{startup.target_market} · {startup.target_customer}</p>
              </div>
              <div className="card-actions">
                <Link to={`/startups/${startup.id}`}>Open overview</Link>
                <Link to={`/startups/${startup.id}/marketing-plan`}>Marketing plan</Link>
              </div>
            </article>
          ))}
        </div>
      </section>
    </PageShell>
  );
}

export default Home;
