import { useState } from "react";
import { Link } from "react-router-dom";
import { getWorkflowRun } from "../../services/api";
import { resultLabel, sourceModeLabel } from "./resultLanguage";

function FeatureRunPanel({ startupId, title, eyebrow, description, runFunction, renderResult, emptyText }) {
  const [run, setRun] = useState(null);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState("");

  const runFeature = async () => {
    setRunning(true);
    setError("");
    try {
      const created = await runFunction(startupId);
      setRun(created);
      const completed = await getWorkflowRun(created.id);
      setRun(completed);
    } catch (requestError) {
      setError(requestError.message || "The workflow could not be completed.");
    } finally {
      setRunning(false);
    }
  };

  const result = run?.result_json || null;
  return (
    <>
      <section className="panel research-header">
        <div>
          <p className="eyebrow">{eyebrow}</p>
          <h2>{title}</h2>
          <p className="muted">{description}</p>
        </div>
        <button className="primary-button" type="button" onClick={runFeature} disabled={running}>
          {running ? "Generating..." : "Generate"}
        </button>
      </section>
      {error ? <p className="error">{error}</p> : null}
      {!run ? <section className="panel empty-state"><p>{emptyText}</p><Link className="primary-link" to={`/startups/${startupId}`}>Back to overview</Link></section> : null}
      {run ? (
        <>
          <section className="quality-grid">
            <article className="panel quality-card"><span>Workflow</span><strong>{resultLabel(run.status)}</strong></article>
            <article className="panel quality-card"><span>Research basis</span><strong>{sourceModeLabel(result)}</strong></article>
            <article className="panel quality-card"><span>Review confidence</span><strong>{resultLabel(result?.data_quality?.confidence || result?.workflow_status)}</strong></article>
          </section>
          {renderResult(result)}
        </>
      ) : null}
    </>
  );
}

export default FeatureRunPanel;
