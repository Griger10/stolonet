import asyncio
import random
from datetime import datetime, timezone

from zmqtt import MQTTClient, QoS

from config import load_config
from contract import TelemetryEnvelope, Reading

NODES = ["node_1", "node_2", "node_3"]
SLEEP_INTERVAL = 5


async def main() -> None:
    config = load_config()
    async with MQTTClient(host=config.host, port=config.port) as client:
        while True:
            for node in NODES:
                contract_payload = TelemetryEnvelope(
                    node_id=node,
                    timestamp=datetime.now(timezone.utc),
                    readings=[
                        Reading(
                            metric="temperature",
                            value=random.uniform(20, 30),
                            unit="C"
                        ),
                        Reading(
                            metric="humidity",
                            value=random.uniform(0, 100),
                            unit="%"
                        )
                    ]
                )
                await client.publish(
                    topic=f"{config.topic}/{node}",
                    qos=QoS.AT_LEAST_ONCE,
                    payload=contract_payload.model_dump_json(),
                )
            await asyncio.sleep(SLEEP_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
