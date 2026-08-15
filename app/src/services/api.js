const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000/api/v1";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(errorBody || `Request failed with status ${response.status}`);
  }

  return response.json();
}

export function createStartup(payload) {
  return request("/startups", { method: "POST", body: JSON.stringify(payload) });
}

export function listStartups() {
  return request("/startups");
}

export function getStartup(startupId) {
  return request(`/startups/${startupId}`);
}

export function updateStartup(startupId, payload) {
  return request(`/startups/${startupId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export function getWorkflowRun(runId) {
  return request(`/workflows/${runId}`);
}

export function startMarketResearchRun(startupId) {
  return request(`/startups/${startupId}/market-research/runs`, { method: "POST" });
}

export function createMarketingPlan(payload) {
  return request("/marketing-plan", { method: "POST", body: JSON.stringify(payload) });
}

export function runMarketResearch(payload) {
  return request("/market-research", { method: "POST", body: JSON.stringify(payload) });
}

export function createSwotAnalysis(payload) {
  return request("/swot", { method: "POST", body: JSON.stringify(payload) });
}

export { API_BASE_URL };
