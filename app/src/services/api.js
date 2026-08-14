const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000/api/v1";

async function post(path, payload) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(errorBody || "Request failed");
  }

  return response.json();
}

export function createMarketingPlan(payload) {
  return post("/marketing-plan", payload);
}

export function runMarketResearch(payload) {
  return post("/market-research", payload);
}

export function createSwotAnalysis(payload) {
  return post("/swot", payload);
}
