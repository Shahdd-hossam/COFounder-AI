export function resultLabel(value) {
  const labels = {
    ready: "Ready to review",
    partial: "Partially researched",
    fallback: "Planning baseline",
    mock: "Reference baseline",
    mock_seed: "Reference baseline",
    mock_reference: "Reference profile",
    source_backed: "Research-backed",
    modeled_estimate: "Planning range",
    llm_estimate: "AI planning view",
    llm_assisted_estimates: "AI planning view",
    transparent_planning_estimates: "Planning range",
    unknown: "Needs validation",
    low: "Early signal",
    medium: "Moderate signal",
    high: "Strong signal",
    not_configured: "Not connected",
    context: "Startup context",
    hypothesis: "Working hypothesis",
    validation_required: "Validate in pilot",
  };
  return labels[value] || value || "Needs review";
}

export function sourceCountLabel(count) {
  if (!count) return "Research basis pending";
  return `${count} research reference${count === 1 ? "" : "s"}`;
}

export function claimValueLabel(claim) {
  if (!claim || claim.value === null || claim.value === undefined || claim.value === "") return "Add evidence during validation";
  return `${claim.value}${claim.unit ? ` ${claim.unit}` : ""}${claim.currency ? ` · ${claim.currency}` : ""}`;
}

export function sourceModeLabel(result) {
  if (result?.data_mode === "mock_seed") return "Reference baseline";
  if (result?.llm_estimate_mode === "structured_reasoning") return "AI planning view";
  if (result?.sources?.length) return "Research-backed";
  return "Planning baseline";
}
