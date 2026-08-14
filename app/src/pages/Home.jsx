import { Link } from "react-router-dom";
import PageShell from "../components/common/PageShell";

function Home() {
  return (
    <PageShell
      title="Turn Ideas Into Launch-Ready Marketing Execution"
      subtitle="Pick a workflow to build strategy drafts, market context, and SWOT snapshots in minutes."
    >
      <section className="home-grid">
        <article className="tile">
          <h2>Marketing Plan</h2>
          <p>Create a focused go-to-market plan with channels, budget split, and delivery timeline.</p>
          <Link className="tile-link" to="/marketing-plan">
            Open module
          </Link>
        </article>
        <article className="tile">
          <h2>Market Research</h2>
          <p>Generate trend signals, competitor snapshots, and opportunity directions.</p>
          <Link className="tile-link" to="/market-research">
            Open module
          </Link>
        </article>
        <article className="tile">
          <h2>SWOT Analysis</h2>
          <p>Build a structured SWOT matrix to clarify priorities and risk management.</p>
          <Link className="tile-link" to="/swot-analysis">
            Open module
          </Link>
        </article>
      </section>
    </PageShell>
  );
}

export default Home;
