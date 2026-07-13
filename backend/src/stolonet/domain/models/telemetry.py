from dataclasses import dataclass

from stolonet.domain.models.reading import Reading


@dataclass(slots=True)
class TelemetryEnvelope:
    node_id: str
    timestamp: str
    readings: list[Reading]
