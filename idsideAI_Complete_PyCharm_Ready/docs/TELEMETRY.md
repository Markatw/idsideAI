# Telemetry

- `/metrics` exposes Prometheus metrics: `idecide_requests_total`, `idecide_request_latency_seconds`.
- Grafana dashboards in `observability/dashboards`.
- Set `OTEL_EXPORTER_OTLP_ENDPOINT` to send traces to OTEL collector.
