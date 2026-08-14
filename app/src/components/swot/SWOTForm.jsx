import { useState } from "react";
import ResultCard from "../common/ResultCard";
import { createSwotAnalysis } from "../../services/api";

const INITIAL_FORM = {
  company_name: "",
  product: "",
  market_context: "",
};

function SWOTForm() {
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
      const data = await createSwotAnalysis(form);
      setResult(data);
    } catch (submitError) {
      setError(submitError.message || "Failed to build SWOT analysis.");
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
          Market Context
          <textarea
            name="market_context"
            value={form.market_context}
            onChange={handleChange}
            rows={3}
            required
          />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? "Building..." : "Create SWOT"}
        </button>
        {error ? <p className="error">{error}</p> : null}
      </form>

      <ResultCard title="SWOT Matrix">
        {!result ? (
          <p>Submit the form to generate SWOT dimensions.</p>
        ) : (
          <div className="swot-grid">
            <article>
              <h3>Strengths</h3>
              <ul>
                {result.strengths.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </article>
            <article>
              <h3>Weaknesses</h3>
              <ul>
                {result.weaknesses.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </article>
            <article>
              <h3>Opportunities</h3>
              <ul>
                {result.opportunities.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </article>
            <article>
              <h3>Threats</h3>
              <ul>
                {result.threats.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </article>
          </div>
        )}
      </ResultCard>
    </div>
  );
}

export default SWOTForm;
