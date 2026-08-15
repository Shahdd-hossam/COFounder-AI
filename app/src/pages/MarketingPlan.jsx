import { useParams } from "react-router-dom";
import PageShell from "../components/common/PageShell";
import FeatureRunPanel from "../components/common/FeatureRunPanel";
import { startMarketingPlanRun } from "../services/api";

function MarketingPlan() {
  const { startupId } = useParams();
  return (
    <PageShell title="Marketing Plan" subtitle="Turn evidence into validation experiments, not unsupported performance forecasts.">
      {!startupId ? <section className="panel"><h2>Create or open a startup</h2><p className="muted">Marketing planning needs a startup context.</p></section> : <FeatureRunPanel
        startupId={startupId}
        title="Validation-first marketing plan"
        eyebrow="Grounded growth planning"
        description="Channels and experiments are tied to evidence where available. Budget allocations and KPI targets remain blank until validated."
        runFunction={startMarketingPlanRun}
        emptyText="Generate a marketing plan from the current context and research."
        renderResult={(result) => <>
          <section className="panel research-section"><div className="section-heading"><h2>Objective</h2><span>{result?.objective?.basis}</span></div><h3>{result?.objective?.title}</h3><p>{result?.objective?.description}</p><p className="muted">Deadline: {result?.objective?.deadline_days || "Unknown"} days · Target: {result?.objective?.target || "Unknown"}</p></section>
          <section className="panel research-section"><div className="section-heading"><h2>Channels</h2><span>{result?.channels?.length || 0}</span></div>{(result?.channels || []).map((channel) => <article className="channel-row" key={channel.name}><div><h3>{channel.name}</h3><p>{channel.role}</p></div><div className="channel-meta"><span>{channel.source_ids?.length || 0} source(s)</span><strong>{channel.measurement}</strong></div></article>)}</section>
          <section className="research-two-column"><article className="panel research-section"><div className="section-heading"><h2>Experiments</h2><span>{result?.experiments?.length || 0}</span></div>{(result?.experiments || []).map((experiment) => <div className="insight-row" key={experiment.name}><h3>{experiment.name}</h3><p>{experiment.hypothesis}</p><span>{experiment.success_metric} · target: {experiment.target || "Unknown"}</span></div>)}</article><article className="panel research-section"><div className="section-heading"><h2>Budget guardrail</h2><span>{result?.budget_guidance?.status}</span></div><p>Total context budget: <strong>{result?.budget_guidance?.total_budget} {result?.budget_guidance?.currency}</strong></p><p>{result?.budget_guidance?.reason}</p></article></section>
          <section className="panel research-section"><div className="section-heading"><h2>KPIs</h2><span>Targets require validation</span></div>{(result?.kpis || []).map((kpi) => <div className="kpi-row" key={kpi.name}><strong>{kpi.name}</strong><span>{kpi.definition}</span><em>{kpi.target || "Unknown"}</em></div>)}</section>
        </>}
      />}
    </PageShell>
  );
}

export default MarketingPlan;
