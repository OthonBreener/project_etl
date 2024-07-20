from datetime import datetime
from typing import Iterator

from sqlalchemy import ForeignKey, create_engine, func
from sqlalchemy.orm import (
    Mapped,
    Session,
    mapped_column,
    registry,
    relationship,
)

from project.settings import Settings

db_alvo_registry = registry()

engine_alvo = create_engine(
    f"postgresql://{Settings().POSTGRES_ALVO_USER}:"
    f"{Settings().POSTGRES_ALVO_PASSWORD}@localhost:"
    f"5433/{Settings().POSTGRES_ALVO_DB}"
)


def get_session_alvo() -> Iterator[Session]:
    with Session(engine_alvo) as session:
        yield session


@db_alvo_registry.mapped_as_dataclass
class Signal:
    __tablename__ = "signal"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(index=True)

    # Relacionamento com a tabela `data`
    data: Mapped[list["Data"]] = relationship(
        "Data", back_populates="signal", init=False
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(), server_default=func.now(), init=False
    )


@db_alvo_registry.mapped_as_dataclass
class Data:
    __tablename__ = "data"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    timestamp: Mapped[datetime]
    mean: Mapped[float]
    min: Mapped[float]
    max: Mapped[float]
    std: Mapped[float]

    signal_id: Mapped[int] = mapped_column(ForeignKey("signal.id"))
    signal: Mapped[Signal] = relationship(
        "Signal", back_populates="data", init=False
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(), server_default=func.now(), init=False
    )
