import express from "express";
import { register, collectDefaultMetrics } from "prom-client";

export function createApp() {
    const app = express();
    app.use(express.json());

    collectDefaultMetrics();

    app.get("/health", (_req, res) => res.json({ ok: true, service: "api-express" }));

    app.get("/metrics", async (_req, res) => {
        res.set("Content-Type", register.contentType);
        res.end(await register.metrics());
    });

    return app;
}
