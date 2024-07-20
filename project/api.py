from datetime import datetime
from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import and_, select, text
from sqlalchemy.orm import Session

from project.orm_alvo.models import Data as DataAlvo
from project.orm_alvo.models import Signal, get_session_alvo
from project.orm_fonte.models import Data, get_session_fonte
from project.schemas import DataSchema, SignalName, SignalSchema

app = FastAPI()


@app.get("/")
def get_data_by_options(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    timestamp: bool = Query(True),
    wind_speed: bool = Query(True),
    power: bool = Query(True),
    ambient_temperature: bool = Query(True),
    limit: int = Query(100),
    skip: int = Query(0),
    session: Session = Depends(get_session_fonte),
):
    select_columns = []
    if timestamp:
        select_columns.append(Data.timestamp)

    if wind_speed:
        select_columns.append(Data.wind_speed)

    if power:
        select_columns.append(Data.power)

    if ambient_temperature:
        select_columns.append(Data.ambient_temperature)

    query = text(
        """
    SELECT {columns} FROM data
    WHERE timestamp >= :start_date AND timestamp <= :end_date
    LIMIT :limit OFFSET :skip
    """.format(columns=", ".join([str(column) for column in select_columns]))
    )

    datas = session.execute(
        query,
        {
            "start_date": start_date,
            "end_date": end_date,
            "limit": limit,
            "skip": skip,
        },
    )

    column_names = datas.keys()

    result = [dict(zip(column_names, data)) for data in datas.fetchall()]

    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Datas not found"
        )

    return result


@app.get("/date", response_model=list[DataSchema])
def get_data_by_date(
    date: datetime, session: Session = Depends(get_session_fonte)
):
    datas = session.scalars(
        select(Data).where(
            and_(
                Data.timestamp >= date,
                Data.timestamp <= date.replace(hour=23, minute=59, second=59),
            )
        )
    ).all()
    if not datas:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Datas not found"
        )

    return datas


@app.get(
    "/signal",
    response_model=SignalSchema,
)
def get_signal_by_name(
    name: SignalName,
    session: Session = Depends(get_session_alvo),
):
    signal = session.scalar(select(Signal).where(Signal.name == name.value))
    if not signal:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Signal not found"
        )

    return signal


@app.get(
    "/signal/date",
    response_model=SignalSchema,
)
def get_signal_by_name_and_date(
    name: SignalName,
    date: datetime,
    session: Session = Depends(get_session_alvo),
):
    signal = session.scalar(
        select(Signal)
        .join(DataAlvo)
        .where(
            and_(
                DataAlvo.timestamp >= date,
                DataAlvo.timestamp
                <= date.replace(hour=23, minute=59, second=59),
            )
        )
        .where(Signal.name == name.value)
    )
    if not signal:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Signal not found"
        )

    return signal
