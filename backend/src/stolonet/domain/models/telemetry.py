from dataclasses import dataclass
from datetime import datetime

from stolonet.domain.models.reading import Reading


@dataclass(slots=True)
class TelemetryEnvelope:
    node_id: str
    timestamp: datetime
    readings: list[Reading]
