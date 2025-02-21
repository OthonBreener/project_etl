from datetime import datetime
from typing import Iterator

from sqlalchemy import create_engine, func
from sqlalchemy.orm import Mapped, Session, mapped_column, registry

from project.settings import Settings

db_fonte_registry = registry()

engine_fonte = create_engine(
    f"postgresql://{Settings().POSTGRES_FONTE_USER}:"
    f"{Settings().POSTGRES_FONTE_PASSWORD}@postgres_fonte:"
    f"5432/{Settings().POSTGRES_FONTE_DB}"
)


def get_session_fonte() -> Iterator[Session]:
    with Session(engine_fonte) as session:
        yield session


@db_fonte_registry.mapped_as_dataclass
class Data:
    __tablename__ = "data"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    timestamp: Mapped[datetime] = mapped_column(index=True)
    wind_speed: Mapped[float]
    power: Mapped[float]
    ambient_temperature: Mapped[float]

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(), server_default=func.now(), init=False
    )
