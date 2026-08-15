import { useState } from "react";
import { useNavigate } from "react-router-dom";
import PageShell from "../components/common/PageShell";
import { createStartup } from "../services/api";

const DEMO_STARTUP = {
  name: "CareerLaunch Egypt",
  description: "An Arabic-English AI career coach for final-year university students.",
  target_customer: "Final-year university students",
  target_market: "Egypt, starting with Alexandria",
  business_model: "Freemium subscription",
  goal: "Acquire the first 100 qualified beta users",
  budget: "10000",
  currency: "EGP",
  time_horizon_days: "30",
  language: "Arabic and English",
};

const EMPTY_STARTUP = {
  name: "",
  description: "",
  target_customer: "",
  target_market: "",
  business_model: "",
  goal: "",
  budget: "",
  currency: "EGP",
  time_horizon_days: "30",
  language: "Arabic and English",
};

function StartupSetup() {
  const [form, setForm] = useState(EMPTY_STARTUP);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const updateField = (event) => {
    const { name, value } = event.target;
    setForm((previous) => ({ ...previous, [name]: value }));
  };

  const submit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const startup = await createStartup({
        ...form,
        budget: Number(form.budget),
        time_horizon_days: Number(form.time_horizon_days),
      });
      navigate(`/startups/${startup.id}`);
    } catch (submitError) {
      setError(submitError.message || "Could not save startup.");
    } finally {
      setLoading(false);
    }
  };

  const loadDemo = () => setForm(DEMO_STARTUP);

  return (
    <PageShell
      title="Create startup workspace"
      subtitle="This shared context becomes the source of truth for every strategy module."
    >
      <form className="panel startup-form" onSubmit={submit}>
        <div className="form-heading">
          <div>
            <p className="eyebrow">Shared context</p>
            <h2>Tell us about the startup</h2>
          </div>
          <button type="button" className="secondary-button" onClick={loadDemo}>Use CareerLaunch demo</button>
        </div>
        <label>Startup name<input name="name" value={form.name} onChange={updateField} required /></label>
        <label>Description<textarea name="description" value={form.description} onChange={updateField} rows={3} required /></label>
        <div className="form-two-column">
          <label>Target customer<input name="target_customer" value={form.target_customer} onChange={updateField} required /></label>
          <label>Target market<input name="target_market" value={form.target_market} onChange={updateField} required /></label>
          <label>Business model<input name="business_model" value={form.business_model} onChange={updateField} required /></label>
          <label>Language<input name="language" value={form.language} onChange={updateField} required /></label>
          <label>Budget<input type="number" min="0.01" name="budget" value={form.budget} onChange={updateField} required /></label>
          <label>Currency<input name="currency" value={form.currency} onChange={updateField} required /></label>
          <label>Time horizon (days)<input type="number" min="1" name="time_horizon_days" value={form.time_horizon_days} onChange={updateField} required /></label>
        </div>
        <label>Primary goal<textarea name="goal" value={form.goal} onChange={updateField} rows={3} required /></label>
        {error ? <p className="error">{error}</p> : null}
        <button className="primary-button" type="submit" disabled={loading}>{loading ? "Saving workspace..." : "Create workspace"}</button>
      </form>
    </PageShell>
  );
}

export default StartupSetup;
