import { createApp } from "./app.js";
import { sendEvent } from "./kafka.js";
import crypto from "crypto";

const port = process.env.PORT || 4000;
const app = createApp();

app.post("/orders", async (req, res) => {
    try
    {
        const { user_id = "u1", amount = 10, currency = "EUR" } = req.body || {};
        const order_id = crypto.randomUUID();

        const event = {
            event_id: crypto.randomUUID(),
            type: "order.created",
            ts: new Date().toISOString(),
            order_id,
            payload: { user_id, amount, currency },
        };

        // this will connect/retry internally until Kafka is up
        await sendEvent("order.created", { ...event, key: order_id });

        return res.status(201).json({ order_id });
    } catch (e)
    {
        console.error("failed to publish:", e);
        return res.status(503).json({ ok: false, error: "Kafka not ready" });
    }
});

app.listen(port, () => console.log(`api-express listening on :${port}`));
