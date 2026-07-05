name=README.md
# Centralized Logging - Otic Fortress

What this bundle contains
- CENTRALIZED_LOGGING.md — Design, architecture, and guidance for centralized logging across Azure Functions, Event Hubs, Service Bus, and distributed services.
- otel-collector-config.yaml — Example OpenTelemetry Collector configuration for receiving OTLP and exporting to Azure Monitor / Log Analytics / Event Hubs.
- host.json, local.settings.json — Example Azure Functions config for telemetry.
- appsettings.json — Example .NET (Serilog) config to push structured logs & enrich with correlation.
- logging_node_example.js — Minimal Node.js logging + OpenTelemetry snippet.
- logging_python_example.py — Minimal Python logging + OpenTelemetry/Application Insights snippet.
- diagnostic-settings-eventhubs.json — Sample ARM-style diagnostic settings for Event Hubs forwarding to Log Analytics & Event Hubs.
- kql_queries.md — Useful KQL queries for logs and events.
- ALERTS.md — Example alert definitions and runbook bullets.
- LOGGING_CHECKLIST.md — Pre-production checklist to validate logging coverage.

How to use
1. Read CENTRALIZED_LOGGING.md to understand architecture and decisions.
2. Copy configuration examples (host.json, local.settings.json, appsettings.json, otel-collector-config.yaml) into the repo/folder and adapt placeholders (connection strings, resource names).
3. Use the instrumentation examples (Node/Python/.NET) as templates to instrument services.
4. Apply diagnostic settings to Azure resources to forward platform telemetry to Log Analytics / Event Hubs / Sentinel.
5. Import KQL queries into Log Analytics workbooks and implement alert queries in Azure Monitor per ALERTS.md.
6. Run through LOGGING_CHECKLIST.md before production rollout.

Security and secrets
- Replace placeholder connection strings and keys with Key Vault references or use managed identities.
- Do not check secrets into git.

If you want, I can:
- produce a ready-to-run Helm chart for the OTEL collector,
- generate Azure CLI commands to apply diagnostic settings,
- create GitHub Actions samples to validate instrumentation during CI.

Which would you like next?