import { createApp } from "./app.js";
import { producer } from "./kafka.js";
import crypto from "crypto";

const port = process.env.PORT || 4000;
const app = createApp();

await producer.connect();
console.log("api-express kafka producer connected");

app.post("/orders", async (req, res) => {
    const { user_id = "u1", amount = 10, currency = "EUR" } = req.body || {};
    const order_id = crypto.randomUUID();

    const event = {
        event_id: crypto.randomUUID(),
        type: "order.created",
        ts: new Date().toISOString(),
        order_id,
        payload: { user_id, amount, currency },
    };

    await producer.send({
        topic: "order.created",
        messages: [{ key: order_id, value: JSON.stringify(event) }],
    });

    res.status(201).json({ order_id });
});

app.listen(port, () => console.log(`api-express listening on :${port}`));
