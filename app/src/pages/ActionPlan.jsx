import { useParams } from "react-router-dom";
import PageShell from "../components/common/PageShell";
import FeatureRunPanel from "../components/common/FeatureRunPanel";
import { startActionPlanRun } from "../services/api";

function ActionPlan() {
  const { startupId } = useParams();
  return (
    <PageShell title="Action Plan" subtitle="Create prioritized next steps while keeping ad launch and spend explicitly disabled.">
      {!startupId ? <section className="panel"><h2>Create or open a startup</h2><p className="muted">Action planning needs a startup context.</p></section> : <FeatureRunPanel
        startupId={startupId}
        title="Next-step execution plan"
        eyebrow="Planning only"
        description="Tasks are designed for validation and growth execution. No ad account is modified and no spend is authorized by this workflow."
        runFunction={startActionPlanRun}
        emptyText="Generate safe next steps from the marketing plan."
        renderResult={(result) => <>
          <section className="panel warning"><strong>Execution disabled.</strong> {result?.reason}</section>
          <section className="panel research-section"><div className="section-heading"><h2>Tasks</h2><span>{result?.tasks?.length || 0}</span></div>{(result?.tasks || []).map((task) => <article className="task-row" key={task.stable_key}><div><h3>{task.title}</h3><span>{task.owner} · {task.evidence_status} · {task.source_ids?.length || 0} source(s)</span></div><strong>{task.status}</strong></article>)}</section>
          <section className="panel research-section"><div className="section-heading"><h2>Budget</h2><span>{result?.budget?.currency}</span></div><p>Available context budget: <strong>{result?.budget?.available_budget}</strong></p><p className="muted">Spend authorized: {String(result?.budget?.spend_authorized)}</p></section>
        </>}
      />}
    </PageShell>
  );
}

export default ActionPlan;
