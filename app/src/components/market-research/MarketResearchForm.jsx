import { useState } from "react";
import ResultCard from "../common/ResultCard";
import { runMarketResearch } from "../../services/api";

const INITIAL_FORM = {
  industry: "",
  region: "",
  audience_segment: "",
};

function MarketResearchForm() {
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
      const data = await runMarketResearch(form);
      setResult(data);
    } catch (submitError) {
      setError(submitError.message || "Failed to generate market research.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="feature-grid">
      <form className="panel" onSubmit={handleSubmit}>
        <label>
          Industry
          <input name="industry" value={form.industry} onChange={handleChange} required />
        </label>
        <label>
          Region
          <input name="region" value={form.region} onChange={handleChange} required />
        </label>
        <label>
          Audience Segment
          <input
            name="audience_segment"
            value={form.audience_segment}
            onChange={handleChange}
            required
          />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Run Research"}
        </button>
        {error ? <p className="error">{error}</p> : null}
      </form>

      <ResultCard title="Research Snapshot">
        {!result ? (
          <p>Submit the form to generate a market snapshot.</p>
        ) : (
          <>
            <h3>Trends</h3>
            <ul>
              {result.trends.map((trend) => (
                <li key={trend}>{trend}</li>
              ))}
            </ul>
            <h3>Competitors</h3>
            <ul>
              {result.competitors.map((competitor) => (
                <li key={competitor.name}>
                  <strong>{competitor.name}</strong>: {competitor.strength} | Weakness: {competitor.weakness}
                </li>
              ))}
            </ul>
            <h3>Opportunities</h3>
            <ul>
              {result.opportunities.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </>
        )}
      </ResultCard>
    </div>
  );
}

export default MarketResearchForm;
