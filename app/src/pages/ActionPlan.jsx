import { useParams } from "react-router-dom";
import PageShell from "../components/common/PageShell";
import FeatureRunPanel from "../components/common/FeatureRunPanel";
import { startActionPlanRun } from "../services/api";
import { resultLabel, sourceCountLabel } from "../components/common/resultLanguage";

function ActionPlan() {
  const { startupId } = useParams();
  return (
    <PageShell title="Action Plan" subtitle="Turn the strategy into safe, prioritized next steps with human approval before any spend.">
      {!startupId ? <section className="panel"><h2>Create or open a startup</h2><p className="muted">Action planning needs a startup context.</p></section> : <FeatureRunPanel
        startupId={startupId}
        title="Next-step execution plan"
        eyebrow="Planning only"
        description="Tasks are designed for validation and growth execution. The workspace prepares actions but never launches ads or authorizes spend."
        runFunction={startActionPlanRun}
        emptyText="Generate safe next steps from the matched marketing plan."
        renderResult={(result) => <>
          <section className="panel warning"><strong>Human approval required.</strong> {result?.reason}</section>
          <section className="panel research-section"><div className="section-heading"><h2>Tasks</h2><span>{result?.tasks?.length ? `${result.tasks.length} next steps` : "Create next steps"}</span></div>{(result?.tasks || []).map((task) => <article className="task-row" key={task.stable_key}><div><h3>{task.title}</h3><span>{task.owner} · {resultLabel(task.evidence_status)} · {sourceCountLabel(task.source_ids?.length || 0)}</span></div><strong>{resultLabel(task.status)}</strong></article>)}</section>
          <section className="panel research-section"><div className="section-heading"><h2>Budget guardrail</h2><span>{result?.budget?.currency || "Review currency"}</span></div><p>Context budget: <strong>{result?.budget?.available_budget || "Review startup budget"}</strong></p><p className="muted">Ad spend remains disabled until a human approves the plan.</p></section>
        </>}
      />}
    </PageShell>
  );
}

export default ActionPlan;
