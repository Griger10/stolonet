from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from stolonet.infrastructure.persistence.db import Base


class ReadingORM(Base):
    __tablename__ = "readings"

    reading_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    node_id: Mapped[int] = mapped_column()
    metric: Mapped[str] = mapped_column()
    value: Mapped[float] = mapped_column()
    unit: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return (
            f"Reading(node_id={self.node_id}, metric={self.metric}, value={self.value}{self.unit})"
        )
