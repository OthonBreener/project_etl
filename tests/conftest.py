from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from project.api import app
from project.orm_alvo.models import db_alvo_registry, get_session_alvo
from project.orm_fonte.models import db_fonte_registry, get_session_fonte
from project.scripts.generate_datas import generate_datas


@pytest.fixture()
def session_fonte():
    engine = create_engine(
        "sqlite:///:memory:",
        # Especificos para o sqlite
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    db_fonte_registry.metadata.create_all(engine)

    interval = (
        datetime(2024, 1, 1),
        datetime(2024, 1, 2),
    )

    generate_datas(interval, engine)

    with Session(engine) as session:
        yield session

    db_fonte_registry.metadata.drop_all(engine)


@pytest.fixture()
def engine_alvo():
    engine = create_engine(
        "sqlite:///:memory:",
        # Especificos para o sqlite
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    return engine


@pytest.fixture()
def session_alvo(engine_alvo):
    db_alvo_registry.metadata.create_all(engine_alvo)

    with Session(engine_alvo) as session:
        yield session

    db_alvo_registry.metadata.drop_all(engine_alvo)


@pytest.fixture()
def client(session_fonte, session_alvo):
    def get_session_override_fonte():
        return session_fonte

    def get_session_override_alvo():
        return session_alvo

    with TestClient(app) as client:
        app.dependency_overrides[get_session_fonte] = (
            get_session_override_fonte
        )

        app.dependency_overrides[get_session_alvo] = get_session_override_alvo

        yield client

    app.dependency_overrides.clear()
