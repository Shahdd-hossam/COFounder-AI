import { useState } from "react";
import ResultCard from "../common/ResultCard";
import { createMarketingPlan } from "../../services/api";

const INITIAL_FORM = {
  company_name: "",
  product: "",
  target_audience: "",
  goal: "",
};

function MarketingPlanForm() {
  const [form, setForm] = useState(INITIAL_FORM);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const data = await createMarketingPlan(form);
      setResult(data);
    } catch (submitError) {
      setError(submitError.message || "Failed to create marketing plan.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="feature-grid">
      <form className="panel" onSubmit={handleSubmit}>
        <label>
          Company Name
          <input name="company_name" value={form.company_name} onChange={handleChange} required />
        </label>
        <label>
          Product
          <input name="product" value={form.product} onChange={handleChange} required />
        </label>
        <label>
          Target Audience
          <input
            name="target_audience"
            value={form.target_audience}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Goal
          <textarea name="goal" value={form.goal} onChange={handleChange} rows={3} required />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? "Generating..." : "Generate Plan"}
        </button>
        {error ? <p className="error">{error}</p> : null}
      </form>

      <ResultCard title="Generated Plan">
        {!result ? (
          <p>Submit the form to see strategy output.</p>
        ) : (
          <>
            <p>{result.summary}</p>
            <h3>Channels</h3>
            <ul>
              {result.channels.map((channel) => (
                <li key={channel}>{channel}</li>
              ))}
            </ul>
            <h3>Budget</h3>
            <ul>
              {Object.entries(result.budget_breakdown).map(([key, value]) => (
                <li key={key}>
                  {key}: {value}
                </li>
              ))}
            </ul>
            <h3>Timeline</h3>
            <ul>
              {result.timeline.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </>
        )}
      </ResultCard>
    </div>
  );
}

export default MarketingPlanForm;
