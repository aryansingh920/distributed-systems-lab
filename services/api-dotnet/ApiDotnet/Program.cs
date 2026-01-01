using Prometheus;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/health", () => Results.Json(new { ok = true, service = "api-dotnet" }));

// Exposes /metrics in Prometheus text format
app.UseMetricServer(url: "/metrics");

// Optional: track HTTP request metrics automatically
app.UseHttpMetrics();

app.Run("http://0.0.0.0:4004");
