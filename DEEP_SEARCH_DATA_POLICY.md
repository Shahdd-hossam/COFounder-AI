# Deep Search Data Policy

## Non-negotiable rule

The application must not present a market number or research statement as verified unless the returned payload includes a valid source URL and the claim is linked to that source. When the evidence is incomplete, the UI displays **Unknown** or **No verified evidence returned**.

## Numeric claim taxonomy

| Type | Meaning | Required evidence |
|---|---|---|
| `source_reported` | The exact value appears in a source | At least one valid `source_id` |
| `derived_from_sources` | The value is calculated from cited source values | Valid source IDs and visible methodology |
| `modeled_estimate` | A model-based estimate | Methodology, assumptions, and any supporting sources |
| `unknown` | The value is missing, malformed, conflicting, or unsupported | No value is shown as fact |

The cleaner downgrades source-free, malformed, or methodologically incomplete claims to `unknown` and removes their numeric value before persistence.

## Text evidence

Market overviews, trends, competitors, customer insights, opportunities, and threats also require valid `source_ids`. Uncited findings are removed. If a tool returns an overview without `market_overview_source_ids`, it is replaced with an explicit unknown statement.

## Missing-data handling

The cleaner preserves `missing_fields`, `conflicts`, `assumptions`, and `cleaning_issues` in `result_json.data_quality`. This makes the absence of evidence visible instead of hiding it behind a confident-sounding summary.

## MCP behavior

The repository contains a feature-neutral MCP gateway and a Tavily result normalizer. The Tavily connector discovered in the current environment is disabled, so the default runtime intentionally returns a partial workflow with unknown values. Enable and authenticate the approved connector in the project runtime before registering a real result handler. Direct MCP calls must remain in the approved connector/runtime layer; the web process does not shell out to the MCP CLI.

## Review checklist

Before enabling a live connector, verify that its output includes valid URLs, source IDs, retrieval dates, and the required numeric-claim fields. Test malformed and source-free responses. Never add a fallback market size, growth rate, competitor count, conversion rate, or price merely to make the dashboard look complete.
