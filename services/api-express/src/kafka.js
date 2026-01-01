import { Kafka } from "kafkajs";

const broker = process.env.KAFKA_BROKER || "kafka:9092";

const kafka = new Kafka({ clientId: "api-express", brokers: [broker] });
export const producer = kafka.producer();
