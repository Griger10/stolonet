from datetime import datetime

from pydantic import BaseModel

from stolonet.domain.enums import MetricType
from stolonet.domain.models import Reading, TelemetryEnvelope


class ReadingDTO(BaseModel):
    metric: MetricType
    value: float
    unit: str


class TelemetryEnvelopeDTO(BaseModel):
    node_id: str
    timestamp: datetime
    readings: list[ReadingDTO]

    def to_domain_model(self) -> TelemetryEnvelope:
        return TelemetryEnvelope(
            node_id=self.node_id,
            timestamp=self.timestamp,
            readings=[Reading(metric=r.metric, value=r.value, unit=r.unit) for r in self.readings],
        )
