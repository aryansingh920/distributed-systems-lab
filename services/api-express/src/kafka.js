import { Kafka } from "kafkajs";

const broker = process.env.KAFKA_BROKER || "kafka:9092";
const kafka = new Kafka({ clientId: "api-express", brokers: [broker] });

let producer;
let ready = false;

async function getProducer() {
    if (ready) return producer;
    if (!producer) producer = kafka.producer();

    while (true)
    {
        try
        {
            await producer.connect();
            ready = true;
            console.log("api-express kafka producer connected");
            return producer;
        } catch (e)
        {
            console.error("Kafka connect failed, retrying in 2s:", e.message);
            await new Promise((r) => setTimeout(r, 2000));
        }
    }
}

export async function sendEvent(topic, eventObj) {
    const p = await getProducer();

    const key = eventObj?.key;     // optional
    const payload = { ...eventObj };
    delete payload.key;

    await p.send({
        topic,
        messages: [{ key, value: JSON.stringify(payload) }],
    });
}
