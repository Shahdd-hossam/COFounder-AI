import { useParams } from "react-router-dom";
import PageShell from "../components/common/PageShell";
import FeatureRunPanel from "../components/common/FeatureRunPanel";
import { startMarketingPlanRun } from "../services/api";
import { resultLabel, sourceCountLabel } from "../components/common/resultLanguage";

function MarketingPlan() {
  const { startupId } = useParams();
  return (
    <PageShell title="Marketing Plan" subtitle="Turn the research baseline into staged experiments, budget choices, and measurable next steps.">
      {!startupId ? <section className="panel"><h2>Create or open a startup</h2><p className="muted">Marketing planning needs a startup context.</p></section> : <FeatureRunPanel
        startupId={startupId}
        title="Validation-first marketing plan"
        eyebrow="Grounded growth planning"
        description="Channels and experiments are tied to the research baseline where possible, with clear review steps for every planning choice."
        runFunction={startMarketingPlanRun}
        emptyText="Generate a marketing plan from the startup context and matched research profile."
        renderResult={(result) => <>
          <section className="panel research-section"><div className="section-heading"><h2>Objective</h2><span>{resultLabel(result?.objective?.basis)}</span></div><h3>{result?.objective?.title}</h3><p>{result?.objective?.description}</p><p className="muted">Timeline: {result?.objective?.deadline_days || "Set during planning"} days · Outcome: {result?.objective?.target || "Define in pilot"}</p></section>
          <section className="panel research-section"><div className="section-heading"><h2>Channels</h2><span>{result?.channels?.length ? `${result.channels.length} options` : "Add options"}</span></div>{(result?.channels || []).map((channel) => <article className="channel-row" key={channel.name}><div><h3>{channel.name}</h3><p>{channel.role}</p></div><div className="channel-meta"><span>{sourceCountLabel(channel.source_ids?.length || 0)}</span><strong>{channel.measurement}</strong></div></article>)}</section>
          <section className="research-two-column"><article className="panel research-section"><div className="section-heading"><h2>Experiments</h2><span>{result?.experiments?.length ? `${result.experiments.length} designed` : "Design experiments"}</span></div>{(result?.experiments || []).map((experiment) => <div className="insight-row" key={experiment.name}><h3>{experiment.name}</h3><p>{experiment.hypothesis}</p><span>{experiment.success_metric} · outcome: {experiment.target || "Define during pilot"}</span></div>)}</article><article className="panel research-section"><div className="section-heading"><h2>Budget guardrail</h2><span>{resultLabel(result?.budget_guidance?.status)}</span></div><p>Context budget: <strong>{result?.budget_guidance?.total_budget} {result?.budget_guidance?.currency}</strong></p><p>{result?.budget_guidance?.reason}</p></article></section>
          <section className="panel research-section"><div className="section-heading"><h2>KPIs</h2><span>Review targets in pilot</span></div>{(result?.kpis || []).map((kpi) => <div className="kpi-row" key={kpi.name}><strong>{kpi.name}</strong><span>{kpi.definition}</span><em>{kpi.target || "Define during pilot"}</em></div>)}</section>
        </>}
      />}
    </PageShell>
  );
}

export default MarketingPlan;
